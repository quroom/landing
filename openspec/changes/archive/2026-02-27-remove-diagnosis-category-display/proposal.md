## Why

현재 진단은 카테고리(축) 단위로 문항을 묶어 해석하지만, 같은 카테고리 안에서도 질문 결(행동 수준/난이도/관점)이 달라 결과 메시지와 체감이 어긋나는 문제가 반복된다.  
진단 신뢰도를 높이기 위해 카테고리 중심 노출/해석 의존을 줄이고, 질문 의도 기반으로 결과를 일치시키는 정리가 필요하다.

## What Changes

- 설문 화면에서 카테고리 라벨/설명 노출을 제거하고 질문 중심 UI를 유지한다.
- q1~q8 문항을 질문 의도(intent) 기준으로 재정렬하고, 같은 흐름의 질문끼리 표현 결을 통일한다.
- 결과 메시지 생성을 카테고리명 중심에서 질문 의도 매핑 중심으로 전환해 진단 결과 일치도를 높인다.
- 핵심 보완 안내/2주 우선과제/추천 툴 문구를 동일한 intent key를 기준으로 생성해 채널 간 드리프트를 줄인다.
- preview/email/웹 결과의 공통 섹션 계약은 유지하되, 카테고리 기반 표현이 과도하게 드러나는 부분을 정리한다.

## Capabilities

### New Capabilities
- 없음

### Modified Capabilities
- `founder-lead-magnet-capture`: 진단 화면에서 카테고리 노출 없이 질문 중심 흐름을 고정한다.
- `ax-diagnosis-question-segmentation`: 문항을 카테고리명보다 질문 의도 기준으로 재정렬하고 결을 통일한다.
- `ax-diagnosis-result-personalization`: 결과 해석/추천 로직을 질문 의도 매핑 기준으로 정합되게 조정한다.
- `lead-magnet-cta-report-format`: 결과 시뮬레이션에서 카테고리 의존 표현을 줄이고 실행 안내를 intent 기반으로 구성한다.
- `lead-magnet-email-followup`: 이메일 해석 문구를 웹/시뮬레이션과 같은 intent 기준으로 동기화한다.

## Impact

- Backend:
  - `landing/ax_tool_stack.py`
  - `landing/views.py`
  - `landing/lead_magnet_sections.py`
  - `landing/mailers.py`
- Frontend/Template:
  - `landing/templates/landing/partials/lead_magnet_form.html`
  - `landing/templates/landing/lead_magnet_report_preview.html`
- Test:
  - `landing/tests/test_lead_magnet_sections.py`
  - `landing/tests/test_contact_form.py`
  - `landing/tests/test_landing_pages.py`
- Spec delta:
  - `openspec/changes/remove-diagnosis-category-display/specs/**/spec.md`
