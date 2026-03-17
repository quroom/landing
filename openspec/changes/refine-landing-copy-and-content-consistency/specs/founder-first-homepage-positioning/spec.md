## MODIFIED Requirements

### Requirement: Main homepage MUST be founder-first
The system MUST position `/` as a founder-focused page with startup execution outcomes as the primary narrative, and it MUST keep founder consultation as the clear first action. Founder-facing copy MUST use practical, low-hype language that helps users judge whether they can trust and delegate work now, rather than sounding like generic strategy consulting or brochure copy.

#### Scenario: Main route presents founder-first value
- **WHEN** a user requests `/`
- **THEN** the page highlights founder problems and accountable execution outcomes
- **AND** founder consultation is shown as the primary CTA
- **AND** any secondary CTA is visually subordinate to the consultation CTA
- **AND** founder services are organized as AX execution, outsourcing-focused track, and startup foundation infrastructure
- **AND** Hero, About, and Contact copy avoid brochure-style, overly abstract, or policy-style wording
- **AND** the page explains why work can be entrusted, not only why discussion may be useful

#### Scenario: Testimonial trust signal appears only after approval threshold
- **WHEN** a user requests `/` and approved testimonial count is below configured threshold
- **THEN** the page does not show a public testimonial section
- **AND** founder-first messaging remains the primary trust narrative

#### Scenario: Approved testimonials can reinforce founder trust narrative
- **WHEN** a user requests `/` and approved testimonial count meets or exceeds configured threshold
- **THEN** the page may show a testimonial section
- **AND** only approved testimonials are rendered

### Requirement: Main homepage MUST not include foreign-developer practical-linkage detail
The system MUST avoid practical-linkage detail for foreign developers on the main homepage and keep that journey as a secondary route.

#### Scenario: Main route avoids mixed-detail messaging
- **WHEN** a user reads the services area on `/`
- **THEN** foreign-developer practical-linkage detail is absent
- **AND** users are directed to `/for-foreign-developers/` for that content
- **AND** the main CTA hierarchy remains founder-first
