# Dataset Statement

## Source and purpose

The project uses institutional smart-meter data supplied through the University of Zimbabwe Department of Electrical and Electronic Engineering under departmental oversight. The data are used to develop and validate an AI-driven energy-management system for institutional networks.

The public repository does not redistribute the source workbooks. The original departmental communication or handover record should be retained privately for due-diligence review.

## Coverage

- 22 monitored facilities
- 1 September 2025 to 30 April 2026
- 30-minute intervals
- 255,552 rows after completion of the expected time grid
- 255,292 forecast-usable rows
- 99.898% forecast usability

## Main fields

- timestamp in SAST, UTC+2
- active power in kW
- reactive measurement in kVAR or meter-export equivalent
- apparent demand in kVA
- power factor
- interval consumption in kWh
- data-point count
- temperature and humidity where available

## Quality findings and treatment

- 7 missing intervals were inserted into the expected time grid and flagged.
- 56 partial intervals were retained with quality flags.
- 196 suspicious negative active-power rows were excluded from forecasting pending confirmation of the meter or current-transformer convention.
- Signed reactive values were preserved. Their physical direction is not interpreted until the meter-export convention is verified.
- Missing power factor occurs primarily at zero load.
- Weather coverage begins late in the period and is excluded from the principal full-period forecast benchmark.

The cleaning process preserves the source values and creates separate cleaned fields and quality flags. It does not silently overwrite suspicious measurements.

## Privacy and repository boundary

The dataset contains operational infrastructure information rather than personal records. It is still treated as confidential institutional data.

The repository may contain aggregate quality counts, source archive hashes, anonymous facility aliases, normalized charts and heatmaps, aggregate model and controller metrics, and synthetic or public sample records.

The repository must not contain the source ZIP or workbooks, exact private interval records, real facility-to-alias mappings, meter identifiers, credentials, or private model artefacts.

## Refresh and pilot use

The current evidence dataset is historical. A live pilot will require an approved meter-feed method, timestamp and schema validation, local buffering, monitoring of missing intervals, and a documented retention policy.
