# Security, Privacy and Responsible AI

## Risk position

The current MVP processes institutional operational data and supports human decisions. It is not a public control system and does not perform autonomous electrical switching.

## Roles

- **Viewer:** read-only access to approved dashboards and reports.
- **Operator:** reviews alerts and records confirm, defer, dismiss or mute decisions.
- **Engineer:** manages facility limits, model configuration and approved operational rules.
- **Administrator:** manages users, deployment configuration and backups.
- **Auditor:** reviews logs, evidence and change history without changing operations.

## Access and authentication

The local demonstration can protect write operations with `AI4I_API_KEY`. A pilot deployment requires institutional authentication, role-based authorization, account revocation and controlled administrator access. Read and write privileges must be separated.

## Data protection

- collect only data required for energy monitoring and decision support;
- keep raw institutional data inside the approved University boundary;
- publish only aggregate or anonymous evidence;
- protect network traffic with TLS in a deployed environment;
- encrypt backups and restrict restore access;
- define retention periods for operational data and audit logs;
- never commit credentials, completed `.env` files, private datasets or private model artefacts.

## Auditability

Log:

- operator decisions and notes;
- important recommendation outputs;
- configuration and model versions;
- authentication and authorization failures;
- meter-feed interruptions and recovery;
- deployments, rollbacks and incidents.

## Responsible AI controls

- AI output is advisory and must not be presented as certain truth.
- High-impact electrical actions require human review.
- Critical loads are excluded from control recommendations.
- The interface must show uncertainty, reason for alert and current operating mode.
- Model performance and alert burden must be reviewed by facility and over time.
- Failure modes and known limitations must remain visible in the repository and submission.

## Misuse risks

Possible misuse includes unauthorized viewing of infrastructure data, falsification of operator decisions, manipulation of thresholds, use of recommendations as automatic switching commands, or publication of confidential facility records.

Controls include role separation, protected write operations, restricted private data, audit logs, code review, security scanning, human approval and disabled autonomous switching.

## Safety boundary for future hardware control

A future PLC, relay or controller interface must not be enabled until the institution approves:

- controllable-load classification;
- protection and isolation design;
- interlocks and command acknowledgement;
- manual override and emergency stop where required;
- fail-safe behavior after communication or power loss;
- commissioning tests and rollback procedures;
- named operational ownership.

## Repository checks

Run:

```powershell
python -m scripts.security_scan --output-dir evidence\validation\security
```

The scan checks for private directories, unsafe model or key files, secret patterns and missing release components. It complements, but does not replace, dependency review, network hardening or institutional security testing.
