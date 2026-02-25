## Why

문의 폼은 이미 구현되어 있지만, SMTP 공급자 연동이 없으면 운영 환경에서 실제 메일이 전송되지 않는다. 월간 메일 볼륨이 낮은 조건에 맞춰 무료 또는 저비용 SMTP 기반으로 안정적으로 수신할 수 있는 표준 구성이 필요하다.

## What Changes

- Django 메일 설정을 SMTP 환경변수 기반으로 표준화한다.
- `.env.sample`에 SMTP 필수 키를 명시해 배포 환경에서 동일하게 구성 가능하도록 한다.
- 문의 메일 전송 성공/실패를 검증하는 테스트 및 운영 점검 절차를 정의한다.
- 공급자(예: Daum SMTP) 설정 시 수신 전용 운영이 가능하도록 기본값과 runbook을 정리한다.

## Capabilities

### New Capabilities
- `smtp-provider-configuration`: 무료/저용량 SMTP 제공자 연동을 위한 환경변수 기반 메일 설정
- `smtp-delivery-verification`: 실제 전송 여부를 확인하는 점검 절차와 장애 시 확인 경로

### Modified Capabilities
- `contact-email-delivery`: 콘솔 백엔드 기본 동작에서 실 SMTP 백엔드 운영을 지원하도록 설정 요구사항 확장

## Impact

- `landing/project/settings.py`: SMTP 관련 Django 설정 키 추가/사용
- `.env.sample`: 운영자 입력용 메일 환경변수 템플릿 보강
- `landing/views.py`: 기존 `send_mail` 로직 유지(설정 기반으로 실제 전송)
- `landing/tests/test_contact_form.py`: 전송 경로/실패 처리 검증 유지 또는 보강
- 운영 문서(`README.md`): SMTP 공급자 값 입력/테스트 방법 반영
