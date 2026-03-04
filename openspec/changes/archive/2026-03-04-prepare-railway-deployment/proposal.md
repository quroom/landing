## Why

현재 프로젝트는 로컬 실행 중심으로 구성되어 있어 Railway 배포 시 환경변수 누락, 정적 파일 처리, 마이그레이션/헬스체크 실패 같은 운영 리스크가 발생할 수 있습니다. 배포 준비 기준을 명시하고 최소 운영 가드를 먼저 갖춰야 릴리즈 속도와 안정성을 동시에 확보할 수 있습니다.

## What Changes

- Railway 기준 배포 준비 항목을 정의하고, 앱 부팅/헬스체크/정적파일/DB 연결/마이그레이션 흐름을 표준화합니다.
- `DEBUG=False` 운영 모드에서 필수 환경변수 검증 및 실패 시 안전한 오류 노출 규칙을 추가합니다.
- 배포 후 즉시 확인 가능한 운영 점검 항목(서비스 가동, 관리자 접근, 메일 경로, 주요 폼 제출)을 체크리스트로 고정합니다.
- 관리자가 배포 검증용 주요 URL을 한 번에 확인할 수 있는 운영 링크 허브 페이지를 추가합니다.
- Railway 배포용 실행 설정(시작 커맨드, 빌드/런타임 전제)과 문서화된 롤백 절차를 포함합니다.

## Capabilities

### New Capabilities
- `railway-deployment-readiness`: Railway 배포를 위한 런타임 설정, 환경변수 계약, 운영 검증 체크리스트를 정의한다.

### Modified Capabilities
- `smtp-provider-configuration`: Railway 환경변수 기반 SMTP 설정 및 운영 모드에서의 안전한 기본값/검증 요구사항을 명확히 한다.
- `admin-dashboard-navigation`: 운영 대시보드 접근 가능 여부를 배포 후 점검 항목으로 포함할 수 있도록 운영 검증 기준을 보강한다.

## Impact

- Affected code: `landing/project/settings.py`, `landing/project/urls.py`(필요 시 헬스체크), 배포 관련 스크립트/설정 파일(`Procfile` 또는 Railway 실행 설정), 운영 문서.
- Affected systems: Railway 서비스 설정, PostgreSQL 연결 정보, SMTP provider, 정적 파일 서빙 경로.
- Dependencies: Railway 환경변수 관리, Django 운영 설정(allowed hosts, security, static), 배포 직후 검증 루틴.
