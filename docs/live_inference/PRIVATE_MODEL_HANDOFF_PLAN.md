# Private Model Handoff and Repackaging Plan

## Folder supplied with this delivery

The outer delivery ZIP contains a sibling folder:

```text
AI4I_PRIVATE_MODEL_WORKSPACE/
├── input/
│   └── PUT_DATASET_ZIP_HERE.txt
├── output/
│   └── README_PRIVATE_OUTPUT.txt
└── TRAIN_AND_INSTALL_PRIVATE_MODEL.bat
```

This folder must remain outside the public GitHub repository.

## Route A: supply the private dataset ZIP

1. Place exactly one authorised dataset ZIP in `AI4I_PRIVATE_MODEL_WORKSPACE/input/`.
2. Run `AI4I_PRIVATE_MODEL_WORKSPACE/TRAIN_AND_INSTALL_PRIVATE_MODEL.bat`.
3. The script parses XLSX or CSV meter exports, assigns private aliases, engineers live-compatible features, trains the model and performs chronological testing.
4. It installs the model as:

```text
AI4I_EMS_Operational_Live_Repository/private_models/uz_live_forecaster.json
```

5. Restart the dashboard. `/api/model-status` must report `source: private_model`.

## Route B: give the trained and tested model folder back for final packaging

Provide a folder containing:

```text
PRIVATE_MODEL_HANDOFF/
├── uz_live_forecaster.json
├── live_model_validation.json
├── feature_contract.json
└── training_notes.txt
```

The model bundle must contain:

- `model`;
- `metadata`;
- `facility_limits_kva`;
- a 30-minute prediction horizon;
- the exact live feature list;
- chronological test dates and metrics;
- no raw rows or real facility names.

For the final public package, the private model will not be committed. The package will retain the public fallback and document how the private deployment loads inside the controlled UZ environment. A separate local deployment overlay may contain the private model.

## Required checks before final repackaging

- feature parity between training and live inference;
- untouched chronological test;
- persistence baseline comparison;
- model and dataset fingerprints;
- no real facility mapping in public outputs;
- live inference with simulated edge values;
- restart recovery and forecast-store deduplication;
- security and repository audits;
- updated screenshots and claim register.
