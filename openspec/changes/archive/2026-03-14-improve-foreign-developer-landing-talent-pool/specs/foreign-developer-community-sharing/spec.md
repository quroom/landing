# Capability: foreign-developer-community-sharing

## ADDED Requirements

### Requirement: Foreign-developer landing MUST provide community-sharing participation path
The system MUST provide an explicit participation path for foreign developers to join a community waitlist for job-search and settlement information sharing.

#### Scenario: User sees community participation path
- **WHEN** a user reviews `/for-foreign-developers/`
- **THEN** the page includes a community-sharing section with waitlist CTA
- **AND** the section explains the scope of shared information (job search, interview, settlement adaptation)
- **AND** the section states that the live community channel opens after operational threshold is reached

### Requirement: Community-sharing messaging MUST define moderation and scope boundaries
The system MUST state that community information is peer-sharing support and not legal/visa agency advice.

#### Scenario: Community boundary statement is visible
- **WHEN** a user is about to join or request community participation
- **THEN** the system displays scope and moderation boundary text
- **AND** the boundary text includes referral guidance for visa/legal matters

### Requirement: Community channel launch threshold MUST be disclosed
The system MUST disclose that community channel launch depends on an operational threshold and MUST define the threshold criteria in policy copy.

#### Scenario: User checks when channel opens
- **WHEN** a user reads community waitlist policy
- **THEN** the policy states channel launch criteria (active candidate count, recurring question volume, and operator moderation capacity)
