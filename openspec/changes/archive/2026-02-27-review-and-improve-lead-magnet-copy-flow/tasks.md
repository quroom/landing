## 1. Action-Copy Contract Alignment

- [x] 1.1 Update shared section copy defaults for summary, two-week task label, completion criterion, and single CTA expression.
- [x] 1.2 Ensure preview and follow-up email consume the same copy contract without channel-specific wording drift.
- [x] 1.3 Keep grade-specific interpretation guidance while preserving one CTA expression across grades.
- [x] 1.4 Confirm CTA note remains support-guidance tone (not pressure/sales-heavy tone) across preview and email.

## 2. Diagnosis-to-Contact Bridging

- [x] 2.1 Pass diagnosis context into contact entry flow and apply recommended pre-selection state.
- [x] 2.2 Preserve user-editable form behavior and keep fallback to current default when pre-selection cannot be applied cleanly.
- [x] 2.3 Verify CTA target normalization remains stable (`#contact` -> `/#contact`) across result and email paths.

## 3. Validation and Regression Safety

- [x] 3.1 Update tests for action-focused copy snapshots and section-order equivalence across preview/email.
- [x] 3.2 Update tests for single CTA expression and diagnosis-context bridging behavior.
- [x] 3.3 Run `./scripts/verify.sh` and confirm change remains apply-ready with green tests.
