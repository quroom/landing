## 1. 문의 저장 모델 및 운영 조회 기반 추가

- [x] 1.1 `landing/models.py`에 문의 이력(`ContactInquiry`) 모델을 추가한다.
- [x] 1.2 `landing/admin.py`에 문의 이력 Admin 목록/필터 구성을 추가한다.
- [x] 1.3 migration 파일을 생성해 모델 스키마를 반영한다.

## 2. 문의 접수 로직 보강

- [x] 2.1 `landing/views.py`의 `contact_submit`에서 유효 문의를 DB에 먼저 저장하도록 변경한다.
- [x] 2.2 메일 전송을 `settings.QUROOM_CONTACT_EMAIL` 대상으로 수행하고 성공/실패 상태를 이력에 업데이트한다.
- [x] 2.3 메일 실패 시 에러 메시지를 저장하되 사용자 응답은 접수 완료 흐름을 유지하도록 처리한다.

## 3. 테스트 및 설정 검증

- [x] 3.1 `landing/tests/test_contact_form.py`에 문의 저장/수신 주소/성공·실패 상태 테스트를 추가한다.
- [x] 3.2 운영 설정 문서에 `QUROOM_CONTACT_EMAIL=help@quroom.kr` 확인 절차를 반영한다.
- [x] 3.3 `./scripts/verify.sh`를 실행해 check/test 통과를 확인한다.
