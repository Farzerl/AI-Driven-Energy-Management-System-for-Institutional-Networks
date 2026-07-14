# AI4I Product-Readiness Alignment

This note maps the repository to the AI4I Track 3 Development Terms of Reference and the Supporting Guidance on Product Readiness.

The repository is assessed as a **working MVP with a credible pilot pathway**, not as a commissioned production system.

## 1. Minimum submission package

| Guidance requirement | Repository evidence | Status |
|---|---|---|
| Clear problem and users | `README.md`, `docs/user_persona_and_journey.md` | Ready |
| Product description or working prototype | FastAPI application, dashboard, launchers | Ready |
| Technical architecture | `docs/architecture.md`, SVG diagrams | Ready |
| Dataset statement | `docs/dataset_statement.md` | Ready |
| User interaction plan | `docs/operator_workflow.md`, dashboard | Ready |
| Risk note | `docs/risk_register.md`, `docs/security_and_compliance.md` | Ready |
| Business or sustainability note | `docs/business_model.md` | Ready |
| Deployment pathway | `docs/deployment_plan.md`, `docs/pilot_deployment_plan.md` | Ready |
| Testing evidence | `tests/`, validation reports, GitHub Actions | Ready |
| Demo instructions | `FINAL_DEMO_INSTRUCTIONS.txt`, screenshots | Ready |
| Written proposal | Maintained separately for the submission package | External deliverable |
| Pitch deck | Planned in the next submission stage | External deliverable |

## 2. Repository quality

| Checklist item | Evidence |
|---|---|
| Judge can understand project without team present | Root README, evidence index, demo instructions |
| Clear setup | Batch launcher and team setup guide |
| No secrets or raw private data | `.gitignore`, security scan, dataset boundary |
| Known bugs and limitations | `docs/known_limitations.md` |
| Screenshots | `docs/screenshots/` |
| Architecture diagram | `docs/diagrams/` |
| Safe sample data | `sample_data/` |
| Version and dependency information | lockfiles and `pyproject.toml` |
| License or usage condition | `LICENSE` |
| Evidence of evolution | `CHANGELOG.md` and repository history |

## 3. Backend and integration

| Required component | Implementation |
|---|---|
| Frontend | Responsive HTML, CSS, and JavaScript dashboard |
| Backend | FastAPI |
| Data store | Public JSON evidence plus local append-only JSONL stores |
| AI layer | Verified benchmark plus operational live feature construction, model loading, next-half-hour inference, risk and recommendations |
| Integration layer | Meter-reading API, simulated edge collector, rolling history, forecast store and live alert generation |
| Authentication | Optional API key for write endpoints; institutional roles planned |
| Monitoring | Health endpoint, edge status, logs, audit files |
| Security | Input validation, environment secrets, security headers, private-data scan |
| Outputs | Alerts, decisions, charts, API responses, cost scenarios |

## 4. Data and AI

| Requirement | Evidence |
|---|---|
| Data source and rights | Departmentally supplied institutional data; no redistribution |
| Data quality | Missing, partial, negative, and weather limitations recorded |
| AI role | Next-half-hour forecasting and peak-risk classification |
| Simpler baseline | Persistence and current-demand threshold rule |
| Validation | Chronological folds and untouched April test |
| Trade-offs | Fewer critical misses, more advisory alerts |
| Human oversight | Operator confirmation and critical-load exclusion |
| Bias and limitation note | Facility-level limitations and alert burden documented |

## 5. User experience

| Guidance evidence | Repository position |
|---|---|
| User persona | Documented |
| User journey | Documented |
| Core screens | Working dashboard and screenshots |
| Information architecture | Overview, Operations, Edge, Live Forecast, Cost, Data, AI, Architecture |
| Data visualisation logic | Explained in `docs/user_persona_and_journey.md` |
| Accessibility | `docs/accessibility_check.md` |
| User feedback | Formal long-duration user testing is not claimed; local walkthrough is provided |

The guidance says user feedback should be included where possible. The submission does not invent a validation report. A structured walkthrough and future pilot feedback are recorded honestly.

## 6. Security and responsible AI

- only necessary operational fields are used;
- raw private data and identifiers are excluded;
- write actions can require an API key;
- credentials remain in environment variables;
- important operator actions are logged;
- high-impact recommendations require human review;
- critical loads are excluded;
- no autonomous switching is enabled;
- cost figures and model limitations are clearly labelled;
- the security and repository audits block unsafe files.

## 7. Testing evidence

The repository contains:

- API endpoint tests;
- data-ingestion tests;
- recommendation and tariff tests;
- forecast/synthetic data tests;
- edge buffer and recovery tests;
- duplicate meter-reading tests;
- cost model and cost API tests;
- release-layout and repository-hygiene tests;
- JavaScript syntax validation in CI;
- security and private-data scanning.

The authoritative count is generated from the current package by `python -m pytest -q`. Historical counts are not used as evidence.

## 8. Business and sustainability

The business model identifies:

- user: Estates and Facilities;
- payer: institution or funded pilot partner;
- beneficiaries: campus users and management;
- first pilot: Central Kitchens and one hostel;
- delivery: institutional licence, integration, onboarding, and support;
- cost drivers: meters, edge equipment, installation, hosting, training, and maintenance;
- indicative public-source energy cost and scenario value;
- adoption risks and pilot success measures.

## 9. Deployment

The repository documents:

- hybrid institutional and edge deployment;
- University-controlled hosting;
- low-connectivity buffering and retry;
- operator onboarding and support;
- monitoring and audit;
- backup and recovery;
- 30-day, 60-day, and 90-day milestones;
- safe monitoring-only pilot boundary.

## 10. Claims register

| Claim | Classification |
|---|---|
| 22 facilities and 255,552 completed intervals | Verified aggregate |
| AI MAE 2.331 kVA | Verified aggregate |
| 14.65% MAE reduction | Verified aggregate |
| 161 critical misses avoided versus simple rule | Verified aggregate |
| Edge ingestion, offline buffering and live inference | Demonstrated with accelerated simulator |
| Raspberry Pi commissioned at UZ | Not claimed |
| USD 603,536.75 UZ bill | Not claimed; public planning estimate |
| USD 14,170.36 realised saving | Not claimed; central scenario estimate |
| Automatic electrical switching | Not implemented or claimed |
| Live campus deployment | Not claimed |

## Remaining external close-out work

The following items are outside this aligned repository package:

- merge the approved branch into `main`;
- confirm judge access or make the sanitized repository public;
- align the final proposal and pitch deck to the current evidence;
- add a photograph of the proposed Raspberry Pi gateway when available;
- run the final ZIP on a clean Windows computer and record the commit SHA.
