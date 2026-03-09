## MODIFIED Requirements

### Requirement: Main homepage MUST be founder-first
The system MUST position `/` as a founder-focused page with startup execution outcomes as the primary narrative.

#### Scenario: Main route presents founder-first value
- **WHEN** a user requests `/`
- **THEN** the page highlights founder problems and execution outcomes
- **AND** founder consultation is shown as the primary CTA
- **AND** founder services are organized as AX execution, outsourcing-focused track, and startup foundation infrastructure

#### Scenario: Testimonial trust signal appears only after approval threshold
- **WHEN** a user requests `/` and approved testimonial count is below configured threshold
- **THEN** the page does not show a public testimonial section
- **AND** founder-first messaging remains the primary trust narrative

#### Scenario: Approved testimonials can reinforce founder trust narrative
- **WHEN** a user requests `/` and approved testimonial count meets or exceeds configured threshold
- **THEN** the page may show a testimonial section
- **AND** only approved testimonials are rendered
