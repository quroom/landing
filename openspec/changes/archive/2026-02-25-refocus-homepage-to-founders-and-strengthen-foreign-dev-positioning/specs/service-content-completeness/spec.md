## MODIFIED Requirements

### Requirement: Service content SHALL include required fields per card
Each service card MUST include service name, target audience, scope summary, and CTA mapping.

#### Scenario: Service card validation in content source
- **WHEN** service content is updated in source data
- **THEN** required fields are present for every card used by main or persona pages
- **AND** founder AX package cards include duration and deliverable summary

### Requirement: Service offerings SHALL remain consistent across spec and implementation
The documented service offerings in `quroom-landing-spec.md` MUST match the implemented service content structure.

#### Scenario: Spec-to-code service consistency check
- **WHEN** maintainers compare the spec and rendered pages
- **THEN** no documented core service is missing from implementation
- **AND** no implemented core service is undocumented in the spec
- **AND** founder AX offerings and foreign-developer practical-linkage offerings stay page-scoped without cross-mixing
