## MODIFIED Requirements

### Requirement: Railway deployment MUST provide a dedicated health endpoint
The system MUST expose a dedicated health endpoint set for deployment and runtime verification without depending on landing-page rendering, and MUST separate liveness and readiness semantics.

#### Scenario: Health endpoint responds in normal operation
- **WHEN** a client requests `GET /healthz`
- **THEN** the system MUST return HTTP 200 with a lightweight summary payload
- **AND** the response MUST be independent from template rendering or user session state

#### Scenario: Liveness endpoint verifies process availability
- **WHEN** a client requests `GET /healthz/live`
- **THEN** the system MUST return HTTP 200 when the app process can serve requests
- **AND** the response MUST NOT require downstream dependency checks

#### Scenario: Readiness endpoint verifies serving readiness
- **WHEN** a client requests `GET /healthz/ready`
- **THEN** the system MUST return HTTP 200 only when required runtime dependencies for serving traffic are ready
- **AND** the response MUST return non-200 when readiness preconditions fail

#### Scenario: Health endpoint is used in deployment automation
- **WHEN** pre-deploy or post-deploy automation runs
- **THEN** the deployment pipeline MUST call `/healthz/live` and `/healthz/ready` as required checks
- **AND** deployment verification MUST fail if either endpoint does not return HTTP 200

### Requirement: Post-deploy checks MUST be automatable in CI/CD
The system MUST support automated post-deploy verification for core operational routes and submit flows using route-specific expected status codes.

#### Scenario: CI/CD post-deploy smoke checks run
- **WHEN** deployment completes in Railway and post-deploy automation is triggered
- **THEN** CI/CD automation MUST verify `/healthz/live` and `/healthz/ready` return HTTP 200
- **AND** CI/CD automation MUST verify staff-only routes with expected redirect/auth behavior
- **AND** CI/CD automation MUST verify submit endpoints with expected method/access status codes
- **AND** automation result MUST be recorded as pass/fail for release gating

#### Scenario: Smoke check fails with actionable reason
- **WHEN** a route response differs from expected status code
- **THEN** the smoke check output MUST include the route, expected status code, and actual status code
- **AND** operators MUST be able to decide retry vs rollback from the output alone
