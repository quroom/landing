## Why

현재 Railway 배포 점검은 기본 골격은 갖춰졌지만, `/healthz/`의 신호 깊이와 smoke check 기준이 얕아 실제 장애를 배포 직후에 놓칠 가능성이 남아 있습니다. 운영자가 한 화면에서 점검 상태를 확인하기 어려워 수동 점검 누락 위험도 존재합니다.

## What Changes

- 배포 상태 확인을 `liveness`와 `readiness`로 분리해 헬스체크 신뢰도를 높입니다.
- post-deploy smoke check를 엔드포인트별 기대 상태코드 기준으로 강화해 오탐/미탐을 줄입니다.
- 운영 링크 페이지를 단순 URL 모음에서 "최근 점검 결과를 함께 보는 운영 점검 허브"로 확장합니다.
- 배포 직후 점검 자동화를 CI 단계에서 실행 가능하도록 정리하고, 실패 시 조치 기준(재시도/롤백)을 런북에 명확히 정의합니다.

## Capabilities

### New Capabilities
- `deployment-operational-status-hub`: 관리자 운영 링크 페이지에서 배포 점검 결과를 한 번에 확인할 수 있는 운영 가시성 기능

### Modified Capabilities
- `railway-deployment-readiness`: readiness/liveness 분리 및 배포 후 점검 자동화 기준 강화
- `admin-dashboard-navigation`: 관리자 상단/운영 링크 진입점에서 운영 점검 허브 접근성과 점검 동선 개선

## Impact

- Affected code:
  - `landing/views.py`, `landing/urls.py`
  - `landing/templates/landing/admin_operation_links.html`, `landing/templates/admin/base_site.html`
  - `landing/management/commands/check_deploy_ready.py`, `landing/deploy_validation.py`
  - `scripts/deploy-check.sh`, `scripts/post-deploy-smoke.sh`
  - `.github/workflows/deploy-readiness.yml`
  - `codex-document/railway-deploy-runbook.md`
- 운영 점검 프로세스와 CI 점검 기준이 함께 변경됩니다.
- 외부 API 계약 변경은 없고, 운영 엔드포인트/런북 기준이 강화됩니다.
