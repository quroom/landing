## Context

랜딩은 현재 `ko/en` 전환 자체는 동작하지만, 다수 문자열이 Python 딕셔너리에 내장되어 있어 번역 리소스 분리와 번역자 협업이 어렵다. Django는 기본적으로 `LocaleMiddleware`, `set_language`, `gettext` 생태계를 제공하므로 이를 표준 레일로 채택해 유지보수 리스크를 줄인다.

## Goals / Non-Goals

**Goals:**
- 템플릿/폼/뷰 노출 문자열을 `gettext` 카탈로그로 이전한다.
- 언어 전환을 Django 표준 쿠키/엔드포인트로 일관화한다.
- 번역 누락을 CI/검증 절차에서 사전에 감지할 수 있게 한다.

**Non-Goals:**
- 자동 번역 파이프라인 도입
- 2개 언어(ko/en) 외 추가 언어 동시 지원
- 랜딩 외 이메일/관리자 UI 전체 번역

## Decisions

### 1) 문자열 소스의 단일 기준을 gettext 카탈로그로 둔다
- 결정: 사용자 노출 문자열은 가능한 한 `.po` 파일에서 관리한다.
- 이유: 번역 변경 시 코드 수정 없이 번역 리소스만 업데이트 가능하다.
- 대안: 기존 locale-key 딕셔너리 유지.
- 미채택 이유: 키 누락 탐지와 번역 협업 효율이 낮다.

### 2) 템플릿은 trans/blocktrans 중심으로 변경한다
- 결정: 하드코딩 텍스트 및 locale-key 출력을 `{% trans %}` 또는 `{% blocktrans %}`로 치환한다.
- 이유: Django 템플릿 번역 도구와 자연스럽게 통합된다.
- 대안: 템플릿은 유지하고 뷰에서 번역값 주입.
- 미채택 이유: 템플릿 변경 추적과 번역 추출 자동화가 어렵다.

### 3) 폼/뷰 문자열은 gettext_lazy/gettext를 사용한다
- 결정: 폼 필드 라벨/에러/placeholder는 `gettext_lazy`, 런타임 메시지는 `gettext`를 사용한다.
- 이유: Form class 초기화 시점 지연 번역이 필요하고, 응답 메시지는 요청 시점 locale을 따라야 한다.

### 4) 검증 단계에 번역 리소스 점검을 포함한다
- 결정: `makemessages` 결과와 `.po` 누락 여부를 점검하고, `compilemessages` 성공을 배포 전 체크한다.
- 이유: 번역 누락/문법 오류를 사전에 차단한다.

## Risks / Trade-offs

- [Risk] 기존 locale-key 로직과 gettext 로직이 한동안 혼재될 수 있음
  -> Mitigation: 단계적으로 모듈 단위 마이그레이션 후 legacy 키 제거 태스크를 명시한다.
- [Risk] `msgid` 변경 시 기존 번역 매핑 손실 가능
  -> Mitigation: 문자열 변경 시 번역 파일 diff 리뷰를 필수화한다.
- [Risk] 개발 환경에 gettext 바이너리 의존성 이슈
  -> Mitigation: 로컬/CI 환경별 gettext 설치 가이드를 문서화한다.

## Migration Plan

1. `locale/` 경로와 `LANGUAGES/LOCALE_PATHS/LocaleMiddleware`를 최종 점검한다.
2. 템플릿과 폼 문자열을 gettext 호출로 전환한다.
3. `makemessages -l ko -l en` 실행 후 번역 문구를 채운다.
4. `compilemessages` 및 테스트/검증을 수행한다.
5. 기존 locale-key 기반 문자열 매핑을 제거하거나 축소한다.

## Open Questions

- 검증 스크립트(`verify.sh`)에 `compilemessages`를 상시 포함할지, 별도 스크립트로 분리할지 결정 필요
- 번역 품질 리뷰 책임자(개발/운영)와 승인 기준 정의 필요
