# Capability: foreign-developer-practical-linkage

## MODIFIED Requirements

### Requirement: Practical-linkage support MUST be confined to foreign-developer page
The system MUST present practical-linkage support for foreign developers only on `/for-foreign-developers/`, and MUST deliver that page with English as the default locale.

#### Scenario: Practical-linkage content scope
- **WHEN** users compare `/` and `/for-foreign-developers/`
- **THEN** practical-linkage support detail appears only on `/for-foreign-developers/`
- **AND** practical-linkage headline and CTA copy are rendered in English by default

### Requirement: Foreign-developer page MUST state support boundary
The system MUST clearly state that visa/legal agency work is out of scope in all supported locales for `/for-foreign-developers/`.

#### Scenario: Boundary statement is visible
- **WHEN** a user reads foreign-developer FAQ or service scope
- **THEN** out-of-scope items include visa/legal agency handling
- **AND** the out-of-scope statement is available in English by default and in selected supported locales when requested

