## Why

랜딩 페이지에서 언어 전환 UI가 브라우저 폭에 따라 상단 상담 CTA와 겹쳐 클릭을 방해할 수 있다.
CTA 가시성과 클릭 가능성은 전환율에 직접 영향을 주므로 충돌을 제거해야 한다.

## What Changes

- 전역 언어 전환 UI 배치를 헤더 CTA와 충돌하지 않도록 조정한다.
- 주요 랜딩 페이지(index/foreign_developers/founders/free_diagnosis)에서 상단 영역의 CTA 가림이 없도록 반응형 동작을 정리한다.
- 관련 템플릿 테스트를 보강해 회귀를 방지한다.

## Capabilities

### Modified Capabilities
- language-switch-layout: 언어 전환 UI가 상단 CTA를 가리지 않도록 배치 규칙을 변경한다.
- responsive-header-cta-visibility: 주요 화면 폭에서 CTA 클릭 가능 상태를 보장한다.

## Impact

- `landing/templates/landing/base.html`: 언어 전환 UI 위치/구조 조정
- `landing/static/landing/css/site.css`: 반응형 배치 스타일 보강
- `landing/tests/test_landing_pages.py`: 회귀 방지 테스트 추가/수정
