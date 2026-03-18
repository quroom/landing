## ADDED Requirements

### Requirement: 외국인 개발자 랜딩은 공유용 alias 경로를 제공해야 한다
시스템은 `/it/`를 인쇄물과 오프라인 공유에 쓰는 foreign-developer 랜딩의 share-friendly alias로 MUST 제공해야 한다.

#### Scenario: 명함용 URL이 의도한 랜딩 경험으로 연결된다
- **WHEN** 사용자가 `/it/`를 요청하면
- **THEN** 시스템은 foreign-developer 랜딩 경험으로 서빙하거나 redirect해야 한다
- **AND** 사용자는 기존 foreign-developer 페이지와 같은 persona 전용 콘텐츠와 CTA 흐름에 도달해야 한다

### Requirement: 공유용 alias 처리는 요청 context를 보존해야 한다
시스템은 `/it/` alias를 처리할 때 query-string과 locale context를 MUST 보존해야 한다.

#### Scenario: alias 요청이 context를 잃지 않는다
- **WHEN** 사용자가 query parameter 또는 locale override와 함께 `/it/`를 요청하면
- **THEN** 최종 foreign-developer 랜딩은 해당 context를 rendering과 funnel tracking에 계속 사용할 수 있어야 한다
- **AND** alias 처리 과정에서 campaign, locale, lead-source 정보가 누락되면 안 된다
