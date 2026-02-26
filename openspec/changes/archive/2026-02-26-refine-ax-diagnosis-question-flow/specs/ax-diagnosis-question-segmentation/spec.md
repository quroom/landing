## ADDED Requirements

### Requirement: AX diagnosis MUST collect responses across at least five diagnostic axes
The system MUST collect free diagnosis responses across five axes: operating context, repetitive bottlenecks, data consistency/visibility, automation fit, and execution readiness.

#### Scenario: User opens diagnosis form
- **WHEN** a visitor starts the free AX diagnosis flow
- **THEN** the form MUST present grouped questions for all five axes
- **AND** each axis MUST include at least one required question

### Requirement: Diagnosis submission MUST produce axis-level score breakdown
The system MUST calculate and persist axis-level score breakdown in addition to overall score.

#### Scenario: Valid diagnosis submission includes mixed-axis answers
- **WHEN** a user submits a valid diagnosis form
- **THEN** the system MUST compute an overall score and per-axis sub-scores
- **AND** the axis-level values MUST be available for result rendering and follow-up email generation
