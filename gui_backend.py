"""
combine_sample_logs_gui.py
--------------------------
Tkinter GUI wrapper for the sample log combiner tool.
No external libraries required — Tkinter is built into Python.

Run with:
  python combine_sample_logs_gui.py
"""

__author__ = "Jake Vaccaro"
__email__ = "jacob.vaccaro@rage-energy.com"
__version__ = "1.0.1"

import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk


# ---------------------------------------------------------------------------
# The shared header (must match exactly what appears in the source files)
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


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def find_sample_files(root_dir):
    matches = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            name_lower = filename.lower()
            if "sample" in name_lower and name_lower.endswith((".log", ".bak")):
                matches.append(os.path.join(dirpath, filename))
    return matches


def is_header_line(line, header):
    return line.strip() == header.strip()


def harvest_data(filepath, header):
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError as e:
        return [], f"[WARNING] Could not read '{filepath}': {e}"

    for i, line in enumerate(lines):
        if is_header_line(line, header):
            data_lines = lines[i + 1:]
            data_lines = [l for l in data_lines if l.strip() != ""]
            return data_lines, None

    return lines, f"[WARNING] Header not found in '{filepath}'. Including all lines."


def combine_logs(root_dir, output_filename, log_callback):
    """
    Core combine routine. Calls log_callback(message) to report progress
    so the GUI can display it in real time.
    """
    root_dir = os.path.abspath(root_dir)
    if not os.path.isdir(root_dir):
        log_callback(f"[ERROR] Directory not found: {root_dir}")
        return False

    log_callback(f"Scanning: {root_dir}\n")
    sample_files = find_sample_files(root_dir)

    if not sample_files:
        log_callback("[INFO] No matching 'sample' .log or .bak files found. Nothing to do.")
        return False

    log_callback(f"Found {len(sample_files)} matching file(s):")
    for f in sample_files:
        log_callback(f"  {f}")
    log_callback("")

    output_path = os.path.join(root_dir, output_filename)
    sample_files = [f for f in sample_files if os.path.abspath(f) != os.path.abspath(output_path)]

    rows_written = 0
    try:
        with open(output_path, "w", encoding="utf-8") as out:
            out.write(HEADER.strip() + "\n\n")
            for filepath in sample_files:
                rel = os.path.relpath(filepath, root_dir)
                data_lines, warning = harvest_data(filepath, HEADER)
                if warning:
                    log_callback(warning)
                log_callback(f"Harvesting: {rel}  ->  {len(data_lines)} row(s)")
                for line in data_lines:
                    out.write(line if line.endswith("\n") else line + "\n")
                rows_written += len(data_lines)
    except OSError as e:
        log_callback(f"[ERROR] Could not write output file: {e}")
        return False

    log_callback(f"\n✅ Done!  {rows_written} total data rows written to:")
    log_callback(f"   {output_path}")
    return True


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sample Log Combiner")
        self.resizable(True, True)
        self.minsize(600, 460)
        self.configure(padx=16, pady=16, bg="#f0f0f0")
        self._build_ui()

    # ---- UI construction ---------------------------------------------------

    def _build_ui(self):
        BG  = "#f0f0f0"
        BTN = "#0078d4"
        FG  = "white"

        # ── Notebook (tabbed container) ───────────────────────────────────────
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        # ── Tab 1: Tool ───────────────────────────────────────────────────────
        tool_frame = tk.Frame(notebook, bg=BG, padx=16, pady=16)
        notebook.add(tool_frame, text="  Tool  ")

        tk.Label(tool_frame, text="Root Folder:", bg=BG, anchor="w").grid(
            row=0, column=0, sticky="w", pady=(0, 4))

        self.folder_var = tk.StringVar()
        tk.Entry(tool_frame, textvariable=self.folder_var, width=52).grid(
            row=1, column=0, sticky="ew", padx=(0, 8))

        tk.Button(tool_frame, text="Browse…", command=self._browse,
                  bg=BTN, fg=FG, relief="flat", padx=8).grid(
            row=1, column=1, sticky="ew")

        tk.Label(tool_frame, text="Output Filename:", bg=BG, anchor="w").grid(
            row=2, column=0, sticky="w", pady=(12, 4))

        self.output_var = tk.StringVar(value="combined_output.log")
        tk.Entry(tool_frame, textvariable=self.output_var, width=52).grid(
            row=3, column=0, sticky="ew", padx=(0, 8))

        self.run_btn = tk.Button(
            tool_frame, text="▶  Run", command=self._run,
            bg="#107c10", fg=FG, relief="flat", padx=12, pady=4,
            font=("Segoe UI", 10, "bold"))
        self.run_btn.grid(row=4, column=0, columnspan=2, pady=14, sticky="ew")

        tk.Label(tool_frame, text="Progress:", bg=BG, anchor="w").grid(
            row=5, column=0, columnspan=2, sticky="w")

        self.log_box = scrolledtext.ScrolledText(
            tool_frame, height=16, state="disabled",
            font=("Consolas", 9), bg="#1e1e1e", fg="#d4d4d4",
            insertbackground="white", relief="flat")
        self.log_box.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=(4, 0))

        tk.Button(tool_frame, text="Clear Log", command=self._clear_log,
                  bg="#555", fg=FG, relief="flat", padx=8).grid(
            row=7, column=0, columnspan=2, sticky="e", pady=(6, 0))

        tool_frame.columnconfigure(0, weight=1)
        tool_frame.rowconfigure(6, weight=1)

        # ── Tab 2: About ──────────────────────────────────────────────────────
        about_frame = tk.Frame(notebook, bg=BG, padx=24, pady=24)
        notebook.add(about_frame, text="  About  ")

        # App title
        tk.Label(about_frame, text="Author Info",
                 bg=BG, font=("Segoe UI", 15, "bold")).pack(anchor="w")

        tk.Frame(about_frame, bg="#cccccc", height=1).pack(fill="x", pady=(6, 16))

        # Author info block
        info = [
            ("Name",   "Jake (Jacob) Vaccaro"),
            ("Position", "Data Engineer"),
            ("Email",    "jacob.vaccaro@rage-energy.com"),
            ("Company",  "RAGE: Rasmussen Air and Gas Energy"),
        ]
        for label, value in info:
            row = tk.Frame(about_frame, bg=BG)
            row.pack(anchor="w", pady=2)
            tk.Label(row, text=f"{label}:", bg=BG,
                     font=("Segoe UI", 10, "bold"), width=10, anchor="w").pack(side="left")
            tk.Label(row, text=value, bg=BG,
                     font=("Segoe UI", 10), anchor="w").pack(side="left")

        tk.Frame(about_frame, bg="#cccccc", height=1).pack(fill="x", pady=(16, 16))

        # README button
        tk.Label(about_frame, text="Documentation", bg=BG,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 6))
        tk.Button(about_frame, text="📄  Open README.txt", command=self._open_readme,
                  bg=BTN, fg=FG, relief="flat", padx=12, pady=6,
                  font=("Segoe UI", 10)).pack(anchor="w")

    # ---- Callbacks ---------------------------------------------------------

    def _open_readme(self):
        """Open README.txt from the same folder as this script."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        readme_path = os.path.join(script_dir, "README.txt")
        if not os.path.isfile(readme_path):
            messagebox.showwarning("Not Found",
                f"README.txt was not found in:\n{script_dir}\n\n"
                "Please make sure README.txt is in the same folder as this script.")
            return
        # Open with the OS default text viewer (Notepad on Windows, TextEdit on Mac, etc.)
        import subprocess, sys as _sys
        if _sys.platform.startswith("win"):
            os.startfile(readme_path)
        elif _sys.platform == "darwin":
            subprocess.Popen(["open", readme_path])
        else:
            subprocess.Popen(["xdg-open", readme_path])

    def _browse(self):
        folder = filedialog.askdirectory(title="Select Root Folder")
        if folder:
            self.folder_var.set(folder)

    def _log(self, message):
        """Append a line to the log box (thread-safe via after())."""
        def _append():
            self.log_box.configure(state="normal")
            self.log_box.insert(tk.END, message + "\n")
            self.log_box.see(tk.END)
            self.log_box.configure(state="disabled")
        self.after(0, _append)

    def _clear_log(self):
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", tk.END)
        self.log_box.configure(state="disabled")

    def _set_running(self, running: bool):
        """Disable/enable the Run button while work is in progress."""
        def _update():
            self.run_btn.configure(
                state="disabled" if running else "normal",
                text="⏳ Running…" if running else "▶  Run")
        self.after(0, _update)

    def _run(self):
        root_dir = self.folder_var.get().strip()
        output_name = self.output_var.get().strip() or "combined_output.log"

        if not root_dir:
            messagebox.showwarning("No Folder", "Please select a root folder first.")
            return

        self._clear_log()
        self._set_running(True)

        # Run the combine in a background thread so the GUI stays responsive
        def worker():
            combine_logs(root_dir, output_name, self._log)
            self._set_running(False)

        threading.Thread(target=worker, daemon=True).start()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app = App()
    app.mainloop()