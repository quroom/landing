## MODIFIED Requirements

### Requirement: Dashboard filtering MUST support status, date range, and lead segmentation
The dashboard MUST support filtering by delivery status, date range, and inquiry segmentation (general inquiry vs lead-magnet diagnosis) for operational triage.

#### Scenario: Staff applies status/date filters
- **WHEN** a staff user selects status and/or date range filters
- **THEN** the dashboard list MUST reflect filtered inquiries
- **AND** filter states MUST remain visible in the UI

#### Scenario: Staff filters lead-magnet records
- **WHEN** a staff user selects inquiry-type segmentation for lead-magnet diagnosis
- **THEN** the dashboard MUST return only lead-magnet submissions
- **AND** segmented counts MUST remain visible in KPI cards
