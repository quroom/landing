## Why

현재 프로젝트의 실행 코드, 문서, 이미지, 임시/운영 파일이 루트에 혼재되어 있어 탐색 비용이 높고 변경 영향 범위를 빠르게 파악하기 어렵습니다. 폴더 구조를 역할별로 정리해 유지보수성, 온보딩 속도, 변경 안전성을 높일 필요가 있습니다.

## What Changes

- 루트 중심 배치를 기능/역할 중심 구조로 재정렬한다 (앱 코드, 문서, 자산, 환경 파일).
- Django 프로젝트 코드는 `landing/` 단일 코드 루트로 통합한다.
- 기존 `quroom_landing/`, `templates/`, `static/`의 코드성/프론트 자산 파일은 `landing/` 하위로 이동한다.
- 문서 경로를 `docs/`와 `openspec/` 역할로 명확히 분리하고 README 진입점을 정리한다.
- 정적/이미지 자산 경로를 일관화하고 템플릿/정적 참조를 갱신한다.
- 개발 실행 절차(로컬 실행, 검증, 배포 준비)를 새 구조 기준으로 업데이트한다.
- **BREAKING**: 기존 하드코딩된 상대경로(예: 루트 기준 import, 파일 참조)가 있으면 동작이 변경될 수 있다.

## Capabilities

### New Capabilities
- `single-landing-code-root`: 프로젝트 코드를 `landing/` 단일 루트로 통합해 코드 탐색 경로를 단순화한다.
- `django-path-stability-after-move`: 코드 이동 이후에도 Django 실행/라우팅/템플릿/정적 자산 경로가 안정적으로 동작하도록 보장한다.
- `developer-navigation-and-runbook`: 새로운 구조 기준으로 탐색/실행/검증 방법을 문서화해 팀 생산성을 유지한다.

### Modified Capabilities
- None.

## Impact

- 애플리케이션 경로: `landing/`, `manage.py`, `images/` (기존 `quroom_landing/`, `templates/`, `static/` 이동 대상)
- 문서 경로: `README.md`, `codex-document/README.md`, `openspec/changes/.../docs/*`
- 설정/실행: `requirements.txt`, Django settings 내 BASE_DIR/STATICFILES 관련 경로
- 검증: `python3 -m compileall`, Django runserver, 주요 URL 라우팅 확인
