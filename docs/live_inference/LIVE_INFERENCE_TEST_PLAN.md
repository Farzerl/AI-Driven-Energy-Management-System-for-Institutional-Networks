# Live Inference Test Plan

## Automated checks

- public model loads without private files;
- fewer than four intervals do not produce a forecast;
- the fourth interval produces a next-half-hour forecast;
- repeated meter values are rejected as duplicates;
- forecast records are not duplicated after a rebuild;
- private model path takes precedence when present;
- live forecasts appear through the API;
- the Estates alert endpoint uses live forecast alerts when risk is medium or high;
- the fallback alert mode remains available before edge data arrives;
- all outputs remain advisory.

## Manual demonstration

1. Run `START_AI4I_EMS.bat`.
2. Run `START_EDGE_DEMO.bat` in another window.
3. Wait for the first four accelerated interval readings.
4. Open **Live forecast** and confirm current, forecast and limit values.
5. Open **Estates and Facilities** and refresh the queue.
6. Confirm the alert source is based on live edge forecasts when a medium or high risk is present.
7. Stop the edge gateway and confirm the last forecast remains visible.
8. Restart the gateway and confirm new timestamps continue without duplicate records.
