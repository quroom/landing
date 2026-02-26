# ax-diagnosis-priority-one-action Specification

## Purpose
TBD - created by archiving change review-and-clarify-free-ax-diagnosis. Update Purpose after archive.
## Requirements
### Requirement: Diagnosis result MUST propose exactly one 2-week priority action

The system MUST output exactly one highest-leverage action for the next two weeks so users can start execution immediately.

#### Scenario: Diagnosis result generated

- **WHEN** a user submits the 10-question diagnosis
- **THEN** the result MUST include one prioritized action item only
- **AND** the action MUST include recommended tools and a concrete 2-week execution instruction

