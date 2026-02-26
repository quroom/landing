# ax-diagnosis-question-segmentation Specification

## Purpose
TBD - created by archiving change refine-ax-diagnosis-question-flow. Update Purpose after archive.
## Requirements
### Requirement: AX diagnosis MUST collect responses across at least five diagnostic axes

The system MUST collect free diagnosis responses across four categories to improve interpretability and reduce cognitive load.

#### Scenario: Diagnosis form and scoring axis are loaded

- **WHEN** the diagnosis form is rendered and scoring axes are computed
- **THEN** questions MUST be mapped to exactly four categories:
  - workflow clarity
  - data operation base
  - automation design
  - execution system
- **AND** axis summaries MUST reflect only these four categories

### Requirement: Diagnosis submission MUST produce axis-level score breakdown
The system MUST calculate and persist axis-level score breakdown in addition to overall score.

#### Scenario: Valid diagnosis submission includes mixed-axis answers
- **WHEN** a user submits a valid diagnosis form
- **THEN** the system MUST compute an overall score and per-axis sub-scores
- **AND** the axis-level values MUST be available for result rendering and follow-up email generation

