from __future__ import annotations

import shutil
import tempfile
from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def default_input_root() -> Path:
    return project_root() / "_INPUT"


def default_output_root() -> Path:
    return project_root() / "_OUTPUT"


def discover_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*") if path.is_file())


def make_stage_dir() -> Path:
    return Path(tempfile.mkdtemp(prefix="monotyper_", dir=project_root()))


def install_stage(stage_dir: Path, output_root: Path) -> None:
    if output_root.exists():
        shutil.rmtree(output_root)
    stage_dir.replace(output_root)
