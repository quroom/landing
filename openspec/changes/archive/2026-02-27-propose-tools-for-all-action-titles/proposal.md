## Why

현재 AX 진단 결과는 우선 실행 1개 중심으로는 명확하지만, `tools_map`에 정의된 8개 intent 전부를 사용자에게 충분히 노출하지 못해 선택지가 좁게 느껴진다.  
진단 신뢰도와 실행 전환율을 높이려면, 설문 결과의 심각도 기준을 유지하면서도 결과 응답 패턴을 최소 8종으로 확장하고 8개 툴 제안 축을 모두 커버해야 한다.

## What Changes

- 진단 결과 응답 패턴을 “심각도 기반”으로 최소 8종 이상으로 확장한다.
- `tools_map`의 8개 intent(`action_titles`와 매핑되는 항목)가 결과 집합에서 누락 없이 제안되도록 규칙을 추가한다.
- 결과 구조는 사용자 노출 기준 `우선 실행 1개`로 고정하되, 내부 패턴/검증 기준에서는 8개 intent가 전체적으로 누락되지 않도록 유지한다.
- preview/이메일/웹 결과에서 동일한 응답 패턴 계약을 사용하도록 정렬한다.
- 회귀 테스트에 “8종 응답 패턴 존재”와 “8 intent 커버리지 보장” 검증을 추가한다.

## Capabilities

### New Capabilities

- 없음

### Modified Capabilities

- `ax-diagnosis-priority-one-action`: 우선 실행 1개 선정은 유지하되, 심각도 기반 결과 패턴 확장 규칙과 함께 동작하도록 변경한다.
- `ax-diagnosis-result-personalization`: 개인화 결과 카피를 최소 8종 응답 패턴으로 확장하고 intent 커버리지 규칙을 반영한다.
- `lead-magnet-cta-report-format`: 웹/preview 결과 포맷에서 우선 실행 1개 노출 원칙은 유지하고, 내부적으로는 8종 패턴/8 intent 커버리지를 일관되게 관리하도록 변경한다.
- `lead-magnet-email-followup`: 이메일 결과도 동일한 8종 응답 패턴/intent 커버리지 계약을 따르도록 동기화한다.

## Impact

- Backend:
  - `landing/views.py`
  - `landing/lead_magnet_sections.py`
  - `landing/mailers.py`
- Frontend/Template:
  - `landing/templates/landing/partials/lead_magnet_form.html` (필요 시 결과 안내 문구 보완)
  - `landing/templates/landing/lead_magnet_report_preview.html`
- Tests:
  - `landing/tests/test_lead_magnet_sections.py`
  - `landing/tests/test_contact_form.py`
  - `landing/tests/test_landing_pages.py`
  - `landing/tests/test_views.py`
- Spec delta:
  - `openspec/changes/propose-tools-for-all-action-titles/specs/**/spec.md`
