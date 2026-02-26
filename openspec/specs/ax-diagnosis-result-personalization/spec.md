# ax-diagnosis-result-personalization Specification

## Purpose
TBD - created by archiving change refine-ax-diagnosis-question-flow. Update Purpose after archive.
## Requirements
### Requirement: Diagnosis result MUST include pattern-based segmentation labels

The system MUST provide personalized interpretation by combining each category with a category-specific A/B/C grade message.

#### Scenario: User receives diagnosis output

- **WHEN** diagnosis scoring is completed
- **THEN** the result MUST display category-level messages for all four categories
- **AND** each category message MUST be selected from grade-specific response variants (A/B/C)
- **AND** the output MUST preserve a concise structure suitable for immediate decision making

### Requirement: Personalized result MUST map to actionable two-week priorities and tool suggestions
The system MUST generate personalized two-week priorities and tool recommendations from segmented patterns, while limiting displayed priorities to the top three for faster decision-making.

#### Scenario: User receives personalized diagnosis output
- **WHEN** the system finishes diagnosis scoring and segmentation
- **THEN** the result section MUST include prioritized actions limited to top three items for the next two weeks
- **AND** recommended tools MUST be mapped to the user’s dominant bottleneck and readiness profile
- **AND** each priority item MUST be separated with readable spacing for quick scanning

