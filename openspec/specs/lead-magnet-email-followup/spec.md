# lead-magnet-email-followup Specification

## Purpose
Define full follow-up report delivery behavior for free diagnosis submissions.

## Requirements
### Requirement: Full diagnosis report MUST be delivered via email after submission
The system MUST deliver the full diagnosis report/checklist to the submitted email address after successful diagnosis submission.

#### Scenario: Delivery succeeds
- **WHEN** a valid diagnosis submission is received and SMTP delivery succeeds
- **THEN** the system MUST send a lead-magnet follow-up email with full report content
- **AND** delivery status MUST be persisted for operational tracking

#### Scenario: Delivery fails
- **WHEN** a valid diagnosis submission is received but SMTP delivery fails
- **THEN** the system MUST keep the submission persisted as a lead record
- **AND** the delivery failure MUST be captured with error details for admin review/resend
