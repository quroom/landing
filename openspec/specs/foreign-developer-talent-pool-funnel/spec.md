# Capability: foreign-developer-talent-pool-funnel

## Purpose
외국인 개발자 랜딩을 단계형 인재풀 유입 퍼널로 운영하기 위한 기준을 정의한다.

## ADDED Requirements

### Requirement: Foreign-developer landing MUST provide two-step talent-pool intake
The system MUST provide two-step talent-pool intake on `/for-foreign-developers/`, consisting of quick intake first and matching profile completion second.

#### Scenario: First-time visitor can submit quick intake without full dossier
- **WHEN** a first-time visitor decides to start on `/for-foreign-developers/`
- **THEN** the system requires only minimal fields for quick intake (`nickname`, `email`, `target_role`)
- **AND** the system provides an optional free-text note field for additional context
- **AND** the system does not require CV, portfolio, or visa details at this stage

#### Scenario: Returning or engaged visitor can complete matching profile
- **WHEN** a visitor proceeds to second-stage intake
- **THEN** the system collects matching-oriented required fields (`cv_or_linkedin`, `github_or_portfolio`, `tech_stack`, `experience_level`, `visa_status`, `work_preference`, `location_preference`, `available_from`)
- **AND** the system associates second-stage submission with the same candidate record or lifecycle

### Requirement: Talent-pool funnel MUST emit stage-specific analytics events
The system MUST emit analytics events for each major foreign-developer funnel stage.

#### Scenario: Stage events are tracked
- **WHEN** a user submits quick intake, completes matching profile, or enters introduction workflow
- **THEN** the system records distinct events per stage
- **AND** each event includes page and lead-source context needed for funnel reporting
