# Model Card

## Model suite

AI4I-EMS next-half-hour demand and peak-risk model suite.

## Intended use

The model supports institutional electrical operators by:

- forecasting the next half-hour facility demand;
- classifying low, medium, or high peak risk;
- supplying evidence to an operator-confirmed recommendation workflow.

The output is not a final switching command.

## Verified models and baselines

### Persistence baseline

Assumes the next interval demand equals the current interval demand.

### Demand forecast

- **Method:** HistGradientBoosting regression.
- **Target:** next-half-hour facility demand in kVA.
- **Validation:** chronological training and validation.
- **Final test:** April 2026, held out from model tuning.

### Peak-risk classification

Converts validated demand and facility-limit features into low, medium, or high next-half-hour risk.

### Simple rule comparison

Uses present facility utilisation only:

- medium warning at 85% of the training-only facility limit;
- high warning at 95%.

## Verified aggregate results

| Measure | Result |
|---|---:|
| Persistence MAE | 2.731 kVA |
| AI model MAE | 2.331 kVA |
| MAE improvement | 14.65% |
| RMSE improvement | 25.95% |
| Forecast-assisted balanced accuracy | 80.85% |
| Simple-rule balanced accuracy | 73.13% |
| Forecast-assisted high-risk warning recall | 98.73% |
| Simple-rule high-risk warning recall | 92.52% |
| Critical high-to-low misses avoided | 161 |

The AI system increases the action and false-action rates. This is an explicit operational trade-off.


## Live deployment model

The API includes a separate live-compatible deployment path. It reproduces features available from incoming completed half-hour values and loads models in this order:

1. explicitly configured model path;
2. ignored private UZ deployment model;
3. public synthetic fallback model.

The public fallback uses scheduled autoregressive ridge regression blended with persistence. Its purpose is reproducible end-to-end demonstration, not replacement of the verified HistGradientBoosting research benchmark. The private workflow is chronologically tested on an untouched April period and keeps its model and facility alias map outside the public repository.

The dashboard identifies the active model source. Live model metrics and verified research metrics are not presented as the same experiment.

## Inputs

Public documentation describes:

- timestamp and time features;
- anonymous facility identity;
- historical kVA and related lag features;
- facility-specific limit features;
- data-quality indicators;
- tariff-period or operating-context features where available.

Private interval records and model binaries are not published.

## Outputs

- next-half-hour kVA forecast;
- low, medium, or high peak risk;
- public-safe explanation and recommended operator action.

## Human oversight

Estates and Facilities personnel review each recommendation and may confirm, defer, dismiss, or mute it. Critical loads remain excluded. The current system has no autonomous control path.

## Experimental modules

The repository retains a physically consistent synthetic-data generator and model-development utility for testing code paths. Synthetic scores are not used for the reported real-data metrics.

Anomaly flagging is experimental. Verified real anomaly labels are unavailable, so supervised anomaly accuracy is not claimed.

## Limitations

- one-half-hour prediction horizon;
- December rolling validation underperformed persistence;
- more alerts than the simple rule;
- no live concept-drift monitoring in the MVP;
- no measured controllable-load response;
- no guarantee of financial savings;
- no commissioned campus meter or live control-system deployment.
