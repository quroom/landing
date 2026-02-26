## ADDED Requirements

### Requirement: Lead-magnet report MUST use a CTA-first concise format
The system MUST format diagnosis reports in a concise CTA-first structure so users can quickly decide the next action without reading long narrative blocks.

#### Scenario: User receives report output
- **WHEN** a diagnosis result is generated
- **THEN** the report MUST include a short summary, top three priorities, and one clear next action CTA
- **AND** non-essential explanatory text MUST be reduced to keep the message scannable

### Requirement: Report output MUST preserve readability spacing across channels
The system MUST apply readable spacing and line breaks in both web and email report outputs.

#### Scenario: Report is rendered in email
- **WHEN** a lead-magnet report email is sent
- **THEN** text blocks MUST include explicit paragraph spacing and line breaks
- **AND** HTML output MUST use readable line-height and section spacing
