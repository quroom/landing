## Why

메인 랜딩의 구조와 서비스 구성은 이미 정리되어 있지만, 카피는 아직 소개서 톤과 번역투가 남아 있습니다. 지금 단계에서는 메시지 구조를 다시 바꾸기보다, 창업자가 읽었을 때 더 실무적이고 신뢰감 있게 느껴지도록 문장 어조를 정리할 필요가 있습니다.

## What Changes

- 메인 홈페이지(`/`)의 창업자 대상 카피를 과장 없는 실무형 어조로 정리합니다.
- Hero, About, Fit intro, Services intro/cards, Contact 문구를 사용자 고유 톤에 맞게 짧고 판단 가능한 문장으로 다듬습니다.
- 기존 CTA 구조, 서비스 구성, 섹션 순서는 유지하고, 의미를 바꾸지 않는 범위에서 표현만 조정합니다.
- 내부 용어, 소개서형 문장, 과한 약속 표현을 줄이고 범위·우선순위·실행 기준이 보이는 문장으로 통일합니다.

## Capabilities

### New Capabilities
- `homepage-copy-tone-guidelines`: 창업자 홈 카피에 적용할 실무형 어조, 문장 길이, 표현 경계 기준을 정의

### Modified Capabilities
- `founder-first-homepage-positioning`: Hero, About, Contact 카피가 founder-first 구조를 유지하면서도 실무형 톤을 따르도록 변경
- `founder-ax-service-offer`: 창업자 서비스 카드 설명을 툴/방법론 소개보다 founder 상황과 실행 판단 중심 문장으로 변경
- `service-content-completeness`: 서비스 카드 카피가 필수 필드를 유지하면서도 과장 없는 전달 문장을 사용하도록 변경

## Impact

- Affected code: `landing/content.py`, `landing/templates/landing/index.html`
- Affected specs: founder homepage and service copy related main specs
- Affected tests: homepage content assertions in `landing/tests/test_landing_pages.py`
