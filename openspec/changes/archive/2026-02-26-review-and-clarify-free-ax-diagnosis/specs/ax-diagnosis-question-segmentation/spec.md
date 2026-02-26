## MODIFIED Requirements

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
