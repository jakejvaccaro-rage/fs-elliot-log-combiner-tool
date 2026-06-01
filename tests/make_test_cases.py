"""
Create small synthetic log fixtures for the Sample Log Combiner.

Run from the project root with:
    python tests/make_test_cases.py
"""

from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path


TESTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TESTS_DIR.parent
CASES_DIR = TESTS_DIR / "cases"


def load_tool_module():
    module_path = PROJECT_ROOT / "combine_sample_logs.py"
    spec = importlib.util.spec_from_file_location("combine_sample_logs", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tool = load_tool_module()
HEADER = tool.HEADER.strip()
HEADER_COLUMNS = tool.split_header_columns(HEADER)
VARIABLE_HEADER_INDEX = tool.VARIABLE_HEADER_INDEX


def header_with_label(label: str) -> str:
    columns = HEADER_COLUMNS[:]
    columns[VARIABLE_HEADER_INDEX] = label
    return "\t".join(columns)


def sample_row(marker: str, runhours: int) -> str:
    columns = ["0.00"] * len(HEADER_COLUMNS)
    columns[0] = f"08:{runhours:02d}:00"
    columns[1] = "01/01/2026"
    columns[2] = str(runhours)

    for label in ("Ains", "Aouts", "Dins", "Douts"):
        columns[HEADER_COLUMNS.index(label)] = label

    columns[-1] = marker
    return "\t".join(columns)


def write_log(path: Path, header_label: str, markers: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [header_with_label(header_label), ""]
    for index, marker in enumerate(markers, start=1):
        lines.append(sample_row(marker, index))
        if index == 1:
            lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def reset_cases_dir() -> None:
    if CASES_DIR.exists():
        shutil.rmtree(CASES_DIR)
    CASES_DIR.mkdir(parents=True)


def build_cases() -> None:
    reset_cases_dir()

    write_log(
        CASES_DIR / "gov_only" / "Sample_GOV_primary.log",
        "GOV",
        ["gov-primary-row-1", "gov-primary-row-2"],
    )
    write_log(
        CASES_DIR / "gov_only" / "Histories" / "260101_010101" / "Sample_GOV_nested.bak",
        "GOV",
        ["gov-nested-row-1"],
    )

    write_log(
        CASES_DIR / "pps_only" / "Sample_PPS_primary.log",
        "PPS",
        ["pps-primary-row-1"],
    )
    write_log(
        CASES_DIR / "pps_only" / "Sample_PPS_archive.bak",
        "PPS",
        ["pps-archive-row-1", "pps-archive-row-2"],
    )

    write_log(
        CASES_DIR / "mixed_gov_pps" / "Sample_GOV.log",
        "GOV",
        ["mixed-gov-row-1"],
    )
    write_log(
        CASES_DIR / "mixed_gov_pps" / "Histories" / "260102_020202" / "Sample_PPS.bak",
        "PPS",
        ["mixed-pps-row-1"],
    )

    write_log(
        CASES_DIR / "nested_and_filtering" / "deep" / "SAMPLE_upper.LOG",
        "GOV",
        ["filter-uppercase-log-row"],
    )
    write_log(
        CASES_DIR / "nested_and_filtering" / "deep" / "sample_lower.bak",
        "GOV",
        ["filter-lowercase-bak-row"],
    )
    write_log(
        CASES_DIR / "nested_and_filtering" / "deep" / "ProcessData.log",
        "GOV",
        ["ignored-name-row"],
    )
    write_text(
        CASES_DIR / "nested_and_filtering" / "deep" / "Sample_wrong_extension.txt",
        header_with_label("GOV") + "\n" + sample_row("ignored-extension-row", 1) + "\n",
    )

    write_text(
        CASES_DIR / "no_header" / "Sample_no_header.log",
        "raw-no-header-alpha\nraw-no-header-beta\n",
    )

    write_log(
        CASES_DIR / "output_exclusion" / "Sample_real_input.log",
        "GOV",
        ["fresh-output-exclusion-row"],
    )
    write_log(
        CASES_DIR / "output_exclusion" / "Sample_existing_output.log",
        "GOV",
        ["stale-output-row"],
    )

    write_text(
        CASES_DIR / "no_matching_files" / "ProcessData.log",
        header_with_label("GOV") + "\n" + sample_row("ignored-no-sample-name", 1) + "\n",
    )
    write_text(
        CASES_DIR / "no_matching_files" / "Sample_wrong_extension.txt",
        header_with_label("GOV") + "\n" + sample_row("ignored-wrong-extension", 1) + "\n",
    )


def main() -> None:
    build_cases()
    print(f"Created test cases in: {CASES_DIR}")


if __name__ == "__main__":
    main()
