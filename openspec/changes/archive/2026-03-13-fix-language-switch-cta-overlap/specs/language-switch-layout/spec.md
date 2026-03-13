## ADDED Requirements

### Requirement: Language Switch Must Not Obscure Header CTA

언어 전환 UI는 헤더 내 CTA(상담 문의하기)와 시각적으로 겹치거나 클릭 가능 영역을 가리지 **MUST** 한다.

#### Scenario: Desktop header with CTA

- **WHEN** 사용자가 데스크톱 화면에서 랜딩 페이지를 열면
- **THEN** 언어 전환 UI는 헤더 CTA와 겹치지 않는다
- **AND** CTA 버튼은 시각적으로 완전 노출되고 클릭 가능해야 한다

#### Scenario: Responsive width changes

- **WHEN** 뷰포트 폭이 넓은 구간에서 좁은 구간으로 바뀌거나 그 반대로 바뀌면
- **THEN** 언어 전환 UI는 CTA를 가리지 않도록 재배치된다
- **AND** 언어 전환 기능은 계속 동작해야 한다

### Requirement: Major Landing Variants Preserve CTA Visibility

공통 베이스 템플릿을 사용하는 주요 랜딩 페이지는 동일한 언어 전환 배치 규칙을 따르도록 **MUST** 구현되어야 한다.

#### Scenario: Shared base template pages

- **WHEN** 사용자가 index, foreign_developers, founders, free_diagnosis 페이지를 본다
- **THEN** 상단 CTA가 언어 전환 UI에 의해 가려지지 않는다
