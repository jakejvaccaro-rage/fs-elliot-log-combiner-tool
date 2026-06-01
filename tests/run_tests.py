"""
Run synthetic test cases for the Sample Log Combiner.

Run from the project root with:
    python tests/run_tests.py
"""

from __future__ import annotations

import contextlib
import importlib.machinery
import importlib.util
import io
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

import make_test_cases


TESTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TESTS_DIR.parent
CASES_DIR = TESTS_DIR / "cases"
TMP_DIR = TESTS_DIR / "_tmp"


@dataclass(frozen=True)
class TestCase:
    name: str
    output_name: str
    expected_header: str | None
    expected_markers: tuple[str, ...] = ()
    forbidden_markers: tuple[str, ...] = ()
    expect_output: bool = True
    expect_no_matching: bool = False


TEST_CASES = (
    TestCase(
        name="gov_only",
        output_name="combined_gov_only.log",
        expected_header="GOV",
        expected_markers=("gov-primary-row-1", "gov-primary-row-2", "gov-nested-row-1"),
    ),
    TestCase(
        name="pps_only",
        output_name="combined_pps_only.log",
        expected_header="PPS",
        expected_markers=("pps-primary-row-1", "pps-archive-row-1", "pps-archive-row-2"),
    ),
    TestCase(
        name="mixed_gov_pps",
        output_name="combined_mixed.log",
        expected_header="GOV/PPS",
        expected_markers=("mixed-gov-row-1", "mixed-pps-row-1"),
    ),
    TestCase(
        name="nested_and_filtering",
        output_name="combined_filtering.log",
        expected_header="GOV",
        expected_markers=("filter-uppercase-log-row", "filter-lowercase-bak-row"),
        forbidden_markers=("ignored-name-row", "ignored-extension-row"),
    ),
    TestCase(
        name="no_header",
        output_name="combined_no_header.log",
        expected_header="GOV",
        expected_markers=("raw-no-header-alpha", "raw-no-header-beta"),
    ),
    TestCase(
        name="output_exclusion",
        output_name="Sample_existing_output.log",
        expected_header="GOV",
        expected_markers=("fresh-output-exclusion-row",),
        forbidden_markers=("stale-output-row",),
    ),
    TestCase(
        name="no_matching_files",
        output_name="combined_no_matching.log",
        expected_header=None,
        expect_output=False,
        expect_no_matching=True,
    ),
)


def load_module(module_name: str, module_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_pyw_module(module_name: str, module_path: Path):
    loader = importlib.machinery.SourceFileLoader(module_name, str(module_path))
    spec = importlib.util.spec_from_loader(module_name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


COMMAND_MODULE = load_module("combine_sample_logs", PROJECT_ROOT / "combine_sample_logs.py")

try:
    GUI_MODULE = load_pyw_module("combine_sample_logs_gui", PROJECT_ROOT / "combine_sample_logs_gui.pyw")
except Exception as exc:
    GUI_MODULE = None
    GUI_IMPORT_ERROR = exc
else:
    GUI_IMPORT_ERROR = None


def run_command_module(root_dir: Path, output_name: str):
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        try:
            COMMAND_MODULE.combine_logs(str(root_dir), output_name)
        except SystemExit as exc:
            code = int(exc.code or 0)
        else:
            code = 0
    return code, stream.getvalue()


def run_gui_module(root_dir: Path, output_name: str):
    messages: list[str] = []
    result = GUI_MODULE.combine_logs(str(root_dir), output_name, messages.append)
    return (0 if result else 1), "\n".join(messages)


def copy_case_to_temp(case: TestCase, temp_root: Path) -> Path:
    source = CASES_DIR / case.name
    target = temp_root / case.name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target)
    return target


def read_output(output_path: Path) -> tuple[str, list[str]]:
    text = output_path.read_text(encoding="utf-8", errors="replace")
    lines = [line for line in text.splitlines() if line.strip()]
    return text, lines


def assert_case_output(case: TestCase, output_path: Path) -> None:
    if not case.expect_output:
        if output_path.exists():
            raise AssertionError(f"{case.name}: output file should not have been created")
        return

    if not output_path.is_file():
        raise AssertionError(f"{case.name}: output file was not created")

    text, lines = read_output(output_path)
    if not lines:
        raise AssertionError(f"{case.name}: output file is empty")

    actual_header = COMMAND_MODULE.get_header_label(lines[0])
    if actual_header != case.expected_header:
        raise AssertionError(
            f"{case.name}: expected header {case.expected_header!r}, got {actual_header!r}"
        )

    header_count = sum(1 for line in lines if COMMAND_MODULE.get_header_label(line))
    if header_count != 1:
        raise AssertionError(f"{case.name}: expected exactly 1 header, got {header_count}")

    for marker in case.expected_markers:
        if marker not in text:
            raise AssertionError(f"{case.name}: missing expected marker {marker!r}")

    for marker in case.forbidden_markers:
        if marker in text:
            raise AssertionError(f"{case.name}: found forbidden marker {marker!r}")


def run_case(case: TestCase, runner_name: str, runner, temp_root: Path) -> None:
    case_root = copy_case_to_temp(case, temp_root / runner_name)
    output_path = case_root / case.output_name
    code, output = runner(case_root, case.output_name)

    if case.expect_no_matching:
        if "No matching" not in output:
            raise AssertionError(f"{case.name}: expected a no-matching-files message")
    elif code != 0:
        raise AssertionError(f"{case.name}: runner returned code {code}\n{output}")

    assert_case_output(case, output_path)


def main() -> int:
    make_test_cases.build_cases()

    runners = [("command", run_command_module)]
    if GUI_MODULE is None:
        print(f"SKIP gui: could not import combine_sample_logs_gui.pyw: {GUI_IMPORT_ERROR}")
    else:
        runners.append(("gui", run_gui_module))

    passed = 0
    failed = 0

    if TMP_DIR.exists():
        shutil.rmtree(TMP_DIR)
    TMP_DIR.mkdir(parents=True)
    temp_root = TMP_DIR

    try:
        for runner_name, runner in runners:
            for case in TEST_CASES:
                label = f"{runner_name}:{case.name}"
                try:
                    run_case(case, runner_name, runner, temp_root)
                except Exception as exc:
                    failed += 1
                    print(f"FAIL {label}: {exc}")
                else:
                    passed += 1
                    print(f"PASS {label}")
    finally:
        shutil.rmtree(TMP_DIR, ignore_errors=True)

    print(f"\n{passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
