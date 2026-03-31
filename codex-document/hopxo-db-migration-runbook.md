# Hopxo DB Migration Runbook

## 목적

`hopxo` 앱이 사용하던 `quroom_prod_db`를 전용 DB인 `hopxo_prod_db`로 분리하고, 앱 연결을 새 DB로 전환한다.

## 이전 상태

- Postgres service: `quroom-prod-db`
- `hopxo` app DATABASE_URL target: `quroom_prod_db`
- `landing` app DATABASE_URL target: `landing_prod_db`
- 별도 Dokku Postgres service `hopxo-db`가 존재했지만 앱 link는 없었음

## 수행 순서

1. 현재 `quroom_prod_db` dump 백업 생성
2. `hopxo_user` / `hopxo_prod_db` 생성
3. `quroom_prod_db` 데이터를 `hopxo_prod_db`로 복원
4. `hopxo` app `DATABASE_URL` 및 `PG*` 환경변수 전환
5. `dokku ps:restart hopxo`
6. 도메인 응답, 로그, DB 목록 확인

## 실행 결과

- 수동 백업 생성 완료
  - `/home/ubuntu/manual-db-backups/quroom_prod_db_before_hopxo_migration_20260331T024524Z.dump`
- 새 DB 생성 완료
  - database: `hopxo_prod_db`
  - owner: `hopxo_user`
- 앱 전환 완료
  - `hopxo`는 현재 `hopxo_prod_db`를 사용
- 프로세스 상태 확인
  - `dokku ps:report hopxo` -> `running`
- 도메인 응답 확인
  - `https://hopxo.com` -> `302`
  - `https://www.hopxo.com` -> `302`
  - `https://next.hopxo.com` -> `302`
- 최근 로그 확인
  - 앱 부팅 성공
  - DB 관련 에러 없음

## 현재 구조

`quroom-prod-db` 내부 DB:

- `landing_prod_db` owned by `landing_user`
- `hopxo_prod_db` owned by `hopxo_user`
- `quroom_prod_db` owned by `postgres`
- `hopxo_db` owned by `postgres`
- `postgres`

## 남은 작업

1. 애플리케이션 실제 사용자 플로우 한 번 더 수동 확인
2. `quroom_prod_db` 보존 기간 결정 후 삭제 여부 판단
3. 미사용 `hopxo-db` service 정리 여부 판단
4. 자동 백업 스크립트를 `APP=hopxo` 기준으로 설치
5. 새 DB 비밀번호를 운영 비밀 저장소에 별도 기록하고 필요 시 rotate

## 주의

- 이 문서에는 민감한 비밀번호 값을 기록하지 않는다.
- `quroom_prod_db`와 `hopxo-db` 삭제는 별도 확인 후 진행한다.
