# Capability: foreign-developer-practical-linkage

## MODIFIED Requirements

### Requirement: Practical-linkage support MUST be confined to foreign-developer page
The system MUST present practical-linkage support for foreign developers only on `/for-foreign-developers/`, and MUST frame the support as staged job-search strategy and profile-readiness assistance rather than guaranteed placement.

#### Scenario: Practical-linkage content scope
- **WHEN** users compare `/` and `/for-foreign-developers/`
- **THEN** practical-linkage support detail appears only on `/for-foreign-developers/`
- **AND** the foreign-developer page includes staged strategy/readiness messaging before company introduction messaging

### Requirement: Foreign-developer page MUST state support boundary
The system MUST clearly state that visa/legal agency work is out of scope, MUST state that job placement is not guaranteed, and MUST state that company introductions are provided only after profile-fit review.

#### Scenario: Boundary statement is visible
- **WHEN** a user reads foreign-developer FAQ or service scope
- **THEN** out-of-scope items include visa/legal agency handling
- **AND** non-guaranteed placement policy is explicitly visible
- **AND** profile-fit prerequisite for introductions is explicitly visible

## ADDED Requirements

### Requirement: Foreign-developer page MUST define regional support mode
The system MUST state that Gwangju/Jeonnam candidates can receive local in-person support when appropriate, while other regions are supported online first.

#### Scenario: Regional support mode is visible
- **WHEN** a user reads the hero support note or support FAQ on `/for-foreign-developers/`
- **THEN** the page explains in-person priority for Gwangju/Jeonnam
- **AND** the page explains online-first support for other regions
