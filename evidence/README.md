# Public Submission Evidence

This folder contains evidence that can be shared with judges without exposing the private University dataset.

## Structure

```text
evidence/
├── public_dashboard/   Approved aggregate dataset and model evidence
├── cost_impact/        Public-source tariff and scenario model
└── validation/         Current tests, security scan, repository audit, and smoke checks
```

Dashboard screenshots are stored under `docs/screenshots/`.

## Evidence rules

Allowed:

- aggregate quality counts;
- anonymous facility aliases;
- normalized charts;
- aggregate forecast and controller metrics;
- public-source cost estimates;
- safe sample readings;
- test and security reports.

Not allowed:

- raw workbooks or source ZIP;
- exact private interval readings;
- real facility mappings;
- private model binaries;
- credentials or completed environment files;
- local runtime logs.

## Reproduction

```powershell
python -m pytest -q
python -m scripts.security_scan --output-dir evidence\validation\security
python -m scripts.repository_audit --output-dir evidence\validation\repository
```

The authoritative evidence is the output generated from the current repository package or commit.
