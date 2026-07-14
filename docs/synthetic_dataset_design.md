# Synthetic Dataset Utility

## Purpose

The synthetic generator is a safe engineering utility used to test ingestion, feature, model-training, and recommendation code without the private University workbooks.

It is not the source of the verified submission metrics.

## Design

The generator creates half-hourly institutional profiles with:

- 22 anonymous or simulated facilities;
- semester and vacation conditions;
- kitchen and hostel demand patterns;
- laboratories, ICT, library, administration, residences, and utilities;
- power-factor variation;
- meter dropouts and quality flags;
- selected synthetic anomalies.

It preserves basic electrical relationships:

```text
kWh = average kW x 0.5 hours
kVA = average kW / power factor
current = kVA x 1000 / (sqrt(3) x voltage)
```

## Use

```bash
python -m software.ai_engine.dataset_generator
python -m software.ai_engine.model_training --days 30 --output-dir runtime/synthetic_model_test
```

Generated datasets and models belong in ignored local folders such as `runtime/` or `software/data/generated/`.

## Claim boundary

Synthetic metrics may be used to test software behaviour. They must not replace or be mixed with the verified aggregate results reported from the controlled real-data validation.
