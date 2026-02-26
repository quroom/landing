## MODIFIED Requirements

### Requirement: Contact submission email MUST target configured operations inbox
The system MUST send both contact submission notifications and lead-magnet report deliveries through the configured mail backend. Operational notification emails MUST target `QUROOM_CONTACT_EMAIL`, and user-facing lead-magnet follow-up emails MUST target the submitter email.

#### Scenario: Valid general inquiry is submitted with SMTP backend configured
- **WHEN** a user submits a valid contact form and SMTP settings are configured
- **THEN** the system MUST send an operations notification email via SMTP to `QUROOM_CONTACT_EMAIL`
- **AND** the persisted inquiry record MUST be marked as successful delivery with send timestamp

#### Scenario: Valid lead-magnet inquiry is submitted with SMTP backend configured
- **WHEN** a user submits a valid lead-magnet diagnosis form and SMTP settings are configured
- **THEN** the system MUST send an operations notification to `QUROOM_CONTACT_EMAIL`
- **AND** the system MUST send a follow-up report email to the submitter address
- **AND** the persisted inquiry record MUST be marked as successful delivery with send timestamp

#### Scenario: SMTP provider rejects or fails delivery
- **WHEN** a valid form submission triggers email sending but SMTP raises an exception
- **THEN** the system MUST keep the submission persisted and return a successful UX response
- **AND** the persisted inquiry record MUST be marked as failed delivery with an error summary
