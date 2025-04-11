# Changelog

All notable changes to this project will be documented in this file.

## [0.0.8] - 2025-04-12
### Added
- **Match Option (-m):**  
  Added a new option to match rows that have the same values as a specified reference row at given columns. For example, `-m10-1-3-4-7` uses row 10 as the reference and selects rows with matching values in columns 1, 3, 4, and 7.
- **Editorial Updates:**  
  Updated documentation and usage instructions to include the new match functionality.

## [0.0.6] - 2025-04-08
### Added
- **Regex Filtering for -f Option:**  
  Users can now specify regular expressions as filters by prefixing a filter value with `regex:`. For example, `-f 2-regex:^A.*$` will filter rows where column 2 matches the regular expression `^A.*$`.

### Changed
- **Execution Command (-x) Handling:**  
  Improved the parsing and execution of shell commands (e.g., awk, grep, sed) so that commands are processed correctly without extraneous quotes.
- **Editorial Updates:**  
  Updated documentation and usage instructions for clarity.

## [0.0.5] - 2025-04-01
### Fixed
- Resolved issues with the `-x` option for executing commands like `awk`.
- Made minor editorial changes in the README.

## [0.0.4] - 2025-03-20
### Added
- Added new parameter options for filtering and output formatting.
- Improved error handling and logging.

## [0.0.3] - 2025-03-10
### Fixed
- Resolved issues with column selection.
- Improved formatting of the output table.

## [0.0.2] - 2025-03-01
### Added
- Initial release with basic CSV formatting.
