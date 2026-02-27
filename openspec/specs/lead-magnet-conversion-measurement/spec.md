# lead-magnet-conversion-measurement Specification

## Purpose
Define fixed KPI formulas and event metadata contract for lead-magnet conversion measurement.

## Requirements
### Requirement: Lead-magnet conversion MUST use fixed KPI formulas
The system MUST define lead-magnet conversion performance with fixed KPI formulas so operators can compare periods consistently.

#### Scenario: KPI values are calculated for dashboard
- **WHEN** lead-magnet events are aggregated for a selected period
- **THEN** the system MUST calculate `submit_rate` as `lead_magnet_submit / lead_magnet_start`
- **AND** the system MUST calculate `mail_success_rate` as `lead_magnet_email_sent / lead_magnet_submit`
- **AND** the system MUST calculate `contact_conversion_rate` as `contact_submit(lead_source=founder_contact_from_diagnosis) / lead_magnet_email_sent`
- **AND** all KPI rates MUST be displayed as percentages rounded to one decimal place
- **AND** if any denominator is zero, the displayed rate MUST be `0.0%`

### Requirement: Conversion measurement MUST preserve event metadata contract
The system MUST preserve a stable event metadata contract so internal dashboard and GA4 analysis can use the same event semantics.

#### Scenario: Lead-magnet events are written
- **WHEN** lead-magnet journey events are tracked
- **THEN** each event MUST include `event_name`, `page_key`, and `lead_source`
- **AND** diagnosis submission events MUST include `score` and `grade`
- **AND** contact submission events from diagnosis bridge MUST be distinguishable with lead-magnet context metadata
- **AND** tracking payload MUST preserve UTM keys (`utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`) when present
