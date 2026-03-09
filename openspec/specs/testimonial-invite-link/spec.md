# Capability: testimonial-invite-link

## Purpose
후기 요청 링크를 토큰 기반으로 안전하게 발급/검증하고 1회성 운영 정책을 보장한다.

## Requirements

### Requirement: Invite links SHALL be tokenized with expiration
The system SHALL issue invite links with unique tokens and SHALL assign an expiration timestamp at issuance time.

#### Scenario: Invite link issuance sets token and expiry
- **WHEN** an operator issues a testimonial invite link
- **THEN** the system stores a unique token
- **AND** the system stores an expiration timestamp based on configured validity window

### Requirement: Invite links SHALL be single-use by default
The system SHALL treat invite links as single-use by default and SHALL mark the link as consumed after a successful testimonial submission.

#### Scenario: Successful submission consumes invite link
- **WHEN** a testimonial is submitted successfully with a valid invite token
- **THEN** the system marks the token as consumed
- **AND** subsequent submission attempts with the same token are rejected

### Requirement: Expired or consumed tokens SHALL be rejected
The system SHALL reject invite links when token status is expired or consumed.

#### Scenario: Expired token cannot open submission form
- **WHEN** a user accesses testimonial submission with an expired token
- **THEN** the system denies access
- **AND** the response indicates the invite has expired

#### Scenario: Consumed token cannot be reused
- **WHEN** a user accesses testimonial submission with a consumed token
- **THEN** the system denies access
- **AND** the response indicates the invite has already been used

### Requirement: Operators SHALL be able to reissue invite links
The system SHALL allow operators to issue a new invite token for the same 상담 건 when previous token is expired or consumed.

#### Scenario: Reissue generates a new active token
- **WHEN** an operator requests reissue for a testimonial invite
- **THEN** the system creates a new token with fresh expiration
- **AND** the old token remains invalid
