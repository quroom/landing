## MODIFIED Requirements

### Requirement: AX diagnosis MUST collect responses across at least five diagnostic axes
The system MUST collect free diagnosis responses across exactly four internal diagnostic categories to preserve interpretability, while presenting the questionnaire in a category-hidden flow.

#### Scenario: Diagnosis form and scoring axis are loaded
- **WHEN** the diagnosis form is rendered and scoring axes are prepared
- **THEN** questions MUST be mapped to exactly four internal categories:
  - workflow clarity
  - data operation base
  - automation design
  - execution system
- **AND** the rendered form MUST show question statements without category headings
- **AND** core questions `q1`, `q3`, `q5`, and `q7` MUST be required
- **AND** optional questions `q2`, `q4`, `q6`, and `q8` MUST remain answerable in the same flow
- **AND** axis summaries MUST reflect only these four categories

### Requirement: Diagnosis submission MUST produce axis-level score breakdown
The system MUST calculate and persist axis-level score breakdown in addition to overall score.

#### Scenario: Valid diagnosis submission includes mixed-axis answers
- **WHEN** a user submits a valid diagnosis with 4 to 8 answered questions
- **THEN** the system MUST compute an overall score and per-axis sub-scores using answered questions as the denominator
- **AND** unanswered optional questions MUST be excluded from denominator calculations
- **AND** axis-level values MUST be available for result rendering and follow-up email generation
- **AND** the result payload MUST include response coverage metadata (`quick` or `detailed`)
