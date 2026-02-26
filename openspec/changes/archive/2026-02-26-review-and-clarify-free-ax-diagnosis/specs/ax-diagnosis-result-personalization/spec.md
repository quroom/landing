## MODIFIED Requirements

### Requirement: Diagnosis result MUST include pattern-based segmentation labels

The system MUST provide personalized interpretation by combining each category with a category-specific A/B/C grade message.

#### Scenario: User receives diagnosis output

- **WHEN** diagnosis scoring is completed
- **THEN** the result MUST display category-level messages for all four categories
- **AND** each category message MUST be selected from grade-specific response variants (A/B/C)
- **AND** the output MUST preserve a concise structure suitable for immediate decision making
