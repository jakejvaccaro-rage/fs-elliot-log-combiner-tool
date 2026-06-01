# Sample Log Combiner README

## Purpose

This tool combines multiple Sample log files into one single `.log` file.

It looks through a selected folder and all of its subfolders, finds files that have `sample` in the file name, and includes files ending in:

- `.log`
- `.bak`

The tool removes the repeated header from each source file and writes one combined output file with the header shown only once at the top.

The original files are not changed.

The core functionality is the same whether you use the GUI version or the regular command-line version.

## Quick Start

### GUI Version

1. Double click `combine_sample_logs_gui.pyw`.
2. Click **Browse...**.
3. Select the highest folder that contains the logs you want combined.
4. Leave the output filename as `combined_output.log`, or type a different `.log` file name.
5. Click **Run**.
6. Look for the output file in the folder that was scanned.

### Command-Line Version

1. Double click `combine_sample_logs.py`.
2. Paste the folder path that contains the logs.
3. Press Enter.
4. Look for `combined_output.log` in the folder that was scanned.

You can also run the command-line version from a terminal:

1. Right click in the folder where `combine_sample_logs.py` is saved and click **Open in Terminal**.
2. Run:

   ```powershell
   py combine_sample_logs.py
   ```

3. Paste the folder path that contains the logs.
4. Press Enter.
5. Look for `combined_output.log` in the folder that was scanned.

If the command window closes too quickly after double clicking, run the script from a terminal instead so you can read the progress messages.

## Which File Should I Use?

- Use `combine_sample_logs_gui.pyw` if you want a window with a folder picker, output filename box, Run button, and progress log.
- Use `combine_sample_logs.py` if you want to run from a terminal, pass arguments, or double click and paste a folder path.
- Keep `gui_backend.py` in the same folder as `combine_sample_logs_gui.pyw`. The GUI version needs it.

## What the Tool Does

1. Asks for, or receives, a root folder to scan.
2. Searches that folder and all subfolders.
3. Finds files where:
   - the file name contains `sample`
   - the file extension is `.log` or `.bak`
4. Reads each matching file.
5. Removes the repeated header from each file.
6. Creates one output `.log` file.
7. Writes the shared header once at the top.
8. Appends all harvested data rows underneath that one header.

## What the Tool Does Not Do

- It does not change or delete the original log files.
- It does not sort the data by date or time.
- It does not check whether the values are correct.
- It does not remove duplicate records.
- It does not combine files that do not have `sample` in the file name.
- It does not include file types other than `.log` and `.bak`.

## Requirements

You need Python installed on the computer.

Recommended:

```text
Python 3.x
```

No external Python packages are required. The GUI version uses Tkinter, which is included with normal Python installations on Windows.

To check whether Python is installed:

1. Open Command Prompt or PowerShell.
2. Type:

   ```powershell
   py --version
   ```

   or:

   ```powershell
   python --version
   ```

3. Press Enter.

If Windows says Python is not recognized or cannot be found, Python may need to be installed or added to the Windows PATH environment variable.

Python can be quickly installed from the Microsoft Store.

## Recommended Folder Setup

Keep the tool in a known folder, for example:

```text
C:\logs\log_automation\
```

The log folder can be anywhere, for example:

```text
C:\logs\log_automation\Solventum 3M\
```

The tool does not have to be inside the same folder as the logs, but it is often easier if it is kept nearby.

For the GUI version, keep these files together in the same folder:

- `combine_sample_logs_gui.pyw`
- `gui_backend.py`
- `README.md`

For the command-line version, keep this file available:

- `combine_sample_logs.py`

## How to Run the GUI Version

### Option 1: Double Click the GUI File

1. Double click `combine_sample_logs_gui.pyw`.
2. In the **Tool** tab, click **Browse...**.
3. Choose the root folder to scan.
4. Check the **Output Filename** field.

   By default, the output file is:

   ```text
   combined_output.log
   ```

5. Click **Run**.
6. Watch the **Progress** box for status messages.
7. When the tool finishes, look for the output file in the root folder that was scanned.

### Option 2: Run the GUI from a Terminal

1. Open Command Prompt or PowerShell.
2. Change to the folder where the GUI files are saved.

   Example:

   ```powershell
   cd "C:\logs\log_automation"
   ```

3. Run:

   ```powershell
   py combine_sample_logs_gui.pyw
   ```

   If that does not work, try:

   ```powershell
   python combine_sample_logs_gui.pyw
   ```

The GUI version writes the same kind of combined `.log` file as the command-line version.

## How to Run the Command-Line Version

### Option 1: Double Click the Command-Line File

1. Double click `combine_sample_logs.py`.
2. When prompted, paste or type the root folder path to scan.
3. Press Enter.
4. Wait for the script to finish.
5. Look for the output file in the root folder that was scanned.

If the command window closes too quickly to read the messages, use one of the terminal options below.

### Option 2: Run the Script and Let It Ask for the Folder

1. Open Command Prompt or PowerShell.
2. Change to the folder where the script is saved.

   Example:

   ```powershell
   cd "C:\logs\log_automation"
   ```

3. Run the script:

   ```powershell
   py combine_sample_logs.py
   ```

   If that does not work, try:

   ```powershell
   python combine_sample_logs.py
   ```

4. When prompted, paste or type the root folder path to scan.

   The path can be easily copied in Windows 11 by clicking on the blank space to the right of the arrow on the top of File Explorer.

   Example:

   ```text
   Desktop > Logs > log_automation > |CLICK HERE AND COPY THIS TEXT|
   ```

   Example path:

   ```text
   C:\Source\log_automation\Solventum 3M
   ```

5. Press Enter.
6. Wait for the script to finish.

### Option 3: Run the Script with the Folder Path Already Included

Use this format:

```powershell
py combine_sample_logs.py "C:\path\to\log folder"
```

Example:

```powershell
py combine_sample_logs.py "C:\logs\log_automation\Solventum 3M"
```

### Option 4: Choose a Custom Output File Name

By default, the script creates:

```text
combined_output.log
```

To choose a different output name, use this format:

```powershell
py combine_sample_logs.py "C:\path\to\log folder" "my_output.log"
```

Example:

```powershell
py combine_sample_logs.py "C:\logs\log_automation\Solventum 3M" "Solventum_combined.log"
```

## Where the Output File Goes

The combined output file is written into the root folder that was scanned.

Example:

If the scanned folder is:

```text
C:\logs\log_automation\Solventum 3M
```

and the default output name is used, the result will be:

```text
C:\logs\log_automation\Solventum 3M\combined_output.log
```

## Default Output File Name

If no custom output name is provided, the tool writes:

```text
combined_output.log
```

If this file already exists, it will be overwritten.

To keep an older output file, rename it before running the tool again, or run the tool with a different output name.

## Example Output

The final file should look like one continuous log file:

```text
Time	Date	Runhours	 Ains	 DPT	SPT	OPT	MAT	IOT	IAT	LVT	HVT	SAPT	OFDP	AFDP	LOLT	ATT	IPT	DST	CFT	CPT	ORT	MOPT	DTT	ACT	FIT	FDT	SDT	SMT	SMT2	SMT3	HOT	LOT	BOT	SIP	TIP	WPT	WTT	IMT	OMT	IDTX	ODTX	IDTX	ODTY	LVTY	HVTY	HVT2	_M5V	_M24V	_MHS	Aouts	 IVT	UVT	Dins	 M	RST	RSP	RU	SAPS	ESTOP	LOLS	DTP	PMI	GOV	AFDPS	OFDPS	TTS	SPARE	REM_ACK	REM_RESET	Douts	 MTR	MST	MSP	TST	ATST	AOP	SVF_CWS_OME	HORN	LT1	CAR	LT2	CTR	TIS	LT3	MSH

data row from file 1
data row from file 1
data row from file 2
data row from file 2
data row from file 3
```

The header appears only once at the top.

There should not be separate headers between files.
There should not be separator lines between files.

## Messages You May See

These messages may appear in the terminal or in the GUI progress box.

**Found matching file(s)**

This means the tool found Sample `.log` or `.bak` files and will combine them.

**Harvesting**

This means the tool is reading one matching file and copying the data rows below the header.

**Done**

This means the combined output file was created successfully.

**No matching files found**

The selected folder did not contain any `.log` or `.bak` files with `sample` in the file name. Check that the correct folder was selected.

**Header not found**

The tool could not find the expected header in one file. It will include the whole file and print a warning. This may mean the file has a different format than expected.

**Could not read**

The file could not be opened. It may be locked, missing, damaged, or blocked by permissions.

## Troubleshooting

### Problem: Python Is Not Recognized

What to try:

Install Python 3, or ask IT to install Python 3. If installing Python yourself, make sure **Add Python to PATH** is selected during installation.

### Problem: The GUI Window Does Not Open

What to check:

- Make sure Python is installed.
- Make sure `combine_sample_logs_gui.pyw` and `gui_backend.py` are in the same folder.
- Try running the GUI from a terminal so any error message stays visible.

### Problem: The Command-Line Window Closes After Double Clicking

What to try:

Run `combine_sample_logs.py` from Command Prompt or PowerShell instead. The tool will still work by double clicking, but running from a terminal makes the messages easier to read.

### Problem: The Tool Says No Matching Files Were Found

What to check:

- Make sure you selected the top-level log folder.
- Make sure the file names contain `sample`.
- Make sure the files end in `.log` or `.bak`.

### Problem: The Output File Is Empty Except for the Header

What to check:

- The matching files may not contain data below the header.
- The wrong folder may have been selected.

### Problem: The Output File Is Very Large

What to know:

This may be normal. The tool combines all matching Sample `.log` and `.bak` files under the selected folder.

### Problem: The Output Looks Misaligned in Notepad

What to know:

The file is tab-delimited. Some text editors display tabs differently. Try opening it in Notepad++, Excel, or another editor that handles large tab-delimited files well.

### Problem: The Ampersand (`&`) Character or Space (` `) Character Is Not Allowed

Try:

Use quotation marks around your specified path:

```powershell
"C:\Users\JacobVaccaro\OneDrive - Rasmussen Air & Gas Energy INC\Desktop\logs\log_automation\Solventum 3M\Log_C3ET2E118_2025 09 30"
```

The tool should easily accept the path after this.

What to know:

Normally file paths cannot contain strings or `&` operators because they are used to mean different things in a command. If we want to pass them as a part of the file path, using quotation marks around it denotes that path as a string, which should be evidenced by the color changing in your terminal.

## Important Notes

- Select the highest folder that contains all of the logs you want combined.
- The search includes all subfolders.
- Both the GUI version and the regular command-line version can be launched by double clicking the file in Windows.
- The order of files is not important for this task.
- The output is meant to be one continuous `.log` file.
- Do not manually add separator lines between harvested sections.
- Keep the output file name ending in `.log`.
- Keep `gui_backend.py` with `combine_sample_logs_gui.pyw` if you use the GUI version.
