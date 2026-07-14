# Integrated Hardware-Software Architecture

## System boundary

AI4I-EMS combines institutional metering, edge data acquisition, software analytics, operator decision support, and a future supervised control interface.

```text
Existing smart meters and optional additional submeters
        ↓
Edge gateway
- protocol adapter or file/API import
- timestamp and schema validation
- local buffering during connectivity loss
        ↓
Institutional data store
- cleaned operational data
- quality flags
- model and configuration versions
        ↓
Analytics and AI layer
- feature generation
- next-half-hour demand forecast
- facility-specific peak-risk classification
- engineering and tariff rules
        ↓
Recommendation service and FastAPI
        ↓
Estates and Facilities dashboard
- demand and risk evidence
- recommended action
- confirm, defer, dismiss, or mute
        ↓
Operator decision and audit log
        ↓
Future supervised PLC or relay interface for approved non-critical loads
```

## Current implementation

The repository implements ingestion, duplicate protection, durable buffering, rolling live features, loaded-model inference, next-half-hour forecast storage, peak-risk scoring, advisory recommendations, public-safe historical evidence, FastAPI, dashboard and decision logging. The public demonstration runs this path from accelerated simulated gateway values. It is not a commissioned campus feed.

## Planned hardware layer

The pilot hardware layer may use existing meters, current transformers and additional submeters where visibility is insufficient. An edge gateway will acquire data through an approved protocol or export mechanism, validate records, and buffer data locally when the institutional network is unavailable.

Hardware selection remains site-dependent. The final bill of materials must follow a meter-interface survey and identify voltage category, communications protocol, isolation, enclosure, auxiliary supply, calibration, and protection requirements.

## Future control boundary

No autonomous switching is implemented or claimed. A future control interface may operate only approved non-critical loads and must include documented load classification, electrical protection review, interlocks, command acknowledgement, manual override, fail-safe return state, operator authorization, and commissioning and rollback procedures.

## Security and monitoring

- role-based access separates viewers, operators, engineers and administrators;
- write actions can be protected by an API key in the demonstration and stronger institutional authentication in deployment;
- credentials remain in environment configuration, not source control;
- API actions, operator decisions, data gaps and model versions are logged;
- network deployment requires TLS through an institutional reverse proxy;
- raw institutional data remain inside the approved private boundary.

Rendered diagrams are available in `docs/diagrams/`.
