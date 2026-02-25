## Context

현재 저장소는 루트에 실행 코드, 정적 자산, 문서, 운영 산출물이 함께 위치한다. 이 상태는 변경 시 영향 범위 파악과 코드 리뷰 범위를 넓히고, 신규 기여자가 구조를 이해하는 데 시간을 증가시킨다. 이번 변경은 기능 추가가 아니라 구조 개선이며, 런타임 동작을 깨지 않는 경로 마이그레이션이 핵심이다.

## Goals / Non-Goals

**Goals:**
- `landing/` 단일 코드 루트를 도입해 프로젝트 코드 탐색 경로를 단순화한다.
- Django 런타임 경로(import, template, static, settings)를 구조 변경 후에도 안정적으로 유지한다.
- README와 실행 가이드를 새 구조 기준으로 갱신한다.

**Non-Goals:**
- 비즈니스 로직 변경
- UI/카피 변경
- 신규 인프라 도입(예: Docker화, CI 신규 구축)

## Decisions

### Decision 1: Incremental move with compatibility checks
- 구조 변경을 한 번에 대규모로 하지 않고, 경로 그룹 단위(코드 → 템플릿/자산 → 문서)로 이동한다.
- 각 단계마다 compile/run 확인을 수행해 문제 지점을 즉시 좁힌다.
- 대안: 일괄 이동 후 일괄 수정은 빠르지만 실패 시 디버깅 비용이 크다.

### Decision 2: Consolidate code under landing/
- `quroom_landing/`, `templates/`, `static/`의 코드성 파일을 `landing/` 하위로 이동해 코드 루트를 하나로 고정한다.
- 엔트리포인트(`manage.py`)는 유지하되, 내부 모듈 참조는 `landing/` 기준으로 통일한다.
- 대안: 기존 분리 구조 유지 시 즉시 변경은 적지만 탐색 복잡도 개선 효과가 낮다.

### Decision 3: Document-first navigation rules
- 폴더 역할 규칙을 README에 명시하고, OpenSpec 문서 위치와 관계를 함께 정의한다.
- 코드 변경만 하고 문서를 미루면 이후 재혼란이 발생하므로 같은 change에서 동시 처리한다.

## Risks / Trade-offs

- [Risk] 경로 이동 중 import 누락 → Mitigation: 단계별 compile/run 검증, 변경 파일 목록 점검
- [Risk] 템플릿/정적 참조 깨짐 → Mitigation: 핵심 페이지 렌더와 static URL 확인
- [Risk] 문서와 실제 구조 불일치 → Mitigation: README와 OpenSpec 관련 문서를 같은 PR 범위에서 업데이트
- [Trade-off] 단기적으로 diff 규모 증가 → 장기적으로 탐색성과 유지보수성 개선

## Migration Plan

1. 목표 구조를 정의하고 현재 파일을 역할별로 매핑한다.
2. `quroom_landing/`, `templates/`, `static/` 관련 코드를 `landing/` 하위로 이동한다.
3. Python import/settings 경로를 `landing/` 기준으로 갱신한다.
3. 템플릿/정적/이미지 경로를 새 구조 기준으로 갱신한다.
4. README 및 운영 문서를 새 구조에 맞게 갱신한다.
5. `python3 -m compileall` 및 핵심 페이지 라우팅 검증을 수행한다.
6. 문제 시 마지막 안정 커밋 기준으로 경로 이동 단계만 롤백한다.

## Open Questions

- `_portfolio_code/`의 보존 위치(archive/docs/examples 중 어디로 둘지) 결정 필요
- `manage.py`를 루트 유지할지, `landing/manage.py`로 이동할지 최종 결정 필요
