from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from monotyper.main import run_render, run_verify


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = PROJECT_ROOT / "examples"


class MonotyperSmokeTests(unittest.TestCase):
    def test_example_verifies(self) -> None:
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            result = run_verify(EXAMPLES)

        self.assertEqual(result, 0)

    def test_example_renders_without_markup_directives(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "rendered"
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                result = run_render(EXAMPLES, output)

            rendered = (output / "smoketest.v").read_text(encoding="utf-8")

        self.assertEqual(result, 0)
        self.assertNotIn("(*@", rendered)
        self.assertIn("SPARSE SYNTAX", rendered)
        self.assertIn("Small directives keep the annotated Rocq source", rendered)

    def test_single_file_render_writes_a_file(self) -> None:
        source = EXAMPLES / "smoketest.v"
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "smoketest-rendered.v"
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                result = run_render(source, output)

            rendered = output.read_text(encoding="utf-8")

        self.assertEqual(result, 0)
        self.assertNotIn("(*@", rendered)
        self.assertIn("SPARSE SYNTAX", rendered)


if __name__ == "__main__":
    unittest.main()
