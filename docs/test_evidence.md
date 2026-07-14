# Validation Evidence

The final package includes machine-generated results under `evidence/validation/`.

## Commands

```powershell
python -m pytest -q
python -m scripts.security_scan --output-dir evidence\validation\security
python -m scripts.repository_audit --output-dir evidence\validation\repository
```

## Interpretation

- **Tests:** code and API behaviour.
- **Security scan:** secrets, private paths, unsafe artefacts, and required release files.
- **Repository audit:** structure, stale content, private data, duplicate folders, documentation links, and manifest hygiene.
- **JavaScript syntax:** checked with Node in CI and during package preparation.
- **Dashboard smoke test:** API endpoints and browser tabs loaded from the local server.
- **Screenshots:** captured from the public-safe local build.

Historical test counts are not used. Review the reports generated from the current package or Git commit.
