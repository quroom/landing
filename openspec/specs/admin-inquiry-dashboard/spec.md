# admin-inquiry-dashboard Specification

## Purpose
TBD - created by archiving change document-admin-dashboard-operations-improvements. Update Purpose after archive.
## Requirements
### Requirement: Staff-only inquiry dashboard MUST be available
The system MUST provide a staff-restricted inquiry operations dashboard that aggregates key contact metrics.

#### Scenario: Staff opens dashboard
- **WHEN** a logged-in staff user accesses `/admin-dashboard/`
- **THEN** the system MUST return a dashboard page with inquiry KPIs and recent inquiries
- **AND** non-staff users MUST be redirected to admin login

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

### Requirement: Dashboard MUST support secure logout action
The dashboard MUST provide a logout control that conforms to Django admin logout method requirements.

#### Scenario: Staff logs out from dashboard
- **WHEN** staff clicks logout on dashboard
- **THEN** logout MUST be submitted as POST
- **AND** user session MUST be terminated
