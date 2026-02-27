## MODIFIED Requirements

### Requirement: Diagnosis result MUST bridge to graded next-action CTAs

The system MUST map diagnosis grade to differentiated execution guidance while keeping one shared CTA expression across grades, and MUST preserve a single CTA button in each result.  
The diagnosis-to-contact flow MUST carry diagnosis context so the contact form can start in a recommended pre-selected state.

#### Scenario: Grade A result bridges with optimization guidance

- **WHEN** a diagnosis result grade is A
- **THEN** the result section MUST show exactly one CTA button using the shared CTA expression
- **AND** the result MUST include immediate optimization actions mapped to detected bottlenecks
- **AND** contact entry MUST include diagnosis context with recommended pre-selection

#### Scenario: Grade B result bridges with two-week execution guidance

- **WHEN** a diagnosis result grade is B
- **THEN** the result section MUST show exactly one CTA button using the shared CTA expression
- **AND** the result MUST include a two-week execution task aligned to the user’s dominant diagnosis axis
- **AND** contact entry MUST include diagnosis context with recommended pre-selection

#### Scenario: Grade C result bridges with stabilization guidance

- **WHEN** a diagnosis result grade is C
- **THEN** the result section MUST show exactly one CTA button using the shared CTA expression
- **AND** the result MUST include core stabilization guidance before expansion actions
- **AND** contact entry MUST include diagnosis context with recommended pre-selection
