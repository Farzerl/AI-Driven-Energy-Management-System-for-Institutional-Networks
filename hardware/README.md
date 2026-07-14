# Hardware and edge-integration scope

This folder documents the proposed field layer of AI4I-EMS. The current repository includes a software edge-gateway simulator and planning documents. It does not claim that a Raspberry Pi, meter interface or automatic load controller has already been commissioned at UZ.

## Current evidence

- `src/edge/collector.py`: sample meter collector and retry logic;
- `src/edge/buffer.py`: durable local JSONL buffer;
- `config/edge.example.json`: public-safe gateway configuration;
- `START_EDGE_DEMO.bat`: Windows edge demonstration launcher;
- dashboard Edge gateway tab: server receipt and gateway status;
- automated edge, buffering and API tests.

## Planning documents

- `edge_gateway_plan.md`
- `proposed_bom.md`
- `meter_interface_options.md`
- `safety_and_control_boundary.md`

A photograph of the intended Raspberry Pi demonstration unit will be added later as supporting evidence and clearly labelled as a proposed pilot gateway, not a commissioned campus installation.
