# Model-Development Utilities

The primary submission evidence is the approved real-data aggregate benchmark stored under `evidence/public_dashboard/`.

This folder contains supporting development utilities for:

- generating safe, physically consistent institutional sample data;
- exercising baseline and machine-learning training code;
- testing regression, classification, and recommendation paths;
- reproducing development behaviour without the private workbooks.

## Commands

```bash
python -m software.ai_engine.dataset_generator
python -m software.ai_engine.model_training --days 30 --output-dir runtime/synthetic_model_test
```

Use `runtime/` or another ignored local path for generated outputs.

## Evidence rule

Do not present synthetic scores as real UZ model performance. The verified submission claims are documented in:

- `README.md`;
- `docs/model_card.md`;
- `docs/ai_justification.md`;
- `evidence/public_dashboard/dashboard_evidence.json`.

The private source data and private trained models remain outside the repository.
