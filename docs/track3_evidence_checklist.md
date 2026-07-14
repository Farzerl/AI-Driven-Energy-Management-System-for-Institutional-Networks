# Track 3 Repository Readiness Checklist

This checklist covers the repository and technical evidence. Proposal and pitch items are external submission deliverables.

## Product and users

- [x] Problem stated as operational decision latency.
- [x] Primary user identified as Estates and Facilities.
- [x] First decision and operational workflow documented.
- [x] Working browser dashboard and API.
- [x] Sample alerts clearly labelled as public demonstration data.
- [x] Advisory and operator-confirmed boundary stated.

## Data and AI

- [x] Dataset source, rights, coverage, and restrictions documented.
- [x] Data-quality counts and cleaning policy documented.
- [x] Chronological validation and held-out April test documented.
- [x] Persistence baseline documented.
- [x] Simple rule controller documented.
- [x] AI-versus-rule trade-off documented.
- [x] Human oversight and critical-load exclusion documented.
- [x] Synthetic utilities separated from verified real-data evidence.
- [x] Unsupported anomaly-accuracy claim excluded.

## Technical evidence

- [x] FastAPI backend.
- [x] Responsive dashboard.
- [x] Meter-ingestion API.
- [x] Simulated edge collector.
- [x] Offline buffer and retry.
- [x] Duplicate protection.
- [x] Cost-impact API and dashboard.
- [x] Architecture and data-flow diagrams.
- [x] Safe sample data.
- [x] Pinned dependencies.
- [x] Automated tests.
- [x] Security and repository audits.
- [x] GitHub Actions workflow.
- [x] Local launch instructions.

## Business and deployment

- [x] User, payer, beneficiary, and value proposition.
- [x] Planning cost ranges and cost drivers.
- [x] Public-source cost model with claim boundary.
- [x] Pilot site and roles.
- [x] Hosting, monitoring, support, backup, connectivity, and scale.
- [x] 30-day, 60-day, and 90-day milestones.
- [x] Hardware and safety boundary.

## Repository hygiene

- [x] No raw private dataset.
- [x] No credentials.
- [x] No `.venv`.
- [x] No caches.
- [x] No runtime logs.
- [x] No obsolete executable launcher.
- [x] No duplicate release or CI folder.
- [x] No stale historical test count.
- [x] License or usage condition included.
- [x] Changelog included.
- [x] Screenshots included.
- [x] Known limitations included.

## Deferred external items

- [ ] Merge approved changes into `main`.
- [ ] Confirm judge access or public repository visibility.
- [ ] Add Raspberry Pi photograph when available.
- [ ] Test the final `main` ZIP on a clean Windows computer.
- [ ] Record final commit SHA in validation evidence.
- [ ] Align final proposal and pitch deck to the current repository.
