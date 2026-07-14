# Reproduction Guide

## Public demonstration

```text
START_AI4I_EMS.bat
```

The public dashboard does not need the private UZ dataset.

Manual start:

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dashboard.lock.txt
python -m uvicorn src.api.server:app --host 127.0.0.1 --port 8000
```

## Edge demonstration

Start the dashboard, then:

```text
START_EDGE_DEMO.bat
```

One pass:

```powershell
.\.venv\Scripts\python.exe -m src.edge.collector --config config\edge.example.json --once
```

## Cost-model reproduction

```text
RUN_STAGE4_COST_MODEL.bat
```

or:

```powershell
.\.venv\Scripts\python.exe scripts\build_public_cost_estimate.py
```

## Tests and audits

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.lock.txt
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.lock.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m scripts.security_scan --output-dir evidence\validation\security
.\.venv\Scripts\python.exe -m scripts.repository_audit --output-dir evidence\validation\repository
```

## Private real-data process

The private data audit and model-training workflow is intentionally not shipped as a public command because it depends on confidential workbooks, mappings, and approved local procedures.

An authorised team member on a University-controlled computer should:

1. confirm the source handover record and permissions;
2. place data in an ignored private directory;
3. run the departmentally controlled cleaning and chronological validation workflow;
4. retain interval-level data and private model artefacts locally;
5. record source hash, code commit, Python version, and dependency versions;
6. publish only reviewed aggregates;
7. verify that no private path or file is staged for Git.

## Evidence integrity

- use chronological validation;
- keep April 2026 untouched for final testing;
- do not tune facility limits on the test period;
- do not publish interval predictions;
- separate synthetic tests from verified aggregates;
- label public tariff estimates;
- record the exact commit for final submission evidence.

## Hardware status

The public repository reproduces the software edge collector and buffer. Physical reproduction requires the actual Raspberry Pi or approved gateway, power supply, storage, communications adapter, and meter-interface approval. Mains-connected work is outside the public software reproduction path.
