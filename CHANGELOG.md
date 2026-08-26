# Changelog

All notable changes to Datapilot will be documented in this file.

The format is inspired by **Keep a Changelog**, and the project follows Semantic Versioning (`MAJOR.MINOR.PATCH`).

---

## [Unreleased]

### Added

- Duplicate row analysis
- Duplicate summary data model
- Duplicate reporting through the `Report` interface

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

## [0.4.0]

### Added

- Dataset Health 2.0 assessment with completeness, duplicates, structure, and consistency dimensions.
- ML Readiness assessment with preparation-level scoring and dimension-level signals.
- ML assessment coverage for dimensions that cannot be assessed from available information.
- Statistical Profile reporting with contextual skewness, kurtosis, and outlier interpretations.
- Data Integrity signals for observable dataset-quality concerns.
- Notebook Readiness assessment.
- Assessment Boundaries reporting distinguishing observed, calculated, interpreted, and not-assessed information.
- HTML report sections for ML Readiness, Statistical Profile, and Assessment Boundaries.
- Real-world validation using the Online Retail II dataset.
- Expanded v0.4 test coverage.

### Changed

- ML preparation scores exclude Not Assessed dimensions from the numerical score.
- HTML report version metadata is now `0.4.0`.

---

## [0.1.0-alpha]

### Added

- Initial release of the Datapilot foundation.