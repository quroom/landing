## Why

현재 리드마그넷 진단 결과는 구조는 명확해졌지만, 랜딩페이지 전체 맥락과 비교했을 때 행동 유도 문구의 강도와 채널 일관성(웹 결과/이메일)에서 개선 여지가 남아 있다.  
전환 직전 구간인 진단 요약/2주 과제/CTA 카피를 더 실행 중심으로 정리해 문의 전환률과 메시지 신뢰도를 동시에 높여야 한다.

## What Changes

- 진단 결과 카피를 `행동 중심`으로 재정의한다. (요약 문구, 2주 과제 라벨/완료 기준, CTA 문구/보조 문구)
- 리드마그넷 결과 화면과 이메일 본문이 동일한 카피 계약을 사용하도록 정렬한다.
- CTA 클릭 이후 문의 구간에서 `진단 맥락`이 이어지도록 연결 문구/기본 선택 흐름을 강화한다.
- 등급별(A/B/C) 결과 톤은 유지하되, 공통 행동 프레임(작업 1개 완료)으로 메시지 일관성을 높인다.

## Capabilities

### New Capabilities
- 없음

### Modified Capabilities
- `lead-magnet-email-followup`: 이메일 후속 카피를 실행 중심 문구로 조정하고 결과 화면과 문구 계약을 동기화한다.
- `lead-magnet-cta-report-format`: 진단 리포트의 CTA/과제/요약 카피를 전환 중심 표현으로 갱신하고 문의 연결 맥락을 강화한다.
- `lead-magnet-result-bridging`: 진단 결과에서 문의 섹션으로 이어지는 문맥 연결(문구/기본 선택 흐름) 요구사항을 보강한다.

## Impact

- Backend:
  - `landing/views.py`
  - `landing/mailers.py`
  - 필요 시 리드마그넷 공통 카피/섹션 유틸
- Frontend/Template:
  - `landing/templates/landing/partials/lead_magnet_form.html`
  - `landing/templates/landing/lead_magnet_report_preview.html`
- Test:
  - `landing/tests/test_contact_form.py`
  - `landing/tests/test_landing_pages.py`
  - `landing/tests/test_lead_magnet_sections.py`
- Spec:
  - `openspec/specs/lead-magnet-email-followup/spec.md`
  - `openspec/specs/lead-magnet-cta-report-format/spec.md`
  - `openspec/specs/lead-magnet-result-bridging/spec.md`
