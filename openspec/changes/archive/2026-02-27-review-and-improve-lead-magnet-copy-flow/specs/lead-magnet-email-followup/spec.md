## MODIFIED Requirements

### Requirement: Full diagnosis report MUST be delivered via email after submission

The lead-magnet follow-up email MUST vary interpretation copy by overall diagnosis grade (A/B/C), MUST use action-oriented language, and MUST remain concise.  
Email text/HTML rendering MUST consume the same shared section model used by preview generation so copy and section order stay aligned.

#### Scenario: Delivery succeeds with action-focused copy

- **WHEN** a diagnosis inquiry email is successfully generated
- **THEN** the email MUST include grade-specific interpretation copy
- **AND** the email MUST include only one weak category as default visible detail
- **AND** the email MUST label the action section as one task to finish in two weeks
- **AND** the email MUST include one explicit completion criterion for that task
- **AND** the email MUST include exactly one primary CTA expression
- **AND** the email MUST keep paragraph spacing and readability in both text and HTML variants
- **AND** the email section order MUST match the shared section model order

#### Scenario: Shared copy contract is updated

- **WHEN** summary/task/CTA base copy is changed in the shared section model
- **THEN** email text output MUST reflect the updated copy without channel-specific divergence
- **AND** email HTML output MUST reflect the same updated copy
