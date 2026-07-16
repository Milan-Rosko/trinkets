# Monotyper

Monotyper is a strict, dependency-free compiler for sparse directives embedded in Rocq/Coq comments. It keeps annotated source minimal, then expands accepted directives into publication-oriented monospaced comments and boxes.

## Requirements

- Python 3.9 or newer

## Install and use

From the repository root:

```console
python3 -m pip install -e ./monotyper
monotyper verify monotyper/examples
monotyper render monotyper/examples monotyper/build
```

From this directory, macOS users can also double-click `monotyper.command`. It renders `examples/` into `build/`.

## Commands

```console
monotyper verify [INPUT]
monotyper render [INPUT] [OUTPUT]
monotyper dump-ast INPUT.v
```

- `verify` parses and validates without writing.
- `render` validates the complete input first, stages the result, and only then replaces the output file or directory.
- `dump-ast` prints parsed directives for one source file.

When paths are omitted, `examples/` and `build/` are used.

## Sparse syntax

```coq
(*@section@[[Identity]]@*)
(*@inline@[[A proof of `P -> P` returns the original assumption.]]@*)
(*@unicodemath@[[∀ P, P → P]]@*)
```

Directives open with `(*@`, close with `@*)`, and carry arguments in consecutive `[[...]]` blocks. Invalid syntax, unknown variants, and wrong argument counts produce source-positioned diagnostics.

The recommended surface is deliberately small:

- `file` inserts the source filename.
- `section` creates a compact section box.
- `inline` formats explanatory prose beside a proof.
- `unicode` and `unicodemath` create fixed-width Unicode comments.
- `todo` creates a visible work marker.

Optional header, genre-card, and long-form documentation directives remain available for existing source trees.

See `reference/markup-examples.txt` for the compact reference and `examples/smoketest.v` for a complete sample.

## Structure

```text
monotyper/
├── pyproject.toml
├── setup.cfg
├── monotyper.command
├── examples/
├── reference/
├── src/monotyper/
└── tests/
```
