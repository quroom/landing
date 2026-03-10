# Capability: landing-spec-persona-governance

## MODIFIED Requirements

### Requirement: Landing spec SHALL define role boundaries for each page type
The documentation MUST define separate responsibilities for main landing and persona landing pages, and MUST define language ownership for each page in supported locales.

#### Scenario: Spec includes page-role definitions
- **WHEN** maintainers read `quroom-landing-spec.md`
- **THEN** they can identify what belongs to main page vs founder page vs foreign-developer page
- **AND** they can verify that foreign-developer practical-linkage detail is not owned by main homepage
- **AND** they can verify each page's default language and translation ownership

### Requirement: Landing spec SHALL define persona CTA governance
The documentation MUST define CTA separation rules so each persona page has distinct primary conversion intent, and MUST preserve that intent consistently across supported languages.

#### Scenario: Spec includes CTA separation rules
- **WHEN** contributors update CTA copy or sections
- **THEN** they can verify persona-specific CTA ownership from the spec without ambiguity
- **AND** founder AX service CTA and foreign-developer practical-linkage CTA are documented separately
- **AND** localized CTA variants preserve the same conversion intent mapping
