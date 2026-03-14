# Capability: contact-inquiry-persistence

## ADDED Requirements

### Requirement: Foreign-developer inquiry data MUST persist staged funnel state
The system MUST persist staged funnel state for foreign-developer inquiries so operators can distinguish quick-intake records from matching-ready profile records.

#### Scenario: Quick intake is stored with initial stage
- **WHEN** a user submits the first-stage foreign-developer quick intake
- **THEN** a contact inquiry record is persisted with stage state set to initial intake
- **AND** required stage-one fields (`nickname`, `email`, `target_role`) are stored with creation timestamp
- **AND** optional stage-one note content is stored when provided

#### Scenario: Matching profile completion updates stage state
- **WHEN** a user completes second-stage matching profile submission
- **THEN** the persisted inquiry data is updated or linked with required matching-profile fields (`cv_or_linkedin`, `github_or_portfolio`, `tech_stack`, `experience_level`, `visa_status`, `work_preference`, `location_preference`, `available_from`)
- **AND** stage state is updated to `matching_pending`

### Requirement: Inquiry lifecycle MUST support operational progression tracking
The system MUST persist lifecycle states for foreign-developer inquiries covering at least new, strategy-in-progress, matching-pending, introduction-in-progress, and closed.

#### Scenario: Operator updates lifecycle state
- **WHEN** an operator advances an inquiry through follow-up workflow
- **THEN** the inquiry lifecycle state change is persisted
- **AND** the current lifecycle state is queryable for dashboard/reporting use
