## Why

현재 랜딩의 서비스 영역은 핵심 AX 오퍼, 외주 집중 트랙, 부가 옵션이 혼재되어 있어 사용자가 서비스 구조와 선택 경로를 빠르게 이해하기 어렵다. 특히 창업 초기 고객은 "무엇을 먼저 갖춰야 하는지"에 대한 기본 인프라 가이드를 필요로 하므로, 개발자가 제공 가능한 필수 기반을 패키지로 명확히 제시할 필요가 있다.

## What Changes

- 메인 랜딩의 서비스 섹션을 `AX 실행 파트`, `외주용역 집중 트랙`, `창업 기본 인프라 구축` 3개 파트로 명확히 분리한다.
- `창업 기본 인프라 구축` 파트에 초기 기업 운영 필수 항목(예: 비즈니스 메일, 기업 홈페이지, 기본 문의/도메인/운영 설정)을 묶어 제안한다.
- `비즈니스 메일 구축` 오퍼는 다음 스마트워크 기준으로, 도메인 구매 / 연결 / DNS 레코드 설정 제공 범위를 명시한다.
- 각 서비스/옵션 카드의 공통 필드(기간, 가격, 대상, 결과물/비고) 표기 규칙을 정리해 일관된 비교가 가능하게 한다.
- 외주용역 집중 트랙 카드 레이아웃을 AX 파트 카드와 동일한 UI 패턴으로 통일한다.
- 포트폴리오/서비스 카피 중 정책 문구(상세 링크 비공개, 비용 표기 방식)를 현재 운영 기준으로 정규화한다.

## Capabilities

### New Capabilities
- `landing-service-package-segmentation`: 메인 서비스 섹션을 3개 파트(AX/외주/창업 기본 인프라)로 분리하고 정보 구조를 고정한다.
- `startup-foundation-infra-offer`: 비즈니스 메일(다음 스마트워크), 기업 홈페이지, 초기 운영 필수 설정 오퍼의 범위/가격/주의사항 표준을 정의한다.

### Modified Capabilities
- `service-content-completeness`: 서비스 카드 필수 필드를 패키지/옵션 공통 규칙으로 확장하고 가격/정책 문구 일관성을 강화한다.
- `founder-ax-package-definition`: AX 파트와 외주 집중 트랙의 관계 및 레이아웃 표준을 반영하도록 요구사항을 보강한다.
- `founder-first-homepage-positioning`: 메인 페이지 내 서비스 정보 구조를 founder-first 전환 흐름에 맞게 구체화한다.

## Impact

- Affected code:
  - `landing/content.py`
  - `landing/templates/landing/index.html`
  - 필요 시 `landing/templates/landing/foreign_developers.html`
- Affected specs:
  - `openspec/specs/service-content-completeness/spec.md`
  - `openspec/specs/founder-ax-package-definition/spec.md`
  - `openspec/specs/founder-first-homepage-positioning/spec.md`
  - 신규 capability spec 2종 추가
- No API breaking changes expected.
