## 1. Health Signal Hardening

- [x] 1.1 Add dedicated liveness/readiness endpoints (`/healthz/live`, `/healthz/ready`) while keeping `/healthz` compatibility.
- [x] 1.2 Implement readiness dependency checks and ensure non-200 response on unmet preconditions.
- [x] 1.3 Add/adjust tests for health endpoint semantics and expected payload/status behavior.

## 2. Deploy Check and Smoke Automation

- [x] 2.1 Update `post-deploy-smoke.sh` to validate route-specific expected status codes instead of generic non-404 checks.
- [x] 2.2 Update deploy readiness command/output format to provide actionable failure context for retry vs rollback decisions.
- [x] 2.3 Update CI workflow (`deploy-readiness.yml`) to surface pre/post deploy check outcomes in a consistent format.

## 3. Operational Visibility Hub

- [x] 3.1 Extend admin operation links page to include `/healthz/live` and `/healthz/ready` and core verification routes.
- [x] 3.2 Add recent check result summary (last run time, overall status, failed items) to the operation links page.
- [x] 3.3 Ensure staff-only access policy and dashboard navigation links remain consistent after hub expansion.

## 4. Runbook and Verification

- [x] 4.1 Update Railway runbook with liveness/readiness meaning, status code matrix, and failure triage flow.
- [x] 4.2 Add/refresh automated tests for operation hub visibility and deploy check behavior.
- [x] 4.3 Run full verification (`./scripts/verify.sh`) and confirm the new change is apply-ready.
