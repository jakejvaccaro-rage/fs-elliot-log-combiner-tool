# Test Cases

This folder contains small synthetic test cases for the Sample Log Combiner.

Run all tests from the project root:

```powershell
python tests/run_tests.py
```

Regenerate the fixture files manually:

```powershell
python tests/make_test_cases.py
```

The test runner checks both the command-line tool and the GUI tool's shared combine logic. It copies each fixture case into a temporary folder before running, so the fixture files under `tests/cases` stay clean.

Covered cases:

- `gov_only`: source files only have a `GOV` header.
- `pps_only`: source files only have a `PPS` header.
- `mixed_gov_pps`: source files include both `GOV` and `PPS`, so the output header should be `GOV/PPS`.
- `nested_and_filtering`: matching files are found recursively, case-insensitive `.LOG` works, and nonmatching names/extensions are ignored.
- `no_header`: a matching file without the expected header is still included with a warning.
- `output_exclusion`: an existing output file with `sample` in the name is not harvested into itself.
- `no_matching_files`: folders without matching `.log` or `.bak` Sample files do not create output.
