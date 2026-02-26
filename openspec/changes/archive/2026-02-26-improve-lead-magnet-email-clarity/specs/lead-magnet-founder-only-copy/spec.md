## ADDED Requirements

### Requirement: Free diagnosis email copy MUST target founders only

The system MUST write free diagnosis follow-up copy for founders only and MUST avoid foreign developer positioning in this flow.

#### Scenario: Founder-focused follow-up email is generated
- **WHEN** a free diagnosis submission triggers follow-up email generation
- **THEN** the email MUST describe results in founder-friendly terms
- **AND** the email MUST avoid foreign-developer support language
- **AND** the email MUST present one clear business execution next step

### Requirement: Sender display name MUST be branded as 큐룸

The follow-up email sender display name MUST be configured and delivered as `큐룸`.

#### Scenario: Follow-up email is sent to user
- **WHEN** a diagnosis follow-up email is delivered
- **THEN** the sender display name MUST appear as `큐룸`
- **AND** the sender address MUST remain `help@quroom.kr`
