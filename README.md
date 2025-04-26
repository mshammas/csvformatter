# csvformatter README

csvformatter is an extension which works on CSV files to print them in a table format. It also provides a variety of options to filter, match, and transform columns.

## Usage

1. **Open a CSV File**  
   Open any CSV file in VS Code.

2. **Trigger the Command**  
   Open the Command Palette (`Ctrl+Shift+P` on Windows/Linux or `Cmd+Shift+P` on macOS) and select **CSVFormatter: Format CSV**.

3. **Enter Parameters**  
   A webview panel will open on the right side of your editor. Fill in the parameters:
   - **Max Size (`-s`)**  
     Maximum character count per column (default is `20`; enter `all` to display full content).
   - **Columns (`-c`)**  
     Specify the number of columns to display (e.g., `2` to display the first two columns).
   - **Range (`-r`)**  
     Enter a list of column numbers separated by hyphens (e.g., `1-3-4`).
   - **Filter (`-f`)**  
     You can click the **+** button to add as many filter fields as you like. Each one is applied in sequence.  
     - For literal matches, supply values separated by dashes (e.g., `3-Integer-float`).  
     - For regex filtering, prefix a value with `regex:` (e.g., `3-regex:.*64.*`).
   - **Match (`-m`)**  
     Match rows that have the same values as a specified reference row at given columns.  
     **Format:** `<row>-<col1>-<col2>-...`  
     *Example:* `10-1-3-4-7` uses row 10 as the reference and only rows matching those column values are kept.
   - **Execute (`-x`)**  
     Execute a shell command on a column’s value (e.g., `1-"awk -F. '{print $5}'"`).  
     *Note:* If both `-m` and `-x` are given, matching is applied first, then commands run on the filtered rows.
   - **Query (`-q`)**  
     Check this box to print the CSV header with column indices and exit.
   - **Output (`-o`)**  
     Enter an output filename to save the formatted CSV (if left blank, the output is shown in a new editor tab).

4. **Submit the Form**  
   Click **Submit**. The extension runs the Python script with your parameters, and you’ll see the formatted output either in a new tab or saved to the specified file.

## Features

- **Multi-step Filtering (`-f`)**  
  Add multiple filter rules in sequence via the “+” button.
- **Regex & Literal Filters**  
  Use `regex:` prefix for regular-expression matching.
- **Row Matching (`-m`)**  
  Select rows based on matching values in a reference row.
- **Shell-Command Execution (`-x`)**  
  Run commands like `awk`, `grep`, or `sed` on cell values.
- **Flexible Column Selection**  
  Use `-r` or `-c` to choose specific columns or a range.
- **Query Mode (`-q`)**  
  Quickly view column indices without formatting.
- **Output to File (`-o`)**  
  Save results to disk instead of just showing in VS Code.
- **Dynamic UI**  
  Easily add or remove filter inputs in the webview form.

![CSV Formatter Screenshot](images/csvformatter.png)

> Tip: Short animations or additional screenshots can really showcase your extension in action!

## Requirements

- **Python 3**  
  Ensure `python3` is on your PATH.
- **Visual Studio Code**  
  Requires VS Code 1.x or later.

## Extension Settings

This extension contributes:

* `csvformatter.enable`: Enable/disable the CSV Formatter extension.
* `csvformatter.someSetting`: (Example) Set to `true` to enable additional features.

## Known Issues

- Depends on Python 3. If not installed/configured correctly, the extension may fail.
- Malformed CSV files can produce script errors.

## Release Notes

### 0.0.8 - 2025-04-XX
- **Multi-filter Support (`-f`):**  
  You can now specify `-f` multiple times (via the “+” button) and filters are applied one after another.
- **Dynamic UI:**  
  Added a **+** button to add more `-f` fields in the webview.
- **Documentation Updates:**  
  README and examples updated to show multi-`-f` usage.

### 0.0.7 - 2025-04-XX
- **Match Option (`-m`):**  
  New feature to match rows based on a reference row’s values in specified columns.
- **Minor Editorial Edits**  

### 0.0.6 - 2025-04-08
- **Regex Filtering (`-f`):** Prefix filter values with `regex:` for regex matches.
- **Improved Execution Handling (`-x`)**  

### 0.0.5 - 2025-04-01
- **Bug Fix:** Resolved issues with the `-x` option (e.g., `awk` handling).
- **Editorial Updates**  

### 0.0.4 - 2025-03-20
- **Added** new options for filtering and output formatting.
- **Improved** error handling and logging.

### 0.0.3 - 2025-03-10
- **Fixed** column-selection issues.
- **Enhanced** table formatting.

### 0.0.2 - 2025-03-01
- **Initial release** with basic CSV formatting and webview parameter input.

---

## Q&A

**Q: How do I apply multiple filters?**  
A: Click the **+** next to a filter field to add another. Each is applied in the order you enter them (e.g. `-f 2-Apple -f 3-Banana`).

**Q: What’s the difference between `-f` and `-m`?**  
A:  
- `-f` applies value or regex filters on a single column.  
- `-m` matches rows against a reference row’s values in multiple columns.

**Q: Which runs first, `-m` or `-x`?**  
A: `-m` (match) is applied before `-x` (execute).

**Q: How can I report issues?**  
A: Post in the Q&A on the Marketplace or open an issue at [github.com/mshammas/csvformatter](https://github.com/mshammas/csvformatter).

---

## Following Extension Guidelines

* [Extension Guidelines](https://code.visualstudio.com/api/references/extension-guidelines)

## Working with Markdown

* Split editor: `Cmd+\` / `Ctrl+\`  
* Toggle preview: `Shift+Cmd+V` / `Shift+Ctrl+V`  
* Markdown snippets: `Ctrl+Space`

**Enjoy!**
