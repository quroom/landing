## Why

현재 메인 랜딩은 창업자 우선 페이지여야 하지만 Hero 카피와 CTA 우선순위가 완전히 정리되지 않아 전환 판단이 분산됩니다. 특히 `OpenClaw와 바이브코딩 기반 자동화 실행 서비스` 같은 표현은 창업자 관점에서 문제 해결/성과보다 도구와 방식이 먼저 보여 신뢰와 이해를 떨어뜨립니다.

## What Changes

- 메인 홈페이지의 핵심 메시지를 창업자의 실행 문제와 사업 성과 중심 언어로 재작성한다.
- `OpenClaw`와 `바이브코딩` 같은 내부/도구 중심 표현을 직접적인 창업자 가치 언어로 치환한다.
- 메인 Hero CTA를 `상담 문의하기` 중심으로 우선순위화하고, 보조 CTA는 시각적/행동적 비중을 낮춘다.
- 메인 페이지 Contact 구간에서도 CTA 설명을 단순화해 첫 행동을 분명히 한다.
- 외국인 개발자 페이지는 메인 페이지와 톤이 충돌하지 않도록 보조 페르소나 페이지로서의 역할 경계를 유지한다.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `founder-first-homepage-positioning`: 메인 Hero와 Contact CTA 우선순위를 창업자 상담 중심으로 강화한다.
- `founder-ax-service-offer`: 창업자 서비스 제안 문구를 도구/방법론 중심에서 문제 해결/성과 중심 표현으로 조정한다.
- `service-content-completeness`: 서비스 카드와 소개 문구에서 모호하거나 내부자 중심인 표현을 줄이고 결과 책임 범위를 더 명확히 한다.
- `persona-landing-pages`: 메인 페이지와 외국인 개발자 페이지의 톤 충돌을 줄이고 메인 페이지의 창업자 우선성을 유지한다.

## Impact

- Affected code:
  - `landing/content.py`
  - `landing/templates/landing/index.html`
  - `landing/templates/landing/foreign_developers.html`
  - related tests under `landing/tests/`
- Affected UX:
  - 메인 Hero 카피
  - 메인 Hero/Contact CTA hierarchy
  - 창업자 서비스 설명 문구
  - 메인 페이지와 외국인 페이지의 역할 분리 인상
