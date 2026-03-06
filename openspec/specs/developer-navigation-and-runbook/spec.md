# developer-navigation-and-runbook Specification

## Purpose
개발자가 저장소 구조를 빠르게 이해하고, 로컬 실행/검증 절차를 혼동 없이 수행할 수 있도록 문서 기준을 정의한다.
## Requirements
### Requirement: Project documentation SHALL describe the new structure
The repository documentation MUST explain the folder structure and where to find code, specs, and assets.

#### Scenario: New contributor onboarding
- **WHEN** a contributor reads the main README
- **THEN** they can identify where application code, OpenSpec docs, and assets are located

### Requirement: Runbook SHALL match the restructured paths
Local run/verify instructions MUST reference updated paths and commands consistent with the new layout.

#### Scenario: Local setup using runbook
- **WHEN** a contributor follows documented setup and verification steps
- **THEN** they can run and validate the project without path confusion

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

