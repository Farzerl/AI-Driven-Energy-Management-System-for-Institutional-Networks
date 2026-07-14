# Edge gateway demonstration

## Objective

Prove that the software MVP can receive validated meter readings through an edge-style data path, preserve readings during a server interruption and recover without duplicate storage.

## Procedure

1. Run `START_AI4I_EMS.bat` and confirm the dashboard is ready.
2. Run `START_EDGE_DEMO.bat` in a second window.
3. Open the **Edge gateway** dashboard tab.
4. Confirm the gateway state, received-reading count and latest values update.
5. Stop the dashboard with `Ctrl+C` while the edge demo remains running.
6. Confirm the collector reports that readings are buffered locally.
7. Restart the dashboard.
8. Confirm the buffered readings are accepted and the local buffer returns to zero.

## Evidence boundary

The input CSV contains synthetic public-safe values. In accelerated mode, each value represents another completed half-hour interval. The demonstration proves interface, validation, buffering, retry, duplicate protection, live feature construction, model inference and advisory alert generation. It does not prove a commissioned UZ meter connection or electrical actuation.
