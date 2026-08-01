# Changelog

All notable changes to Datapilot will be documented in this file.

The format is inspired by **Keep a Changelog**, and the project follows Semantic Versioning (`MAJOR.MINOR.PATCH`).

---

## [Unreleased]

### Added

- Missing value analysis
- Missing value summary data model
- Missing value reporting through the `Report` interface


### Added

- Project structure and package architecture
- Public API using `analyze()`
- Dataset loader supporting:
  - Pandas DataFrame
  - CSV files
  - Excel files
- `Report` class as the primary interface
- Dataset summary analysis
- `DatasetSummary` data model
- Initial project documentation:
  - README
  - API
  - Architecture
  - Specification
  - Roadmap
  - Contribution Guide
  - Code of Conduct

### Changed

- Refactored package structure for improved modularity
- Moved `Report` implementation into `core`

### Fixed

- Corrected package import structure
- Converted memory usage output to native Python `float`

---

## [0.1.0-alpha]

### Added

- Initial release of the Datapilot foundation.