from __future__ import annotations

import re

from diagnostics import Diagnostic, Severity
from model import MarkupNode, RawMarkupBlock

KIND_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
VARIANT_RE = re.compile(r"^[A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)*$")


def parse_block(block: RawMarkupBlock) -> tuple[MarkupNode | None, list[Diagnostic]]:
    raw = block.raw.replace("\r\n", "\n").replace("\r", "\n")

    if not raw:
        return None, [_parse_error(block, 0, "PM201", "empty markup directive")]

    has_separator = "@" in raw
    if has_separator:
        header, args_payload = raw.split("@", 1)
        if not args_payload:
            offset = len(header)
            return None, [
                _parse_error(
                    block,
                    offset,
                    "PM202",
                    "markup argument separator '@' must be followed by one or more [[...]] blocks",
                )
            ]
    else:
        header = raw
        args_payload = ""

    if not header:
        return None, [_parse_error(block, 0, "PM203", "empty markup header")]

    if any(character.isspace() for character in header):
        return None, [
            _parse_error(block, 0, "PM204", "illegal whitespace inside markup header")
        ]

    if any(character in header for character in "[]@"):
        return None, [_parse_error(block, 0, "PM205", "malformed markup header")]

    kind: str
    variant: str | None
    if "." in header:
        kind, variant = header.split(".", 1)
        if not kind or not variant:
            return None, [_parse_error(block, 0, "PM206", "malformed directive or variant")]
    else:
        kind = header
        variant = None

    if not KIND_RE.fullmatch(kind):
        return None, [_parse_error(block, 0, "PM207", f"invalid directive name '{kind}'")]

    if variant is not None and not VARIANT_RE.fullmatch(variant):
        return None, [_parse_error(block, 0, "PM208", f"invalid variant name '{variant}'")]

    args, diagnostics = _parse_args(block, raw, args_payload)
    if diagnostics:
        return None, diagnostics

    node = MarkupNode(
        kind=kind,
        variant=variant,
        args=args,
        path=block.path,
        line=block.start_line,
        column=block.start_column,
        end_line=block.end_line,
        end_column=block.end_column,
        raw=raw,
        start_index=block.start_index,
        end_index=block.end_index,
    )
    return node, []


def _parse_args(
    block: RawMarkupBlock,
    raw: str,
    args_payload: str,
) -> tuple[list[str], list[Diagnostic]]:
    if not args_payload:
        return [], []

    args: list[str] = []
    offset = len(raw) - len(args_payload)

    while offset < len(raw):
        if not raw.startswith("[[", offset):
            return [], [
                _parse_error(
                    block,
                    offset,
                    "PM209",
                    "markup arguments must be written only as consecutive [[...]] blocks",
                )
            ]

        payload_start = offset + 2
        payload_end = raw.find("]]", payload_start)
        if payload_end == -1:
            return [], [
                _parse_error(
                    block,
                    offset,
                    "PM210",
                    "unmatched argument opener '[['",
                )
            ]

        payload = raw[payload_start:payload_end]
        if "[[" in payload:
            nested_offset = payload_start + payload.index("[[")
            return [], [
                _parse_error(
                    block,
                    nested_offset,
                    "PM211",
                    "nested argument openers are not supported",
                )
            ]

        args.append(payload.replace("\r\n", "\n").replace("\r", "\n"))
        offset = payload_end + 2

    return args, []


def _parse_error(
    block: RawMarkupBlock,
    raw_offset: int,
    code: str,
    message: str,
) -> Diagnostic:
    line, column = _position_for_offset(block, raw_offset)
    return Diagnostic(
        severity=Severity.ERROR,
        code=code,
        path=block.path,
        line=line,
        column=column,
        message=message,
    )


def _position_for_offset(block: RawMarkupBlock, raw_offset: int) -> tuple[int, int]:
    line = block.start_line
    column = block.start_column + 3
    for character in block.raw[:raw_offset]:
        if character == "\n":
            line += 1
            column = 1
        else:
            column += 1
    return line, column
