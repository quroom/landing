## Why

메인 랜딩은 Hero와 CTA 방향은 많이 정리됐지만, 섹션별 톤과 역할이 아직 완전히 일치하지 않는다. 일부 구간은 실무형 카피, 일부는 정책 문장, 일부는 패키지 소개형 문장으로 남아 있어 전체 신뢰 흐름과 전환 논리가 약해진다.

## What Changes

- 메인 홈페이지(`/`)의 핵심 카피를 `맡길 수 있는 파트너` 관점으로 재정렬한다.
- Hero, About, Services, Contact 문장을 실무형 톤으로 통일하고, 과하게 설명적이거나 정책성인 문구를 제거한다.
- 신뢰 근거는 Hero 신뢰 카드처럼 자연스러운 증빙 단서로 유지하고, 방문자용 가치가 낮은 별도 `trust-policy` 섹션은 제거하거나 흡수한다.
- 서비스 카드 문장은 `무엇을 하느냐`보다 `언제 맡기면 되는가`가 드러나도록 정리한다.
- founder 관련 서브 카피와 메인 홈 카피를 같은 언어 레벨로 맞춰 페이지 간 일관성을 높인다.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `founder-first-homepage-positioning`: 메인 홈페이지 카피가 `믿고 맡길 수 있는 파트너` 포지셔닝과 자연스러운 신뢰 흐름을 유지하도록 요구사항을 강화한다.
- `homepage-copy-tone-guidelines`: 브로슈어형, 정책형, 컨설팅형 문장을 줄이고 실무형 문장으로 통일하는 기준을 추가한다.
- `service-content-completeness`: 서비스 카드가 founder의 구매 판단 기준에 맞는 요약과 적용 상황을 보여주도록 요구사항을 강화한다.
- `evidence-link-governance`: 검증 가능한 신뢰 근거는 유지하되, 내부 운영 정책을 방문자용 별도 섹션으로 노출하지 않도록 요구사항을 보완한다.
- `founder-ax-service-offer`: founder 서비스 카피가 실제 맡길 수 있는 범위와 실행 기준을 더 직접적으로 드러내도록 조정한다.

## Impact

- Affected code: `landing/content.py`, `landing/templates/landing/index.html`, founder-related tests
- Affected systems: homepage copy rendering, service card wording, trust section rendering
- No new dependency or data model changes are expected
