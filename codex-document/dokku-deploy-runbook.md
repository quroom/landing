# Dokku Deploy Runbook

## 1) 앱 생성 및 리모트 연결

```bash
# Dokku 서버에서 1회 실행
dokku apps:create landing

# 로컬 저장소에서 실행
git remote add dokku dokku@<dokku-host>:landing
```

### 서버 로컬 저장소(`~/projects/landing`) 배포 방식

```bash
# Dokku 서버(ubuntu 계정)에서 1회 실행
mkdir -p ~/projects
cd ~/projects
git clone git@github.com:quroom/landing.git landing
cd landing
git remote add dokku dokku@127.0.0.1:landing
```

서버에서 재배포할 때는 아래만 실행합니다.

```bash
cd ~/projects/landing
git pull origin main && git push dokku main
```

## 2) 필수 환경변수

```bash
dokku config:set --no-restart landing \
  DJANGO_DEBUG=0 \
  DJANGO_SECRET_KEY='<strong-random-secret>' \
  DJANGO_ALLOWED_HOSTS='<your-domain>' \
  DJANGO_CSRF_TRUSTED_ORIGINS='https://<your-domain>' \
  DJANGO_SITE_BASE_URL='https://<your-domain>'
```

추가(사용 시):
- SMTP: `DJANGO_EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS/SSL`, `DJANGO_DEFAULT_FROM_EMAIL`
- DB(Postgres): `DATABASE_URL` 또는 `PG*`/`DB*` 변수
- 운영 메일: `QUROOM_CONTACT_EMAIL`

## 3) 배포 전 점검

```bash
./scripts/deploy-check.sh
./scripts/verify.sh
```

## 4) 배포

이 저장소는 `Procfile`에 `release`/`web`가 이미 정의되어 있어, push 시 아래 순서로 실행됩니다.
1. `python manage.py migrate --no-input`
2. `python manage.py collectstatic --no-input`
3. `gunicorn ... landing.project.wsgi:application`

```bash
git push dokku main
```

## 5) 배포 후 확인

```bash
BASE_URL='https://<your-domain>' ./scripts/post-deploy-smoke.sh
```

기대 상태:
- `/healthz/` -> `200`
- `/healthz/live/` -> `200`
- `/healthz/ready/` -> `200`
- `/admin-dashboard/` -> `302`
- `/admin-operation-links/` -> `302`
- `/contact/submit/` -> `405`
- `/lead-magnet/submit/` -> `405`

## 6) 운영 체크

- 관리자 운영 링크: `/admin-operation-links/`
- 관리자 대시보드: `/admin-dashboard/`
- 헬스체크: `/healthz/`, `/healthz/live/`, `/healthz/ready/`

## 7) 롤백 리허설 시나리오 및 메뉴얼

이 서버 Dokku 버전은 `releases:list`/`releases:rollback` 대신 `git:sync` 기반으로 복구를 수행합니다.

### 시나리오

- 목표: 문제 배포 발생 시, 직전 안정 커밋으로 5분 내 복구 가능 여부 확인
- 성공 기준:
- 롤백 후 `/healthz/ready/`가 `200`
- `post-deploy-smoke.sh` 전체 통과
- 복구(원복)까지 동일 절차로 재진입 가능

### 사전 준비

```bash
# 1) 현재 배포 커밋(원복용) 기록
ssh ubuntu@43.200.44.34 "sudo -n dokku git:report landing | grep 'Git sha:'"

# 2) 롤백 대상 커밋 선정 (직전 안정 커밋)
git log --oneline -n 10
```

### 롤백 실행

자동 롤백(권장):

```bash
# 기본: 현재 배포 SHA의 직전 커밋으로 롤백 + 스모크 체크
./scripts/dokku-rollback.sh

# 특정 SHA로 롤백
./scripts/dokku-rollback.sh --target-sha <rollback_sha>
```

수동 롤백:

```bash
# <rollback_sha>를 직전 안정 커밋으로 교체
ssh ubuntu@43.200.44.34 \
  "sudo -n dokku git:sync landing git@github.com:quroom/landing.git <rollback_sha>"

# 롤백 검증
BASE_URL='https://<your-domain>' ./scripts/post-deploy-smoke.sh
```

### 원복(최신으로 복귀)

자동 원복(권장):

```bash
# 롤백 완료 로그에 출력된 이전 SHA 사용
./scripts/dokku-rollback.sh --target-sha <current_sha>
```

수동 원복:

```bash
# <current_sha>를 사전 준비에서 기록한 현재 배포 커밋으로 교체
ssh ubuntu@43.200.44.34 \
  "sudo -n dokku git:sync landing git@github.com:quroom/landing.git <current_sha>"

# 원복 검증
BASE_URL='https://<your-domain>' ./scripts/post-deploy-smoke.sh
```

### 운영 주의사항

- 롤백 리허설은 트래픽이 낮은 시간대에 수행
- 수행 전/후 `dokku ps:report landing`로 프로세스 상태 확인
- DB 마이그레이션이 비가역인 배포는 롤백 전에 데이터 호환성 검토 필수

## 8) Git push 자동 재배포 (GitHub Actions)

`.github/workflows/deploy-dokku.yml`가 `main` 브랜치 push 시 자동 배포를 수행합니다.

필수 GitHub Secret:
- `DOKKU_SSH_PRIVATE_KEY`: `dokku@43.200.44.34`에 push 가능한 개인키

동작 순서:
1. `./scripts/verify.sh` + `./scripts/deploy-check.sh` 선행 실행
2. 현재 배포 SHA 조회(`dokku git:report`)
3. `git push dokku HEAD:main --force` 배포
4. `BASE_URL=https://quroom.kr` smoke check 실행
5. 배포/스모크 실패 시 직전 SHA로 자동 롤백(`git push dokku <previous_sha>:main --force`)

주의:
- 롤백이 성공해도 워크플로우는 실패 상태로 종료되어, 운영자가 이슈를 확인할 수 있게 합니다.
