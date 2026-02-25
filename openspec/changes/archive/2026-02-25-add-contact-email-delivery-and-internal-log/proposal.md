## Why

현재 문의 폼은 이메일 전송이 실패해도 서버 내부에서 별도 이력이 남지 않아 누락 여부를 확인하기 어렵다. `help@quroom.kr` 수신 신뢰도를 높이고 운영자가 빠르게 확인할 수 있는 내부 저장/조회 경로가 필요하다.

## What Changes

- 문의 접수 시 이메일 발송 대상이 `help@quroom.kr`로 확실히 설정되도록 구성값과 검증 흐름을 명확히 한다.
- 문의 접수 데이터를 내부 DB에 저장해 이메일 실패 여부와 무관하게 누락 방지 이력을 보존한다.
- 문의 이력의 이메일 발송 상태(성공/실패/오류 메시지)를 저장해 운영 확인성을 높인다.
- 운영자가 가장 쉬운 방식으로 확인할 수 있도록 Django Admin에서 문의 이력을 조회/필터링 가능하게 한다.
- 기본 테스트에 문의 저장/이메일 발송/실패 처리 케이스를 추가한다.

## Capabilities

### New Capabilities
- `contact-email-delivery`: 문의 접수 이메일이 `help@quroom.kr`로 발송되도록 설정/처리 규칙을 정의한다.
- `contact-inquiry-persistence`: 문의 데이터를 내부 저장소에 기록하고 누락 없이 보존하는 동작을 정의한다.
- `contact-inquiry-operational-review`: 운영자가 문의 이력과 발송 상태를 쉽게 확인하는 조회 흐름을 정의한다.

### Modified Capabilities
- (none)

## Impact

- Affected code:
  - `landing/views.py`
  - `landing/forms.py` (필요 시 정규화 보조)
  - `landing/models.py` (신규)
  - `landing/admin.py` (신규/수정)
  - `landing/tests/test_contact_form.py`
  - 신규 migration 파일
- Operational impact:
  - 배포 후 DB migration 필요
  - 환경변수 `QUROOM_CONTACT_EMAIL` 기본값/실제값 검증 필요
