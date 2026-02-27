## MODIFIED Requirements

### Requirement: Founder landing MUST provide a free AX diagnosis lead magnet flow
The system MUST provide a founder-focused free diagnosis flow on the main landing page that can be completed within a short interaction and capture both business context and execution friction, while keeping the questionnaire UI question-first.

#### Scenario: User starts diagnosis from main landing
- **WHEN** a visitor clicks the free diagnosis CTA on the main landing page
- **THEN** the system MUST display a diagnosis form as a sequential question list without exposing internal category labels
- **AND** the flow MUST require answers for core questions `q1`, `q3`, `q5`, and `q7` before submission
- **AND** the flow MUST allow optional answers for `q2`, `q4`, `q6`, and `q8` as an additional step
- **AND** each answered question MUST be stored individually for downstream scoring and copy mapping
- **AND** the flow MUST be labeled as a free founder-oriented AX diagnosis

### Requirement: Diagnosis submission MUST return immediate partial result
The system MUST calculate and show an immediate partial result after valid diagnosis submission.

#### Scenario: Valid diagnosis is submitted
- **WHEN** a user submits required contact fields and all required core questions
- **THEN** the system MUST calculate a diagnosis score and grade (A/B/C)
- **AND** the system MUST calculate segmented labels using answered questions only
- **AND** the system MUST include a response coverage indicator (`quick` for 4 answers, `detailed` for 8 answers)
- **AND** the system MUST show an immediate partial result summary including prioritized next action guidance
