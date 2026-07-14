# Operational Edge-to-AI Inference Flow

## What is operational in this build

The public demonstration now completes the following path:

```text
Accelerated edge simulator
    -> validated half-hour meter values
    -> duplicate-protected runtime store
    -> four-interval rolling history
    -> live feature construction
    -> loaded forecasting model
    -> next-half-hour kVA forecast
    -> facility-limit utilisation and risk
    -> advisory recommendation
    -> Estates and Facilities alert queue
```

The dashboard no longer treats edge readings as display-only values. After at least four completed intervals for one facility, the API generates and stores a live forecast.

## Model selection

The API loads models in this order:

1. `AI4I_MODEL_PATH`, when explicitly configured;
2. `private_models/uz_live_forecaster.json`, when trained locally from authorised data;
3. `models/public_demo/live_forecaster.json`, the public synthetic demonstration fallback.

The dashboard exposes the active source and model mode. It does not present the public synthetic model as the verified UZ research benchmark.

## Time handling

The operational model expects completed 30-minute interval values. The edge simulator accelerates time so that each demonstration value represents another completed half-hour interval. This makes the end-to-end path visible within seconds.

A real gateway may poll a meter more frequently, but raw samples must first be aggregated into a complete half-hour interval before inference.

## Safety boundary

The output is advisory. No endpoint commands relays, breakers, contactors, PLC outputs or critical loads. An operator may confirm, defer, dismiss or mute a recommendation, and that decision is logged.
