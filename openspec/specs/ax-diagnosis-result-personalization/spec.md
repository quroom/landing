# ax-diagnosis-result-personalization Specification

## Purpose
TBD - created by archiving change refine-ax-diagnosis-question-flow. Update Purpose after archive.
## Requirements
### Requirement: Diagnosis result MUST include pattern-based segmentation labels
The system MUST classify submissions into segmented result labels based on response patterns, including operation type, bottleneck risk type, and execution readiness type.

#### Scenario: Submission patterns indicate high operational bottleneck
- **WHEN** diagnosis responses match high-friction repetitive work and weak data consistency patterns
- **THEN** the system MUST assign a bottleneck-focused segmentation label
- **AND** the result summary MUST explain why the label was assigned

### Requirement: Personalized result MUST map to actionable two-week priorities and tool suggestions
The system MUST generate personalized two-week priorities and tool recommendations from segmented patterns.

#### Scenario: User receives personalized diagnosis output
- **WHEN** the system finishes diagnosis scoring and segmentation
- **THEN** the result section MUST include prioritized actions for the next two weeks
- **AND** recommended tools MUST be mapped to the user’s dominant bottleneck and readiness profile

