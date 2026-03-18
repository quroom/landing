## MODIFIED Requirements

### Requirement: foreign-developer 랜딩은 2단계 talent-pool intake를 제공해야 한다
시스템은 `/for-foreign-developers/`와 승인된 share alias에서 2단계 talent-pool intake를 MUST 제공해야 하며, 1단계는 가벼운 quick intake, 2단계는 qualified foreign software engineer lead를 위한 matching profile completion으로 구성되어야 한다.

#### Scenario: 첫 방문자는 전체 서류 없이 quick intake를 제출할 수 있다
- **WHEN** 첫 방문자가 `/for-foreign-developers/`에서 시작하려고 하면
- **THEN** 시스템은 quick intake에 `nickname`, `email`, 초기 role 또는 fit signal만 요구해야 한다
- **AND** 시스템은 추가 맥락을 위한 optional free-text note 필드를 제공해야 한다
- **AND** 이 단계에서는 CV, portfolio, visa 정보를 요구하면 안 된다

#### Scenario: quick intake는 더 넓은 유입을 분기할 수 있다
- **WHEN** 방문자가 1단계 intake를 사용하지만 현재 foreign software engineer matching path에 명확히 맞지 않으면
- **THEN** 시스템은 그 사례를 matching-ready software engineer lead와 구분할 수 있을 정도의 fit context를 수집해야 한다
- **AND** 시스템은 곧바로 2단계 matching 필드를 강제하는 대신 community 참여 또는 manual follow-up 같은 더 가벼운 다음 단계를 제시해야 한다

#### Scenario: 적합한 방문자는 matching profile을 완성할 수 있다
- **WHEN** 방문자가 foreign software engineer path에 적합하고 2단계 intake로 진행하면
- **THEN** 시스템은 `cv_or_linkedin`, `github_or_portfolio`, `tech_stack`, `experience_level`, `visa_status`, `work_preference`, `location_preference`, `available_from` 필드를 수집해야 한다
- **AND** 시스템은 2단계 제출을 동일한 candidate record 또는 lifecycle에 연결해야 한다

### Requirement: talent-pool funnel은 단계별 analytics 이벤트를 기록해야 한다
시스템은 foreign-developer funnel의 주요 단계마다 analytics event를 MUST 기록해야 하며, 더 넓은 international-talent 유입자의 qualification context도 MUST 보존해야 한다.

#### Scenario: 단계별 이벤트가 추적된다
- **WHEN** 사용자가 quick intake를 제출하거나, matching profile을 완료하거나, introduction workflow에 진입하면
- **THEN** 시스템은 단계별로 구분된 이벤트를 기록해야 한다
- **AND** 각 이벤트에는 funnel reporting에 필요한 page 및 lead-source context가 포함되어야 한다
- **AND** quick-intake analytics에는 방문자가 foreign software engineer path에 맞는지, 아니면 lighter community/referral path인지 구분 정보가 남아야 한다
