# lead-magnet-weakest-intent-alignment Specification

## Purpose
TBD - created by archiving change align-weakest-intent-copy-with-action. Update Purpose after archive.
## Requirements
### Requirement: Weakest-point copy and primary action MUST align to the same anchor intent
The system SHALL derive the user-facing weakest-point primary copy and the single two-week primary action from the same anchor intent lineage, and SHALL expose this alignment in the result contract used by preview and email rendering.

#### Scenario: Result generated from 8-question diagnosis
- **WHEN** diagnosis scoring and weakest anchor selection are completed
- **THEN** the result MUST include exactly one anchor `intent_key`
- **AND** the weakest-point displayed copy MUST be generated from that same anchor `intent_key`
- **AND** the two-week primary action MUST be generated from that same anchor `intent_key`
- **AND** the result contract MUST include intent alignment fields that can be asserted by automated tests

#### Scenario: Perfect score result generated
- **WHEN** all eight questions are answered with top score
- **THEN** the output MUST keep intent alignment contract fields present
- **AND** weakest-point block MAY be omitted in user-facing copy
- **AND** one-action block and summary MUST remain internally traceable to a single intent lineage

### Requirement: Preview grouping MUST preserve intent-review traceability
The preview renderer SHALL allow grouping of equivalent bodies while preserving operator visibility into intent alignment.

#### Scenario: Multiple simulation cases are grouped
- **WHEN** preview cards are grouped by equivalent response body
- **THEN** each grouped card MUST expose the representative anchor `intent_key`
- **AND** grouped scenario titles MUST remain visible for audit
- **AND** grouping MUST NOT merge items that differ in weakest/action intent alignment contract

