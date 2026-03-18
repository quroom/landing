## MODIFIED Requirements

### Requirement: 실무 연계 지원은 foreign-developer 페이지에 한정되어야 한다
시스템은 practical work-in-Korea 지원을 `/for-foreign-developers/`와 승인된 alias에서만 MUST 제공해야 하며, 해당 페이지를 국제 인재용 entry page로 framing하되 현재 가장 강한 지원 대상이 foreign software engineers임을 MUST 명시해야 한다.

#### Scenario: 실무 연계 콘텐츠 범위가 foreign-developer 페이지에만 머문다
- **WHEN** 사용자가 `/`와 `/for-foreign-developers/`를 비교하면
- **THEN** 한국에서 일하기 위한 실무 지원 상세는 `/for-foreign-developers/`에서만 보여야 한다
- **AND** foreign-developer 페이지는 국제 인재 진입 framing을 사용하되 현재 foreign software engineer 중심 초점을 함께 보여야 한다
- **AND** 페이지는 회사 소개 연결 메시지보다 먼저 career strategy, resume/portfolio readiness, Korea guidance를 보여줘야 한다

### Requirement: foreign-developer 페이지는 지원 범위를 명확히 밝혀야 한다
시스템은 Korea guidance가 직접적인 비자·법률 대행이 아니라 실무 적응 가이드와 파트너 연결이라는 점을 MUST 밝혀야 하며, 취업 보장이 없고 회사 소개는 프로필 적합도 검토 이후에만 진행된다는 점도 MUST 밝혀야 한다.

#### Scenario: 경계 문구가 명확히 보인다
- **WHEN** 사용자가 foreign-developer FAQ 또는 서비스 범위를 읽으면
- **THEN** 직접적인 비자 또는 법률 대행이 out-of-scope임을 확인할 수 있어야 한다
- **AND** 취업 비보장 정책이 명시적으로 보여야 한다
- **AND** 소개 전 프로필 적합도 검토가 필요하다는 점이 명시적으로 보여야 한다
- **AND** Korea guidance는 직접 자격 서비스를 뜻하지 않고 practical guidance 또는 partner referral로 설명되어야 한다
