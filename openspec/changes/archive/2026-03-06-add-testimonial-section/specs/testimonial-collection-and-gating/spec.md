## ADDED Requirements

### Requirement: System SHALL provide invite-only testimonial submission
The system SHALL provide a testimonial submission page that is accessible only through a valid invite link token and SHALL not expose this page from public navigation.

#### Scenario: Valid invite token opens testimonial form
- **WHEN** a user opens the testimonial submission URL with a valid token
- **THEN** the system displays the testimonial form
- **AND** the form requires testimonial content and consent fields defined for publication review

#### Scenario: Missing or invalid token is blocked
- **WHEN** a user opens the testimonial submission URL without a valid token
- **THEN** the system denies access to the form
- **AND** the system shows guidance to contact the 상담 담당자 for a new invite

### Requirement: Submitted testimonials SHALL be stored as pending review by default
The system SHALL store every submitted testimonial with a default moderation status of `pending` and SHALL keep it non-public until an operator approves it.

#### Scenario: Submission creates pending testimonial
- **WHEN** a user submits a testimonial through a valid invite link
- **THEN** the system stores the testimonial with status `pending`
- **AND** the testimonial is not included in public testimonial output

### Requirement: Public testimonial section SHALL be gated by approved-count threshold
The system SHALL keep the public testimonial section hidden until the number of approved testimonials reaches the configured threshold value, with default threshold `3`.

#### Scenario: Approved count below threshold keeps section hidden
- **WHEN** the public homepage is rendered and approved testimonial count is lower than threshold
- **THEN** the testimonial section is not shown

#### Scenario: Approved count at threshold shows section
- **WHEN** the public homepage is rendered and approved testimonial count is equal to or greater than threshold
- **THEN** the testimonial section is shown using only approved testimonials
