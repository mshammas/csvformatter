# Changelog

All notable changes to this project will be documented in this file.

## [0.0.9] - 2025-04-26
### Added
- **Multi-filter Support (`-f`)**  
  Users can now click the **+** button and specify multiple `-f` rules; they apply sequentially.
- **Dynamic UI**  
  Added a “+” button in the webview to add additional filter inputs.
- **Documentation**  
  UPDATED examples and usage in README.

## [0.0.8] - 2025-04-12
### Added
- **Match Option (`-m`)**  
  New feature to select rows that match a reference row’s values in specified columns.
- **Editorial Updates**

## [0.0.6] - 2025-04-08
### Added
- **Regex Filtering (`-f`)**  
  Support for `regex:` prefix in filter values for regular-expression matching.
### Changed
- **Execution Handling (`-x`)**  
  Improved shell-command parsing and quoting.

## [0.0.5] - 2025-04-01
### Fixed
- Resolved issues with the `-x` option (e.g., correct handling of `awk`).
- Minor editorial fixes in README.

## [0.0.4] - 2025-03-20
### Added
- New filtering and output formatting options.
- Enhanced error handling and logging.

## [0.0.3] - 2025-03-10
### Fixed
- Column-selection bugs.
- Table-formatting improvements.

## [0.0.2] - 2025-03-01
### Added
- Initial release with basic CSV formatting and webview parameter form.
