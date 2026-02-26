## Why

현재 무료 AX 진단은 자동화 준비도를 빠르게 파악하는 데는 유효하지만, 진단 축이 제한적이라 사용자 상황을 충분히 세분화하지 못한다. 문항 축을 다면화해 운영 맥락, 병목, 데이터 상태, 자동화 난이도, 실행 준비도를 함께 반영해야 결과 리포트가 실제 실행 계획으로 연결된다.

## What Changes

- 무료 AX 진단 문항을 다축(최소 5축)으로 개편한다:
  - 업무/운영 맥락(예: 리드관리, 콘텐츠 운영, 고객 응대, 내부 협업)
  - 반복 불편/병목(복붙, 누락, 승인 지연, 응답 지연, 데이터 분산)
  - 데이터 정합성/가시성(한곳 관리 여부, 상태값 표준화, 집계 가능성)
  - 자동화 적합도(규칙형/판단형, 빈도, 오류 비용, 알림 필요성)
  - 실행 준비도(담당자, 도입 의지, 2주 내 실험 가능성, 운영 점검 루틴)
- 진단 결과를 단순 점수 외에 세부 유형별로 분류한다:
  - 업무 운영 유형
  - 병목 위험 유형
  - 자동화 우선순위 유형
  - 실행 준비도 유형
  - 추천 실행 방식(즉시 적용, 2주 실행, 고도화 과제)
- 결과 메시지(화면/메일)에서 체크 항목 기반 설명을 강화한다.
- 기존 A/B/C 등급은 유지하되, 등급 내부에서도 체크 패턴에 따라 제안 내용을 달리한다.

## Capabilities

### New Capabilities

- `ax-diagnosis-question-segmentation`: 업무 맥락/병목/데이터/자동화 적합도/실행 준비도를 함께 수집하는 다축 진단 문항 체계와 분류 로직 정의
- `ax-diagnosis-result-personalization`: 체크 패턴 기반으로 결과 리포트/추천 툴/실행 우선순위를 세분화하는 규칙 정의

### Modified Capabilities

- `founder-lead-magnet-capture`: 무료 진단 폼의 질문 구조를 기존 단일 축에서 업무+불편 혼합 구조로 변경
- `lead-magnet-result-bridging`: 진단 결과를 등급 중심 CTA에서 유형별 실행 제안까지 포함하는 브릿지로 확장
- `lead-magnet-email-followup`: 후속 메일 리포트를 체크 패턴 기반 개인화 문구로 강화

## Impact

- Backend:
  - `landing/forms.py` (질문 필드/검증 구조 개편)
  - `landing/views.py` (점수/분류/결과 생성 로직 개편)
  - `landing/ax_tool_stack.py` (질문-툴 매핑 및 우선순위 매핑 확장)
  - `landing/mailers.py` (개인화 리포트 템플릿 데이터 반영)
- Frontend:
  - `landing/templates/landing/partials/lead_magnet_form.html` (문항 UI 재구성)
  - `landing/templates/landing/free_diagnosis.html` (결과 섹션 세분화)
  - `landing/templates/landing/lead_magnet_report_preview.html` (개인화 리포트 반영)
- Test:
  - `landing/tests/test_contact_form.py`
  - `landing/tests/test_landing_pages.py`
