## MODIFIED Requirements

### Requirement: Diagnosis result MUST include pattern-based segmentation labels
The system MUST provide personalized interpretation using a severity-based response-pattern set, while ensuring the primary weakest-point guidance and the primary two-week action are generated from the same anchor question intent.

#### Scenario: User receives diagnosis output
- **WHEN** diagnosis scoring is completed
- **THEN** the result MUST select one response pattern from a maintained pattern catalog
- **AND** the pattern catalog MUST contain at least eight distinct response patterns
- **AND** each selected pattern message MUST use plain-language wording aligned to survey intent keys
- **AND** the output MUST avoid exposing internal axis keys in user-facing primary summary copy
- **AND** the weakest-point secondary message MUST NOT expose per-question anchor text such as `우선 항목`
- **AND** the weakest-point anchor question key MUST match the primary one-action anchor question key
- **AND** the output MUST preserve a concise structure suitable for immediate decision making

### Requirement: Personalized result MUST map to actionable two-week priorities and tool suggestions
The system MUST generate personalized two-week priorities and tool recommendations from severity patterns by combining non-execution signals with business impact weights, while preventing weakest-point/action mismatch and intent coverage gaps.

#### Scenario: User receives personalized diagnosis output
- **WHEN** the system finishes diagnosis scoring and pattern selection
- **THEN** the system MUST derive the primary action candidate set from the same weakest-axis anchor used for weakest-point selection
- **AND** the system MUST rank candidates in that set by `(2 - answer_score) * impact_weight`
- **AND** candidates with equal impact weight MUST rank `not doing` ahead of `partially doing`
- **AND** the output MUST expose exactly one primary recommendation for immediate execution
- **AND** recommended tools MUST be mapped to the same intent key used by the selected primary recommendation

#### Scenario: Pattern catalog coverage is validated
- **WHEN** the system validates response-pattern definitions
- **THEN** the pattern catalog MUST cover all eight intent keys defined in `tools_map`
- **AND** no intent key in `tools_map` MUST remain unmapped by the full pattern set
