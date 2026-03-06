## Why

현재 무료 자동화 진단 결과는 "핵심 보완 포인트"(축/카테고리 레벨)와 "2주 내 끝낼 작업 1개"(질문/intent 레벨)가 서로 다른 해상도로 생성되어, 사용자가 읽을 때 매칭이 어긋나 보이는 문제가 반복됩니다. 진단 신뢰도를 높이려면 보완 메시지와 실행 작업이 같은 intent 기준으로 1:1 정렬되어야 합니다.

## What Changes

- "핵심 보완 포인트" 생성 기준을 축 중심 문구에서 anchor intent 중심 문구로 전환한다.
- "2주 내 끝낼 작업 1개"는 기존처럼 단일 실행 항목을 유지하되, 동일 anchor intent에서 파생되도록 계약을 명시한다.
- preview/메일/텍스트 렌더링에서 보완 포인트와 2주 작업의 intent 일치 여부를 공통 검증 로직으로 보장한다.
- 관리자 preview는 검토 편의를 위해 그룹화 표시를 유지하되, 묶음 내부에서도 "동일 intent 기반"임을 확인 가능한 정보를 제공한다.

## Capabilities

### New Capabilities
- `lead-magnet-weakest-intent-alignment`: 핵심 보완 포인트와 2주 실행 작업을 동일 anchor intent 기준으로 정렬하는 규칙/표현 계약

### Modified Capabilities
- `ax-diagnosis-priority-one-action`: 2주 작업 선정 기준과 핵심 보완 포인트의 정렬 요구사항을 강화
- `lead-magnet-cta-report-format`: preview/메일 섹션 계약에 intent 정렬 검증 항목 추가
- `ax-diagnosis-result-personalization`: 축 기반 메시지와 intent 기반 메시지 우선순위/노출 규칙 수정

## Impact

- Affected code: `landing/views.py`, `landing/lead_magnet_sections.py`, `landing/mailers.py`
- Affected templates: `landing/templates/landing/lead_magnet_report_preview.html`
- Affected tests: `landing/tests/test_lead_magnet_sections.py`, `landing/tests/test_landing_pages.py`, 관련 스냅샷/계약 테스트
- Behavioral impact: 사용자에게 보이는 보완 메시지와 2주 실행 항목의 의미 정합성 개선, 리뷰/QA 판단 비용 감소
