from __future__ import annotations

import re

from diagnostics import Diagnostic, Severity
from model import MarkupNode
from _rules import RuleSpec, full_name_from_parts, get_rule, get_variants

ROMAN_NUMERAL_RE = re.compile(
    r"(?i)^(m{0,4}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3}))$"
)


def validate_node(node: MarkupNode) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    directive_spec = get_variants(node.kind)
    if directive_spec is None:
        diagnostics.append(
            Diagnostic(
                severity=Severity.ERROR,
                code="PM301",
                path=node.path,
                line=node.line,
                column=node.column,
                message=f"unknown directive '{node.kind}'",
            )
        )
        return diagnostics

    rule = get_rule(node.kind, node.variant)
    if rule is None:
        known_variants = sorted(
            variant for variant in directive_spec.keys() if variant is not None
        )
        expected = ", ".join(known_variants) if known_variants else "no variant"
        diagnostics.append(
            Diagnostic(
                severity=Severity.ERROR,
                code="PM302",
                path=node.path,
                line=node.line,
                column=node.column,
                message=(
                    f"unknown variant '{node.variant}' for directive '{node.kind}'"
                    if node.variant is not None
                    else f"directive '{node.kind}' requires one of: {expected}"
                ),
            )
        )
        return diagnostics

    diagnostics.extend(_validate_arity(node, rule))

    if rule.first_arg_format is not None and node.args:
        if not _matches_first_arg_format(node.args[0], rule.first_arg_format):
            diagnostics.append(
                Diagnostic(
                    severity=Severity.ERROR,
                    code="PM304",
                    path=node.path,
                    line=node.line,
                    column=node.column,
                    message=(
                        f"directive '{full_name(node)}' requires the first argument "
                        f"to be {_describe_first_arg_format(rule.first_arg_format)}"
                    ),
                    hint=_first_arg_hint(node, rule.first_arg_format),
                )
            )

    return diagnostics


def full_name(node: MarkupNode) -> str:
    return full_name_from_parts(node.kind, node.variant)


def _validate_arity(node: MarkupNode, rule: RuleSpec) -> list[Diagnostic]:
    count = len(node.args)
    if rule.min_args <= count <= rule.max_args:
        return []

    if rule.min_args == rule.max_args:
        expected = f"exactly {rule.min_args}"
    else:
        expected = f"between {rule.min_args} and {rule.max_args}"

    return [
        Diagnostic(
            severity=Severity.ERROR,
            code="PM303",
            path=node.path,
            line=node.line,
            column=node.column,
            message=(
                f"directive '{full_name(node)}' expects {expected} arguments, "
                f"got {count}"
            ),
        )
    ]


def _matches_first_arg_format(value: str, format_name: str) -> bool:
    if format_name == "positive_int":
        return value.isdigit() and int(value) > 0
    if format_name == "roman_numeral":
        return bool(value) and bool(ROMAN_NUMERAL_RE.fullmatch(value))
    raise ValueError(f"unsupported first-argument format: {format_name}")


def _describe_first_arg_format(format_name: str) -> str:
    if format_name == "positive_int":
        return "a positive integer string"
    if format_name == "roman_numeral":
        return "a Roman numeral string"
    return "a valid marker string"


def _first_arg_hint(node: MarkupNode, format_name: str) -> str:
    sample = "2" if format_name == "positive_int" else "i"
    return f"use (*@{full_name(node)}@[[{sample}]][[Your text here]]@*)"
