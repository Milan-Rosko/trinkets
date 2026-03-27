from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class RawMarkupBlock:
    path: Path
    start_index: int
    end_index: int
    start_line: int
    start_column: int
    end_line: int
    end_column: int
    raw: str


@dataclass(slots=True, frozen=True)
class MarkupNode:
    kind: str
    variant: str | None
    args: list[str]
    path: Path
    line: int
    column: int
    end_line: int
    end_column: int
    raw: str
    start_index: int
    end_index: int


@dataclass(slots=True, frozen=True)
class Replacement:
    start_index: int
    end_index: int
    text: str
