## ADDED Requirements

### Requirement: 외국인 개발자 랜딩은 국제 인재 진입 메시지를 사용해야 한다
시스템은 `/for-foreign-developers/`를 국제 인재를 위한 `한국에서 일하기 위한 실무 지원` 진입 페이지로 MUST 제시해야 하며, 현재 가장 강한 지원 대상이 foreign software engineers임을 MUST 명시해야 한다.

#### Scenario: 히어로가 명함 메시지와 현재 초점을 함께 보여준다
- **WHEN** 사용자가 `/for-foreign-developers/`에 진입하면
- **THEN** 히어로는 `Work in Korea with practical support`와 정렬되는 국제 인재용 진입 메시지를 보여줘야 한다
- **AND** 페이지는 현재 핵심 지원 초점이 foreign software engineers임을 명확히 전달해야 한다

### Requirement: 진입 지원 축은 명함 약속과 직접 연결되어야 한다
시스템은 명함의 `career strategy`, `resume/portfolio readiness`, `Korea guidance` 약속과 직접 대응되는 지원 축을 MUST 제시해야 한다.

#### Scenario: 방문자가 명함과 랜딩의 연결을 바로 이해한다
- **WHEN** 사용자가 `/for-foreign-developers/`의 히어로 또는 첫 서비스 섹션을 확인하면
- **THEN** 페이지는 career strategy, resume/portfolio readiness, Korea guidance에 해당하는 지원 축을 보여줘야 한다
- **AND** 해당 카피는 QuRoom의 현재 실무 지원 범위 안에서 표현되어야 하며, 범용 국제 인재 에이전시처럼 보이면 안 된다
