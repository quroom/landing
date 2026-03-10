# Capability: persona-landing-pages

## MODIFIED Requirements

### Requirement: Persona-specific landing pages SHALL be independently accessible
The system SHALL provide dedicated landing pages for founders and foreign developers, each with a unique route, focused messaging, and a defined default locale per persona.

#### Scenario: Founder landing page route resolves
- **WHEN** a user requests `/for-founders/`
- **THEN** the system returns a founder-focused landing page
- **AND** the page includes founder-specific CTA and AX-oriented service framing
- **AND** the page default locale is Korean unless the user explicitly selects another supported locale

#### Scenario: Foreign developer landing page route resolves
- **WHEN** a user requests `/for-foreign-developers/`
- **THEN** the system returns a foreign-developer-focused landing page
- **AND** the page includes practical-linkage/career-link CTA and support-boundary content
- **AND** the page default locale is English unless the user explicitly selects another supported locale

### Requirement: Persona pages SHALL define separate FAQ and KPI ownership
The system SHALL define separate FAQ focus and KPI tracking per persona journey, and SHALL preserve persona-specific meaning across supported locales.

#### Scenario: Persona FAQ/KPI boundaries are maintained
- **WHEN** content owners update FAQ or KPI definitions
- **THEN** founder and foreign-developer entries remain separated by page intent
- **AND** locale-specific copy preserves the same CTA intent and KPI mapping for each persona

