## Context

현재 `contact_submit`은 유효한 문의를 받으면 `send_mail(..., fail_silently=True)`로 메일을 전송하고 바로 성공 응답을 반환한다. 이 구조는 메일 서버 문제나 환경 설정 오류가 생겨도 운영자가 누락을 탐지하기 어렵다. 또한 접수 데이터가 DB에 저장되지 않아 사후 검증 경로가 없다.

## Goals / Non-Goals

**Goals:**
- 문의 접수 데이터를 DB에 항상 저장한다.
- 메일 발송 성공/실패 상태를 문의 이력에 기록한다.
- 운영자가 Django Admin에서 최근 문의와 실패 건을 빠르게 확인할 수 있게 한다.
- 기존 프론트 문의 UX(HTMX 응답 구조)는 유지한다.

**Non-Goals:**
- 큐 시스템(Celery) 기반 비동기 메일 파이프라인 도입
- 별도 운영 대시보드 페이지 구축
- 자동 재전송 스케줄러 구현

## Decisions

### Decision 1: `ContactInquiry` 모델을 도입해 문의 원본과 발송 상태를 함께 저장
- 문의 원본 필드(이름, 회사, 연락채널, 이메일, 문의유형, 메시지, 개인정보동의시각)와 발송 상태 필드(`email_delivery_status`, `email_error`, `emailed_at`)를 저장한다.
- 이유: 누락 방지와 감사 추적에 필요한 최소 데이터를 한 엔터티에서 관리할 수 있다.

### Decision 2: 메일 전송 실패를 사용자 응답과 분리하고 내부 상태로 관리
- `send_mail`은 `fail_silently=False`로 호출하고 예외를 캡처해 상태를 `failed`로 기록한다.
- 사용자에게는 접수 성공 메시지를 유지하되, 운영자가 Admin에서 실패 건을 확인하도록 한다.
- 이유: 접수 자체의 신뢰성과 운영 감시를 동시에 충족한다.

### Decision 3: 운영 확인 경로는 Django Admin을 기본 채널로 사용
- `ContactInquiryAdmin`에 목록 컬럼/필터(`email_delivery_status`, `inquiry_type`, `created_at`)를 제공한다.
- 이유: 추가 UI 개발 없이 즉시 사용 가능하고 접근 제어도 기본 제공된다.

### Decision 4: 설정값 검증을 테스트로 고정
- 테스트에서 수신자 주소가 `settings.QUROOM_CONTACT_EMAIL`로 사용되는지 검증한다.
- 이유: 배포 전 설정 실수를 자동으로 탐지한다.

## Risks / Trade-offs

- [Risk] 메일 실패 시 사용자에게 성공 메시지가 노출되어 오해 가능 → Admin 실패 모니터링 절차와 재처리 운영 가이드를 문서화한다.
- [Risk] 개인정보 저장 범위 확대 → 최소 필드만 저장하고 접근은 Admin 권한 사용자로 제한한다.
- [Risk] DB 쓰기 실패 시 접수 실패 가능 → 저장/메일 처리 단계를 명확히 분리하고 예외 로그를 남긴다.

## Migration Plan

1. `ContactInquiry` 모델 및 Admin 등록 구현
2. Migration 생성/적용
3. `contact_submit`에서 저장 → 메일 발송 → 상태 업데이트 순서로 리팩터링
4. 테스트 추가/수정 후 `./scripts/verify.sh` 실행
5. 운영 환경에서 `QUROOM_CONTACT_EMAIL=help@quroom.kr` 확인

Rollback:
- 모델/뷰 변경 롤백 시 기존 메일 전송만 수행하는 로직으로 즉시 복귀 가능
- 필요 시 migration rollback 수행

## Open Questions

- 실패 건 재전송을 Admin 액션으로 바로 제공할지, 다음 change에서 분리할지 결정 필요
- 개인정보 보관 기간(예: 1년)과 파기 정책을 정책 문서에 즉시 반영할지 확인 필요
