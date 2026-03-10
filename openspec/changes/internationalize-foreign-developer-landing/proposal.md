## Why

현재 `foreign developer` 랜딩 페이지는 라우팅은 분리되어 있지만 기본 문서 언어와 카피 구조가 한국어 중심이라 해외 사용자의 이해성과 접근성이 낮다. 외국인 개발자 유입을 실제 전환으로 연결하려면 해당 페이지를 영어 기본으로 전환하고, 랜딩 전체를 다국어 운영 가능한 구조로 명확히 정의해야 한다.

## What Changes

- `for-foreign-developers` 페이지의 기본 언어를 영어로 정의하고, 언어 선택 시 영어가 기본으로 노출되도록 요구사항을 명시한다.
- 랜딩 페이지 전반(`/`, `/for-foreign-developers/`, 공통 UI/폼 텍스트)에 국제화(i18n) 지원 기준을 추가한다.
- 언어별 콘텐츠 소스와 렌더링 규칙(기본 언어, 폴백, 미번역 처리)을 스펙 레벨에서 정의한다.
- 기존 페르소나 분리 요구사항에 언어별 경험 일관성 조건을 추가한다.

## Capabilities

### New Capabilities
- `landing-page-internationalization`: 랜딩 페이지 전반의 다국어 지원(기본 언어, 폴백, 번역 키 운영, 언어 전환 UX) 요구사항을 정의한다.

### Modified Capabilities
- `persona-landing-pages`: 페르소나별 랜딩 접근성 요구사항에 페이지 언어 기본값과 언어별 CTA/FAQ 일관성 기준을 추가한다.
- `foreign-developer-practical-linkage`: `/for-foreign-developers/` 페이지에서 영어 기본 언어 및 영어 우선 정보 전달 요구사항을 추가한다.

## Impact

- Affected specs: `persona-landing-pages`, `foreign-developer-practical-linkage`, 신규 `landing-page-internationalization`
- Affected code (expected): `landing/views.py`, `landing/content.py`, `landing/templates/landing/*.html`, `landing/forms.py`, 관련 테스트 파일
- Operational impact: 콘텐츠 관리 시 언어별 카피 유지 및 번역 품질 검수 프로세스 필요
- No external API breaking change expected
