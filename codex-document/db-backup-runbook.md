# Production DB Backup Runbook

배포 서버 `ssh.quroom.kr` 의 Dokku 앱 `landing` 이 사용하는 PostgreSQL DB를 주기적으로 백업하고, 필요 시 로컬로 내려받아 복원하는 절차입니다.

## 목적

- 운영 DB 데이터 유실 위험 완화
- 로컬에서 운영 데이터 스냅샷 확인
- GA4/대시보드 작업 전 실제 운영 데이터 검증

## 전제

- Dokku 앱 이름: `landing`
- Dokku SSH 접속: `ubuntu@ssh.quroom.kr`
- 운영 DB 연결 정보는 Dokku app config 의 `DATABASE_URL` 또는 `PG*`/`DB*` 변수에 설정되어 있어야 함
- 원격 호스트에는 `docker`, `dokku`, `python3`, `sha256sum`, `flock` 사용 가능해야 함
- 실제 dump 는 Postgres 컨테이너 내부의 `pg_dump` 를 사용함
- 로컬 복원에는 `pg_restore`, `createdb`, `dropdb` 사용 가능해야 함

## 포함된 스크립트

- `scripts/remote-prod-db-backup.sh`
  - 원격 호스트에서 실제 백업 생성
  - custom-format `.dump`, `.sha256`, `.json` manifest 생성
  - retention 기간 지난 파일 자동 삭제
- `scripts/install-prod-db-backup-cron.sh`
  - 원격 호스트에 백업 스크립트 업로드
  - cron 등록
- `scripts/fetch-prod-db-backup.sh`
  - 최신 또는 지정 백업을 로컬로 다운로드
- `scripts/restore-prod-db-backup-local.sh`
  - 다운로드한 dump 를 로컬 PostgreSQL DB 에 복원

## 1) 원격 cron 설치

```bash
./scripts/install-prod-db-backup-cron.sh
```

기본값:

- host: `ubuntu@ssh.quroom.kr`
- app: `landing`
- schedule: `15 3 * * *`
- remote backup root: `/home/ubuntu/backups/landing/postgres`
- retention: `14` days

예시:

```bash
./scripts/install-prod-db-backup-cron.sh \
  --host ubuntu@ssh.quroom.kr \
  --app landing \
  --schedule "30 2 * * *" \
  --retention-days 21
```

Dry-run:

```bash
./scripts/install-prod-db-backup-cron.sh --dry-run
```

## 2) 원격 1회 수동 실행

cron 설치 전/후에는 1회 수동 실행으로 동작을 확인합니다.

```bash
ssh ubuntu@ssh.quroom.kr \
  'APP=landing BACKUP_ROOT=/home/ubuntu/backups/landing/postgres RETENTION_DAYS=14 /home/ubuntu/bin/landing-prod-db-backup.sh'
```

생성 결과:

- `landing-<timestamp>.dump`
- `landing-<timestamp>.sha256`
- `landing-<timestamp>.json`

## 3) 최신 백업을 로컬로 가져오기

```bash
./scripts/fetch-prod-db-backup.sh
```

기본 다운로드 경로:

- `backups/prod-db/landing/`

특정 파일:

```bash
./scripts/fetch-prod-db-backup.sh --file landing-20260331T030000Z
```

## 4) 로컬 PostgreSQL 로 복원

기본 DB 이름:

- `landing_prod_snapshot`

```bash
./scripts/restore-prod-db-backup-local.sh
```

특정 DB 이름:

```bash
./scripts/restore-prod-db-backup-local.sh --db-name landing_prod_snapshot
```

현재 DB 를 유지한 채 복원만 하려면:

```bash
./scripts/restore-prod-db-backup-local.sh --skip-drop-create
```

## 5) Docker Compose 로 landing snapshot 띄우기

로컬 PostgreSQL 도구 없이 테스트하려면 snapshot DB와 Django app을 둘 다 compose로 띄웁니다.
app 이미지는 [`Dockerfile.landing-snapshot`](/home/quroom/workspace/homepage/Dockerfile.landing-snapshot) 으로 빌드되고, [`requirements.txt`](/home/quroom/workspace/homepage/requirements.txt) 를 설치한 뒤 저장소를 마운트해 실행합니다.
처음 실행하면 gitignore 된 `.env.landing-snapshot` 파일을 자동 생성하고, 로컬 snapshot 비밀번호를 그 안에만 저장합니다.

```bash
./scripts/up-landing-snapshot-compose.sh --fetch-latest
./scripts/run-landing-snapshot-local.sh
```

선택적으로 먼저 설정 파일만 확인하려면:

```bash
cp .env.landing-snapshot.example .env.landing-snapshot
```

기본 접속 주소:

- app: `http://127.0.0.1:8011`
- db: `127.0.0.1:55432`

점검 예시:

```bash
sudo -n docker compose --env-file .env.landing-snapshot -p landing-snapshot -f compose.landing-snapshot.yml exec -T app \
  python manage.py showmigrations landing
```

중지:

```bash
./scripts/down-landing-snapshot-compose.sh
```

볼륨까지 제거:

```bash
./scripts/down-landing-snapshot-compose.sh --remove-volume
```

## 운영 권장

- 최소 일 1회 백업
- retention 은 14~30일 권장
- 주 1회 정도는 실제로 `fetch -> restore` 리허설 수행
- 백업 파일 저장 디렉터리는 디스크 사용량 모니터링 필요
- 추후 필요하면 S3 등 외부 스토리지로 2차 복제 추가 검토
