# Railway Deploy Runbook

## 1) Pre-deploy

1. 필수 환경변수 확인
- `DJANGO_DEBUG=0`
- `DJANGO_SECRET_KEY` (기본값 금지)
- `DJANGO_ALLOWED_HOSTS` (와일드카드 `*` 금지)
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `DJANGO_EMAIL_BACKEND`
- SMTP 사용 시: `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DJANGO_DEFAULT_FROM_EMAIL`

2. 사전 점검 실행
```bash
./scripts/deploy-check.sh
```

3. 기본 검증 실행
```bash
./scripts/verify.sh
```

## 2) Deploy Sequence

릴리즈 단계는 아래 순서를 유지:
1. `migrate`
2. `collectstatic`
3. app start

## 3) Post-deploy

1. 운영 점검 링크 사용
- `/admin-operation-links/` 접속
- `/healthz/` 요약 상태 확인 (`ok` 또는 `degraded`)
- `/healthz/live/` 200 확인 (프로세스 생존)
- `/healthz/ready/` 200 확인 (트래픽 수용 준비)
- `/admin-dashboard/` 접근 확인
- 핵심 submit 경로 동작 확인

2. 자동 smoke check (선택)
```bash
BASE_URL="https://<railway-domain>" ./scripts/post-deploy-smoke.sh
```

3. CI/CD에서 수동 실행
- GitHub Actions `Deploy Readiness` workflow 실행
- `base_url` 입력 시 post-deploy smoke 단계까지 수행

### Smoke 체크 기대 상태코드

- `/healthz/` -> `200`
- `/healthz/live/` -> `200`
- `/healthz/ready/` -> `200`
- `/admin-dashboard/` -> `302` (비인증 접근 시 로그인 리다이렉트)
- `/admin-operation-links/` -> `302` (비인증 접근 시 로그인 리다이렉트)
- `/contact/submit/` -> `405` (GET 불가)
- `/lead-magnet/submit/` -> `405` (GET 불가)

### 실패 시 조치 기준

- `healthz/live` 실패: 앱 프로세스/런타임 장애 가능성, 즉시 재배포 또는 롤백 검토
- `healthz/ready` 실패: 설정/DB 준비 실패 가능성, 환경변수와 DB 연결 우선 점검
- Admin/submit 경로 상태코드 불일치: 라우팅/권한/메서드 정책 회귀 가능성, 최근 배포 변경점 우선 확인
- 2회 연속 smoke 실패: 즉시 롤백 후 원인 분석

## 4) Rollback

1. Railway에서 직전 안정 배포로 롤백
2. 롤백 후 점검
- `/healthz/live/` 200
- `/healthz/ready/` 200
- `/admin-dashboard/` 접근
- 메일/문의 제출 경로 동작 확인

3. DB 호환성 점검
- 비가역 스키마 변경이 있었는지 확인
- 필요 시 데이터 백업 기준으로 복구 계획 실행
