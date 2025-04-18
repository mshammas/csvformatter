#!/usr/bin/env python3
"""
csvformatter.py 
author : Mohammed Shammas Oliyath (mohammed.shammas@gmail.com)
version: Initial (Mar 2025)

usage: csvformatter.py [-h] [-s SIZE] [-c COLUMNS] [-r RANGE] [-f FILTER] [-m MATCH]
                       [-x EXECUTE] [-q] [-o OUTPUT]
                       csv_file

Print CSV contents in a formatted table with optional filtering, execution, and column selection.

positional arguments:
  csv_file              Path to the CSV file

options:
  -h, --help            show this help message and exit

Sample CSV file (sample.csv):
---------------------------------------------
name,bio,level,city,occupation
Alice,"Alice is a software engineer with extensive experience in developing innovative solutions",Integer,New York,Engineer
Bob,"Bob is a creative designer specializing in user experience and visual storytelling",String,Los Angeles,Designer
Charlie,"Charlie is a seasoned manager with a strong track record in project delivery and team leadership",Integer,Chicago,Manager
---------------------------------------------

Options:
  -s, --size <value>
      Set maximum character count per column (default: 20).
      Use "all" to display full cell contents.
      Examples:
         -s 15      -> Truncate cells to 15 characters.
         -s all     -> Show full cell content.

  -c, --columns <N>
      Print only the first N columns.
      Example: -c 2 prints only the first two columns.

  -r, --range <list>
      Select specific columns to display (1-indexed), separated by hyphens.
      Example: -r 1-3-5 prints columns 1, 3, and 5.

  -f, --filter <column>-<value1>-<value2>-...
      Filter rows where the specified column (1-indexed) equals one or more given values.
      To use regex filtering, prefix a value with "regex:".
      Examples:
         -f 3-Integer-float
         -f 2-regex:^A.*$
      (In the second example, rows where column 2 matches the regex '^A.*$' are shown.)

  -m, --match <row>-<col1>-<col2>-...
      Match rows that have the same values as the specified reference row at the given columns.
      For example, -m10-1-3-4-7 uses row 10 as the reference (1-indexed) and only prints rows
      that have the same values in columns 1, 3, 4 and 7 as row 10.
      
  -x, --execute <column>-<command>
      Execute a shell command on the value of the specified column (1-indexed).
      The command receives the cell value via standard input, and its output replaces the original value.
      NOTE:
         - When using commands like awk that use a dollar sign (e.g. "$5"), escape the dollar sign as \\$5.
         - If -r is used, the column index for -x corresponds to the columns of the filtered output.
      Example: -x 1-"awk -F. '{print \\$5}'" applies the awk command to column 1.

  -q, --quick
      Print the CSV header with column indices (1-indexed) and exit.

  -o, --output <filename>
      Save the filtered CSV data (without truncation) to the specified file.
"""

import csv
import argparse
import sys
import subprocess
import os
import re  # Required for regex filtering

def read_csv(filename):
    """Read the CSV file and return its contents as a list of rows."""
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        return list(csvreader)

def format_table(data, max_width):
    """Return a formatted table string given CSV data.
    
    If max_width is an integer, values longer than that are truncated.
    If max_width is None, full cell values are displayed.
    """
    if not data:
        return "No data to display."
    
    if max_width is None:
        display_data = data
    else:
        def truncate(text, width):
            text = str(text)
            return text if len(text) <= width else text[:width-3] + "..."
        display_data = [[truncate(cell, max_width) for cell in row] for row in data]

    num_cols = len(display_data[0])
    col_widths = [max(len(str(row[i])) for row in display_data) for i in range(num_cols)]
    separator = "+".join("-" * (w + 2) for w in col_widths)
    lines = []
    for idx, row in enumerate(display_data):
        formatted_row = " | ".join(cell.ljust(col_widths[i]) for i, cell in enumerate(row))
        lines.append(formatted_row)
        if idx == 0:
            lines.append(separator)
    return "\n".join(lines)

def main():
    epilog_text = r"""
Sample CSV file (sample.csv):
---------------------------------------------
name,bio,level,city,occupation
Alice,"Alice is a software engineer with extensive experience in developing innovative solutions",Integer,New York,Engineer
Bob,"Bob is a creative designer specializing in user experience and visual storytelling",String,Los Angeles,Designer
Charlie,"Charlie is a seasoned manager with a strong track record in project delivery and team leadership",Integer,Chicago,Manager
---------------------------------------------

Options:
  -s, --size <value>
      Set maximum character count per column (default: 20).
      Use "all" to display full cell contents.

  -c, --columns <N>
      Print only the first N columns.

  -r, --range <list>
      Select specific columns to display (1-indexed), separated by hyphens.

  -f, --filter <column>-<value1>-<value2>-...
      Filter rows where the specified column (1-indexed) equals one or more given values.
      To use regex filtering, prefix a value with "regex:".
      Examples:
         -f 3-Integer-float
         -f 2-regex:^A.*$

  -m, --match <row>-<col1>-<col2>-...
      Match rows that have the same values as the specified reference row at the given columns.
      Example: -m10-1-3-4-7

  -x, --execute <column>-<command>
      Execute a shell command on a column value. Format: <column>-<command>.
      Example: -x 1-"awk -F. '{print \\$5}'" 

  -q, --quick
      Print CSV header with column indices (1-indexed) and exit.

  -o, --output <filename>
      Save the filtered CSV data (without truncation) to the specified file.
"""
    parser = argparse.ArgumentParser(
        description="Print CSV contents in a formatted table with optional filtering, execution, and column selection.",
        epilog=epilog_text,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("csv_file", help="Path to the CSV file")
    parser.add_argument("-s", "--size", type=str, default="20",
                        help="Maximum character count for each column (default: 20, use 'all' for full size)")
    parser.add_argument("-c", "--columns", type=int,
                        help="Print only the first N columns")
    parser.add_argument("-r", "--range", type=str,
                        help="List of column numbers to print, separated by '-' (e.g., 1-3-4)")
    parser.add_argument("-f", "--filter", type=str,
                        help="Filter rows in the format <column>-<value1>-<value2>-... "
                             "For regex filtering prefix a value with 'regex:'")
    parser.add_argument("-m", "--match", type=str,
                        help="Match rows that have the same values as the specified reference row at given columns. "
                             "Format: <row>-<col1>-<col2>-... (e.g., -m10-1-3-4-7)")
    parser.add_argument("-x", "--execute", action="append",
                        help="Execute a shell command on a column value. Format: <column>-<command>.")
    parser.add_argument("-q", "--quick", action="store_true",
                        help="Print CSV header with column index numbers and exit")
    parser.add_argument("-o", "--output", type=str,
                        help="CSV filename to save the filtered CSV contents (without truncation)")
    args = parser.parse_args()

    data = read_csv(args.csv_file)

    if args.quick:
        if not data:
            print("CSV file is empty.")
            sys.exit(0)
        header = data[0]
        print("CSV Header with column indices:")
        for index, col in enumerate(header, 1):
            print(f"{index}: {col}")
        sys.exit(0)

    # Process filtering (-f option) - support literal and regex filters
    if args.filter is not None:
        try:
            filter_parts = args.filter.split("-")
            if len(filter_parts) < 2:
                raise ValueError("Invalid filter format. Expected <column>-<value1>-...")
            filter_col_index = int(filter_parts[0]) - 1
            allowed_values = filter_parts[1:]
        except Exception as e:
            print(f"Error parsing filter: {e}")
            sys.exit(1)
        
        allowed_filters = []
        for value in allowed_values:
            value = value.strip()
            if value.startswith("regex:"):
                pattern = value[len("regex:"):]
                try:
                    regex = re.compile(pattern)
                except re.error as e:
                    print(f"Invalid regex '{pattern}': {e}")
                    sys.exit(1)
                allowed_filters.append(("regex", regex))
            else:
                allowed_filters.append(("literal", value))
        
        header = data[0]
        filtered_rows = []
        for row in data[1:]:
            if filter_col_index < len(row):
                cell_value = row[filter_col_index]
                matched = False
                for typ, criterion in allowed_filters:
                    if typ == "literal":
                        if cell_value == criterion:
                            matched = True
                            break
                    else:
                        if criterion.search(cell_value):
                            matched = True
                            break
                if matched:
                    filtered_rows.append(row)
        data = [header] + filtered_rows

    # Process match (-m option)
    if args.match is not None:
        try:
            # Expecting format: <row>-<col1>-<col2>-...
            match_parts = args.match.split("-")
            if len(match_parts) < 2:
                raise ValueError("Invalid match format. Expected <row>-<col1>-<col2>-...")
            ref_row = int(match_parts[0])
            ref_index = ref_row - 1  # convert to 0-indexed
            col_indices = [int(x) - 1 for x in match_parts[1:]]
            if ref_index < 0 or ref_index >= len(data):
                raise ValueError("Reference row number out of range.")
            ref_values = []
            for col in col_indices:
                if col < len(data[ref_index]):
                    ref_values.append(data[ref_index][col])
                else:
                    ref_values.append("")
        except Exception as e:
            print(f"Error processing match option: {e}")
            sys.exit(1)
        
        # Preserve header row and filter other rows based on match
        header = data[0]
        matched_rows = [header]
        for i, row in enumerate(data[1:], start=1):
            match_all = True
            for col, ref_val in zip(col_indices, ref_values):
                if col >= len(row) or row[col] != ref_val:
                    match_all = False
                    break
            if match_all:
                matched_rows.append(row)
        data = matched_rows

    if args.range is not None:
        try:
            col_indices = [int(x) - 1 for x in args.range.split('-') if x]
        except Exception as e:
            print(f"Error parsing column range: {e}")
            sys.exit(1)
        data = [[row[i] for i in col_indices if i < len(row)] for row in data]
    elif args.columns is not None:
        data = [row[:args.columns] for row in data]

    # Process execution commands (-x option)
    if args.execute:
        for rule in args.execute:
            rule = rule.strip()
            # Remove wrapping quotes from the entire rule if present.
            if (rule.startswith('"') and rule.endswith('"')) or (rule.startswith("'") and rule.endswith("'")):
                rule = rule[1:-1]
            try:
                col_str, cmd = rule.split('-', 1)
                col_index = int(col_str) - 1
            except Exception as e:
                print(f"Error parsing execute rule '{rule}': {e}")
                sys.exit(1)
            
            # Clean the command string by removing wrapping quotes if any.
            cmd = cmd.strip()
            if (cmd.startswith('"') and cmd.endswith('"')) or (cmd.startswith("'") and cmd.endswith("'")):
                cmd = cmd[1:-1]
            
            # Execute command for each row starting from row index 1 (skip header)
            for i in range(1, len(data)):
                if col_index < len(data[i]):
                    original_value = data[i][col_index]
                    try:
                        result = subprocess.run(
                            cmd,
                            input=original_value,
                            text=True,
                            shell=True,
                            capture_output=True,
                            executable="/bin/bash",
                            env=os.environ.copy()
                        )
                        # For grep, note that exit code 1 is acceptable (no match)
                        if result.returncode in (0, 1):
                            new_value = result.stdout.strip()
                        else:
                            new_value = original_value
                    except Exception as e:
                        print(f"Error executing command '{cmd}' on '{original_value}': {e}")
                        new_value = original_value
                    data[i][col_index] = new_value

    if args.output:
        try:
            with open(args.output, 'w', newline='') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(data)
            print(f"Filtered CSV saved to {args.output}")
        except Exception as e:
            print(f"Error writing output file: {e}")
            sys.exit(1)

    if args.size.lower() == "all":
        max_width = None
    else:
        try:
            max_width = int(args.size)
        except ValueError:
            print("Invalid value for -s. Use an integer or 'all'.")
            sys.exit(1)

    table_str = format_table(data, max_width)
    print(table_str)

if __name__ == "__main__":
    main()
