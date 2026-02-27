## Why

설문에서 카테고리 노출을 제거했지만, `free-diagnosis/preview/`와 결과 문구에는 여전히 4개 분류형 보완 포인트와 `우선 항목` 표현이 남아 있어 응답 체감과 리포트 해석이 어긋난다.  
또한 2주 내 끝낼 작업의 완료 기준 문구와 진단 결과 메시지에 중복/불필요 표현이 남아 검토 피로가 높으므로, 응답-결과 매핑을 더 단일하고 명확한 문장 계약으로 정리할 필요가 있다.

## What Changes

- `free-diagnosis/preview/` 결과 카드에서 4개 분류형 보완 포인트 블록을 제거하고, 핵심 보완 포인트 1개 중심으로 노출을 단순화한다.
- 핵심 보완 포인트 보조 문구에서 `우선 항목: ...` 노출을 제거해 사용자 노출 문장을 행동 가이드 중심으로 정리한다.
- 2주 내 끝낼 작업의 완료 기준 문구를 intent별로 중복 없이 재작성해 같은 문장 반복을 줄이고 실행 기준을 구체화한다.
- 진단 결과 메시지에서 의사결정에 기여하지 않는 중복/부연 문장을 제거해 핵심 안내만 남긴다.
- `free-diagnosis/preview/`에서 제목 외 응답 본문이 동일한 시나리오는 하나로 묶어 표시해 검토 효율을 높인다.
- 웹 결과/preview/이메일 공통 섹션 계약과 스냅샷 테스트를 갱신해 채널 간 카피 일관성을 유지한다.

## Capabilities

### New Capabilities

- 없음

### Modified Capabilities

- `ax-diagnosis-result-personalization`: 핵심 보완 포인트 해석 문구에서 내부 우선 항목 노출을 제거하고 응답 의도 기반 안내만 유지한다.
- `ax-diagnosis-priority-one-action`: 2주 실행 과제 완료 기준 문구를 intent별로 중복 없이 구체화한다.
- `lead-magnet-cta-report-format`: preview 리포트에서 4개 분류형 보완 포인트 노출을 제거하고 핵심 보완 포인트 1개 중심 형식으로 정렬하며, 제목 외 응답 본문이 같은 케이스를 묶어 보여준다.
- `lead-magnet-email-followup`: 웹/preview에서 갱신된 핵심 보완 포인트/완료 기준 문구 계약을 이메일에도 동일하게 반영한다.

## Impact

- Backend:
  - `landing/views.py`
  - `landing/lead_magnet_sections.py`
  - `landing/mailers.py`
- Frontend/Template:
  - `landing/templates/landing/lead_magnet_report_preview.html`
  - `landing/templates/landing/partials/lead_magnet_form.html` (필요 시 동일 용어 정렬)
- Tests:
  - `landing/tests/test_landing_pages.py`
  - `landing/tests/test_views.py` (preview 묶음 표시 검증 추가 시)
  - `landing/tests/test_lead_magnet_sections.py`
  - `landing/tests/test_contact_form.py`
- Spec delta:
  - `openspec/changes/align-free-diagnosis-report-with-answers/specs/**/spec.md`
