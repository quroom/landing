## Why

무료 진단 설문 문항과 결과 메시지 시뮬레이션의 표현 수준이 섞여 있어, 사용자 입장에서 질문 의도와 결과 해석이 자연스럽게 연결되지 않는 구간이 있다.  
지금 시점에서 문항을 더 단순하고 일관된 언어로 정리하고, 결과 카피를 문항 의도와 1:1로 맞춰 전환 신뢰도를 높일 필요가 있다.

## What Changes

- 설문 화면에서 카테고리 그룹 노출을 제거하고, 질문만 순차적으로 선택하도록 단순화한다.
- 문항은 `핵심 4개 우선` + `추가 4개 선택` 구조로 재배치해 응답 부담을 줄이되, 각 항목별 응답 데이터는 유지한다.
- 설문 문항(특히 q1~q8)의 표현을 대중적인 문장으로 단순화하고, 같은 카테고리 내 문항 결(관점/행동 단위/난이도)을 통일한다.
- `하고 있지 않음` 응답이 많은 항목 중 사업 임팩트가 큰 항목을 우선 추천하는 규칙을 결과 생성 로직에 반영한다.
- 무료 진단 결과 메시지 시뮬레이션(요약/카테고리 메시지/2주 작업/완료 기준)을 문항 의도 및 우선추천 규칙과 정합되게 재작성한다.
- preview/이메일 결과 카피 계약을 유지하면서, 문항-결과 매칭 규칙 회귀를 방지하는 검증 기준을 강화한다.

## Capabilities

### New Capabilities
- 없음

### Modified Capabilities
- `founder-lead-magnet-capture`: 설문 표시 방식을 카테고리 노출형에서 질문 순차 선택형으로 조정하고, 핵심 4문항 우선 흐름을 반영한다.
- `ax-diagnosis-question-segmentation`: 축별 문항을 단순한 표현으로 재정렬하고, 4+4 단계형 응답 구조에서 축 계산 일관성을 유지한다.
- `ax-diagnosis-result-personalization`: 미실행 항목 비중과 사업 임팩트를 함께 고려한 우선추천 규칙을 반영하고, 메시지 매칭을 강화한다.
- `ax-diagnosis-priority-one-action`: 우선 실행 1개 추천 기준을 `미실행 항목 우선 + 사업 임팩트` 규칙으로 명확화한다.
- `lead-magnet-cta-report-format`: 시뮬레이션 리포트 카피를 단순화된 문항 구조에 맞게 정리하고 채널 간 일관성을 유지한다.
- `lead-magnet-email-followup`: 이메일 본문 해석 문구를 설문/시뮬레이션과 동일한 의미 체계로 동기화한다.

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
  - `openspec/changes/improve-free-diagnosis-survey-and-result-simulation-copy/specs/**/spec.md`
