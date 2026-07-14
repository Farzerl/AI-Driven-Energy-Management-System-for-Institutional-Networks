# Demo Walkthrough

This walkthrough is designed for a local submission demonstration without audio and without the private dataset.

## Start

```text
START_AI4I_EMS.bat
```

Wait for:

```text
API import check: PASS
Dashboard status: READY
```

## Recommended order

1. **Overview**
   - explain the problem as decision latency;
   - show dataset scale and forecast results;
   - state the advisory operating boundary.

2. **Estates and Facilities**
   - explain one sample alert;
   - choose an operator action;
   - show the audit log.

3. **Edge gateway**
   - run `START_EDGE_DEMO.bat`;
   - show meter values, sent readings, and gateway state;
   - explain offline buffering and retry.

4. **Cost impact**
   - show indicative expenditure and the central scenario;
   - state that the figures are public-source planning estimates.

5. **Data evidence**
   - show heatmap, monthly index, profiles, facility concentration, and quality.

6. **AI vs rule**
   - explain why forecasting adds value before a threshold is crossed;
   - show fewer high-to-low misses and the higher alert burden.

7. **Architecture**
   - show field, edge, data, AI, API, user, audit, and future-control layers.

8. **API**
   - open `/docs`;
   - show sample request and response schemas.

## Demonstration boundaries

Describe forecasts as live outputs from simulated gateway values, not as live campus readings. Do not state that the Raspberry Pi is commissioned, that the bill estimate is an invoice, that the scenario is realised savings, or that automatic switching is active.
