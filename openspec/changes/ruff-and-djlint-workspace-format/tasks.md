## 1. Tooling Baseline

- [x] 1.1 Add Ruff dependency and baseline configuration for formatting + import ordering.
- [x] 1.2 Add djLint dependency and baseline configuration for Django template formatting.
- [x] 1.3 Define workspace-level formatter mapping so Python and Django template files use the intended tools.

## 2. Workflow Integration

- [x] 2.1 Add or update scripts for local format/apply and format/check commands.
- [x] 2.2 Integrate formatting checks into CI/verification flow without breaking existing test sequence.
- [x] 2.3 Ensure format check outputs provide actionable remediation commands.

## 3. Runbook and Documentation

- [x] 3.1 Update developer runbook with Ruff and djLint setup + execution order.
- [x] 3.2 Document template formatting guardrails (when to use ignore pragmas, when to avoid generic HTML formatter).
- [x] 3.3 Add quick-start commands for new machines to reproduce local and CI formatting behavior.

## 4. Validation

- [ ] 4.1 Run format commands on representative Python and template files to confirm deterministic output.
- [ ] 4.2 Run full verification sequence to ensure formatting integration does not regress existing checks.
- [x] 4.3 Capture known limitations and follow-up items for incremental tightening of formatting scope.
