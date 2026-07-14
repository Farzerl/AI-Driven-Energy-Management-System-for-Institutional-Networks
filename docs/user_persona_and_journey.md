# User Persona and Operational Journey

## Primary persona

**Role:** Estates and Facilities electrical or maintenance operator.

**Context:** Responsible for multiple institutional buildings and services, often with limited time, mixed meter coverage, changing timetables, and intermittent connectivity.

**Pain point:** Existing information is mainly retrospective. The operator may learn that a peak occurred only after the demand interval or billing period has passed.

**Decision needed:** Determine whether an emerging facility-level condition requires monitoring, investigation, load staggering, temporary deferral, or no action.

**Constraints:**

- critical services must not be disrupted;
- recommendations must be understandable quickly;
- the operator must remain accountable for the final action;
- alerts must work with limited connectivity;
- private infrastructure information must remain controlled;
- unnecessary alerts can create fatigue.

## Secondary personas

### Finance or management reviewer

Uses aggregate trends and verified pilot results to assess cost exposure, intervention outcomes, and funding decisions. Does not operate the live alert queue.

### Engineering administrator

Maintains facility limits, data interfaces, user access, logs, model versions, and deployment configuration.

## User journey

```text
Meter or safe sample reading arrives
        |
        v
System validates and stores the reading
        |
        v
Forecast and peak-risk evidence are updated
        |
        v
Operator sees facility, risk, context, and recommended action
        |
        v
Operator checks safety and operational context
        |
        +--> Confirm
        +--> Defer
        +--> Dismiss
        +--> Mute
        |
        v
Decision and note are recorded
        |
        v
Pilot compares the decision with actual demand and service outcomes
```

## Information architecture

- **Overview:** dataset scale, forecast evidence, and current product boundary.
- **Estates and Facilities:** actionable alert queue and decision audit.
- **Edge gateway:** connectivity, buffering, and received readings.
- **Cost impact:** public-source expenditure and planning scenarios.
- **Data evidence:** heatmap, profiles, facility concentration, and quality.
- **AI vs rule:** forecast-assisted trade-off against a simple controller.
- **Architecture:** hardware, software, security, and deployment boundary.

## Visualisation choices

- KPI cards surface the few results needed in the first minute.
- Bar charts compare alternatives directly.
- Line charts show time or validation changes.
- Heatmaps expose repeated operating patterns.
- Tables preserve exact planning values.
- Risk labels and action buttons convert evidence into an operational decision.

## Validation position

A formal usability study is not claimed. The repository provides a repeatable local walkthrough for judges and team members. Formal Estates feedback should be collected during the controlled pilot rather than invented for submission.
