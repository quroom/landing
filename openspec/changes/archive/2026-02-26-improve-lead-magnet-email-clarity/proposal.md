## Why

현재 무료 진단 메일은 내용이 길고 표현이 복잡해, 창업가가 핵심을 빠르게 이해하기 어렵다.  
무료 진단은 창업가 대상 흐름이므로, 메일도 창업가 관점의 쉬운 표현과 짧은 구조로 정리해야 한다.

## What Changes

- 무료 진단 결과 메일 톤을 `창업가 실행 관점`으로 통일한다.
- 메일 구조를 `진단 요약 -> 2주 실행 1개 -> 다음 행동`으로 고정한다.
- 카테고리 결과는 `핵심 취약 카테고리 1개`만 기본 노출하고, 전체 4개는 선택 노출로 전환한다.
- 어려운 용어를 제거하고, 짧고 쉬운 문장으로 바꾼다.
- 외국인 개발자 관련 문구는 무료 진단 메일에서 제거한다.
- 등급(A/B/C)과 카테고리 분기는 유지하되, 문구를 창업가가 바로 실행 가능한 표현으로 바꾼다.
- 메일 발신자 표시 이름은 `help`가 아니라 `큐룸`으로 고정한다.

## Capabilities

### New Capabilities

- `lead-magnet-founder-only-copy`: 무료 진단 메일을 창업가 전용 카피로 운영하는 정책

### Modified Capabilities

- `lead-magnet-email-followup`: 창업가 관점으로 메일 본문/HTML 카피 구조를 단순화
- `lead-magnet-cta-report-format`: 리포트-메일 연결 문구를 쉬운 용어로 정리

## Impact

- Backend:
  - `landing/mailers.py`
  - `landing/views.py` (리포트/CTA 문구 동기화 범위)
  - `landing/project/settings.py` 또는 `.env` (발신자 표시 이름 설정)
- Test:
  - `landing/tests/test_contact_form.py`
  - 필요 시 `landing/tests/test_landing_pages.py`
- Spec:
  - `openspec/specs/lead-magnet-email-followup/spec.md`
  - `openspec/specs/lead-magnet-cta-report-format/spec.md`
