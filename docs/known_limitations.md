# Known Limitations

## Live data and deployment

- The public build runs operational inference from accelerated simulated gateway values. It is not connected to a commissioned UZ meter.
- Incoming values are treated as completed half-hour intervals. A production gateway must aggregate faster raw polls before inference.
- The public synthetic model exists to prove the end-to-end interface. It is not the verified real-data research benchmark.
- A private live-compatible model can be trained locally and loaded automatically, but its artefact and facility mapping must remain outside the public repository.
- The deployment has no PLC, relay, breaker or automatic electrical actuation path.

## Model and operational evidence

- The verified research forecast has a one-half-hour horizon.
- December rolling validation underperformed persistence, so performance is not uniform across all months.
- Forecast-assisted control generates more alerts and false actions than the simple rule.
- The deployment model has no automated concept-drift retraining or production model registry.
- The live model requires at least four valid consecutive facility intervals before it can forecast.
- Real anomaly labels are unavailable, so supervised anomaly-detection accuracy is not claimed.

## Cost and control evidence

- Public cost results are planning estimates, not invoices or realised savings.
- No measured controllable-load response dataset is available.
- Applicable account tariff details, taxes, meter multipliers and demand-register rules require private pilot verification.
- Critical loads are excluded from all proposed control actions.

## Data limitations

- Raw UZ workbooks, real facility mapping and private model artefacts are excluded from the public repository.
- Weather coverage begins late in the study period and is excluded from the principal benchmark.
- Signed reactive-power direction requires meter/export convention confirmation.
