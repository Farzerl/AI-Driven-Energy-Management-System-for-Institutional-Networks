# Final Package Validation Evidence

This folder contains machine-generated checks for the aligned repository package.

| Evidence | Result |
|---|---|
| Python test suite | 30 passed |
| API smoke test | 15 of 15 checks passed |
| Dashboard JavaScript syntax | Passed |
| Cost-model reproduction | Passed |
| Security and private-data scan | See `security/security_scan_report.md` |
| Repository alignment audit | See `repository/repository_audit_report.md` |
| Dashboard screenshots | Seven public-safe screenshots inventoried |

## Files

- `pytest_output.txt`: exact final pytest output.
- `javascript_syntax_check.txt`: Node syntax-check result.
- `api_smoke_test.json`: endpoint, write-authentication, duplicate-protection, and security-header checks.
- `cost_model_reproduction.json`: comparison between regenerated and committed cost evidence.
- `screenshot_inventory.json`: image dimensions, sizes, and hashes.
- `security/`: private-data and secret scan.
- `repository/`: repository structure and alignment audit.

These checks validate the packaged public repository. They do not constitute electrical commissioning, billing verification, a live campus installation, or a realised-savings study.
