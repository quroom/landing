## MODIFIED Requirements

### Requirement: Full diagnosis report MUST be delivered via email after submission
The lead-magnet follow-up email MUST vary interpretation copy by severity pattern, MUST use action-oriented language, and MUST remain concise. Email text/HTML rendering MUST consume the same shared section model used by preview generation so copy and section order stay aligned.

#### Scenario: Delivery succeeds with action-focused copy
- **WHEN** a diagnosis inquiry email is successfully generated from a submission with all eight diagnosis answers
- **THEN** the email MUST include pattern-specific interpretation copy aligned with simplified survey wording
- **AND** the email MUST include one primary two-week action derived from the same intent mapping and weakest-point anchor rule as preview
- **AND** the email MUST include one explicit completion criterion for that action
- **AND** the completion criterion MUST use intent-specific wording without repeated boilerplate prefix
- **AND** the email weakest-point interpretation block MUST NOT include anchor-question disclosure text such as `우선 항목`
- **AND** the email MUST include one detailed-mode indicator for eight answered questions
- **AND** the email MUST NOT include quick-mode indicator text
- **AND** the email MUST include exactly one primary CTA expression
- **AND** the email MUST keep paragraph spacing and readability in both text and HTML variants
- **AND** the email section order MUST match the shared section model order

#### Scenario: Shared copy contract is updated
- **WHEN** summary/task/CTA base copy is changed in the shared section model
- **THEN** email text output MUST reflect the updated copy without channel-specific divergence
- **AND** email HTML output MUST reflect the same updated copy
- **AND** email interpretation blocks MUST keep intent-key mapping parity with preview output
- **AND** email response variants MUST be selectable from the same minimum-eight pattern catalog used by preview

#### Scenario: Email delivery is reflected in conversion metrics
- **WHEN** lead-magnet email delivery succeeds
- **THEN** the system MUST emit delivery success tracking event for conversion funnel metrics
- **AND** delivery status metadata MUST be queryable in admin conversion summaries
