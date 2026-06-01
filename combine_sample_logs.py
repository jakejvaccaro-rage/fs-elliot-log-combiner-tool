"""
combine_sample_logs.py
----------------------
Scans a root directory (and its subfolders) for .log and .bak files whose
names contain "sample" (case-insensitive), strips the shared header from
each file, and writes a single combined output .log file with the header
appearing only once at the top.

Expected folder structure (both layouts are handled automatically):
  root/
  ├── Sample1Hour.log
  ├── Sample1Hour.bak
  └── Histories/
      ├── 240910_024502/
      │   ├── Sample1Hour.log
      │   └── Sample1Hour.bak
      └── 241015_130000/
          ├── Sample1Hour.log
          └── Sample1Hour.bak

Usage:
  python combine_sample_logs.py                        # prompts for root folder
  python combine_sample_logs.py "C:/path/to/root"      # pass root folder directly
  python combine_sample_logs.py "C:/path/to/root" "my_output.log"  # custom output name
"""

__author__ = "Jake Vaccaro"
__email__ = "jacob.vaccaro@rage-energy.com"
__version__ = "1.2"

import os
import sys


# ---------------------------------------------------------------------------
# The shared header layout. The GOV/PPS column label can vary by site.
# ---------------------------------------------------------------------------
HEADER = (
    "Time\tDate\tRunhours\t Ains\t DPT\tSPT\tOPT\tMAT\tIOT\tIAT\tLVT\tHVT\t"
    "SAPT\tOFDP\tAFDP\tLOLT\tATT\tIPT\tDST\tCFT\tCPT\tORT\tMOPT\tDTT\tACT\t"
    "FIT\tFDT\tSDT\tSMT\tSMT2\tSMT3\tHOT\tLOT\tBOT\tSIP\tTIP\tWPT\tWTT\t"
    "IMT\tOMT\tIDTX\tODTX\tIDTX\tODTY\tLVTY\tHVTY\tHVT2\t_M5V\t_M24V\t_MHS\t"
    "Aouts\t IVT\tUVT\tDins\t M\tRST\tRSP\tRU\tSAPS\tESTOP\tLOLS\tDTP\tPMI\t"
    "GOV\tAFDPS\tOFDPS\tTTS\tSPARE\tREM_ACK\tREM_RESET\tDouts\t MTR\tMST\tMSP\t"
    "TST\tATST\tAOP\tSVF_CWS_OME\tHORN\tLT1\tCAR\tLT2\tCTR\tTIS\tLT3\tMSH\t"
)

VARIABLE_HEADER_LABELS = {"GOV", "PPS", "GOV/PPS"}


def split_header_columns(line):
    return [
        part.strip().lstrip("\ufeff")
        for part in line.strip().split("\t")
        if part.strip()
    ]


EXPECTED_HEADER_COLUMNS = split_header_columns(HEADER)
VARIABLE_HEADER_INDEX = EXPECTED_HEADER_COLUMNS.index("GOV")


def get_header_label(line):
    """
    Returns GOV, PPS, or GOV/PPS when a line is a known log header.
    Returns None for data rows or unknown header shapes.
    """
    columns = split_header_columns(line)
    if len(columns) != len(EXPECTED_HEADER_COLUMNS):
        return None

    for i, column in enumerate(columns):
        if i == VARIABLE_HEADER_INDEX:
            if column not in VARIABLE_HEADER_LABELS:
                return None
        elif column != EXPECTED_HEADER_COLUMNS[i]:
            return None

    return columns[VARIABLE_HEADER_INDEX]


def select_output_header_label(header_labels):
    labels = set(header_labels)
    if "GOV/PPS" in labels or {"GOV", "PPS"}.issubset(labels):
        return "GOV/PPS"
    if "PPS" in labels:
        return "PPS"
    return "GOV"


def make_output_header(header_label):
    return HEADER.strip().replace("\tGOV\t", f"\t{header_label}\t")


def find_sample_files(root_dir):
    """
    Recursively walk root_dir and return a list of matching file paths.
    A file matches if:
      - Its name contains 'sample' (case-insensitive)
      - Its extension is .log or .bak
    """
    matches = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            name_lower = filename.lower()
            if "sample" in name_lower and name_lower.endswith((".log", ".bak")):
                matches.append(os.path.join(dirpath, filename))
    return matches


def is_header_line(line):
    """
    Returns True if the line matches a known log header variant.
    """
    return get_header_label(line) is not None


def detect_header_label(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                label = get_header_label(line)
                if label:
                    return label
    except OSError:
        return None
    return None


def harvest_data(filepath):
    """
    Reads a file and returns all lines that come AFTER the header line.
    If the header is not found, returns all lines (with a warning).
    """
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError as e:
        print(f"  [WARNING] Could not read '{filepath}': {e}")
        return []

    # Find the header line
    for i, line in enumerate(lines):
        if is_header_line(line):
            data_lines = lines[i + 1:]  # everything after the header
            # Filter out all blank/whitespace-only lines anywhere in the file
            data_lines = [l for l in data_lines if l.strip() != ""]
            return data_lines

    # Header not found — include all lines but warn
    print(f"  [WARNING] Header not found in '{filepath}'. Including all lines.")
    return lines


def combine_logs(root_dir, output_filename="combined_output.log"):
    """
    Main routine: find files, harvest data, write combined output.
    """
    root_dir = os.path.abspath(root_dir)
    if not os.path.isdir(root_dir):
        print(f"[ERROR] Root directory not found: {root_dir}")
        sys.exit(1)

    print(f"\nScanning: {root_dir}")
    sample_files = find_sample_files(root_dir)

    if not sample_files:
        print("[INFO] No matching 'sample' .log or .bak files found. Nothing to do.")
        sys.exit(0)

    print(f"Found {len(sample_files)} matching file(s):")
    for f in sample_files:
        print(f"  {f}")

    # Write combined output to the root directory
    output_path = os.path.join(root_dir, output_filename)

    # Guard: don't accidentally harvest the output file if it already exists
    sample_files = [f for f in sample_files if os.path.abspath(f) != os.path.abspath(output_path)]
    output_header_label = select_output_header_label(
        detect_header_label(f) for f in sample_files
    )
    print(f"Output header: {output_header_label}")

    rows_written = 0
    with open(output_path, "w", encoding="utf-8") as out:
        # Write the header once
        out.write(make_output_header(output_header_label) + "\n\n")

        for filepath in sample_files:
            print(f"\nHarvesting: {os.path.relpath(filepath, root_dir)}")
            data_lines = harvest_data(filepath)
            print(f"  -> {len(data_lines)} data row(s)")
            for line in data_lines:
                out.write(line if line.endswith("\n") else line + "\n")
            rows_written += len(data_lines)

    print(f"\nDone! {rows_written} total data rows written to:")
    print(f"  {output_path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Argument 1: root directory (optional — will prompt if not provided)
    if len(sys.argv) >= 2:
        root_directory = sys.argv[1]
    else:
        root_directory = input("Enter the root folder path to scan: ").strip().strip('"')

    # Argument 2: output filename (optional)
    output_name = sys.argv[2] if len(sys.argv) >= 3 else "combined_output.log"

    combine_logs(root_directory, output_name)
    
