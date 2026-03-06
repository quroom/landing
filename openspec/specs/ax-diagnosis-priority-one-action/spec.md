# ax-diagnosis-priority-one-action Specification

## Purpose
TBD - created by archiving change review-and-clarify-free-ax-diagnosis. Update Purpose after archive.
## Requirements
### Requirement: Diagnosis result MUST propose exactly one 2-week priority action
The system MUST output exactly one highest-leverage action for the next two weeks so users can start execution immediately, and that action MUST be derived from the same weakest-point anchor used for the primary improvement insight.

#### Scenario: Diagnosis result generated
- **WHEN** a user submits the diagnosis with all eight question answers completed
- **THEN** the result MUST include one prioritized action item only
- **AND** the action candidate set MUST be selected from the same weakest-axis anchor logic used by the weakest-point interpretation
- **AND** the selected action MUST use the same `question_key` / `intent_key` lineage as the weakest-point anchor question
- **AND** ranking inside that anchor candidate set MUST use `(2 - answer_score) * impact_weight`
- **AND** the action MUST include one plain-language task sentence for the next two weeks
- **AND** the action MUST include one explicit completion criterion sentence
- **AND** the completion criterion sentence MUST be intent-specific
- **AND** completion criterion wording MUST NOT repeat an identical boilerplate prefix across different intent keys
- **AND** the action MUST include matched tool recommendation text
- **AND** user-facing output MUST NOT expose additional parallel "primary actions" beyond this one
- **AND** the weakest-point primary copy shown to users MUST resolve from the same `intent_key` used by this one action

