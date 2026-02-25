## Why

현재 메인 랜딩에 창업자 대상 메시지와 외국인 개발자 대상 메시지가 혼합되어 전환 목적이 흐려집니다. 또한 내부 KPI 문구(연내 고액 외주 목표)는 대외 랜딩의 신뢰/가치 전달과 직접 관련이 낮아 제거가 필요합니다.

## What Changes

- 메인 랜딩의 Hero에서 `hero_kpi_text` 노출을 제거한다.
- 페르소나 분리 랜딩 2개를 추가한다.
- 창업자 대상 페이지: 외주/제품화/수익화 전환 중심 메시지와 CTA를 독립 구성한다.
- 외국인 개발자 대상 페이지: 실무 연계/온보딩/커리어 연결 메시지와 CTA를 독립 구성한다.
- 기존 통합 페이지는 공통 신뢰 정보와 회사 소개 중심으로 단순화한다.
- 제공 서비스 섹션의 누락 항목을 점검하고, 페르소나별 페이지에 맞는 서비스 콘텐츠를 보완한다.
- OpenSpec 문서(`quroom-landing-spec.md`)를 페르소나 분리 운영 구조에 맞게 갱신한다.

## Capabilities

### New Capabilities
- `persona-landing-pages`: 창업자/외국인 개발자 대상의 독립 랜딩 페이지와 라우팅을 제공한다.
- `hero-kpi-suppression`: 외부 노출용 랜딩에서 내부 운영 KPI 문구를 표시하지 않는다.
- `landing-spec-persona-governance`: 명세 문서에 메인/페르소나 페이지 역할, 콘텐츠 분리 원칙, CTA 운영 규칙을 명시한다.
- `service-content-completeness`: 제공 서비스 항목 누락을 방지하고, 메인/페르소나 페이지별 서비스 설명을 일관되게 유지한다.

### Modified Capabilities
- None.

## Impact

- 문서: `openspec/changes/consolidate-codex-docs-into-openspec/docs/quroom-landing-spec.md`
- 콘텐츠 정의: `landing/content.py`
- 뷰/라우팅: `landing/views.py`, `landing/urls.py`, `quroom_landing/urls.py`
- 템플릿: `templates/landing/index.html` 및 신규 페르소나 템플릿
- QA: 페이지별 CTA 동작 확인, 기존 링크/SEO 메타 영향 점검
