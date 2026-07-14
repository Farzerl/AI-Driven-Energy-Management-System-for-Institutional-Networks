# Edge gateway demonstration

This module proves the data path between an institutional meter interface and the AI4I-EMS API without claiming a commissioned campus installation.

## Demonstrated functions

- reads safe sample interval data from CSV;
- validates timestamp, facility ID, kVA, kWh and power factor;
- posts readings to `POST /api/meter-readings`;
- buffers new readings locally when the API is unavailable;
- retries buffered readings when connectivity returns;
- writes gateway health to `runtime/edge_status.json`;
- prevents duplicate storage using a deterministic reading identifier.

## Run

Start the dashboard first:

```powershell
.\START_AI4I_EMS.bat
```

Then start the edge demo in another terminal:

```powershell
.\START_EDGE_DEMO.bat
```

For a one-batch test:

```powershell
.\.venv\Scripts\python.exe -m src.edge.collector --config config\edge.example.json --once
```

The demo uses public-safe synthetic values. It does not connect to mains wiring or switch loads.
