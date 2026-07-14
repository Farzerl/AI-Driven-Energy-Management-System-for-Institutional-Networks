# Submission Claim Register

This register defines the wording that may be used consistently across the repository, proposal, pitch, and demonstration.

| Claim | Status | Permitted wording | Evidence or limitation |
|---|---|---|---|
| Dataset covers 22 facilities | Verified | The study dataset covers 22 facilities. | `dataset_statement.md`; aggregate evidence |
| Study period is September 2025 to April 2026 | Verified | Eight months of half-hourly institutional electricity data were analysed. | Dataset statement and evidence JSON |
| Completed interval grid is 255,552 rows | Verified | Chronological completion produced 255,552 facility intervals. | Public dashboard evidence |
| Forecast-usable rows are 255,292, or 99.898% | Verified | Conservative cleaning retained 255,292 forecast-usable rows. | Public dashboard evidence |
| AI MAE is 2.331 kVA versus 2.731 kVA persistence | Verified on held-out April test | The model reduced MAE by 14.65% on the untouched April 2026 test. | Model card and AI justification |
| AI reduces critical high-to-low misses by 161 versus the simple rule | Verified on April test | Forecast assistance avoided 161 critical misses in the test comparison. | Controller comparison evidence |
| AI is always better than the rule | Prohibited | Do not make this claim. | AI increases alert and false-action burden; human confirmation is retained. |
| Edge ingestion, buffering, retry, and duplicate protection work | Demonstrated with simulator | The software edge path is demonstrated using safe sample readings. | Edge tests, API, dashboard, and demo script |
| Raspberry Pi is installed at UZ | Not claimed | A Raspberry Pi is the proposed pilot gateway; a photograph and on-device demonstration are deferred. | `DEFERRED_ITEMS.md` |
| UZ paid USD 603,537 | Prohibited | Do not state an exact UZ bill. | The confidential bill and tariff are not disclosed. |
| Indicative study-period expenditure is about USD 604,000 | Public-source planning estimate | Applying the public average tariff to aggregate study energy gives an indicative eight-month estimate of about USD 604,000. | Cost methodology and public cost model |
| Potential central-scenario value is about USD 14,000 | Planning estimate | A central planning scenario indicates about USD 14,000, subject to tariff, meter, and controllable-load verification. | Cost-impact evidence |
| The product has realised financial savings | Not claimed | No realised financial saving is claimed before a measured pilot. | Measurement and verification plan |
| Autonomous load shedding is deployed | Prohibited | The MVP is advisory and operator-confirmed only. | Architecture and safety boundary |
| Future supervised control is part of the project pathway | Proposed | Future control is limited to approved non-critical loads after protection review, interlocks, manual override, testing, and institutional approval. | Hardware safety documentation |
| Simulated edge forecasts are live campus meter readings | Prohibited | The API performs live inference on accelerated simulated values; no commissioned campus feed is claimed. | Live inference API and dashboard boundary |
| Raw UZ data is included in the repository | Prohibited | Only safe samples, aggregates, anonymous aliases, and derived evidence are published. | Dataset statement and security policy |

## Rule

Where a result is labelled **verified**, it is verified only for the documented dataset split and method. Where a value is labelled **planning estimate**, it must not be presented as an invoice value, realised saving, or guaranteed outcome.

| Edge values trigger model inference | Demonstrated | Four completed simulated intervals produce a next-half-hour forecast, risk and advisory recommendation. | Live inference tests and API |
| Private UZ live model is published | Prohibited | The public repository contains only a synthetic fallback; the private model remains in the controlled environment. | Model handoff plan |
