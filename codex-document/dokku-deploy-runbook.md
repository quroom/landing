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

## 7) 롤백

```bash
# 배포 히스토리 확인
dokku releases:list landing

# 이전 릴리즈로 롤백
dokku releases:rollback landing <version>
```

롤백 후에도 `post-deploy-smoke.sh`를 다시 실행해 상태를 확인합니다.

## 8) Git push 자동 재배포 (GitHub Actions)

`.github/workflows/deploy-dokku.yml`가 `main` 브랜치 push 시 자동 배포를 수행합니다.

필수 GitHub Secret:
- `DOKKU_SSH_PRIVATE_KEY`: `dokku@43.200.44.34`에 push 가능한 개인키

동작 순서:
1. Dokku 서버 SSH known_hosts 등록
2. `git push dokku HEAD:main --force`
3. `BASE_URL=http://43.200.44.34`로 smoke check 실행
