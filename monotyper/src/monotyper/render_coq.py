from __future__ import annotations

import textwrap
from pathlib import Path

from .diagnostics import Diagnostic, Severity
from .model import MarkupNode, Replacement
from ._rules import RuleSpec, full_name_from_parts, get_rule

PARAGRAPH_LEFT_PADDING = 6
PARAGRAPH_CONTENT_WIDTH = 74
PARAGRAPH_PREFIX = " " * PARAGRAPH_LEFT_PADDING
TOC_DESCRIPTION_LEFT_PADDING = 8
TOC_DESCRIPTION_CONTENT_WIDTH = 72
TOC_DESCRIPTION_PREFIX = " " * TOC_DESCRIPTION_LEFT_PADDING
BOX_WIDTH = 78
SIDE_WIDTH = 71
STAR_BOX_WIDTH = 75
STAR_BOX_INNER_WIDTH = STAR_BOX_WIDTH - 2
STAR_BLOCK_WIDTH = 59
BAR_TEXT_WIDTH = 47
BRIDGE_BOX_TOTAL_WIDTH = 75
BRIDGE_BODY_WIDTH = BRIDGE_BOX_TOTAL_WIDTH - 4
BRIDGE_SIDE_PADDING = 2
BRIDGE_TEXT_WIDTH = BRIDGE_BODY_WIDTH - (BRIDGE_SIDE_PADDING * 2)
SUBSECTION_BOX_MAX_TEXT_WIDTH = 67
TODO_BOX_INDENT = " " * 4
TODO_BOX_INNER_WIDTH = 58
TODO_CONTENT_PADDING = 6
TODO_TEXT_WIDTH = 46
LEGACY_DOC_FRAGMENT_INNER_WIDTH = 72
LEGACY_PROOFCASE_INNER_WIDTH = 78
LEGACY_DOC_TEXT_WIDTH = 75
LEGACY_DOC_PREFIX = "  "
LEGACY_INLINE_LEFT_PADDING = 10
LEGACY_INLINE_TEXT_WIDTH = 59
LEGACY_INLINE_PREFIX = "│" + (" " * LEGACY_INLINE_LEFT_PADDING)
LEGACY_CENTERED_COMMENT_WIDTH = 70
FIXED_COMMENT_BODY_WIDTH = 76









COPY_TEMPLATE = "\n".join(
    [
        "(*",
        "┌─────────────────────────────────────────┐",
        "│ Copyright and author remark. Author(s): │",
        "│ Milan Rosko https://www.milanrosko.com. │",
        "│ Licence. This file is distributed under │",
        "│ the v2.0 Mozilla Public License bellow. │",
        "│ --------------------------------------- │",
        "│  https://www.mozilla.org/en-US/MPL/2.0  │",
        "│ --------------------------------------- │",
        "└─────────────────────────────────────────┘",
        "*)",
        " ",

    ]
)

SIG_TEMPLATE = "\n".join(
    [
        "(*",
        "(c)",
        "╔════════╤═══════════════╗",
        "║ ╭╮╮╮─╮ │               ║",
        "║ ││││╭╯ │  Milan Rosko  ║",
        "║  ╯╯╯╰  │               ║",
        "╚════════╧═══════════════╝",
        "https://www.milanrosko.com",
        'hi "at" milanrosko "." com',
        "Mozilla Public License 2.0",
        "*)",
        " ",
    ]
)

LEGACY_HEAD_START_TEMPLATE = "(*"
LEGACY_HEAD_END_TEMPLATE = "*)"

LEGACY_COPYRIGHT_FRAGMENT = "\n".join(
    [
        "┌──────────────────────────────────────────────────────────────────────────────┐",
        "│                                      Author and Copyright remark. Author(s): │",
        "│                ╭╮╮╮─╮                Milan Rosko  https://www.milanrosko.com │",
        "│                ││││╭╯                Licence. This file is distributed under │",
        "│                 ╯╯╯╰                 the Mozilla Public License Version 2.0, │",
        "│                                      visit https://www.mozilla.org/en-US/MPL │",
        "└──────────────────────────────────────────────────────────────────────────────┘",
    ]
)

LEGACY_SIGNATURE_TEMPLATE = "\n".join(
    [
        "(*",
        "(c)",
        "╔════════╤═══════════════╗",
        "║ ╭╮╮╮─╮ │               ║",
        "║ ││││╭╯ │  Milan Rosko  ║",
        "║  ╯╯╯╰  │               ║",
        "╚════════╧═══════════════╝",
        "https://www.milanrosko.com",
        "hi `at` milanrosko `.` com",
        "Mozilla Public License 2.0",
        "*)",
    ]
)


GENRE_MULTIPLEXER_TEMPLATE = "\n".join(
    [
        "│                                               _____",
        "│                        _______     _______   /____|\\__",
        "│                       | _____ |   | _____ |  \\    \\ \\ |",
        "│                       ||_   _||   ||_   _||   \\    \\ ||",
        "│                       |/    /||   |/    /||   |\\_  _\\||",
        "│                       /    / ||   /    / ||   ||     ||",
        "│                      /____/ /-|  /____/ / |   |'—————'|",
        "│                      \\____|/––'  \\____|/––'    –––––––'",
        "│                        Phase 1     Phase 2     Phase 3",
        "│",
        "│",
        "│        This file  specifies the order by selecting imported components",
        "│        and governing the overall sequence length. Each imported module",
        "│        is  routed  according  to structural role and dependency order,",
        "│        ensuring   that  control  passes  through  a  single,  coherent",
        "│        coordination layer.",
        "",
    ]
)

GENRE_IO_TEMPLATE = "\n".join(
    [
        "│              _____",
        "│             ´  _  \\",
        "│            ( /  \\  \\",
        "│             `    \\  \\            ,--.    ,-           ,--.    ,-",
        "│                   \\  \\          (_.\\ \\  //\\_)        (_.\\ \\  //\\_)",
        "│                  /    \\             \\ \\//                \\ \\//",
        "│                 /  /\\  \\             \\ (                  \\ (",
        "│                /  /  \\  \\            /, \\                 /, \\",
        "│               /  /    \\  \\          // \\ \\               // \\ \\",
        "│              /  /      \\  \\_,     _//   \\ \\_,   .-.    _//   \\ \\_,",
        "│             /__/        \\___/    (_/     \\__/   ._.   (_/     \\__/",
        "│",
        "│",
        "│        This file specifies the effective interface of the development,",
        "│        exposing   computational  content  together  with  input–output",
        "│        contracts.   Each  computational  artifact  is  linked  to  its",
        "│        semantic  interpretation  via  adequacy theorems. This layer is",
        "│        machine-oriented   and   designed   to   remain   stable  under",
        "│        extraction, testing, automation, and downstream reuse.",
        " ",
    ]
)

GENRE_API_TEMPLATE = "\n".join(
    [
        "│                                     __^__",
        "│                                     \\   /",
        "│                               __/\\__/   \\__/\\__",
        "│                               \\               /",
        "│                               /__           __\\",
        "│                                  \\         /",
        "│                    __/\\__      __/         \\__      __/\\__",
        "│                    \\    /      \\             /      \\    /",
        "│              __/\\__/    \\__/\\__/             \\__/\\__/    \\__/\\__",
        "│",
        "│",
        "│        This  file  exposes  an  API to a general formal dependency. It",
        "│        isolates  the  computational  interface  as  an abstract layer,",
        "│        while systematically relegating requests.",
        " ",
    ]
)

GENRE_QED_TEMPLATE = "\n".join(
    [
        "│        _____________________________ ___ _____ ________ ___",
        "│        ____________________________  __ \\ ___  ____/__  __ \\",
        "│        ___________________________  / / / __  __/  __  / / /",
        "│        __________________________  /_/ /___  /______  /_/ /__",
        "│        __________________________\\___\\_\\(_)_____/(_)_____/_(_)",
        "│",
        "│",
        "│        This  file specifies the exact public targets and the Rocq-side",
        "│        criteria  required by the development. It serves as the central",
        "│        certification layer, fixes the public contracts, certifies each",
        "│        endpoint  by  direct  reuse,  and  makes  the  key  assumptions",
        "│        explicit for inspection and audit.",
        " ",
    ]
)

GENRE_PREMISE_TEMPLATE = "\n".join(
    [
        "│                   ___________________   ___________________",
        "│               .-´|                   \\ /                   |`-.",
        "│               ||||    PROBLEM X.     .|    ___________     ||||",
        "│               ||||    ----------     .|   |     |     |    ||||",
        "│               ||||    Given:         .|   |  -+-+-+-  |    ||||",
        "│               ||||    -= --- - - ==  .|   |     |     |    ||||",
        "│               ||||       -=-=--      .|   `-----------´    ||||",
        "│               ||||    -- ==-- -- =-  .|   -= -- -===- -    ||||",
        "│               ||||    -=- =--=- - -  .|   Such that:       ||||",
        "│               ||||    Show:          .|   -=- -==- --=-    ||||",
        "│               ||||    --=- --= - -=  .|   -- --- -= - =    ||||",
        "│               ||||    - =--          .|   -=- --           ||||",
        "│               ||||                   .|                    ||||",
        "│               ||||         --        .|         --         ||||",
        "│               ||||___________________.| ___________________||||",
        "│               ||/====================\\|/====================\\||",
        "│                `----------------------„_„----------------------´",
        "│",
        "│",
        "│        This file provides the canonical specification of the problem’s",
        "│        premises,  to  the exclusion of any source of such. Its role is",
        "│        not  to certify premises established elsewhere, but to fix them",
        "│        at the level of the semantics themselves.",
        "",
    ]
)

GENRE_ROADMAP = "\n".join(
    [
        "│                                       .",
        "│                                       -",
        "│                                      ___",
        "│                           `  .    .'     `.     .  ´",
        "│                                  /         \\",
        "│                                 |           |",
        "│                         _  .    |           |    .  _",
        "│                                  .  :~~~:  .",
        "│                                   `. \\ / .'",
        "│                               .     |_|_|     .",
        "│                              ´      (===)      `",
        "│                                      `-´",
        "│",
        "│        This file serves as a proof-semantic synopsis and comprehension",
        "│        aid. It introduces no new constructive content  or derivations;",
        "│        rather, we c onsolidate  active  semantic layers, certification",
        "│        routes, and  package-level endpoints into one unified structure",
        "│        for readability, inspection, and auditability.",
        "",
    ]
)

TEMPLATE_CONSTANTS: dict[str, str] = {
    "copy": COPY_TEMPLATE,
    "sig": SIG_TEMPLATE,
    "legacy_head_start": LEGACY_HEAD_START_TEMPLATE,
    "legacy_head_end": LEGACY_HEAD_END_TEMPLATE,
    "legacy_signature": LEGACY_SIGNATURE_TEMPLATE,
    "genre_multiplexer": GENRE_MULTIPLEXER_TEMPLATE,
    "genre_io": GENRE_IO_TEMPLATE,
    "genre_api": GENRE_API_TEMPLATE,
    "genre_qed": GENRE_QED_TEMPLATE,
    "genre_premise": GENRE_PREMISE_TEMPLATE,
    "genre_roadmap": GENRE_ROADMAP,

}


def build_replacements(
    nodes: list[MarkupNode],
    source_text: str,
    source_path: Path,
) -> tuple[list[Replacement], list[Diagnostic]]:
    replacements: list[Replacement] = []
    diagnostics: list[Diagnostic] = []
    legacy_main_classes_profile = _uses_legacy_main_classes_profile(nodes)
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

        rendered, render_diagnostics = render_single_node(
            node,
            source_path,
            legacy_main_classes_profile=legacy_main_classes_profile,
        )
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
    *,
    legacy_main_classes_profile: bool = False,
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

    if legacy_main_classes_profile and _full_name(node) == "copyright":
        return LEGACY_COPYRIGHT_FRAGMENT, []

    if rule.render_mode == "bar_comment":
        text_arg = int(rule.render_options["text_arg"])
        paragraph_arg = rule.render_options.get("paragraph_arg")
        paragraph_number = None if paragraph_arg is None else node.args[int(paragraph_arg)]
        paragraph_label = rule.render_options.get("paragraph_label")
        return _render_bar_comment(
            node.args[text_arg],
            paragraph_number=paragraph_number,
            paragraph_label=None if paragraph_label is None else str(paragraph_label),
        ), []

    if rule.render_mode == "bar_raw":
        text_arg = int(rule.render_options["text_arg"])
        return _render_bar_raw(node.args[text_arg]), []

    if rule.render_mode == "synt_comment":
        text_arg = int(rule.render_options["text_arg"])
        return _render_synt_comment(node.args[text_arg]), []

    if rule.render_mode == "unicode_comment":
        text_arg = int(rule.render_options["text_arg"])
        return _render_unicode_comment(node.args[text_arg]), []

    if rule.render_mode == "unicodemath_lines":
        return _render_unicodemath_lines(node.args), []

    if rule.render_mode == "legacy_doc_proofcase":
        return _render_legacy_proofcase(source_path), []

    if rule.render_mode == "legacy_doc_header":
        return _render_legacy_doc_header(node.args[0]), []

    if rule.render_mode == "legacy_doc_paragraph":
        return _render_legacy_doc_paragraph(node.args[0]), []

    if rule.render_mode == "legacy_inline_block":
        text_arg = int(rule.render_options["text_arg"])
        return _render_legacy_inline_block(node.args[text_arg]), []

    if rule.render_mode == "legacy_centered_comment_lines":
        return _render_legacy_centered_comment_lines(node.args), []

    if rule.render_mode == "subsection_box":
        label_arg = int(rule.render_options["label_arg"])
        title_arg = int(rule.render_options["title_arg"])
        return _render_subsection_box(node.args[label_arg], node.args[title_arg]), []

    if rule.render_mode == "bridge_box":
        label_arg = int(rule.render_options["label_arg"])
        text_arg = int(rule.render_options["text_arg"])
        return _render_bridge_box(node.args[label_arg], node.args[text_arg]), []

    if rule.render_mode == "todo_box":
        text_arg = int(rule.render_options["text_arg"])
        return _render_todo_box(node.args[text_arg]), []

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


def _render_legacy_proofcase(source_path: Path) -> str:
    return _render_legacy_box_fragment(
        [f"Proofcase / {source_path.stem}"],
        centered=True,
        inner_width=LEGACY_PROOFCASE_INNER_WIDTH,
    )


def _render_legacy_box_fragment(
    content_lines: list[str],
    *,
    centered: bool,
    inner_width: int = LEGACY_DOC_FRAGMENT_INNER_WIDTH,
) -> str:
    lines = [
        f"┌{'─' * inner_width}┐",
    ]
    for line in content_lines:
        normalized = _normalize_inline(line)
        if centered:
            body = normalized.center(inner_width)
        else:
            body = normalized.ljust(inner_width)
        lines.append(f"│{body}│")
    lines.append(f"└{'─' * inner_width}┘")
    return "\n".join(lines)


def _render_legacy_doc_header(text: str) -> str:
    normalized = _normalize_inline(text).upper()
    if not normalized:
        return LEGACY_DOC_PREFIX
    wrapped = textwrap.wrap(
        normalized,
        width=LEGACY_DOC_TEXT_WIDTH,
        break_long_words=False,
        break_on_hyphens=False,
    )
    return "\n".join(f"{LEGACY_DOC_PREFIX}{line}" for line in wrapped)


def _render_legacy_doc_paragraph(text: str) -> str:
    wrapped = _wrap_text(text, LEGACY_DOC_TEXT_WIDTH)
    return "\n".join(f"{LEGACY_DOC_PREFIX}{line}".rstrip() for line in wrapped)


def _render_legacy_inline_block(text: str) -> str:
    lines = ["(*", "│"]
    for line in _wrap_text(text, LEGACY_INLINE_TEXT_WIDTH):
        lines.append(f"{LEGACY_INLINE_PREFIX}{line}".rstrip())
    lines.extend(["│", "*)"])
    return "\n".join(lines)


def _render_legacy_centered_comment_lines(lines: list[str]) -> str:
    return "\n".join(
        f"(*{_normalize_inline(line).center(LEGACY_CENTERED_COMMENT_WIDTH)}*)"
        for line in lines
    )


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


def _render_bar_comment(
    text: str,
    paragraph_number: str | None = None,
    paragraph_label: str | None = None,
) -> str:
    lines = ["(*", "│"]
    if paragraph_number is not None:
        if paragraph_label is None:
            lines.append(f"│  ({paragraph_number})")
        else:
            lines.append(f"│  {paragraph_label} {paragraph_number}.")

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


def _render_synt_comment(text: str) -> str:
    content = text.replace("\r\n", "\n").replace("\r", "\n").strip("\n")
    lines = ["(*", ""]

    if content:
        for raw_line in content.split("\n"):
            if raw_line:
                lines.append(f"   {raw_line.rstrip()}")
            else:
                lines.append("")
    else:
        lines.append("   ")

    lines.extend(["", "*)"])
    return "\n".join(lines)


def _render_unicode_comment(text: str) -> str:
    content = text.replace("\r\n", "\n").replace("\r", "\n").strip("\n")
    if content:
        return "\n".join(
            _render_fixed_width_comment_line(raw_line.rstrip(), centered=False)
            for raw_line in content.split("\n")
        )
    return _render_fixed_width_comment_line("", centered=False)


def _render_unicodemath_lines(items: list[str]) -> str:
    lines: list[str] = []
    for item in items:
        wrapped = _wrap_text(item, FIXED_COMMENT_BODY_WIDTH)
        lines.extend(
            _render_fixed_width_comment_line(line, centered=True)
            for line in wrapped
        )
    return "\n".join(lines)


def _render_fixed_width_comment_line(text: str, *, centered: bool) -> str:
    content = _normalize_inline(text)
    if centered:
        body = content.center(FIXED_COMMENT_BODY_WIDTH)
    else:
        body = f" {content}".ljust(FIXED_COMMENT_BODY_WIDTH)
    return f"(*{body}*)"


def _render_subsection_box(label: str, title: str) -> str:
    label_line = f"({_normalize_inline(label)})"
    title_lines = _wrap_text(title, SUBSECTION_BOX_MAX_TEXT_WIDTH)
    content_lines = [label_line, *title_lines]
    inner_width = max(len(line) for line in content_lines) + 4

    return _render_padded_box(
        content_lines,
        top_left="┌",
        horizontal="─",
        top_right="┐",
        side="│",
        bottom_left="└",
        bottom_right="┘",
        inner_width=inner_width,
    )


def _render_bridge_box(label: str, text: str) -> str:
    label_line = f"({_normalize_inline(label)})"
    text_lines = _wrap_text(text, BRIDGE_TEXT_WIDTH)
    blank_line = f"├╴{' ' * BRIDGE_BODY_WIDTH}╶┤"
    lines = [
        "(*",
        _render_bridge_border(top=True),
        blank_line,
    ]
    for line in [label_line, *text_lines]:
        padded = f"{' ' * BRIDGE_SIDE_PADDING}{line}{' ' * BRIDGE_SIDE_PADDING}".ljust(BRIDGE_BODY_WIDTH)
        lines.append(f"├╴{padded}╶┤")
    lines.extend(
        [
            blank_line,
            _render_bridge_border(top=False),
            "*)",
        ]
    )
    return "\n".join(lines)


def _render_bridge_border(*, top: bool) -> str:
    left = "┌" if top else "└"
    junction = "┬" if top else "┴"
    right = "┐" if top else "┘"
    middle_width = BRIDGE_BOX_TOTAL_WIDTH - 2
    pairs, remainder = divmod(middle_width, 2)
    middle = ("─" + junction) * pairs
    if remainder:
        middle += "─"
    return f"{left}{middle}{right}"


def _render_padded_box(
    content_lines: list[str],
    *,
    top_left: str,
    horizontal: str,
    top_right: str,
    side: str,
    bottom_left: str,
    bottom_right: str,
    inner_width: int,
) -> str:
    lines = [
        "(*",
        f"{top_left}{horizontal * inner_width}{top_right}",
        f"{side}{' ' * inner_width}{side}",
    ]
    for line in content_lines:
        padded = f"  {line}".ljust(inner_width)
        lines.append(f"{side}{padded}{side}")
    lines.extend(
        [
            f"{side}{' ' * inner_width}{side}",
            f"{bottom_left}{horizontal * inner_width}{bottom_right}",
            "*)",
        ]
    )
    return "\n".join(lines)


def _render_todo_box(text: str) -> str:
    text_lines = _wrap_text(text, TODO_TEXT_WIDTH)
    return _render_framed_box(
        ["TODO:", "", *text_lines],
        indent=TODO_BOX_INDENT,
        top_left="╭",
        top_fill="─",
        top_right="╮",
        side_left="│",
        side_right="│",
        bottom_left="╰",
        bottom_fill="─",
        bottom_right="╯",
        inner_width=TODO_BOX_INNER_WIDTH,
        left_padding=TODO_CONTENT_PADDING,
        right_padding=TODO_CONTENT_PADDING,
        top_blank_lines=2,
        bottom_blank_lines=2,
    )


def _render_framed_box(
    content_lines: list[str],
    *,
    top_left: str,
    top_fill: str,
    top_right: str,
    side_left: str,
    side_right: str,
    bottom_left: str,
    bottom_fill: str,
    bottom_right: str,
    inner_width: int,
    left_padding: int,
    right_padding: int,
    top_blank_lines: int,
    bottom_blank_lines: int,
    indent: str = "",
) -> str:
    blank_line = f"{indent}{side_left}{' ' * inner_width}{side_right}"
    lines = [
        "(*",
        f"{indent}{top_left}{top_fill * inner_width}{top_right}",
    ]
    lines.extend(blank_line for _ in range(top_blank_lines))
    for line in content_lines:
        padded = f"{' ' * left_padding}{line}{' ' * right_padding}".ljust(inner_width)
        lines.append(f"{indent}{side_left}{padded}{side_right}")
    lines.extend(blank_line for _ in range(bottom_blank_lines))
    lines.extend(
        [
            f"{indent}{bottom_left}{bottom_fill * inner_width}{bottom_right}",
            "*)",
        ]
    )
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
    wrapped = _wrap_text(text, STAR_BLOCK_WIDTH)
    left_margin = (STAR_BOX_INNER_WIDTH - STAR_BLOCK_WIDTH) // 2
    right_margin = STAR_BOX_INNER_WIDTH - STAR_BLOCK_WIDTH - left_margin
    blank_line = f"*{' ' * STAR_BOX_INNER_WIDTH}*"

    lines = [
        "(*",
        "*" * STAR_BOX_WIDTH,
        blank_line,
    ]
    for index, line in enumerate(wrapped):
        if centered:
            content = line.center(STAR_BLOCK_WIDTH)
        else:
            content = _justify_line(line, STAR_BLOCK_WIDTH, final=index == len(wrapped) - 1)
        lines.append(f"*{' ' * left_margin}{content}{' ' * right_margin}*")
    lines.extend(
        [
            blank_line,
            "*" * STAR_BOX_WIDTH,
            "*)",
        ]
    )
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


LEGACY_HEADER_DIRECTIVES = {
    "head.start",
    "head.end",
    "doc.proofcase",
    "doc.header",
    "doc.pl",
}


def _uses_legacy_main_classes_profile(nodes: list[MarkupNode]) -> bool:
    return any(_full_name(node) in LEGACY_HEADER_DIRECTIVES for node in nodes)


def _full_name(node: MarkupNode) -> str:
    return full_name_from_parts(node.kind, node.variant)
