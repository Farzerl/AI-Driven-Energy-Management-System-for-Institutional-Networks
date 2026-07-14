# Estates and Facilities Operator Workflow

## Primary user

The primary operational user is the University of Zimbabwe Estates and Facilities team responsible for campus electrical operations.

## Decision flow

```text
Meter or approved data input
        ↓
Quality validation and current demand context
        ↓
Next-half-hour demand forecast and peak-risk level
        ↓
Engineering-rule screening and critical-load exclusion
        ↓
Recommended operational action
        ↓
Estates and Facilities review
        ↓
Confirm, defer, dismiss, or mute
        ↓
Operator note and audit log
```

## Alert contents

Each advisory alert should show:

- facility or public-safe alias;
- current demand context;
- next-half-hour risk level;
- reason for the warning;
- recommended action;
- expected operational effect expressed conservatively;
- action deadline or review window;
- safety or critical-load restriction where relevant.

## Operator choices

- **Confirm:** accept the advisory action for manual or supervised implementation.
- **Defer:** postpone action and record the reason or new review time.
- **Dismiss:** reject the recommendation and record the reason.
- **Mute:** suppress repeated alerts for the selected facility or condition for a limited period.

## Human oversight

The AI recommendation is not a final switching command. The operator remains responsible for checking operational context, maintenance activity, critical services, safety constraints, and authorization before any action.

## Current demonstration boundary

Before the edge simulator starts, the dashboard uses clearly labelled public fallback alerts. After at least four simulated half-hour values arrive, `/api/alerts` switches to advisory alerts generated from live edge forecasts. This proves the operational inference and audit workflow but does not claim a commissioned campus meter connection or hardware actuator. Production deployment still requires approved integration, user accounts, role-based access, monitoring and operator feedback.

## Demonstration and future validation

The repository provides a repeatable local walkthrough rather than an invented formal validation report. During a controlled pilot, record operator role, tasks attempted, confusing alerts, accepted actions, rejected actions, alert burden, and changes made to the workflow.