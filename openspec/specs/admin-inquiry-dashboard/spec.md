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

### Requirement: Dashboard filtering MUST support status and date range
The dashboard MUST support filtering inquiries by delivery status and date range for operational triage.

#### Scenario: Staff applies filters
- **WHEN** a staff user selects status and/or date range filters
- **THEN** the dashboard list MUST reflect filtered inquiries
- **AND** filter states MUST remain visible in the UI

### Requirement: Dashboard MUST support secure logout action
The dashboard MUST provide a logout control that conforms to Django admin logout method requirements.

#### Scenario: Staff logs out from dashboard
- **WHEN** staff clicks logout on dashboard
- **THEN** logout MUST be submitted as POST
- **AND** user session MUST be terminated

