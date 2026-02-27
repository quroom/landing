# lead-magnet-email-followup Specification

## Purpose
Define full follow-up report delivery behavior for free diagnosis submissions.
## Requirements
### Requirement: Full diagnosis report MUST be delivered via email after submission

The lead-magnet follow-up email MUST vary copy by overall diagnosis grade (A/B/C), MUST keep language simple for founders, and MUST remain concise.  
Email text/HTML rendering MUST consume a shared channel-neutral section model that is also used by preview generation so section order and CTA contract stay aligned.

#### Scenario: Delivery succeeds

- **WHEN** a diagnosis inquiry email is successfully generated
- **THEN** the email MUST include grade-specific interpretation copy
- **AND** the email MUST include only one weak category as default visible detail
- **AND** the email MUST include one prioritized 2-week action
- **AND** the email MUST include exactly one primary CTA
- **AND** the email MUST keep paragraph spacing and readability in both text and HTML variants
- **AND** the email section order MUST match the shared section model order

#### Scenario: Shared section model is updated

- **WHEN** section definition (title/order/body/cta) changes in the shared model
- **THEN** email text output MUST reflect the updated definition without channel-specific divergence
- **AND** email HTML output MUST reflect the same updated definition
