## Why

현재 메인 홈페이지, 창업자 전용, 외국인 개발자 전용 페이지의 메시지 경계가 충분히 분리되지 않아 전환 동선이 흐려집니다. 메인 페이지를 창업자 전용 가치 제안에 집중하고, 외국인 개발자 전용 페이지는 대표자의 대기업 실무 이력/개발사 네트워크/직무 연계 강점을 독립적으로 강조해 각 타겟의 신뢰와 행동 전환을 높여야 합니다.

## What Changes

- 메인 홈페이지의 핵심 메시지를 창업자 대상(외주/서비스화/수익화)으로 재정렬한다.
- 메인 홈페이지에서 외국인 개발자 실무 연계 지원 메시지는 제거하고, 해당 내용은 외국인 개발자 전용 페이지로만 노출한다.
- 제공서비스 섹션의 비어 있거나 임시 문구를 제거하고, 실제 제공 가능 항목으로 정리한다.
- 메인 홈페이지(창업자 대상)에 AX 서비스 제안을 추가한다.
  - OpenClaw, 바이브코딩 기반으로 아이디어 검증 자동화, 업무 자동화, MVP 실행 가속 등 창업자 실행 관점의 서비스를 명시한다.
- 외국인 개발자 전용 페이지에는 실무 연계 지원과 커리어 전환 지원 메시지를 집중 배치한다.
- 대표자 경력 타임라인을 명시한다.
  - 2011.01~2012.07: 삼성 소프트웨어 멤버십
  - 2012.08~2014.10: 삼성전자
  - 2020.03~현재: 큐룸
- 메인 또는 About/신뢰 섹션에 대표자의 삼성전자 근무 경력을 명확히 반영한다.
- 외국인 개발자 전용 페이지 카피를 별도 강화하여 아래 강점을 구조적으로 노출한다:
  - 대기업 취업/실무 경험 기반 멘토링 관점
  - 전남대 출신 로컬 정착/산학·지역 맥락 이해 기반 가이드 관점
  - 국내 개발사/협력업체 네트워크 기반 연계 가능성
  - 공인중개사 자격 및 현장 네트워크를 활용한 정착/실무 협업 이해도
- 창업자 페이지와 외국인 페이지의 CTA/증거 요소/FAQ를 혼합하지 않고 페르소나별로 분리한다.
- 사실 기반 신뢰 문구 정책을 적용한다(검증 가능한 사실만 사용, 과장/추정 표현 분리).
- 외국인 전용 페이지에는 실무 연계 지원 범위를 명시하고, 비자/법률 대행은 범위 외로 표기한다.
- 신뢰 항목별 증빙 링크 정책(LinkedIn/포트폴리오/GitHub)을 정의한다.
- 페르소나별 KPI를 분리한다(창업자 상담 전환, 외국인 연계 문의/면담 전환).
- OpenSpec 기준 랜딩 스펙 문서를 위 방향으로 업데이트해 구현 기준을 명확히 한다.

## Capabilities

### New Capabilities
- `founder-first-homepage-positioning`: 메인 페이지를 창업자 문제 해결 중심의 가치 제안과 CTA로 일관되게 구성한다.
- `founder-ax-service-offer`: 메인/창업자 페이지에 AX(OpenClaw/바이브코딩) 기반 실행 서비스 오퍼를 구조화해 노출한다.
- `founder-ax-package-definition`: 메인/창업자 페이지의 AX 오퍼를 2~3개 패키지(예: AX 진단 90분, 자동화 구축 2주, 실행 코칭 4주)로 고정한다.
- `foreign-developer-credibility-signals`: 외국인 개발자 전용 페이지에 대기업 실무 경험, 개발사 네트워크, 공인중개사/현장 네트워크 기반 신뢰 요소를 구조화해 노출한다.
- `foreign-developer-practical-linkage`: 외국인 개발자 전용 페이지에 실무 연계 지원, 취업/협업 연결 동선, 네트워크 기반 지원 범위를 명시한다.
- `career-credential-placement`: 삼성전자 근무 경력 등 핵심 커리어 자격을 메인/페르소나 페이지의 신뢰 블록에 일관된 문구로 배치한다.
- `evidence-link-governance`: 경력/프로젝트/강점 항목별 증빙 링크 타입과 공개 규칙을 정의한다.

### Modified Capabilities
- `persona-landing-pages`: 메인/창업자/외국인 페이지 간 역할 분리와 FAQ/KPI 분리 규칙을 함께 반영하도록 요구사항을 수정한다.
- `landing-spec-persona-governance`: 페르소나별 메시지 혼합 금지와 CTA 분리 원칙을 강화한다.
- `service-content-completeness`: 메인/창업자 페이지는 AX 서비스 중심, 외국인 전용 페이지는 실무 연계 지원 중심으로 서비스 설명 범위를 분리한다.

## Impact

- 스펙/문서:
  - `openspec/changes/consolidate-codex-docs-into-openspec/docs/quroom-landing-spec.md`
- 콘텐츠/뷰:
  - `landing/content.py`
  - `landing/views.py`
- 템플릿:
  - `landing/templates/landing/index.html`
  - `landing/templates/landing/founders.html`
  - `landing/templates/landing/foreign_developers.html`
- 검증:
  - 페르소나별 CTA 분리, 경력/자격 노출 일관성, 메인 페이지 메시지 집중도 확인
