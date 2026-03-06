## 1. Intent Alignment Contract

- [x] 1.1 Add explicit intent-alignment contract fields to the lead-magnet result payload (`weakest_insight.intent_key`, `one_action.intent_key`, representative anchor intent metadata).
- [x] 1.2 Refactor weakest-point copy generation to use anchor intent templates as primary source while keeping axis info as secondary metadata.
- [x] 1.3 Ensure one-action generation continues to resolve from the same anchor intent and fail-safe fallback keeps intent consistency.

## 2. Section Rendering and Preview Traceability

- [x] 2.1 Update section AST assembly so weakest-point and one-action blocks always render from the same anchor intent lineage.
- [x] 2.2 Extend preview grouping signature/metadata so grouped cards keep intent-review traceability (representative intent + grouped scenario titles).
- [x] 2.3 Keep preview and email section order/headings identical after intent-aligned copy changes.

## 3. Validation and Regression Safety

- [x] 3.1 Update unit tests to assert weakest-point/action intent equality and contract-field presence for normal + perfect-score scenarios.
- [x] 3.2 Update preview tests to verify grouping does not merge cross-intent mismatches and still displays reviewable scenario linkage.
- [x] 3.3 Refresh text snapshot expectations for section rendering and email body where intent-aligned wording changed.

## 4. Verification

- [x] 4.1 Run focused diagnosis/report tests for lead-magnet result generation, preview rendering, and mail rendering.
- [x] 4.2 Run full project verification (`./scripts/verify.sh`) to confirm no regression outside diagnosis flow.
