## MODIFIED Requirements

### Requirement: Full diagnosis report MUST be delivered via email after submission
The lead-magnet follow-up email MUST vary interpretation copy by overall diagnosis grade (A/B/C), MUST use action-oriented language, and MUST remain concise. Email text/HTML rendering MUST consume the same shared section model used by preview generation so copy and section order stay aligned.

#### Scenario: Delivery succeeds with action-focused copy
- **WHEN** a diagnosis inquiry email is successfully generated
- **THEN** the email MUST include grade-specific interpretation copy aligned with simplified survey wording
- **AND** the email MUST include one primary two-week action derived from the same intent mapping and priority rule as preview
- **AND** the email MUST include one explicit completion criterion for that action
- **AND** the completion criterion MUST use intent-specific wording without repeated boilerplate prefix
- **AND** the email weakest-point interpretation block MUST NOT include anchor-question disclosure text such as `우선 항목`
- **AND** the email MUST include one mode indicator (`quick` or `detailed`) based on answered question coverage
- **AND** the email MUST include exactly one primary CTA expression
- **AND** the email MUST keep paragraph spacing and readability in both text and HTML variants
- **AND** the email section order MUST match the shared section model order

#### Scenario: Shared copy contract is updated
- **WHEN** summary/task/CTA base copy is changed in the shared section model
- **THEN** email text output MUST reflect the updated copy without channel-specific divergence
- **AND** email HTML output MUST reflect the same updated copy
- **AND** email interpretation blocks MUST keep intent-key mapping parity with preview output
