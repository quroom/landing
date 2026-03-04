## 1. Health and Admin Verification Routes

- [x] 1.1 `GET /healthz` 엔드포인트를 추가하고 경량 JSON `{"status":"ok"}` 응답 계약을 고정한다.
- [x] 1.2 `admin_operation_links` staff 전용 페이지를 추가하고 `/healthz`, `/admin-dashboard/`, 핵심 랜딩/제출 경로 one-click 링크를 노출한다.
- [x] 1.3 Django admin 상단 userlinks에 `운영 링크` 진입점을 `문의 대시보드` 옆에 추가한다.
- [x] 1.4 비관리자 접근 차단(redirect/permission policy) 테스트와 관리자 접근 렌더링 테스트를 추가한다.

## 2. Production Startup Validation

- [x] 2.1 `DEBUG=False` 기준 필수 환경변수(SECRET_KEY, DB, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS, SMTP 계약) 검증 로직을 settings 시작 경로에 추가한다.
- [x] 2.2 운영 모드에서 로컬 전용 이메일 backend가 선택되면 앱 시작을 실패시키는 가드를 추가한다.
- [x] 2.3 검증 실패 시 누락 키/설정 충돌을 식별 가능한 오류 메시지로 노출하도록 정리한다.
- [x] 2.4 운영 모드/개발 모드 분기 테스트(허용/차단 케이스)를 추가한다.

## 3. Pre-deploy Readiness Command

- [x] 3.1 배포 전 점검 관리 명령(`manage.py check_deploy_ready` 또는 동등 명령)을 추가한다.
- [x] 3.2 명령에서 DB 연결, SMTP 계약, 필수 환경변수, 정적파일 설정 계약을 검증한다.
- [x] 3.3 점검 실패 시 non-zero 종료코드와 actionable 출력 포맷을 고정한다.
- [x] 3.4 명령 성공/실패 테스트를 추가하고 CI에서 실행 가능하도록 스크립트 진입점(예: `scripts/deploy-check.sh`)을 정의한다.

## 4. Post-deploy Automation and Runbook

- [x] 4.1 post-deploy smoke check 스크립트에서 `/healthz`, `/admin-dashboard/`, 핵심 submit flow 점검 절차를 자동화한다.
- [x] 4.2 CI/CD(예: GitHub Actions) 단계에 pre-deploy/post-deploy 검증 단계를 추가해 배포 게이트로 연결한다.
- [x] 4.3 Railway 배포/롤백/운영 점검 문서(runbook)에 명령 순서(`migrate -> collectstatic -> start`)와 체크리스트를 업데이트한다.
- [x] 4.4 운영 링크 페이지, 헬스체크, 배포 자동 점검 흐름이 문서와 실제 라우트/스크립트와 일치하는지 최종 검증한다.
