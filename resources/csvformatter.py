#!/usr/bin/env python3
"""
csvformatter.py 
author : Mohammed Shammas Oliyath (mohammed.shammas@gmail.com)
version: Initial (Mar 2025)

usage: csvformatter.py [-h] [-s SIZE] [-c COLUMNS] [-r RANGE] [-f FILTER] [-m MATCH]
                       [-x EXECUTE] [-q] [-o OUTPUT]
                       csv_file

Print CSV contents in a formatted table with optional filtering, execution, and column selection.
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
        return list(csv.reader(csvfile))

def format_table(data, max_width):
    """Return a formatted table string given CSV data."""
    if not data:
        return "No data to display."
    if max_width is None:
        display_data = data
    else:
        def truncate(text, width):
            text = str(text)
            return text if len(text) <= width else text[:width-3] + "..."
        display_data = [[truncate(cell, max_width) for cell in row] for row in data]

    col_widths = [max(len(str(row[i])) for row in display_data) for i in range(len(display_data[0]))]
    separator = "+".join("-" * (w + 2) for w in col_widths)
    lines = []
    for idx, row in enumerate(display_data):
        lines.append(" | ".join(cell.ljust(col_widths[i]) for i, cell in enumerate(row)))
        if idx == 0:
            lines.append(separator)
    return "\n".join(lines)

def main():
    epilog = r"""
Sample CSV file and options...
    """
    parser = argparse.ArgumentParser(
        description="Print CSV contents in a formatted table with optional filtering, execution, and column selection.",
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("csv_file", help="Path to the CSV file")
    parser.add_argument("-s", "--size", type=str, default="20",
                        help="Max character count per column (default:20; use 'all')")
    parser.add_argument("-c", "--columns", type=int, help="Print only the first N columns")
    parser.add_argument("-r", "--range", type=str, help="Columns to print, hyphen-separated (1-indexed)")
    parser.add_argument("-f", "--filter", action="append", type=str,
                        help="Filter rows: <col>-<val1>-<val2>-...; prefix val with regex: for regex. Can be used multiple times.")
    parser.add_argument("-m", "--match", type=str,
                        help="Match rows to a reference row: <row>-<col1>-<col2>-...")
    parser.add_argument("-x", "--execute", action="append",
                        help="Execute shell command on column: <col>-<command>. Can be used multiple times.")
    parser.add_argument("-q", "--quick", action="store_true",
                        help="Print header with indices and exit")
    parser.add_argument("-o", "--output", type=str,
                        help="Write filtered CSV to this file")
    args = parser.parse_args()

    data = read_csv(args.csv_file)

    # Quick
    if args.quick:
        if not data:
            print("CSV file is empty."); sys.exit(0)
        for idx, col in enumerate(data[0], 1):
            print(f"{idx}: {col}")
        sys.exit(0)

    # Sequential filters (-f)
    if args.filter:
        for raw in args.filter:
            rule = raw.strip().strip('\'"')
            parts = rule.split("-")
            if len(parts) < 2:
                print(f"Error parsing filter '{raw}'"); sys.exit(1)
            col_idx = int(parts[0]) - 1
            vals = parts[1:]
            criteria = []
            for v in vals:
                v = v.strip()
                if v.startswith("regex:"):
                    try:
                        criteria.append(("regex", re.compile(v[len("regex:"):])) )
                    except re.error as e:
                        print(f"Invalid regex '{v}': {e}"); sys.exit(1)
                else:
                    criteria.append(("literal", v))
            # apply this filter
            header, *rows = data
            new_rows = []
            for row in rows:
                cell = row[col_idx] if col_idx < len(row) else ""
                keep = False
                for kind, crit in criteria:
                    if kind=="literal" and cell==crit:
                        keep = True; break
                    if kind=="regex" and crit.search(cell):
                        keep = True; break
                if keep:
                    new_rows.append(row)
            data = [header] + new_rows

    # Match (-m)
    if args.match:
        rule = args.match.strip().strip('\'"')
        parts = rule.split("-")
        if len(parts) < 2:
            print(f"Error parsing match '{args.match}'"); sys.exit(1)
        ref_row = int(parts[0]) - 1
        cols = [int(x)-1 for x in parts[1:]]
        if ref_row<0 or ref_row>=len(data):
            print("Reference row out of range"); sys.exit(1)
        ref_vals = [ data[ref_row][c] if c<len(data[ref_row]) else "" for c in cols ]
        header, *rows = data
        matched = []
        for row in rows:
            if all( (row[c] == ref_vals[i] if c<len(row) else False)
                    for i,c in enumerate(cols) ):
                matched.append(row)
        data = [header] + matched

    # Range/columns
    if args.range:
        idxs = [int(x)-1 for x in args.range.split("-") if x]
        data = [[row[i] for i in idxs if i<len(row)] for row in data]
    elif args.columns:
        data = [row[:args.columns] for row in data]

    # Execute (-x)
    if args.execute:
        for raw in args.execute:
            rule = raw.strip().strip('\'"')
            col_str, cmd = rule.split("-",1)
            ci = int(col_str)-1
            cmd = cmd.strip().strip('\'"')
            for i in range(1, len(data)):
                if ci < len(data[i]):
                    orig = data[i][ci]
                    res = subprocess.run(cmd, input=orig, text=True,
                                         shell=True, capture_output=True,
                                         executable="/bin/bash",
                                         env=os.environ.copy())
                    if res.returncode in (0,1):
                        data[i][ci] = res.stdout.strip()

    # Output file
    if args.output:
        try:
            with open(args.output,"w",newline="") as out:
                csv.writer(out).writerows(data)
            print(f"Saved to {args.output}")
        except Exception as e:
            print(f"Error saving output: {e}"); sys.exit(1)

    # Size and print
    if args.size.lower()=="all":
        mw = None
    else:
        try: mw = int(args.size)
        except: print("Invalid size"); sys.exit(1)
    print(format_table(data, mw))


if __name__=="__main__":
    main()
