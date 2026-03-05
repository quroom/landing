## MODIFIED Requirements

### Requirement: Admin operation link page MUST provide one-click verification routes
The system MUST provide a staff-only operation link page that aggregates deployment verification routes and MUST present recent operational check summary information for rapid triage.

#### Scenario: Staff opens operation link page
- **WHEN** an authenticated staff user opens the operation link page
- **THEN** the page MUST show one-click links for `/healthz`, `/healthz/live`, `/healthz/ready`, `/admin-dashboard/`, and core landing/submit verification routes
- **AND** each link target MUST be reachable from the same environment domain

#### Scenario: Staff reviews recent check summary
- **WHEN** the operation link page renders for a staff user
- **THEN** the page MUST show the latest available deploy-check and smoke-check result summary
- **AND** the summary MUST include at least execution time, overall status, and failed route list when failures exist

#### Scenario: Non-staff user requests operation link page
- **WHEN** a non-staff user accesses the operation link page URL
- **THEN** the system MUST deny access using the same staff authorization policy as admin dashboard routes
