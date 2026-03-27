from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

from diagnostics import Diagnostic, Severity, format_diagnostic
from fs_ops import default_input_root, default_output_root, discover_files, install_stage, make_stage_dir
from model import MarkupNode
from parser import parse_block
from render_coq import apply_replacements, build_replacements
from scanner import scan_markup
from validate import validate_node


@dataclass(slots=True)
class FileResult:
    path: Path
    nodes: list[MarkupNode]
    diagnostics: list[Diagnostic]
    rendered_text: str | None

    @property
    def has_errors(self) -> bool:
        return any(diagnostic.severity == Severity.ERROR for diagnostic in self.diagnostics)


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "verify":
        return run_verify(args.input)
    if args.command == "render":
        return run_render(args.input, args.output)
    if args.command == "dump-ast":
        return run_dump_ast(args.input)
    raise ValueError(f"unsupported command: {args.command}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Strict markup compiler for Rocq/Coq source files.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    verify_parser = subparsers.add_parser("verify", help="validate .v files")
    verify_parser.add_argument("input", nargs="?", type=Path, default=default_input_root())

    render_parser = subparsers.add_parser("render", help="render _INPUT to _OUTPUT")
    render_parser.add_argument("input", nargs="?", type=Path, default=default_input_root())
    render_parser.add_argument("output", nargs="?", type=Path, default=default_output_root())

    dump_ast_parser = subparsers.add_parser("dump-ast", help="print parsed nodes")
    dump_ast_parser.add_argument("input", type=Path)

    return parser


def run_verify(input_path: Path) -> int:
    input_path = input_path.resolve()
    file_results = _collect_results(input_path)
    _print_diagnostics(file_results)
    _print_summary(file_results)
    return 1 if any(result.has_errors for result in file_results) else 0


def run_render(input_path: Path, output_path: Path) -> int:
    input_path = input_path.resolve()
    output_path = output_path.resolve()
    file_results = _collect_results(input_path)

    _print_diagnostics(file_results)
    _print_summary(file_results)
    sys.stdout.flush()

    if any(result.has_errors for result in file_results):
        print("No output written because validation failed.", file=sys.stderr)
        return 1

    stage_dir = make_stage_dir()
    try:
        if input_path.is_file():
            stage_output = stage_dir / output_path.name
            stage_output.parent.mkdir(parents=True, exist_ok=True)
            _write_single_file(file_results[0], stage_output)
        else:
            _write_tree(input_path, stage_dir, file_results)
        install_stage(stage_dir, output_path)
    finally:
        if stage_dir.exists():
            shutil.rmtree(stage_dir, ignore_errors=True)

    written = len([result for result in file_results if result.path.suffix == ".v"])
    print(f"Wrote {written} output files to {output_path}")
    return 0


def run_dump_ast(input_path: Path) -> int:
    input_path = input_path.resolve()
    if input_path.is_dir():
        print("dump-ast expects a single .v file", file=sys.stderr)
        return 1

    result = _process_v_file(input_path)
    _print_file_diagnostics(result)
    if result.has_errors:
        return 1

    for node in result.nodes:
        variant = f".{node.variant}" if node.variant else ""
        print(f"{input_path}:{node.line}:{node.column} {node.kind}{variant} args={node.args!r}")
    return 0


def _collect_results(input_path: Path) -> list[FileResult]:
    if not input_path.exists():
        result = FileResult(
            path=input_path,
            nodes=[],
            diagnostics=[
                Diagnostic(
                    severity=Severity.ERROR,
                    code="PM001",
                    path=input_path,
                    line=1,
                    column=1,
                    message="input path does not exist",
                )
            ],
            rendered_text=None,
        )
        return [result]

    if input_path.is_file():
        if input_path.suffix != ".v":
            return [
                FileResult(
                    path=input_path,
                    nodes=[],
                    diagnostics=[
                        Diagnostic(
                            severity=Severity.ERROR,
                            code="PM002",
                            path=input_path,
                            line=1,
                            column=1,
                            message="input file must have a .v extension",
                        )
                    ],
                    rendered_text=None,
                )
            ]
        return [_process_v_file(input_path)]

    results: list[FileResult] = []
    for path in discover_files(input_path):
        if path.suffix == ".v":
            results.append(_process_v_file(path))
    return results


def _process_v_file(path: Path) -> FileResult:
    text = path.read_text(encoding="utf-8")
    blocks, diagnostics = scan_markup(path, text)

    nodes: list[MarkupNode] = []
    for block in blocks:
        node, parse_diagnostics = parse_block(block)
        diagnostics.extend(parse_diagnostics)
        if node is None:
            continue
        nodes.append(node)

    for node in nodes:
        diagnostics.extend(validate_node(node))

    rendered_text: str | None = None
    if not any(diagnostic.severity == Severity.ERROR for diagnostic in diagnostics):
        replacements, render_diagnostics = build_replacements(nodes, text, path)
        diagnostics.extend(render_diagnostics)
        if not any(diagnostic.severity == Severity.ERROR for diagnostic in diagnostics):
            rendered_text = apply_replacements(text, replacements)

    diagnostics.sort(key=lambda diagnostic: (str(diagnostic.path), diagnostic.line, diagnostic.column, diagnostic.code))
    return FileResult(path=path, nodes=nodes, diagnostics=diagnostics, rendered_text=rendered_text)


def _write_tree(input_root: Path, stage_dir: Path, file_results: list[FileResult]) -> None:
    result_map = {result.path: result for result in file_results}
    for source_path in discover_files(input_root):
        destination = stage_dir / source_path.relative_to(input_root)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source_path.suffix == ".v":
            _write_single_file(result_map[source_path], destination)
        else:
            shutil.copy2(source_path, destination)


def _write_single_file(result: FileResult, destination: Path) -> None:
    if result.rendered_text is None:
        raise RuntimeError(f"cannot write failed file: {result.path}")
    destination.write_text(result.rendered_text, encoding="utf-8")


def _print_diagnostics(file_results: list[FileResult]) -> None:
    for result in file_results:
        _print_file_diagnostics(result)


def _print_file_diagnostics(result: FileResult) -> None:
    for diagnostic in result.diagnostics:
        stream = sys.stderr if diagnostic.severity == Severity.ERROR else sys.stdout
        print(format_diagnostic(diagnostic), file=stream)


def _print_summary(file_results: list[FileResult]) -> None:
    warnings = sum(
        1
        for result in file_results
        for diagnostic in result.diagnostics
        if diagnostic.severity == Severity.WARNING
    )
    rejected = sum(1 for result in file_results if result.has_errors)
    accepted = len(file_results) - rejected

    print(f"Scanned {len(file_results)} files")
    print(f"Accepted: {accepted}")
    print(f"Warnings: {warnings}")
    print(f"Rejected: {rejected}")


if __name__ == "__main__":
    raise SystemExit(main())
