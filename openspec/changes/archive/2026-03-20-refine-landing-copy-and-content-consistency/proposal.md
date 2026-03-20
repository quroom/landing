## Why

메인 랜딩은 전체 구조와 메시지 방향은 이미 충분히 정리되어 있다. 다만 몇몇 문장이 번역투로 읽히거나, 한국어 톤이 덜 자연스럽거나, 브랜드 표기처럼 불필요한 요소가 남아 있었다. 최근 반영은 실제로도 `전면 재작성`이 아니라 `미세 문구 정리`에 가까웠기 때문에, active change도 현재 코드 상태와 사용자 선호에 맞게 좁은 범위로 정리할 필요가 있다.

## What Changes

- 메인 홈페이지(`/`)의 founder 카피에서 어색한 표현만 미세 조정한다.
- `Official`처럼 불필요한 브랜드 보조 표기를 제거한다.
- `한 타임`, `조율`처럼 번역투 또는 덜 자연스러운 표현을 현재 톤을 유지한 채 더 읽기 쉬운 문장으로 바꾼다.
- 큰 메시지 구조나 섹션 역할은 유지하고, 문장 단위 polish와 테스트 동기화까지만 포함한다.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `founder-first-homepage-positioning`: 메인 홈페이지가 founder-first 포지셔닝을 유지하면서도 어색한 보조 문구를 줄이도록 정리한다.
- `homepage-copy-tone-guidelines`: 전면 카피 재작성 대신, 현재 톤을 유지한 미세 polish 기준으로 범위를 축소한다.

## Impact

- Affected code: `landing/content.py`, `landing/templates/landing/index.html`, founder-related tests
- Affected systems: homepage copy rendering
- No new dependency or data model changes are expected
