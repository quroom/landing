# admin-dashboard-navigation Specification

## Purpose
TBD - created by archiving change document-admin-dashboard-operations-improvements. Update Purpose after archive.
## Requirements
### Requirement: Admin entry page MUST expose dashboard shortcut
The admin interface MUST include a visible shortcut to inquiry dashboard so operators do not need to memorize direct URLs.

#### Scenario: Admin user enters /admin
- **WHEN** a logged-in admin user loads `/admin/`
- **THEN** the top user links area MUST include a navigation link to the inquiry dashboard
- **AND** link target MUST resolve to the staff dashboard route

#### Scenario: Deployment smoke check verifies admin dashboard route
- **WHEN** post-deploy validation runs
- **THEN** the deployment check MUST verify the inquiry dashboard route responds for authorized staff session context
- **AND** the check MUST fail deployment verification if dashboard route is unavailable

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

### Requirement: Inquiry resend operation MUST be available in admin list
The contact inquiry admin list MUST provide a batch action to resend selected inquiry notification emails.

#### Scenario: Admin runs resend action
- **WHEN** admin selects inquiries and executes resend action
- **THEN** the system MUST attempt email delivery for each selected inquiry
- **AND** each inquiry delivery status and error field MUST be updated based on result

