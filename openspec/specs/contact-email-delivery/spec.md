# contact-email-delivery Specification

## Purpose
TBD - created by archiving change add-contact-email-delivery-and-internal-log. Update Purpose after archive.
## Requirements
### Requirement: Contact submission email MUST target configured operations inbox
The system MUST send contact submission notifications to `QUROOM_CONTACT_EMAIL`, and production configuration MUST allow `help@quroom.kr`.

#### Scenario: Valid contact submission uses configured recipient
- **WHEN** a valid contact form is submitted
- **THEN** the email recipient list uses `settings.QUROOM_CONTACT_EMAIL`
- **AND** the configured value can be set to `help@quroom.kr`

### Requirement: Email delivery result MUST be explicitly captured
The system MUST treat email send success/failure as explicit outcomes for each submission.

#### Scenario: Email send succeeds
- **WHEN** email backend accepts the submission notification
- **THEN** the submission is marked as delivery success

#### Scenario: Email send fails
- **WHEN** email backend raises an exception for the submission notification
- **THEN** the submission is marked as delivery failed
- **AND** failure reason is stored for operational review

