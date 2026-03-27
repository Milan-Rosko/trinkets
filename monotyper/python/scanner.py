from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from diagnostics import Diagnostic, Severity
from model import RawMarkupBlock


@dataclass(slots=True)
class Cursor:
    text: str
    index: int = 0
    line: int = 1
    column: int = 1

    def startswith(self, token: str) -> bool:
        return self.text.startswith(token, self.index)

    def at_end(self) -> bool:
        return self.index >= len(self.text)

    def advance(self, count: int = 1) -> None:
        for _ in range(count):
            if self.at_end():
                return
            char = self.text[self.index]
            self.index += 1
            if char == "\n":
                self.line += 1
                self.column = 1
            else:
                self.column += 1


def scan_markup(path: Path, text: str) -> tuple[list[RawMarkupBlock], list[Diagnostic]]:
    cursor = Cursor(text=text)
    blocks: list[RawMarkupBlock] = []
    diagnostics: list[Diagnostic] = []

    while not cursor.at_end():
        if cursor.startswith("(*@"):
            block, block_diagnostics = _consume_markup(path, cursor)
            if block is not None:
                blocks.append(block)
            diagnostics.extend(block_diagnostics)
            continue

        if cursor.startswith("(*"):
            _consume_ordinary_comment(cursor)
            continue

        cursor.advance()

    return blocks, diagnostics


def _consume_ordinary_comment(cursor: Cursor) -> None:
    cursor.advance(2)
    depth = 1

    while depth > 0 and not cursor.at_end():
        if cursor.startswith("(*"):
            depth += 1
            cursor.advance(2)
            continue

        if cursor.startswith("*)"):
            depth -= 1
            cursor.advance(2)
            continue

        cursor.advance()


def _consume_markup(path: Path, cursor: Cursor) -> tuple[RawMarkupBlock | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []

    start_index = cursor.index
    start_line = cursor.line
    start_column = cursor.column

    cursor.advance(3)
    payload_start = cursor.index

    while not cursor.at_end():
        if cursor.startswith("@*)"):
            raw = cursor.text[payload_start:cursor.index]
            cursor.advance(3)
            block = RawMarkupBlock(
                path=path,
                start_index=start_index,
                end_index=cursor.index,
                start_line=start_line,
                start_column=start_column,
                end_line=cursor.line,
                end_column=cursor.column,
                raw=raw,
            )
            return block, diagnostics

        if cursor.startswith("(*"):
            diagnostics.append(
                Diagnostic(
                    severity=Severity.ERROR,
                    code="PM103",
                    path=path,
                    line=cursor.line,
                    column=cursor.column,
                    message="nested Rocq comments are not allowed inside markup blocks",
                    hint="close the markup block before opening another comment",
                )
            )
            _consume_invalid_markup(cursor)
            return None, diagnostics

        if cursor.startswith("*)"):
            diagnostics.append(
                Diagnostic(
                    severity=Severity.ERROR,
                    code="PM102",
                    path=path,
                    line=cursor.line,
                    column=cursor.column,
                    message="markup block closed with legacy sentinel '*)'; expected '@*)'",
                    hint="rewrite the closing delimiter to '@*)'",
                )
            )
            cursor.advance(2)
            return None, diagnostics

        cursor.advance()

    diagnostics.append(
        Diagnostic(
            severity=Severity.ERROR,
            code="PM101",
            path=path,
            line=start_line,
            column=start_column,
            message="unterminated markup block",
            hint="every markup block must close with '@*)'",
        )
    )
    return None, diagnostics


def _consume_invalid_markup(cursor: Cursor) -> None:
    while not cursor.at_end():
        if cursor.startswith("@*)"):
            cursor.advance(3)
            return
        if cursor.startswith("*)"):
            cursor.advance(2)
            return
        cursor.advance()
