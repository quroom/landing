# Capability: persona-landing-pages

## Purpose
창업자/외국인 개발자 대상 랜딩을 분리해 전환 목적을 명확히 한다.

## ADDED Requirements

### Requirement: Persona-specific landing pages SHALL be independently accessible
The system SHALL provide dedicated landing pages for founders and foreign developers, each with a unique route and focused messaging.

#### Scenario: Founder landing page route resolves
- **WHEN** a user requests `/for-founders/`
- **THEN** the system returns a founder-focused landing page
- **AND** the page includes founder-specific CTA and AX-oriented service framing

#### Scenario: Foreign developer landing page route resolves
- **WHEN** a user requests `/for-foreign-developers/`
- **THEN** the system returns a foreign-developer-focused landing page
- **AND** the page includes practical-linkage/career-link CTA and support-boundary content

### Requirement: Main landing page SHALL stay as a trust-oriented hub
The system SHALL keep `/` as the common company landing page focused on credibility and shared value without persona-mixed CTA overload.

#### Scenario: Main route presents founder-priority common narrative
- **WHEN** a user requests `/`
- **THEN** the system renders founder-priority company overview and shared trust signals
- **AND** foreign-developer practical-linkage detail is deferred to `/for-foreign-developers/`

### Requirement: Persona pages SHALL define separate FAQ and KPI ownership
The system SHALL define separate FAQ focus and KPI tracking per persona journey.

#### Scenario: Persona FAQ/KPI boundaries are maintained
- **WHEN** content owners update FAQ or KPI definitions
- **THEN** founder and foreign-developer entries remain separated by page intent
