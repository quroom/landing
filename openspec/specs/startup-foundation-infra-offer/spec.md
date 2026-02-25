# Capability: startup-foundation-infra-offer

## Purpose
창업 초기 필수 인프라 오퍼를 독립 서비스 파트로 정의해 전달한다.

## Requirements

### Requirement: Startup foundation infrastructure offer MUST be explicitly defined
The system MUST define startup foundation infrastructure as a first-class service group for early-stage business setup.

#### Scenario: Foundation offer appears as dedicated group
- **WHEN** a user reviews founder service groups
- **THEN** startup foundation infrastructure appears as its own group, not as a generic optional addon

### Requirement: Business mail setup MUST define Daum Smartwork scope
The system MUST state that business mail setup includes domain purchase, domain connection, and DNS record configuration under a Daum Smartwork-based setup flow.

#### Scenario: Business mail scope is clear
- **WHEN** a user reads the business mail offer card
- **THEN** the scope includes domain purchase, domain connection, and DNS record configuration
- **AND** the scope text references Daum Smartwork as the baseline setup path
