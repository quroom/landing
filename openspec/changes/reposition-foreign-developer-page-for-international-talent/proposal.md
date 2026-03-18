## Why

현재 `/for-foreign-developers/` 페이지는 외국인 개발자 취업 전략 페이지로 읽히지만, 준비 중인 명함은 QuRoom을 `For international talent`, `Especially foreign software engineers`, `Work in Korea with practical support`로 더 넓게 소개합니다. 이 차이 때문에 QR로 유입된 사람이 명함에서 기대한 메시지와 랜딩에서 받는 첫인상이 어긋나고, 오프라인 네트워킹에서 만나는 비개발자 외국인 인재도 초반에 이탈할 가능성이 있습니다.

## What Changes

- 외국인 개발자 랜딩을 더 넓은 `international talent` 진입 페이지로 재포지셔닝하되, 현재 가장 강한 지원 대상은 `foreign software engineers`임을 명시한다.
- 히어로와 서비스 구성을 명함 문구와 맞춘다: `Work in Korea with practical support`, `Career strategy`, `Resume / portfolio`, `Korea guide`.
- 인쇄물과 오프라인 공유용으로 `/it/` 경로 alias를 추가하되, 기존 `/for-foreign-developers/` 페이지의 운영 주체와 의미는 유지한다.
- 개발자가 아닌 국제 인재가 유입되더라도 현재 지원 범위와 적합도를 이해할 수 있도록 community/intake 진입 카피를 조정한다.
- 기존 경계는 유지한다: 취업 보장 없음, 비자·법률 직접 대행 없음, 소개는 프로필 적합도 검토 이후에만 진행.

## Capabilities

### New Capabilities
- `international-talent-entry-framing`: 명함과 맞는 진입 메시지를 정의해, 더 넓은 국제 인재를 받으면서도 현재 핵심 지원 대상이 외국인 소프트웨어 엔지니어임을 분명히 한다.
- `share-link-routing`: 인쇄물/오프라인 공유용 짧고 직관적인 alias 라우팅과 canonical 처리 기준을 정의한다.

### Modified Capabilities
- `persona-landing-pages`: 외국인 개발자 랜딩이 기존 canonical 경로와 share-friendly alias 양쪽에서 열리도록 요구사항을 조정하되, 홈페이지와의 페르소나 경계는 유지한다.
- `foreign-developer-practical-linkage`: 단계형 취업 준비 중심 메시지를 `한국에서 일하기 위한 실무 지원`이라는 더 상위 표현으로 넓히되, 현재 경계 조건은 유지한다.
- `foreign-developer-community-sharing`: 개발자가 아닌 인접 국제 인재도 커뮤니티 참여 범위와 현재 운영 초점을 이해할 수 있도록 메시지를 조정한다.
- `foreign-developer-talent-pool-funnel`: 1차 intake에서 더 넓은 국제 인재 유입을 받을 수 있게 하되, 외국인 소프트웨어 엔지니어 지원 경로와 lighter community/referral 경로를 구분할 수 있도록 요구사항을 보완한다.

## Impact

- Affected code: `landing/urls.py`, `landing/views.py`, `landing/content.py`, `landing/templates/landing/foreign_developers.html`, 외국인 개발자 관련 form/test
- Affected systems: 명함 QR 및 공유 URL 라우팅, 외국인 개발자 랜딩 카피, intake 적합도 분기, community 진입 메시지, foreign-developer funnel analytics
- 새로운 외부 의존성 추가는 예상하지 않는다
