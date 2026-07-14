# API Reference

Base URL during local operation:

```text
http://127.0.0.1:8000
```

Interactive OpenAPI documentation:

```text
http://127.0.0.1:8000/docs
```

## Authentication

Read endpoints are open in the local demonstration.

When `AI4I_API_KEY` is configured, write endpoints require:

```http
X-API-Key: <configured value>
```

Production deployment requires institutional authentication and role-based access. The API key is a demonstration control, not the final identity model.

## Endpoints

### Health

```http
GET /api/health
```

Example response:

```json
{
  "status": "online",
  "evidence_ready": true,
  "operating_mode": "advisory",
  "api_key_required": false
}
```

### Summary

```http
GET /api/summary
```

Returns compact dataset, forecast, peak-risk, controller, cost-status, and operating-mode indicators.

### Full public evidence

```http
GET /api/evidence
```

Returns approved aggregate data-quality, forecast, controller, and visualisation evidence.

### Controller comparison

```http
GET /api/control-comparison
```

Returns simple-rule and forecast-assisted aggregate metrics.

### Cost impact

```http
GET /api/cost-impact
```

Returns public-source planning summary, monthly estimates, and scenarios.

### Sample alerts

```http
GET /api/alerts
```

Returns live forecast alerts after sufficient edge history is available. Before that, it returns clearly labelled public fallback alerts. Neither mode represents a commissioned campus meter connection.

### Operator decisions

```http
GET /api/operator-decisions?limit=30
POST /api/operator-decisions
```

Example request:

```json
{
  "alert_id": "alert-demo-001",
  "decision": "defer",
  "operator": "demo-operator",
  "note": "Meal preparation schedule checked",
  "requested_reduction_kva": 25.0
}
```

Valid decisions:

```text
confirm
defer
dismiss
mute
```

### Meter readings

```http
GET /api/meter-readings?limit=50
POST /api/meter-readings
```

Single-reading request:

```json
{
  "timestamp": "2026-07-14T09:30:00+02:00",
  "facility_id": "F17",
  "kva": 482.6,
  "kwh": 228.7,
  "power_factor": 0.90,
  "source": "edge-demo"
}
```

Batch request:

```json
{
  "readings": [
    {
      "timestamp": "2026-07-14T09:30:00+02:00",
      "facility_id": "F17",
      "kva": 482.6,
      "kwh": 228.7,
      "power_factor": 0.90,
      "source": "edge-demo"
    }
  ]
}
```

The store uses deterministic identifiers to reject duplicate readings.

### Edge status

```http
GET /api/edge-status
```

Returns gateway state, meter-store summary, last activity, and the monitoring-only boundary.

## Validation and errors

FastAPI and Pydantic validate required fields, types, limits, timestamps, decisions, and meter values.

Typical responses:

- `200`: request completed;
- `401`: missing or incorrect API key;
- `422`: schema or validation error;
- `500`: unhandled server or storage failure.

## Data export

All read endpoints return JSON. Public CSV evidence is also available under `evidence/`. The current dashboard does not provide a one-click export button.

## Live inference endpoints

### `GET /api/model-status`

Returns active model source, mode, training metadata, test metrics and readiness.

### `GET /api/live-forecasts`

Returns forecasts generated from received edge values, including current kVA, next-half-hour forecast, facility limit, utilisation, risk and recommendation.

### `GET /api/live-alerts`

Returns medium- and high-risk advisory alerts derived from the latest live forecast per facility.

### `POST /api/live-inference/rebuild`

Rebuilds missing forecasts from the append-only meter store. This write endpoint uses the configured API key when protection is enabled.

### `POST /api/meter-readings`

Validates and stores one reading or a batch, then refreshes live inference.
