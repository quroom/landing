## ADDED Requirements

### Requirement: Practical-linkage support MUST be confined to foreign-developer page
The system MUST present practical-linkage support for foreign developers only on `/for-foreign-developers/`.

#### Scenario: Practical-linkage content scope
- **WHEN** users compare `/` and `/for-foreign-developers/`
- **THEN** practical-linkage support detail appears only on `/for-foreign-developers/`

### Requirement: Foreign-developer page MUST state support boundary
The system MUST clearly state that visa/legal agency work is out of scope.

#### Scenario: Boundary statement is visible
- **WHEN** a user reads foreign-developer FAQ or service scope
- **THEN** out-of-scope items include visa/legal agency handling
