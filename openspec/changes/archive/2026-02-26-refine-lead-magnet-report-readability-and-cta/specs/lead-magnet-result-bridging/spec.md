## MODIFIED Requirements

### Requirement: Diagnosis result MUST bridge to graded next-action CTAs
The system MUST map diagnosis grade to differentiated next-action CTAs that align with service tiers, include segmented execution guidance based on response patterns, and expose only one CTA button per result.

#### Scenario: Grade A result bridges to productivity consulting
- **WHEN** a diagnosis result grade is A
- **THEN** the result section MUST show exactly one CTA button for single-session productivity improvement consulting
- **AND** the result MUST include immediate optimization actions mapped to detected bottlenecks

#### Scenario: Grade B result bridges to AX build consultation
- **WHEN** a diagnosis result grade is B
- **THEN** the result section MUST show exactly one CTA button for AX build consultation
- **AND** the result MUST include a two-week execution plan aligned to the user’s dominant diagnosis axis

#### Scenario: Grade C result bridges to outsourcing track policy
- **WHEN** a diagnosis result grade is C
- **THEN** the result section MUST show exactly one CTA button for outsourcing-focused consultation
- **AND** the message MUST include the concurrent-capacity policy (동시 1개사 진행)
