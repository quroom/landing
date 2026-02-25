# contact-inquiry-operational-review Specification

## Purpose
TBD - created by archiving change add-contact-email-delivery-and-internal-log. Update Purpose after archive.
## Requirements
### Requirement: Operators MUST be able to review inquiry history in Django Admin
The system MUST expose stored contact inquiries in Django Admin with essential fields for operational review.

#### Scenario: Admin list shows inquiry overview
- **WHEN** an authenticated staff user opens contact inquiry admin list
- **THEN** list shows submitter identity, inquiry type, created time, and email delivery status

### Requirement: Operators MUST be able to find failed deliveries quickly
The system MUST provide admin filtering to isolate failed delivery records.

#### Scenario: Filter failed inquiries
- **WHEN** an operator applies delivery status filter `failed`
- **THEN** only failed inquiry records are shown
- **AND** each record exposes failure reason for follow-up action

