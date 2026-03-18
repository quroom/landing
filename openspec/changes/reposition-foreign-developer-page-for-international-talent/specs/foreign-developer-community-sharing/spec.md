## MODIFIED Requirements

### Requirement: foreign-developer 랜딩은 community 참여 경로를 제공해야 한다
시스템은 foreign software engineers와 인접 international-talent 방문자가 work-in-Korea, job-search, settlement 정보 공유를 위한 community waitlist에 참여할 수 있는 명시적 경로를 MUST 제공해야 하며, 현재 운영 초점도 MUST 설명해야 한다.

#### Scenario: 사용자가 community 참여 경로를 확인한다
- **WHEN** 사용자가 `/for-foreign-developers/`를 살펴보면
- **THEN** 페이지는 community-sharing 섹션 또는 waitlist opt-in 경로를 포함해야 한다
- **AND** 해당 경로는 공유 정보 범위가 work in Korea, job search, interview, settlement adaptation임을 설명해야 한다
- **AND** 현재 운영 초점이 foreign software engineers에 가장 강하게 맞춰져 있음을 설명해야 한다
- **AND** live community 채널은 운영 임계치가 충족된 뒤 열린다는 점을 밝혀야 한다

### Requirement: community 메시지는 운영 및 범위 경계를 정의해야 한다
시스템은 community 정보가 peer-sharing support이며 법률 또는 비자 대행 조언이 아니고, 전문적 취업 보장을 의미하지 않으며, 초기 운영은 foreign software engineer 지원 초점을 중심으로 moderation된다는 점을 MUST 밝혀야 한다.

#### Scenario: community 경계 문구가 보인다
- **WHEN** 사용자가 community 참여를 시도하거나 요청하려고 하면
- **THEN** 시스템은 범위와 moderation 경계 문구를 보여줘야 한다
- **AND** 해당 문구는 비자 또는 법률 이슈에 대한 referral guidance를 포함해야 한다
- **AND** community 참여가 matching 또는 취업 보장을 뜻하지 않는다는 점을 밝혀야 한다
