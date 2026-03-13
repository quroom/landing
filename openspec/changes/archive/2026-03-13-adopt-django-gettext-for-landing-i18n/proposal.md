## Why

현재 랜딩 i18n은 코드 내부의 locale-key 딕셔너리 중심이라 번역 누락 관리, 문자열 재사용, 운영 번역 워크플로우가 비효율적이다. Django 표준 국제화(`gettext`, `LocaleMiddleware`, `.po/.mo`)로 정렬해 한국어/영어 전환을 운영 가능한 방식으로 고도화할 필요가 있다.

## What Changes

- 랜딩 페이지 문자열을 Django `gettext` 기반 번역 카탈로그(`locale/`)로 이전한다.
- 템플릿은 `{% trans %}`/`{% blocktrans %}`를 사용하고, Python 코드는 `gettext`/`gettext_lazy`를 사용하도록 요구사항을 정의한다.
- 언어 전환은 Django `set_language` 경로와 언어 쿠키를 표준 방식으로 사용하도록 정리한다.
- 번역 누락 점검(`makemessages`/`compilemessages`)과 검증 절차를 운영 체크리스트에 포함한다.

## Capabilities

### New Capabilities
- `django-gettext-localization`: 랜딩 페이지 국제화를 Django 표준 번역 시스템(`gettext`, locale catalogs, set_language`)으로 운영하는 요구사항을 정의한다.

### Modified Capabilities
- `landing-spec-persona-governance`: 페르소나 랜딩 거버넌스에 언어 리소스 관리 책임(번역 카탈로그/검수 절차) 기준을 추가한다.

## Impact

- Affected code: `landing/templates/landing/*.html`, `landing/forms.py`, `landing/views.py`, `landing/project/settings.py`, `landing/project/urls.py`
- New artifacts: `locale/ko/LC_MESSAGES/django.po`, `locale/en/LC_MESSAGES/django.po`
- Ops impact: 번역 문자열 변경 시 `makemessages`/`compilemessages` 절차 필요
- API/URL breaking change 없음
