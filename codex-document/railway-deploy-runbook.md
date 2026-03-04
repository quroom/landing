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
- `/healthz/` 200 확인
- `/admin-dashboard/` 접근 확인
- 핵심 submit 경로 동작 확인

2. 자동 smoke check (선택)
```bash
BASE_URL="https://<railway-domain>" ./scripts/post-deploy-smoke.sh
```

3. CI/CD에서 수동 실행
- GitHub Actions `Deploy Readiness` workflow 실행
- `base_url` 입력 시 post-deploy smoke 단계까지 수행

## 4) Rollback

1. Railway에서 직전 안정 배포로 롤백
2. 롤백 후 점검
- `/healthz/` 200
- `/admin-dashboard/` 접근
- 메일/문의 제출 경로 동작 확인

3. DB 호환성 점검
- 비가역 스키마 변경이 있었는지 확인
- 필요 시 데이터 백업 기준으로 복구 계획 실행
