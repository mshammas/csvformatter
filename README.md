# csvformatter README

csvformatter is an extension which works on CSV files to print them in a table format. It also provides a variety of options to filter and manipulate columns.

## Usage

1. **Open a CSV File**  
   Open any CSV file in VS Code.

2. **Trigger the Command**  
   Open the Command Palette (`Ctrl+Shift+P` on Windows/Linux or `Cmd+Shift+P` on macOS) and select **CSVFormatter: Format CSV**.

3. **Enter Parameters**  
   A web view panel will open on the right side of your editor. Fill in the parameters:
   - **Max Size (-s):** Maximum character count per column (default is `20`; enter `all` to display full content).
   - **Columns (-c):** Specify the number of columns to display (e.g., `2` to display the first two columns).
   - **Range (-r):** Enter a list of column numbers separated by hyphens (e.g., `1-3-4`).
   - **Filter (-f):** Filter rows by specifying a column and its values.  
     For literal matches, supply values separated by dashes (e.g., `3-Integer-float`).  
     For regex filtering, prefix a value with `regex:` (e.g., `3-regex:.*64.*`).
   - **Match (-m):** Match rows that have the same values as a specified reference row at given columns.  
     **Format:** `<row>-<col1>-<col2>-...` (e.g., `10-1-3-4-7` means that row 10 is used as a reference and only rows with the same values in columns 1, 3, 4, and 7 will be printed).
   - **Execute (-x):** Execute a shell command on a column value (e.g., `1-"awk -F. '{print $5}'"`).  
     **Note:** If both -m and -x are given, the match filter (-m) is applied first, and then the execution commands (-x) are applied on the filtered rows.
   - **Query (-q):** Check this box to print the CSV header with column indices and exit.
   - **Output (-o):** Enter an output filename to save the formatted CSV (if left blank, the output will be shown in a new editor tab).

4. **Submit the Form**  
   Click **Submit**. The extension will run the Python script with your parameters, and you’ll see the formatted output either in a new tab or saved to the specified file.

## Features

- **CSV Formatting:**  
  Format CSV files into a clean, tabular view using a Python script.
- **Interactive Parameter Input:**  
  Provides an intuitive split-view web form with text boxes and checkboxes to input parameters such as maximum size, columns, range, filter, match, execute commands, query flag, and output file.
- **Command-Line Options:**  
  Supports various options (-s, -c, -r, -f, -m, -x, -q, -o) to customize the CSV output.
- **User-Friendly Interface:**  
  The web view panel opens split on the right, making it easy to enter options while viewing your CSV file.

![CSV Formatter Screenshot](images/csvformatter.png)

> Tip: Consider adding short animations or additional screenshots to showcase your extension in action.

## Requirements

- **Python 3:**  
  Ensure that Python 3 is installed and accessible (i.e., the `python3` command is available in your PATH).
- **Visual Studio Code:**  
  Requires VS Code version 1.x or later.

## Extension Settings

This extension contributes the following settings:

* `csvformatter.enable`: Enable/disable the CSV Formatter extension.
* `csvformatter.someSetting`: (Example setting) Set to `true` to enable additional features.

## Known Issues

- The extension depends on Python 3. If Python 3 is not installed or configured correctly, the extension might not function as expected.
- Improperly formatted CSV files might cause the Python script to return errors.

## Release Notes

### 0.0.8 - 2025-04-12
- **Match Option (-m):**  
  Added a new option to match rows that have the same values as a specified reference row at given columns.  
  *Example:* `-m10-1-3-4-7` uses row 10 as the reference and selects rows with matching values in columns 1, 3, 4, and 7.
- **Editorial Updates:**  
  Updated documentation and usage instructions to include the new match functionality.

### 0.0.6 - 2025-04-08
- **Regex Filtering (-f):**  
  Users can now filter rows using regular expressions by prefixing filter values with `regex:`.  
  *Example:* `-f 2-regex:^A.*$` filters rows where column 2 starts with "A".
- **Execution Handling (-x):**  
  Improved parsing and execution of shell commands so that commands (e.g., awk, sed, grep) run without extraneous quotes.

### 0.0.5 - 2025-04-01
- Fixed issues with the `-x` option for executing commands (e.g., awk).
- Made minor editorial changes to the README.

### 0.0.4 - 2025-03-20
- Added new parameter options for filtering and output formatting.
- Improved error handling and logging throughout.

### 0.0.3 - 2025-03-10
- Resolved issues with column selection.
- Improved formatting of the output table.

### 0.0.2 - 2025-03-01
- Initial release with basic CSV formatting and parameter input via a WebView panel.
---

## Q&A

**Q: What does CSVFormatter do?**  
**A:** CSVFormatter formats CSV files into a clean, tabular view and provides options for filtering rows, matching rows based on a reference row, and executing shell commands on CSV data.

**Q: How do I use the -f (filter) option?**  
**A:** The `-f` option filters rows based on the content of a specified column. For literal matches, provide values separated by dashes (e.g., `3-Integer-float`). To use regex filtering, prefix a value with `regex:` (e.g., `3-regex:.*64.*`).

**Q: How does the -m (match) option work?**  
**A:** The `-m` option lets you match rows that have the same values as a reference row at specified columns.  
*Format:* `<row>-<col1>-<col2>-...`  
*Example:* `-m10-1-3-4-7` means row 10 is used as the reference, and only rows with matching values in columns 1, 3, 4, and 7 are included.

**Q: Which option is applied first if both -m and -x are used?**  
**A:** When both options are provided, the match (-m) filter is applied first, and then the execution (-x) commands run on the filtered rows.

**Q: How do I report issues or request features?**  
**A:** You can post questions or report issues in the Q&A section on the Visual Studio Marketplace or open an issue in our [GitHub repository](https://github.com/yourusername/csvformatter).

---

## Following Extension Guidelines

Ensure that you've read through the extension guidelines and follow the best practices for creating your extension.

* [Extension Guidelines](https://code.visualstudio.com/api/references/extension-guidelines)

## Working with Markdown

You can author your README using Visual Studio Code. Here are some useful editor keyboard shortcuts:

* Split the editor (`Cmd+\` on macOS or `Ctrl+\` on Windows and Linux).
* Toggle preview (`Shift+Cmd+V` on macOS or `Shift+Ctrl+V` on Windows and Linux).
* Press `Ctrl+Space` (Windows, Linux, macOS) to see a list of Markdown snippets.

## For More Information

* [Visual Studio Code's Markdown Support](http://code.visualstudio.com/docs/languages/markdown)
* [Markdown Syntax Reference](https://help.github.com/articles/markdown-basics/)

**Enjoy!**
