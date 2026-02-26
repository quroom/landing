## Why

현재 무료 AX 진단 결과는 정보량이 많아 핵심 액션이 묻히고, 화면/메일 모두 가독성이 떨어져 전환 유도력이 낮다. 우선순위를 축소하고 메시지 구조를 간결화해, 사용자가 즉시 상담 CTA로 이동하도록 리포트 흐름을 재정비해야 한다.

## What Changes

- 진단 결과 우선순위 제안을 `Top 5`에서 `Top 3`으로 축소한다.
- 결과 UI와 메일 본문에서 항목 간 개행/간격을 늘려 가독성을 개선한다.
- 메일 텍스트 및 HTML의 줄간격(line-height)과 블록 간 간격을 조정한다.
- 리포트 preview가 실제 등급/점수 기준과 동일한 계산/표시 로직을 사용하도록 정합성을 맞춘다.
- 리포트 내용을 장문 나열형에서 CTA 유도형(핵심 진단 + 즉시 실행 3개 + 상담 유도)으로 재구성한다.

## Capabilities

### New Capabilities

- `lead-magnet-cta-report-format`: 진단 리포트를 CTA 중심 구조로 압축하는 출력 포맷 정의

### Modified Capabilities

- `ax-diagnosis-result-personalization`: 결과 개인화 출력을 Top 3 우선순위 중심으로 조정
- `lead-magnet-result-bridging`: 등급별 브릿지 메시지를 짧고 행동 유도 중심으로 개선
- `lead-magnet-email-followup`: 메일 본문/HTML 가독성 및 CTA 유도 구조로 재작성

## Impact

- Backend:
  - `landing/views.py` (Top 3 산출/메시지 포맷/preview 정합성)
  - `landing/mailers.py` (메일 레이아웃/줄간격/CTA 섹션)
- Frontend:
  - `landing/templates/landing/partials/lead_magnet_form.html` (결과 표시 개행/간격)
  - `landing/templates/landing/lead_magnet_report_preview.html` (preview 표기 정합성)
- Test:
  - `landing/tests/test_contact_form.py`
  - `landing/tests/test_landing_pages.py`
