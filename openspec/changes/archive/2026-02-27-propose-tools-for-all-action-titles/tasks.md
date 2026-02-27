## 1. Pattern Catalog and Coverage Rules

- [x] 1.1 Define a minimum-eight severity response pattern catalog keyed by intent combinations in `landing/views.py`.
- [x] 1.2 Add a coverage validator that guarantees all 8 `tools_map` intent keys are covered by the full pattern set.
- [x] 1.3 Ensure single-user rendering still resolves to exactly one primary two-week action while keeping internal pattern coverage checks.

## 2. Shared Result Contract Alignment

- [x] 2.1 Refactor result assembly into shared logic so web/preview/email consume the same section contract.
- [x] 2.2 Update weakest-point and one-action mapping to enforce the same anchor `question_key`/`intent_key` lineage.
- [x] 2.3 Keep user-facing output concise with one primary action block and one matching tool recommendation.

## 3. Channel Rendering and Regression Tests

- [x] 3.1 Update preview/email rendering paths to preserve identical shared section order and copy semantics.
- [x] 3.2 Add tests for minimum-eight response pattern existence and full 8-intent coverage across the pattern catalog.
- [x] 3.3 Add parity tests confirming preview/email outputs remain equivalent for shared sections under the new pattern rules.
