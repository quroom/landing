## MODIFIED Requirements

### Requirement: Admin dashboard MUST segment lead-magnet records from general inquiries
The system MUST allow operators to distinguish lead-magnet submissions from general contact inquiries in the dashboard.

#### Scenario: Operator filters lead-magnet inquiries
- **WHEN** a staff user views the admin dashboard and applies inquiry type filters
- **THEN** lead-magnet records MUST be queryable independently from other inquiry types
- **AND** segmented counts MUST be visible for operational triage

### Requirement: Internal event tracking MUST include lead-magnet funnel events
The system MUST record lead-magnet-specific funnel events for internal conversion measurement.

#### Scenario: Lead magnet journey events are tracked
- **WHEN** a visitor starts or submits the lead magnet flow
- **THEN** the system MUST create funnel events with lead source metadata
- **AND** those events MUST be available in admin metrics

#### Scenario: Admin dashboard shows MVP lead-magnet funnel KPIs
- **WHEN** a staff user opens admin dashboard
- **THEN** the dashboard MUST display lead-magnet funnel counts for `start`, `submit`, `mail_sent`, and `contact_submit`
- **AND** the dashboard MUST display `submit_rate`, `mail_success_rate`, and `contact_conversion_rate`
- **AND** each rate MUST be computed with fixed KPI formulas and shown as percentage
- **AND** division-by-zero cases MUST render as `0.0%` without errors
