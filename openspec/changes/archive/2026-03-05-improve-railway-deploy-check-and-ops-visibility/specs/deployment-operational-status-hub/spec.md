## ADDED Requirements

### Requirement: Deployment operational status hub MUST present unified check visibility
The system MUST provide a staff-facing operational status hub that consolidates deployment readiness and post-deploy smoke outcomes into a single view.

#### Scenario: Staff opens operational status hub
- **WHEN** an authenticated staff user opens the operational status hub page
- **THEN** the page MUST display pre-deploy check status and post-deploy smoke status in one screen
- **AND** each status block MUST clearly show pass/fail state

#### Scenario: Hub displays actionable failure context
- **WHEN** the latest check result is failed
- **THEN** the page MUST display which check failed and why (missing env key, route status mismatch, or dependency readiness failure)
- **AND** the page MUST provide direct links to rerun/check steps in runbook or CI workflow

### Requirement: Deployment check status data MUST be consumable by both page and automation
The system MUST store or expose deployment check result data in a normalized structure that can be rendered in the operational status hub and reused by CI/reporting flows.

#### Scenario: Deploy check writes normalized result
- **WHEN** pre-deploy or post-deploy check executes
- **THEN** the result MUST be captured with timestamp, check type, overall status, and detail items
- **AND** consumers MUST be able to read the latest result without parsing free-form logs

#### Scenario: No historical result exists
- **WHEN** the operational status hub loads before any check has run
- **THEN** the page MUST show a clear "no result yet" state
- **AND** the page MUST show how to execute the first check
