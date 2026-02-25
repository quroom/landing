## ADDED Requirements

### Requirement: Project code SHALL be consolidated under landing
The repository MUST consolidate Django project code under the `landing/` directory as the single code root.

#### Scenario: Code root unification
- **WHEN** a developer lists the project root
- **THEN** implementation code is located under `landing/`
- **AND** root-level code scattering is removed

### Requirement: Code placement SHALL be predictable
The restructured layout MUST make `landing/` the default location for new project code files.

#### Scenario: Adding a new module file
- **WHEN** a contributor adds a new backend module
- **THEN** they place it under `landing/` without ambiguity
