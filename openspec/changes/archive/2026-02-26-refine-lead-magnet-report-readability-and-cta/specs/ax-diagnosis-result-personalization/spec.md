## MODIFIED Requirements

### Requirement: Personalized result MUST map to actionable two-week priorities and tool suggestions
The system MUST generate personalized two-week priorities and tool recommendations from segmented patterns, while limiting displayed priorities to the top three for faster decision-making.

#### Scenario: User receives personalized diagnosis output
- **WHEN** the system finishes diagnosis scoring and segmentation
- **THEN** the result section MUST include prioritized actions limited to top three items for the next two weeks
- **AND** recommended tools MUST be mapped to the user’s dominant bottleneck and readiness profile
- **AND** each priority item MUST be separated with readable spacing for quick scanning
