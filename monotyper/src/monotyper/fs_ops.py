from __future__ import annotations

import shutil
import tempfile
from pathlib import Path


def default_input_root() -> Path:
    return Path.cwd() / "examples"


def default_output_root() -> Path:
    return Path.cwd() / "build"


def _is_shadow_path(root: Path, path: Path) -> bool:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return False

    return any(
        parts[index:index + 2] == ("scratch", "shadow")
        for index in range(len(parts) - 1)
    )


def discover_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and not _is_shadow_path(root, path)
    )


def make_stage_dir(output_root: Path) -> Path:
    output_parent = output_root.resolve().parent
    output_parent.mkdir(parents=True, exist_ok=True)
    return Path(
        tempfile.mkdtemp(
            prefix=f".{output_root.name}.monotyper-",
            dir=output_parent,
        )
    )


def install_stage(stage_path: Path, output_path: Path) -> None:
    if output_path.is_symlink() or output_path.is_file():
        output_path.unlink()
    elif output_path.exists():
        shutil.rmtree(output_path)
    stage_path.replace(output_path)
