from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(slots=True, frozen=True)
class Diagnostic:
    severity: Severity
    code: str
    path: Path
    line: int
    column: int
    message: str
    hint: str | None = None


def format_diagnostic(diagnostic: Diagnostic) -> str:
    lines = [
        f"{diagnostic.severity.value}[{diagnostic.code}] "
        f"{diagnostic.path}:{diagnostic.line}:{diagnostic.column}",
        f"  {diagnostic.message}",
    ]
    if diagnostic.hint:
        lines.append(f"  hint: {diagnostic.hint}")
    return "\n".join(lines)
