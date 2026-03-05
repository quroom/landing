## ADDED Requirements

### Requirement: Developer runbook MUST define formatting workflow before verification
The developer runbook MUST include a clear formatting sequence using Ruff and djLint before running functional verification commands.

#### Scenario: Developer follows local workflow documentation
- **WHEN** a developer follows the documented local development workflow
- **THEN** formatting commands for Python and Django templates MUST run before verification commands
- **AND** the workflow MUST specify expected pass/fail behavior for formatting checks

#### Scenario: Formatting and verification responsibilities are separated
- **WHEN** a developer reads runbook command sections
- **THEN** formatting commands and runtime/test verification commands MUST be documented as separate steps
- **AND** the runbook MUST explain when to run each step (pre-commit, pre-PR, CI)
