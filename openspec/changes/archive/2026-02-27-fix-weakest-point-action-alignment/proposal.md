## Why

현재 무료 진단 결과에서 `핵심 보완 포인트`와 `2주 내 끝낼 작업 1개`가 서로 다른 의도로 생성되는 경우가 있어 사용자 신뢰를 떨어뜨립니다.  
또한 8문항 진단임에도 4문항만으로 결과가 생성되는 경로가 남아 있어, 결과 해석과 비교 기준이 일관되지 않습니다.

## What Changes

- 핵심 보완 포인트와 2주 실행 과제가 동일한 진단 근거(동일 질문 의도/축)에서 생성되도록 우선순위 로직을 정렬한다.
- 보완 포인트 문구와 실행 과제 문구가 서로 충돌하지 않도록 intent 기반 매핑 규칙을 단일 경로로 통합한다.
- `free-diagnosis/preview/`와 고객 이메일 본문이 동일한 섹션 계약(요약/보완 포인트/2주 과제/CTA)을 사용하도록 정합성을 강화한다.
- 진단 제출 시 8문항 전체 응답을 필수로 고정하고, 4문항 간단 진단 경로/라벨/검증을 제거한다.
- 폼 안내 문구, 결과 라벨, 테스트 스냅샷을 8문항 필수 기준으로 갱신한다.

## Capabilities

### New Capabilities

- 없음

### Modified Capabilities

- `ax-diagnosis-priority-one-action`: 2주 실행 과제가 핵심 보완 포인트와 같은 근거에서 선택되도록 우선순위/선정 규칙을 조정한다.
- `ax-diagnosis-result-personalization`: 보완 포인트 해석 문구와 실행 과제 문구의 매칭 규칙을 단일화해 결과 정합성을 높인다.
- `founder-lead-magnet-capture`: 8문항 전체 필수 응답으로 진단 입력 계약을 변경한다.
- `lead-magnet-cta-report-format`: preview 결과 카드가 메일 본문과 동일한 섹션 계약을 따르도록 검증 기준을 강화한다.
- `lead-magnet-email-followup`: 이메일 본문이 preview와 같은 보완 포인트/2주 과제 조합을 사용하도록 동기화한다.

## Impact

- Backend:
  - `landing/ax_tool_stack.py`
  - `landing/forms.py`
  - `landing/views.py`
  - `landing/lead_magnet_sections.py`
  - `landing/mailers.py`
- Frontend/Template:
  - `landing/templates/landing/partials/lead_magnet_form.html`
  - `landing/templates/landing/free_diagnosis.html`
  - `landing/templates/landing/lead_magnet_report_preview.html`
- Test:
  - `landing/tests/test_contact_form.py`
  - `landing/tests/test_lead_magnet_sections.py`
  - `landing/tests/test_landing_pages.py`
  - `landing/tests/test_views.py`
- Spec delta:
  - `openspec/changes/fix-weakest-point-action-alignment/specs/**/spec.md`
