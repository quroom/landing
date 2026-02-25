## ADDED Requirements

### Requirement: Persona-specific landing pages SHALL be independently accessible
The system SHALL provide dedicated landing pages for founders and foreign developers, each with a unique route and focused messaging.

#### Scenario: Founder landing page route resolves
- **WHEN** a user requests `/for-founders/`
- **THEN** the system returns a founder-focused landing page
- **AND** the page includes founder-specific CTA and service framing

#### Scenario: Foreign developer landing page route resolves
- **WHEN** a user requests `/for-foreign-developers/`
- **THEN** the system returns a foreign-developer-focused landing page
- **AND** the page includes onboarding/career-link CTA and content

### Requirement: Main landing page SHALL stay as a trust-oriented hub
The system SHALL keep `/` as the common company landing page focused on credibility and shared value without persona-mixed CTA overload.

#### Scenario: Main route presents common narrative
- **WHEN** a user requests `/`
- **THEN** the system renders company overview and shared trust signals
- **AND** persona-specific deep conversion copy is deferred to persona pages
