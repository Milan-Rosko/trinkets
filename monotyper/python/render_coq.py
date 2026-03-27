from __future__ import annotations

import textwrap
from pathlib import Path

from diagnostics import Diagnostic, Severity
from model import MarkupNode, Replacement
from _rules import RuleSpec, full_name_from_parts, get_rule

PARAGRAPH_LEFT_PADDING = 6
PARAGRAPH_CONTENT_WIDTH = 74
PARAGRAPH_PREFIX = " " * PARAGRAPH_LEFT_PADDING
TOC_DESCRIPTION_LEFT_PADDING = 8
TOC_DESCRIPTION_CONTENT_WIDTH = 72
TOC_DESCRIPTION_PREFIX = " " * TOC_DESCRIPTION_LEFT_PADDING
BOX_WIDTH = 73
SIDE_WIDTH = 71
STAR_TEXT_WIDTH = 63
BAR_TEXT_WIDTH = 47
SUBSECTION_BOX_MAX_TEXT_WIDTH = 67

QEDINFO_TEMPLATE = "\n".join(
    [
        "(*",
        "┌─────────────────────────────────────────────────────────────────────────┐",
        "│                                                                         │",
        "│                          CERTIFICATION LAYER                            │",
        "│                                                                         │",
        "│     ________________________ __________________                         │",
        "│     ___________________  __ \\ ___  ____/__  __ \\                        │",
        "│     __________________  / / / __  __/  __  / / /                        │",
        "│     _________________/ /_/ /___  /______  /_/ /__                       │",
        "│     _________________\\___\\_\\(_)_____/(_)_____/_(_)                      │",
        "│                                                                         │",
        "│                                                                         │",
        "│     This  file  specifies the exact public target and the Rocq-side     │",
        "│     criteria  required  by  the  reductions.  It  forms the central     │",
        "│     certificate  layer of the development and serves as the primary     │",
        "│     point  of verification. It also defines the contract fixing the     │",
        "│     subject  of proof, certifies each endpoint by direct reuse, and     │",
        "│     makes all key assumptions explicit for inspection and audit.        │",
        "│                                                                         │",
        "│                                                                         │",
        "└─────────────────────────────────────────────────────────────────────────┘",
        "*)",
    ]
)

COMPREHENSION_TEMPLATE = "\n".join(
    [
        "(*",
        "┌─────────────────────────────────────────────────────────────────────────┐",
        "│                                                                         │",
        "│                          COMPREHENSION LAYER                            │",
        "│                                                                         │",
        "│                                   .                                     │",
        "│                                   -                                     │",
        "│                                  ___                                    │",
        "│                       `  .    .'     `.     .  ´                        │",
        "│                              /         \\                                │",
        "│                             |           |                               │",
        "│                     _  .    |           |    .  _                       │",
        "│                              .  :~~~:  .                                │",
        "│                               `. \\ / .'                                 │",
        "│                           .     |_|_|     .                             │",
        "│                          ´      (===)      `                            │",
        "│                                  `-´                                    │",
        "│                                                                         │",
        "│     This file serves as a proof-semantic synopsis and comprehension     │",
        "│     aid.  Its  primary  purpose is to support human readability and     │",
        "│     auditability.  It  introduces  no  new  constructive content or     │",
        "│     derivations,  rather,  it  consolidates the odd-part arithmetic     │",
        "│     interface—namely, finite odd-codomain control, the CIC contract     │",
        "│     layer,  and  the divisibility endpoint—into a unified structure     │",
        "│     for clarity, inspection, and verification.                          │",
        "│                                                                         │",
        "└─────────────────────────────────────────────────────────────────────────┘",
        "*)",
    ]
)

TEMPLATE_CONSTANTS: dict[str, str] = {
    "comprehension": COMPREHENSION_TEMPLATE,
    "qedinfo": QEDINFO_TEMPLATE,
}


def build_replacements(
    nodes: list[MarkupNode],
    source_text: str,
    source_path: Path,
) -> tuple[list[Replacement], list[Diagnostic]]:
    replacements: list[Replacement] = []
    diagnostics: list[Diagnostic] = []
    index = 0

    while index < len(nodes):
        node = nodes[index]

        if _is_doc_flow(node):
            end_index = index + 1
            while end_index < len(nodes):
                gap = source_text[nodes[end_index - 1].end_index : nodes[end_index].start_index]
                if not _is_doc_flow(nodes[end_index]) or gap.strip():
                    break
                end_index += 1
            replacement_start, indentation = _replacement_prefix(
                source_text,
                nodes[index].start_index,
            )

            replacements.append(
                Replacement(
                    start_index=replacement_start,
                    end_index=nodes[end_index - 1].end_index,
                    text=_with_indentation(
                        render_doc_block(nodes[index:end_index]),
                        indentation,
                    ),
                )
            )
            index = end_index
            continue

        rendered, render_diagnostics = render_single_node(node, source_path)
        diagnostics.extend(render_diagnostics)
        if rendered is not None:
            replacement_start, indentation = _replacement_prefix(
                source_text,
                node.start_index,
            )
            replacements.append(
                Replacement(
                    start_index=replacement_start,
                    end_index=node.end_index,
                    text=_with_indentation(
                        rendered,
                        indentation,
                    ),
                )
            )
        index += 1

    return replacements, diagnostics


def apply_replacements(text: str, replacements: list[Replacement]) -> str:
    parts: list[str] = []
    cursor = 0

    for replacement in replacements:
        parts.append(text[cursor:replacement.start_index])
        parts.append(replacement.text)
        cursor = replacement.end_index

    parts.append(text[cursor:])
    return "".join(parts)


def render_single_node(
    node: MarkupNode,
    source_path: Path,
) -> tuple[str | None, list[Diagnostic]]:
    rule = get_rule(node.kind, node.variant)
    if rule is None:
        full_name = _full_name(node)
        return None, [
            Diagnostic(
                severity=Severity.ERROR,
                code="PM501",
                path=node.path,
                line=node.line,
                column=node.column,
                message=f"no Coq renderer is implemented for '{full_name}'",
            )
        ]

    if rule.render_mode == "file_comment":
        return f"(*{source_path.name}*)", []

    if rule.render_mode == "bar_comment":
        text_arg = int(rule.render_options["text_arg"])
        paragraph_arg = rule.render_options.get("paragraph_arg")
        paragraph_number = None if paragraph_arg is None else node.args[int(paragraph_arg)]
        return _render_bar_comment(node.args[text_arg], paragraph_number=paragraph_number), []

    if rule.render_mode == "bar_raw":
        text_arg = int(rule.render_options["text_arg"])
        return _render_bar_raw(node.args[text_arg]), []

    if rule.render_mode == "subsection_box":
        label_arg = int(rule.render_options["label_arg"])
        title_arg = int(rule.render_options["title_arg"])
        return _render_subsection_box(node.args[label_arg], node.args[title_arg]), []

    if rule.render_mode == "template_constant":
        template_name = str(rule.render_options["template"])
        template_text = TEMPLATE_CONSTANTS.get(template_name)
        if template_text is not None:
            return template_text, []
        return _missing_renderer(node)

    if rule.render_mode == "star_banner":
        fixed_text = rule.render_options.get("fixed_text")
        if fixed_text is None:
            text_arg = int(rule.render_options["text_arg"])
            banner_text = node.args[text_arg]
        else:
            banner_text = str(fixed_text)
        centered = bool(rule.render_options["centered"])
        return _render_star_banner(banner_text, centered=centered), []

    if rule.render_mode == "box":
        return _render_box(node.args[0], double=bool(rule.render_options["double"])), []

    return _missing_renderer(node)


def render_doc_block(nodes: list[MarkupNode]) -> str:
    lines = ["(*"]
    toc_style: str | None = None
    toc_index = 0

    for node in nodes:
        rule = get_rule(node.kind, node.variant)
        if rule is None:
            continue

        if rule.render_mode == "doc_heading":
            lines.extend(
                _render_heading(str(rule.render_options["level"]), node.args[0], lines)
            )
            continue

        if rule.render_mode == "doc_paragraph":
            toc_style = None
            toc_index = 0
            lines.extend(
                _render_paragraph(str(rule.render_options["align"]), node.args[0], lines)
            )
            continue

        if rule.render_mode == "doc_list":
            toc_style = None
            toc_index = 0
            lines.extend(
                _render_list(str(rule.render_options["style"]), node.args, lines)
            )
            continue

        if rule.render_mode == "doc_toc_entry":
            style = str(rule.render_options["style"])
            if toc_style == style:
                toc_index += 1
            else:
                toc_style = style
                toc_index = 1
            lines.extend(_render_toc_entry(style, toc_index, node.args[0], node.args[1], lines))
            continue

        toc_style = None
        toc_index = 0

    lines.append("*)")
    return "\n".join(lines)


def _render_heading(level: str, text: str, lines: list[str]) -> list[str]:
    indent_map = {"1": "  ", "2": "    ", "3": "      ", "4": "        "}
    underline_map = {"1": "=", "2": "-", "3": "~", "4": "."}
    indent = indent_map.get(level, "  ")
    underline = underline_map.get(level, "-")
    heading_text = _normalize_inline(text)

    rendered: list[str] = []
    if len(lines) > 1 and lines[-1] != "":
        rendered.append("")
    rendered.append(f"{indent}{heading_text}")
    rendered.append(f"{indent}{underline * len(heading_text)}")
    return rendered


def _render_paragraph(variant: str, text: str, lines: list[str]) -> list[str]:
    rendered: list[str] = []
    if len(lines) > 1 and lines[-1] != "":
        rendered.append("")

    wrapped = _wrap_text(text, PARAGRAPH_CONTENT_WIDTH)
    for index, line in enumerate(wrapped):
        aligned = _align_text(
            line,
            PARAGRAPH_CONTENT_WIDTH,
            variant,
            final=index == len(wrapped) - 1,
        )
        rendered.append(f"{PARAGRAPH_PREFIX}{aligned}".rstrip())
    return rendered


def _render_list(variant: str, items: list[str], lines: list[str]) -> list[str]:
    rendered: list[str] = []
    if len(lines) > 1 and lines[-1] != "":
        rendered.append("")

    markers = [_list_marker(variant, index) for index, _ in enumerate(items, 1)]
    marker_width = max((len(marker) for marker in markers), default=0)
    text_width = max(1, PARAGRAPH_CONTENT_WIDTH - marker_width - 2)

    for index, item in enumerate(items, 1):
        prefix, continuation = _list_prefix(markers[index - 1], marker_width)
        wrapped = _wrap_text(item, text_width, break_long_words=True)
        for line_number, line in enumerate(wrapped):
            current_prefix = prefix if line_number == 0 else continuation
            rendered.append(f"{current_prefix}{line}")
    return rendered


def _render_bar_comment(text: str, paragraph_number: str | None = None) -> str:
    lines = ["(*", "│"]
    if paragraph_number is not None:
        lines.append(f"│  ({paragraph_number})")

    for line in _wrap_text(text, BAR_TEXT_WIDTH):
        lines.append(f"│  {line}")

    lines.extend(["│", "*)"])
    return "\n".join(lines)


def _render_bar_raw(text: str) -> str:
    content = text.replace("\r\n", "\n").replace("\r", "\n").strip("\n")
    lines = ["(*"]
    for raw_line in content.split("\n"):
        if raw_line:
            lines.append(f"│  {raw_line.rstrip()}")
        else:
            lines.append("│")
    lines.append("*)")
    return "\n".join(lines)


def _render_subsection_box(label: str, title: str) -> str:
    label_line = f"({label})"
    title_lines = _wrap_text(title, SUBSECTION_BOX_MAX_TEXT_WIDTH)
    content_lines = [label_line, *title_lines]
    inner_width = max(len(line) for line in content_lines) + 4

    lines = ["(*", f"┌{'─' * inner_width}┐"]
    for line in content_lines:
        padded = f"  {line}".ljust(inner_width)
        lines.append(f"│{padded}│")
    lines.extend([f"└{'─' * inner_width}┘", "*)"])
    return "\n".join(lines)


def _render_toc_entry(
    style: str,
    index: int,
    title: str,
    description: str,
    lines: list[str],
) -> list[str]:
    rendered: list[str] = []
    if len(lines) > 1 and lines[-1] != "":
        rendered.append("")

    marker = _list_marker(style, index)
    rendered.append(f"{PARAGRAPH_PREFIX}{marker}")

    for line in _wrap_text(title, PARAGRAPH_CONTENT_WIDTH):
        rendered.append(f"{PARAGRAPH_PREFIX}{line}".rstrip())

    rendered.append("")

    wrapped_description = _wrap_text(description, TOC_DESCRIPTION_CONTENT_WIDTH)
    for line in wrapped_description:
        rendered.append(f"{TOC_DESCRIPTION_PREFIX}{line}".rstrip())

    return rendered


def _render_box(title: str, double: bool) -> str:
    if double:
        top_left, horizontal, top_right = "╔", "═", "╗"
        side = "║"
        bottom_left, bottom_right = "╚", "╝"
    else:
        top_left, horizontal, top_right = "┌", "─", "┐"
        side = "│"
        bottom_left, bottom_right = "└", "┘"

    title_text = _normalize_inline(title).center(BOX_WIDTH)
    lines = [
        "(*",
        f"{top_left}{horizontal * BOX_WIDTH}{top_right}",
        f"{side}{' ' * BOX_WIDTH}{side}",
        f"{side}{title_text}{side}",
        f"{side}{' ' * BOX_WIDTH}{side}",
        f"{bottom_left}{horizontal * BOX_WIDTH}{bottom_right}",
        "*)",
    ]
    return "\n".join(lines)


def _render_star_banner(text: str, centered: bool) -> str:
    outer_blank = f"(*{' ' * SIDE_WIDTH}*)"
    border = f"(*{'*' * SIDE_WIDTH}*)"
    wrapped = _wrap_text(text, STAR_TEXT_WIDTH)

    lines = [border, outer_blank]
    for index, line in enumerate(wrapped):
        if centered:
            content = line.center(STAR_TEXT_WIDTH)
        else:
            content = _justify_line(line, STAR_TEXT_WIDTH, final=index == len(wrapped) - 1)
        lines.append(f"(*{' ' * 4}{content}{' ' * 4}*)")
    lines.extend([outer_blank, border])
    return "\n".join(lines)


def _justify_line(line: str, width: int, final: bool) -> str:
    if final or len(line) >= width or " " not in line:
        return line.ljust(width)

    words = line.split()
    gaps = len(words) - 1
    letters = sum(len(word) for word in words)
    spaces = width - letters
    base, extra = divmod(spaces, gaps)

    parts: list[str] = []
    for index, word in enumerate(words[:-1]):
        padding = base + (1 if index < extra else 0)
        parts.append(word)
        parts.append(" " * padding)
    parts.append(words[-1])
    return "".join(parts)


def _wrap_text(text: str, width: int, *, break_long_words: bool = False) -> list[str]:
    normalized = _normalize_inline(text)
    if not normalized:
        return [""]
    return textwrap.wrap(
        normalized,
        width=width,
        break_long_words=break_long_words,
        break_on_hyphens=False,
    )


def _normalize_inline(text: str) -> str:
    return " ".join(text.replace("\n", " ").split())


def _replacement_prefix(source_text: str, index: int) -> tuple[int, str]:
    line_start = source_text.rfind("\n", 0, index) + 1
    prefix = source_text[line_start:index]
    if prefix.strip():
        return index, ""
    return line_start, prefix


def _with_indentation(text: str, indentation: str) -> str:
    if not indentation:
        return text
    return "\n".join(f"{indentation}{line}" for line in text.split("\n"))


def _missing_renderer(node: MarkupNode) -> tuple[str | None, list[Diagnostic]]:
    full_name = _full_name(node)
    return None, [
        Diagnostic(
            severity=Severity.ERROR,
            code="PM501",
            path=node.path,
            line=node.line,
            column=node.column,
            message=f"no Coq renderer is implemented for '{full_name}'",
        )
    ]


def _align_text(line: str, width: int, variant: str, *, final: bool) -> str:
    if variant == "c":
        return line.center(width)
    if variant == "j":
        return _justify_line(line, width, final=final)
    return line


def _list_prefix(marker: str, marker_width: int) -> tuple[str, str]:
    padded_marker = marker.rjust(marker_width)
    prefix = f"{PARAGRAPH_PREFIX}{padded_marker}  "
    continuation = " " * len(prefix)
    return prefix, continuation


def _list_marker(variant: str, index: int) -> str:
    if variant == "arabic":
        return f"({index})"
    if variant == "roman":
        return f"({_to_roman(index).lower()})"
    if variant == "smallcaps":
        return f"({_to_alpha(index)})"
    return "-"


def _to_roman(number: int) -> str:
    values = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]
    result: list[str] = []
    remainder = number
    for value, glyph in values:
        while remainder >= value:
            result.append(glyph)
            remainder -= value
    return "".join(result)


def _to_alpha(number: int) -> str:
    result: list[str] = []
    remainder = number

    while remainder > 0:
        remainder -= 1
        result.append(chr(ord("a") + (remainder % 26)))
        remainder //= 26

    return "".join(reversed(result))


def _is_doc_flow(node: MarkupNode) -> bool:
    rule = get_rule(node.kind, node.variant)
    return rule is not None and rule.render_group == "doc"


def _full_name(node: MarkupNode) -> str:
    return full_name_from_parts(node.kind, node.variant)
