# API Review

## Public API

| Method | Decision | Notes |
|----------|----------|-------|
| analyze() | Keep | Excellent entry point |
| summary() | Keep | Clear and intuitive |
| missing_values() | Keep | Explicit and beginner friendly |
| duplicates() | Keep | Natural name |
| data_types() | Keep | Clear |
| dataset_health() | Keep | Consider adding health() alias in v0.4 |
| statistics() | Keep | Familiar terminology |
| outliers() | Keep | Natural |
| correlation() | Keep | Familiar |
| insights() | Keep | Strong API design |

## Future Additions

The following methods are intentionally postponed until future releases.

- report.show()
- report.save()
- report.to_html()
- report.to_pdf()
- report.export()