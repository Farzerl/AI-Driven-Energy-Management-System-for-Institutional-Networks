# Changelog

## 1.3.0 - Operational live inference

- connected accepted edge readings to rolling live feature construction;
- added public demo model loading and private model precedence;
- added next-half-hour forecast storage, risk scoring and recommendations;
- changed the Estates alert endpoint to use live forecast alerts when available;
- added the Live forecast dashboard tab and model-status evidence;
- added accelerated half-hour gateway demonstration;
- added private dataset ZIP training and chronological testing workflow;
- added out-of-distribution persistence guard and adaptive demo limit;
- added end-to-end tests, private workflow validation and handoff documentation.


## Submission-aligned package - 14 July 2026

### Added

- working FastAPI dashboard and operator workflow;
- edge-gateway collector, offline buffer, retry, duplicate protection, and status;
- meter-ingestion and cost-impact API endpoints;
- public-source tariff and cost scenario evidence;
- guideline alignment, API reference, persona, accessibility, team ownership, and demo guides;
- dashboard screenshots;
- repository audit and hygiene tests;
- final package manifest and validation evidence.

### Corrected

- replaced stale cost-status wording with the public planning-estimate boundary;
- aligned API documentation with edge and cost endpoints;
- removed contradictory synthetic-model positioning;
- removed the obsolete requirement for a formal validation report;
- corrected cost chart compatibility and browser cache handling;
- clarified that API-key protection is a demonstration control;
- removed a reproduction command for a script that was not included;
- aligned hardware claims to a simulated edge gateway and future Raspberry Pi evidence.

### Removed

- local `.venv`;
- Python and pytest caches;
- runtime meter and operator logs;
- duplicate `release/` launcher;
- duplicate `ci/` workflow;
- duplicate `env.example`;
- stale command-line screenshots;
- empty proposal placeholder;
- unused hardware placeholder folders;
- internal workbook preview images;
- synthetic result artefacts that could be confused with verified real-data evidence.

### Verified evidence retained

- 22 facilities;
- 255,552 completed intervals;
- 2.331 kVA AI MAE;
- 14.65% MAE reduction versus persistence;
- 161 critical misses avoided versus the simple rule;
- public planning estimate of USD 603,536.75;
- central scenario estimate of USD 14,170.36.

## Earlier development stages

- baseline ingestion, tariff, recommendation, and model modules;
- facility-specific peak limits;
- public-safe aggregate dashboard evidence;
- architecture and deployment documentation;
- Windows launcher and dependency locks;
- GitHub Actions quality and security workflow.
