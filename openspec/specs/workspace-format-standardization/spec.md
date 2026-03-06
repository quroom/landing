# workspace-format-standardization Specification

## Purpose
TBD - created by archiving change ruff-and-djlint-workspace-format. Update Purpose after archive.
## Requirements
### Requirement: Workspace MUST standardize Python formatting with Ruff
The workspace MUST define Ruff as the canonical Python formatting and import-order tool for local development and automated checks.

#### Scenario: Developer formats Python files locally
- **WHEN** a developer runs the documented Python formatting command
- **THEN** Python files MUST be formatted using Ruff rules
- **AND** import ordering MUST be enforced by Ruff without requiring a separate isort command

#### Scenario: CI validates Python style consistency
- **WHEN** CI runs format/lint validation for Python code
- **THEN** the check MUST fail when files deviate from configured Ruff rules
- **AND** the failure output MUST indicate Ruff-based remediation commands

### Requirement: Workspace MUST standardize Django template formatting with djLint
The workspace MUST define djLint as the canonical formatter for Django templates to prevent template-syntax regressions caused by generic HTML formatters.

#### Scenario: Developer saves Django template file
- **WHEN** a developer formats a file under Django template paths
- **THEN** the file MUST be formatted by djLint rules
- **AND** the formatting process MUST preserve Django template variable/tag semantics

#### Scenario: Template formatting regression is detected
- **WHEN** template formatting output diverges from configured djLint rules
- **THEN** automated checks MUST report the mismatch
- **AND** developers MUST be able to reproduce the same result locally with documented commands

### Requirement: Workspace formatting guidance MUST be reproducible across machines
The repository MUST include workspace-level configuration and commands so different machines produce the same formatting result.

#### Scenario: New machine onboarding
- **WHEN** a developer clones the repository on a new machine
- **THEN** the repository documentation MUST provide setup and execution commands for Ruff and djLint
- **AND** running those commands MUST produce deterministic results equivalent to CI checks

