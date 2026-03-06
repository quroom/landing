## Why

현재 워크스페이스에는 Python 코드와 Django 템플릿의 포맷 기준이 명시적으로 고정되어 있지 않아, 저장 시점/개발자 환경에 따라 스타일이 흔들리고 템플릿 문법이 깨지는 문제가 반복됩니다. `ruff + djlint`를 기준 도구로 표준화해 동일한 결과를 재현 가능한 개발 환경을 만드는 것이 필요합니다.

## What Changes

- Python 포맷/정렬 기준을 `ruff` 단일 도구(`format`, `check --fix`)로 통합합니다.
- Django 템플릿 포맷 기준을 `djlint`로 고정하고, HTML 기본 포맷터와 충돌하지 않도록 워크스페이스 설정을 정리합니다.
- 로컬/CI에서 같은 기준으로 실행할 수 있도록 포맷 명령과 검증 동선(문서/스크립트)을 표준화합니다.
- 템플릿 포맷 회귀(템플릿 변수 깨짐/줄바꿈 충돌)를 방지하기 위한 최소 검증 규칙을 추가합니다.

## Capabilities

### New Capabilities
- `workspace-format-standardization`: ruff + djlint 기반의 저장/검증/CI 포맷 기준을 워크스페이스 단위로 일관되게 적용하는 기능

### Modified Capabilities
- `developer-navigation-and-runbook`: 개발자 실행 가이드에 포맷 표준 절차를 반영

## Impact

- Affected code/config:
  - `.vscode/settings.json` (존재 시), `.editorconfig` (존재 시)
  - `pyproject.toml`(또는 동등 설정 파일), `.djlintrc`, `.prettierignore`(필요 시)
  - `scripts/verify.sh` 또는 포맷 전용 스크립트
  - 관련 문서(`README.md`, `codex-document/*`)
- Development workflow:
  - 저장 시 포맷 도구 충돌 감소
  - 로컬/CI 포맷 결과 일치
