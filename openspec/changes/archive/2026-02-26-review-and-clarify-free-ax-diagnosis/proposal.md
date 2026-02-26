## Why

무료 자동화 실행 진단의 결과 메시지가 여전히 길고 추상적인 부분이 있어, 사용자가 "지금 무엇을 해야 하는지"를 즉시 판단하기 어렵다. 진단 축을 단순화하고 등급별/카테고리별 응답을 명확히 해서 2주 실행 전환률을 높여야 한다.

## What Changes

- 진단 축을 5개 혼합 구조에서 4개 카테고리 구조로 명확히 재정의한다.
- 카테고리별 A/B/C 해석(총 4x3 패턴)을 결과 카드/리포트/메일에 일관 적용한다.
- 2주 실행 제안은 여러 개 목록 대신 "우선 1개 실행 과제"만 제시한다.
- 추천 툴은 과도한 나열을 줄이고 우선 과제 중심의 핵심 툴 소수만 노출한다.
- 메일 본문을 등급별 안내 + 단일 다음 행동 CTA 중심으로 재작성한다.

## Capabilities

### New Capabilities

- `ax-diagnosis-priority-one-action`: 진단 결과에서 2주 실행 우선 1개 과제를 강제 제안하는 출력 규칙

### Modified Capabilities

- `ax-diagnosis-question-segmentation`: 진단 카테고리를 4개 축으로 재구성하고 질문 매핑을 변경
- `ax-diagnosis-result-personalization`: 카테고리별 A/B/C 응답 분기를 포함한 개인화 결과 포맷으로 변경
- `lead-magnet-cta-report-format`: "다음 액션" 문구를 명확한 실행/상담 안내로 정리한 리포트 포맷으로 변경
- `lead-magnet-email-followup`: 등급별 안내 문구 + 우선 1개 실행 과제 + 단일 CTA 구조로 메일 포맷 변경

## Impact

- Backend:
  - `landing/ax_tool_stack.py`
  - `landing/views.py`
  - `landing/mailers.py`
- Frontend:
  - `landing/templates/landing/free_diagnosis.html`
  - `landing/templates/landing/partials/lead_magnet_form.html`
  - `landing/templates/landing/lead_magnet_report_preview.html`
- Tests:
  - `landing/tests/test_contact_form.py`
  - `landing/tests/test_landing_pages.py`
