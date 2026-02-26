## MODIFIED Requirements

### Requirement: Lead-magnet report MUST use a CTA-first concise format

The report MUST avoid vague "next action" wording and MUST explicitly communicate one immediate execution step and one consultation CTA.

#### Scenario: Report content generated for web/preview/email

- **WHEN** report text is built
- **THEN** the report MUST include a clear section for immediate execution guidance
- **AND** the report MUST show only the weakest category by default
- **AND** the report MUST provide optional access to full category detail instead of always expanding all categories
- **AND** the report MUST include a separate, explicit consultation bridge with one CTA
- **AND** tool recommendations MUST be limited to a small, high-signal set (not a long list)

### Requirement: Report output MUST preserve readability spacing across channels

The system MUST apply readable spacing and line breaks in both web and email report outputs.

#### Scenario: Report is rendered in email

- **WHEN** a lead-magnet report email is sent
- **THEN** text blocks MUST include explicit paragraph spacing and line breaks
- **AND** HTML output MUST use readable line-height and section spacing
- **AND** CTA links that use `#contact` MUST resolve to homepage contact URL format (`/#contact`)
