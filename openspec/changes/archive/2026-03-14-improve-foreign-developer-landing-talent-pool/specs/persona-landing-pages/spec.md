# Capability: persona-landing-pages

## MODIFIED Requirements

### Requirement: Persona pages SHALL define separate FAQ and KPI ownership
The system SHALL define separate FAQ focus and KPI tracking per persona journey, and SHALL use a staged funnel KPI model for foreign-developer journeys instead of a single inquiry-submit KPI.

#### Scenario: Persona FAQ/KPI boundaries are maintained
- **WHEN** content owners update FAQ or KPI definitions
- **THEN** founder and foreign-developer entries remain separated by page intent
- **AND** foreign-developer KPI definitions include stage-based funnel checkpoints (quick intake, profile completion, introduction start)

## ADDED Requirements

### Requirement: Foreign-developer persona journey SHALL support staged CTA progression
The system SHALL provide a low-friction first CTA and a separate second-stage CTA for detailed profile completion on `/for-foreign-developers/`.

#### Scenario: Staged CTA progression is presented
- **WHEN** a user lands on `/for-foreign-developers/`
- **THEN** the page presents an initial quick-intake CTA with minimal required fields
- **AND** the page presents or links to a second-stage profile completion CTA for matching readiness
