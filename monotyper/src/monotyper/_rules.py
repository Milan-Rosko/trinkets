from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True)
class RuleSpec:
    kind: str
    variant: str | None
    min_args: int
    max_args: int
    first_arg_format: str | None = None
    render_group: str = "standalone"
    render_mode: str = "standalone"
    render_options: Mapping[str, object] = field(default_factory=dict)


def full_name_from_parts(kind: str, variant: str | None) -> str:
    return kind if variant is None else f"{kind}.{variant}"


def full_name_for_rule(rule: RuleSpec) -> str:
    return full_name_from_parts(rule.kind, rule.variant)


def get_rule(kind: str, variant: str | None) -> RuleSpec | None:
    return RULES_BY_NAME.get(full_name_from_parts(kind, variant))


def get_variants(kind: str) -> dict[str | None, RuleSpec] | None:
    variants = RULES_BY_KIND.get(kind)
    if variants is None:
        return None
    return dict(variants)


def _rule(
    kind: str,
    variant: str | None,
    min_args: int,
    max_args: int,
    *,
    first_arg_format: str | None = None,
    render_group: str = "standalone",
    render_mode: str = "standalone",
    **render_options: object,
) -> RuleSpec:
    return RuleSpec(
        kind=kind,
        variant=variant,
        min_args=min_args,
        max_args=max_args,
        first_arg_format=first_arg_format,
        render_group=render_group,
        render_mode=render_mode,
        render_options=render_options,
    )


# To add a new rule, define one new entry here. If it fits an existing
# render_mode family, no other file needs to change.
_rules: tuple[RuleSpec, ...] = (
    # Sparse, general-purpose surface.
    _rule("file", None, 0, 0, render_mode="file_comment"),
    _rule("section", None, 1, 1, render_mode="box", double=False),
    _rule("inline", None, 1, 1, render_mode="legacy_inline_block", text_arg=0),
    _rule("unicode", None, 1, 1, render_mode="unicode_comment", text_arg=0),
    _rule("unicodemath", None, 1, 10_000, render_mode="unicodemath_lines"),
    _rule("todo", None, 1, 1, render_mode="todo_box", text_arg=0),

    # File headers and identity fragments.
    _rule(
        "head",
        "start",
        0,
        0,
        render_mode="template_constant",
        template="legacy_head_start",
    ),
    _rule(
        "head",
        "end",
        0,
        0,
        render_mode="template_constant",
        template="legacy_head_end",
    ),
    _rule("mr", None, 0, 0, render_mode="template_constant", template="sig"),
    _rule(
        "signature",
        None,
        0,
        0,
        render_mode="template_constant",
        template="legacy_signature",
    ),
    _rule(
        "copyright",
        None,
        0,
        0,
        render_mode="template_constant",
        template="copy",
    ),
    _rule("doc", "proofcase", 0, 0, render_mode="legacy_doc_proofcase"),
    _rule("doc", "header", 1, 1, render_mode="legacy_doc_header"),
    _rule("doc", "pl", 1, 1, render_mode="legacy_doc_paragraph"),

    # Reusable, fixed genre cards.
    _rule(
        "genre",
        "multiplexer",
        0,
        0,
        render_mode="template_constant",
        template="genre_multiplexer",
    ),
    _rule(
        "genre",
        "io",
        0,
        0,
        render_mode="template_constant",
        template="genre_io",
    ),
    _rule(
        "genre",
        "api",
        0,
        0,
        render_mode="template_constant",
        template="genre_api",
    ),
    _rule(
        "genre",
        "qed",
        0,
        0,
        render_mode="template_constant",
        template="genre_qed",
    ),
    _rule(
        "genre",
        "premise",
        0,
        0,
        render_mode="template_constant",
        template="genre_premise",
    ),
    _rule(
        "genre",
        "roadmap",
        0,
        0,
        render_mode="template_constant",
        template="genre_roadmap",
    ),

    # Structured proof comments.
    _rule("c", "inline", 1, 1, render_mode="bar_comment", text_arg=0),
    _rule(
        "c",
        "step",
        2,
        2,
        first_arg_format="positive_int",
        render_mode="bar_comment",
        text_arg=1,
        paragraph_arg=0,
        paragraph_label="Step",
    ),
    _rule("c", "standard", 1, 1, render_mode="bar_comment", text_arg=0),
    _rule("c", "steps", 1, 1, render_mode="bar_comment", text_arg=0),
    _rule(
        "c",
        "road",
        2,
        2,
        first_arg_format="positive_int",
        render_mode="bar_comment",
        text_arg=1,
        paragraph_arg=0,
    ),
    _rule(
        "c",
        "subsection",
        2,
        2,
        first_arg_format="roman_numeral",
        render_mode="subsection_box",
        label_arg=0,
        title_arg=1,
    ),
    _rule(
        "c",
        "bridge",
        2,
        2,
        render_mode="bridge_box",
        label_arg=0,
        text_arg=1,
    ),
    _rule("r", "owner", 1, 1, render_mode="synt_comment", text_arg=0),

    # Long-form documentation flow.
    _rule("H", "1", 1, 1, render_group="doc", render_mode="doc_heading", level="1"),
    _rule("H", "2", 1, 1, render_group="doc", render_mode="doc_heading", level="2"),
    _rule("H", "3", 1, 1, render_group="doc", render_mode="doc_heading", level="3"),
    _rule("H", "4", 1, 1, render_group="doc", render_mode="doc_heading", level="4"),
    _rule("p", "l", 1, 1, render_group="doc", render_mode="doc_paragraph", align="l"),
    _rule("p", "c", 1, 1, render_group="doc", render_mode="doc_paragraph", align="c"),
    _rule("p", "j", 1, 1, render_group="doc", render_mode="doc_paragraph", align="j"),
    _rule(
        "plist",
        "arabic",
        1,
        10_000,
        render_group="doc",
        render_mode="doc_list",
        style="arabic",
    ),
    _rule(
        "plist",
        "roman",
        1,
        10_000,
        render_group="doc",
        render_mode="doc_list",
        style="roman",
    ),
    _rule(
        "plist",
        "bullet",
        1,
        10_000,
        render_group="doc",
        render_mode="doc_list",
        style="bullet",
    ),
    _rule(
        "plist",
        "smallcaps",
        1,
        10_000,
        render_group="doc",
        render_mode="doc_list",
        style="smallcaps",
    ),
    _rule(
        "ptoclist",
        "roman",
        2,
        2,
        render_group="doc",
        render_mode="doc_toc_entry",
        style="roman",
    ),

    # Compatibility aliases used by existing personal sources.
    _rule("steps", None, 1, 1, render_mode="bar_comment", text_arg=0),
    _rule("r", "section", 1, 1, render_mode="box", double=True),
    _rule(
        "r",
        "subsection",
        2,
        2,
        first_arg_format="roman_numeral",
        render_mode="subsection_box",
        label_arg=0,
        title_arg=1,
    ),
    _rule(
        "r",
        "step",
        2,
        2,
        first_arg_format="positive_int",
        render_mode="bar_comment",
        text_arg=1,
        paragraph_arg=0,
        paragraph_label="Step",
    ),
    _rule("temp", "section", 1, 1, render_mode="box", double=True),
    _rule(
        "temp",
        "subsection",
        2,
        2,
        first_arg_format="roman_numeral",
        render_mode="subsection_box",
        label_arg=0,
        title_arg=1,
    ),
    _rule(
        "temp",
        "step",
        2,
        2,
        first_arg_format="positive_int",
        render_mode="bar_comment",
        text_arg=1,
        paragraph_arg=0,
        paragraph_label="Step",
    ),
    _rule("box", "section", 1, 1, render_mode="box", double=True),
)

RULES_BY_NAME: dict[str, RuleSpec] = {
    full_name_for_rule(rule): rule for rule in _rules
}

_rules_by_kind: dict[str, dict[str | None, RuleSpec]] = defaultdict(dict)
for _rule_spec in _rules:
    _rules_by_kind[_rule_spec.kind][_rule_spec.variant] = _rule_spec
RULES_BY_KIND: dict[str, dict[str | None, RuleSpec]] = dict(_rules_by_kind)
