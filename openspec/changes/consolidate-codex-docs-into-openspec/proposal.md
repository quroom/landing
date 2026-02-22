## Why

현재 랜딩/바이브코딩 관련 문서들이 `codex-document/`에 흩어져 있어 OpenSpec 흐름과 분리되어 있습니다. 문서가 분산되어 있으면 온보딩과 변경 추적이 어려워집니다. OpenSpec 안으로 통합해 단일 진입점과 변경 이력을 갖추려 합니다.

## What Changes

- 기존 문서(`codex-document/*.md`: 랜딩 명세, 바이브코딩 가이드/프롬프트 등)를 OpenSpec 변경 폴더로 이동/정리하고 원본 위치는 아카이브 또는 포인터로 대체
- 통합된 문서를 OpenSpec 체계(변경/아카이브) 하에 관리할 구조 제안
- README/관련 레퍼런스에 새로운 위치를 안내

## Capabilities

### New Capabilities
- `doc-consolidation`: 랜딩/바이브코딩 문서를 OpenSpec 내로 통합하고, 아카이브/포인터를 통해 단일 소스와 변경 추적 가능하게 함

### Modified Capabilities
- None

## Impact

- `codex-document/*.md` (이동/포인터 처리)
- `openspec/changes/consolidate-codex-docs-into-openspec/` (통합 문서 수용)
- `README.md` 또는 기타 안내 문서(새 위치 안내)
