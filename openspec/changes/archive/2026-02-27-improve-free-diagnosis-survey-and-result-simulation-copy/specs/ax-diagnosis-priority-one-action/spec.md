## MODIFIED Requirements

### Requirement: Diagnosis result MUST propose exactly one 2-week priority action
The system MUST output exactly one highest-leverage action for the next two weeks so users can start execution immediately, using both non-execution status and business impact weighting.

#### Scenario: Diagnosis result generated
- **WHEN** a user submits the diagnosis with all required core questions completed
- **THEN** the result MUST include one prioritized action item only
- **AND** the action ranking MUST use `(2 - answer_score) * impact_weight` across answered questions
- **AND** the action MUST include one plain-language task sentence for the next two weeks
- **AND** the action MUST include one explicit completion criterion sentence
- **AND** the action MUST include matched tool recommendation text
