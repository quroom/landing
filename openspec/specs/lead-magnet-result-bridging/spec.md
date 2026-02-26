# lead-magnet-result-bridging Specification

## Purpose
Define grade-based action bridging from diagnosis result to next consultation CTA.

## Requirements
### Requirement: Diagnosis result MUST bridge to graded next-action CTAs
The system MUST map diagnosis grade to differentiated next-action CTAs that align with service tiers.

#### Scenario: Grade A result bridges to productivity consulting
- **WHEN** a diagnosis result grade is A
- **THEN** the result section MUST show a CTA for single-session productivity improvement consulting

#### Scenario: Grade B result bridges to AX build consultation
- **WHEN** a diagnosis result grade is B
- **THEN** the result section MUST show a CTA for AX build consultation

#### Scenario: Grade C result bridges to outsourcing track policy
- **WHEN** a diagnosis result grade is C
- **THEN** the result section MUST show a CTA for outsourcing-focused consultation
- **AND** the message MUST include the concurrent-capacity policy (동시 1개사 진행)
