# lead-magnet-cta-report-format Specification

## Purpose
TBD - created by archiving change refine-lead-magnet-report-readability-and-cta. Update Purpose after archive.
## Requirements
### Requirement: Lead-magnet report MUST use a CTA-first concise format
The report MUST avoid vague wording and MUST communicate one immediate execution task and one consultation CTA in a conversion-oriented format. Report content generation for preview and email MUST use the same channel-neutral section contract.

#### Scenario: Report content generated for web/preview/email
- **WHEN** report text is built
- **THEN** the report MUST include a clear summary section written in plain action-oriented language
- **AND** the report MUST provide intent-aligned interpretation that directly maps to answered question meaning
- **AND** the report MUST label the execution block as one task to finish in two weeks
- **AND** the report MUST include one completion criterion sentence for that task
- **AND** the report MUST include one explicit consultation bridge with one CTA
- **AND** preview and email MUST keep identical section order and section headings for shared content
- **AND** preview MUST render only one weakest-point block and MUST NOT render an additional full 4-point expansion block
- **AND** weakest-point secondary text MUST NOT expose anchor-question disclosure text such as `우선 항목`
- **AND** the weakest-point block and one-action block MUST resolve from the same anchor question intent lineage
- **AND** user-facing report output MUST keep exactly one primary two-week action block
- **AND** weakest-point primary copy visible to users MUST be generated from the same anchor `intent_key` as the one-action block

#### Scenario: Report generated from full diagnosis mode
- **WHEN** all eight diagnosis questions are answered
- **THEN** the report MUST disclose detailed diagnosis mode status for eight answers
- **AND** the report MUST NOT emit quick diagnosis mode labels
- **AND** the report MUST preserve the same section contract across preview and email

#### Scenario: Preview groups duplicate response bodies
- **WHEN** preview reports are generated for multiple simulation inputs
- **THEN** items with identical response body text except title MUST be grouped into one preview card
- **AND** each grouped card MUST expose all associated scenario titles so reviewers can trace grouped cases
- **AND** each grouped card MUST expose the representative anchor intent used by both weakest-point and one-action blocks

### Requirement: Report output MUST preserve readability spacing across channels
The system MUST apply readable spacing and line breaks in both web and email report outputs while preserving the same core copy contract.

#### Scenario: Report is rendered in email
- **WHEN** a lead-magnet report email is sent
- **THEN** text blocks MUST include explicit paragraph spacing and line breaks
- **AND** HTML output MUST use readable line-height and section spacing
- **AND** CTA links that use `#contact` MUST resolve to homepage contact URL format (`/#contact`)

#### Scenario: Cross-channel equivalence is validated
- **WHEN** preview and email outputs are generated from the same diagnosis input
- **THEN** the system MUST verify shared section equivalence (section titles/order/CTA link target)
- **AND** preview duplicate-grouping MUST compare response bodies while ignoring scenario title differences
- **AND** the system MUST retain text snapshot coverage for rendered copy regression detection
- **AND** equivalence checks MUST include weakest-point/action anchor intent alignment

