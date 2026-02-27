## MODIFIED Requirements

### Requirement: Founder landing MUST provide a free AX diagnosis lead magnet flow
The system MUST provide a founder-focused free diagnosis flow on the main landing page that can be completed within a short interaction and capture both business context and execution friction, while keeping the questionnaire UI question-first and category-hidden.

#### Scenario: User starts diagnosis from main landing
- **WHEN** a visitor clicks the free diagnosis CTA on the main landing page
- **THEN** the system MUST display a diagnosis form as a single ordered question list
- **AND** the form MUST NOT expose internal category labels or category descriptions in the questionnaire area
- **AND** the flow MUST require answers for all questions `q1` through `q8` before submission
- **AND** each answered question MUST be stored individually for downstream scoring and copy mapping
- **AND** the flow MUST be labeled as a free founder-oriented AX diagnosis
- **AND** lead-magnet journey start events MUST be tracked with lead source metadata for conversion analysis

### Requirement: Diagnosis submission MUST return immediate partial result
The system MUST calculate and show an immediate result after valid diagnosis submission.

#### Scenario: Valid diagnosis is submitted
- **WHEN** a user submits required contact fields and all eight diagnosis questions
- **THEN** the system MUST calculate a diagnosis score and grade (A/B/C)
- **AND** the system MUST calculate segmented labels using all eight answers
- **AND** the system MUST expose a detailed coverage indicator for 8 answered questions
- **AND** the system MUST NOT generate quick-mode result labels or quick-mode result branches
- **AND** the immediate summary and one-action guidance MUST be generated from question intent mapping rather than category heading text
- **AND** submission tracking MUST include score/grade metadata for conversion segmentation
