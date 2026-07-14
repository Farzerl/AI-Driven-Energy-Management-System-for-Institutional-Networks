# AI Justification and Validation Note

## Why rules alone are insufficient

A fixed threshold controller reacts to the present interval. It can flag a facility after demand is already high, but it cannot reliably anticipate the next half-hour condition when several institutional loads change together because of timetables, kitchens, hostels, laboratories, weather, or operational schedules.

The AI component is used only where prediction adds value: next-half-hour demand forecasting and peak-risk classification. Engineering rules remain responsible for safety boundaries, critical-load exclusions, allowable actions, and human approval.

## Validated method

- Target: next half-hour facility demand in kVA.
- Model: HistGradientBoosting using facility-normalized demand-change features.
- Validation: chronological training and testing, not random splitting.
- Final test: April 2026 held out from model tuning.
- Baseline: persistence, meaning the next interval is assumed equal to the current interval.
- Additional comparison: a simple current-utilisation threshold controller.

## Forecast result

| Measure | Persistence | AI model | Improvement |
|---|---:|---:|---:|
| MAE | 2.731 kVA | 2.331 kVA | 14.65% lower |
| RMSE | 7.760 kVA | 5.746 kVA | 25.95% lower |
| WAPE | 7.996% | 6.824% | 14.65% lower |

The model won four of five rolling monthly validation folds by MAE. It lost in December, which is disclosed as a regime-sensitivity limitation.

## Forecast-assisted control versus a simple rule

| Measure | Simple rule | Forecast-assisted |
|---|---:|---:|
| Balanced accuracy | 73.13% | 80.85% |
| High-risk events warned medium or high | 92.52% | 98.73% |
| High-risk events missed as low | 194 | 33 |
| False-action rate on actual low intervals | 3.57% | 10.71% |

Forecast assistance avoided 161 critical high-to-low misses, but it generated more advisory actions. The result supports advisory or operator-confirmed use, not autonomous switching.

## Human oversight

The AI output is a recommendation, not a final electrical control command. Estates and Facilities personnel review the alert and may confirm, defer, dismiss, or mute it. Critical loads remain excluded. Future supervised control requires engineering approval, interlocks, manual override, and fail-safe testing.

## Claims not made

- No realised electricity-bill savings are claimed. The separate cost model is explicitly a public-source planning estimate.
- No avoided kVA is claimed without controllable-load response data.
- No supervised anomaly-detection accuracy is claimed because verified anomaly labels are unavailable.
- No autonomous switching capability is claimed in the current MVP.
