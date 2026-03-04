# railway-deployment-readiness Specification

## Purpose
Define runtime/deploy readiness checks for Railway deployment and operation verification.

## Requirements
### Requirement: Railway deployment MUST provide a dedicated health endpoint
The system MUST expose a dedicated `/healthz` endpoint for deployment and runtime health verification without depending on landing-page rendering.

#### Scenario: Health endpoint responds in normal operation
- **WHEN** a client requests `GET /healthz`
- **THEN** the system MUST return HTTP 200 with a lightweight health payload
- **AND** the response MUST be independent from template rendering or user session state

#### Scenario: Health endpoint is used in deployment automation
- **WHEN** pre-deploy or post-deploy automation runs
- **THEN** the deployment pipeline MUST call `/healthz` as a required check
- **AND** deployment verification MUST fail if `/healthz` does not return HTTP 200

### Requirement: Production startup MUST enforce required environment validation
The system MUST validate required runtime configuration at startup in production mode to prevent partially configured releases.

#### Scenario: Required environment values are missing in production mode
- **WHEN** `DEBUG=False` and at least one required setting is missing
- **THEN** the application MUST fail fast during startup
- **AND** it MUST emit a clear validation error identifying missing configuration keys

#### Scenario: Required environment values are complete in production mode
- **WHEN** `DEBUG=False` and all required settings are provided
- **THEN** the application MUST start successfully
- **AND** runtime service initialization MUST continue without validation errors

### Requirement: Deployment readiness MUST support pre-deploy command checks
The system MUST provide a management command to validate deployment prerequisites before release.

#### Scenario: Pre-deploy check command succeeds
- **WHEN** operator or CI runs deployment readiness command with valid configuration
- **THEN** the command MUST verify critical prerequisites including database connectivity and mail configuration contract
- **AND** the command MUST exit with success status

#### Scenario: Pre-deploy check command fails
- **WHEN** deployment readiness command detects invalid configuration
- **THEN** the command MUST exit with non-zero status
- **AND** the command output MUST include actionable failure reasons for operators

### Requirement: Post-deploy checks MUST be automatable in CI/CD
The system MUST support automated post-deploy verification for core operational routes and submit flows.

#### Scenario: CI/CD post-deploy smoke checks run
- **WHEN** deployment completes in Railway
- **THEN** CI/CD automation MUST verify `/healthz` and `/admin-dashboard/` reachability
- **AND** CI/CD automation MUST execute at least one core submit-flow smoke check
- **AND** automation result MUST be recorded as pass/fail for release gating
