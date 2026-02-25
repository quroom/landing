## MODIFIED Requirements

### Requirement: Contact submission email MUST target configured operations inbox
The system MUST send contact submission notifications to `QUROOM_CONTACT_EMAIL` using the configured mail backend, and production configuration MUST allow `help@quroom.kr`.

#### Scenario: Valid inquiry is submitted with SMTP backend configured
- **WHEN** a user submits a valid contact form and SMTP settings are configured
- **THEN** the system MUST send an email via SMTP to `QUROOM_CONTACT_EMAIL`
- **AND** the persisted inquiry record MUST be marked as successful delivery with send timestamp

#### Scenario: SMTP provider rejects or fails delivery
- **WHEN** a valid contact form is submitted but SMTP sending raises an exception
- **THEN** the system MUST return the same successful form submission response to the user
- **AND** the persisted inquiry record MUST be marked as failed delivery with an error summary
