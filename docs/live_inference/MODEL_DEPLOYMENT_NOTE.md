# Research Benchmark and Deployment Model

Two model contexts must remain distinct.

## Verified research benchmark

The public evidence package reports the strongest verified chronological benchmark from the private UZ analysis, including an AI MAE of 2.331 kVA against a persistence MAE of 2.731 kVA. This evidence supports the technical case for forecast-assisted control.

## Live-compatible deployment model

The operational API needs a compact model whose features can be reproduced from incoming meter values. This package includes a public synthetic fallback model so judges can test the complete edge-to-AI path without receiving private data or model artefacts.

The private training workflow builds a live-compatible model from:

- facility alias;
- timestamp and tariff-period features;
- current kVA, interval kWh and power factor;
- one- and two-interval lag values;
- four-interval rolling mean and maximum;
- facility and half-hour schedule effects.

The private workflow uses a chronological April 2026 holdout and writes its model to the ignored `private_models` directory. The public repository contains only a privacy-safe aggregate pipeline-validation record.

The live deployment model should not replace the verified research benchmark in the proposal. It proves operational inference compatibility. A later integration can package the approved strongest trained model after its feature contract and model artefact are supplied.
