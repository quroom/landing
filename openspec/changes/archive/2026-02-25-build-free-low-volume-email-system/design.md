## Context

문의 폼 저장과 `send_mail` 호출은 이미 구현되어 있다. 현재 운영에서 실메일 수신을 위해서는 SMTP 공급자(예: Daum) 연동이 필요하며, 환경별로 안전한 기본값과 운영 점검 절차가 함께 있어야 한다.

## Goals / Non-Goals

**Goals:**
- SMTP 연동을 환경변수 중심으로 구성해 코드 수정 없이 운영 전환 가능하게 한다.
- 저용량 운영에 맞는 무료/저비용 공급자 설정 경로를 명확히 한다.
- 전송 실패 시에도 문의 데이터 유실 없이 추적 가능하게 유지한다.

**Non-Goals:**
- 큐/재시도 워커(Celery 등) 도입
- 다중 공급자 자동 failover
- 대량 발송 최적화

## Decisions

### Decision 1: Django SMTP backend + env configuration
- `django.core.mail.backends.smtp.EmailBackend`를 운영 표준으로 사용한다.
- SMTP host/port/user/password/TLS/SSL/timeout은 전부 환경변수로 주입한다.
- 개발 기본값은 console backend를 유지해 오발송을 방지한다.

### Decision 2: 수신 전용 운영 모델 유지
- 문의 메일은 `QUROOM_CONTACT_EMAIL` 단일 수신 주소로 보낸다.
- `DEFAULT_FROM_EMAIL`는 SMTP 공급자가 허용하는 발신 주소(계정 주소)와 일치시킨다.

### Decision 3: 실패 내구성은 기존 persistence 모델 재사용
- 전송 실패 시 `ContactInquiry`는 저장 유지.
- `email_delivery_status`, `emailed_at`, `email_error`로 운영자가 실패를 확인한다.

## Risks / Trade-offs

- [공급자 보안 정책 변경] → 앱 비밀번호/SMTP 허용 정책 변경 시 즉시 `.env` 갱신 절차 문서화
- [DNS/네트워크 제한 환경에서 테스트 실패] → 로컬/배포 환경에서 별도 전송 검증 커맨드 제공
- [발신 주소 불일치로 거부] → `DEFAULT_FROM_EMAIL == EMAIL_HOST_USER` 운영 규칙 권장

## Migration Plan

1. SMTP 관련 settings/env 키를 확정한다.
2. `.env.sample`에 운영 입력값을 반영한다.
3. 실제 SMTP 계정 값을 `.env`에 설정한다.
4. 테스트 메일 커맨드 실행 후 수신함 도착 확인.
5. 폼 제출 테스트 후 DB의 delivery status를 확인한다.

## Open Questions

- 운영 문서에 공급자별(다음/네이버/구글) 예시를 어디까지 포함할지
- 실패 건 재발송 기능을 다음 change로 분리할지
