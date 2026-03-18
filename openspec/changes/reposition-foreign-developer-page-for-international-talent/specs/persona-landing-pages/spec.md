## MODIFIED Requirements

### Requirement: 페르소나 전용 랜딩은 독립적으로 접근 가능해야 한다
시스템은 founders와 foreign developers를 위한 전용 랜딩을 SHALL 제공해야 하며, foreign-developer 여정은 기존 경로와 승인된 share-friendly alias 양쪽에서 독립적으로 접근 가능해야 한다.

#### Scenario: founder 랜딩 경로가 정상 동작한다
- **WHEN** 사용자가 `/for-founders/`를 요청하면
- **THEN** 시스템은 founder 중심 랜딩 페이지를 반환해야 한다
- **AND** 페이지는 founder 전용 CTA와 AX 서비스 framing을 포함해야 한다

#### Scenario: foreign-developer 기본 경로가 정상 동작한다
- **WHEN** 사용자가 `/for-foreign-developers/`를 요청하면
- **THEN** 시스템은 foreign-developer 랜딩 페이지를 반환해야 한다
- **AND** 페이지는 한국에서 일하기 위한 실무 지원 CTA와 지원 범위 경계 문구를 포함해야 한다

#### Scenario: foreign-developer 공유용 alias가 정상 동작한다
- **WHEN** 사용자가 `/it/`를 요청하면
- **THEN** 시스템은 같은 foreign-developer 랜딩 여정으로 연결해야 한다
- **AND** 해당 페이지는 `/`에 내용을 섞지 않고 persona 전용 범위를 유지해야 한다
