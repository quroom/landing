## Why

리드마그넷 진단은 제출/메일 발송까지는 동작하지만, 전환 병목을 정량으로 파악하고 개선 실험을 반복할 수 있는 측정 체계가 약합니다. 지금 단계에서 퍼널 지표 정의와 실험 루프를 명확히 만들어야 전환 개선을 안정적으로 누적할 수 있습니다.

## What Changes

- 리드마그넷 퍼널을 단계별(진입/작성/제출/메일성공/상담전환)로 측정하는 공통 지표 계약을 추가한다.
- 관리자 화면에서 기간별 전환율, 이탈 구간, 메일 발송 성공률을 확인할 수 있는 집계 뷰를 강화한다.
- CTA/카피/노출 구조 개선을 위한 실험 단위를 정의하고, 실험군별 성과 비교가 가능하도록 이벤트 메타를 확장한다.
- 전환 개선 실험이 리포트/메일 계약을 깨지 않도록 최소 회귀 검증 기준을 추가한다.

### Measurement Scope (Detailed)

- Primary KPI를 아래 3개로 고정한다.
  - `submit_rate = lead_magnet_submit / lead_magnet_start`
  - `mail_success_rate = lead_magnet_email_sent_user / lead_magnet_submit`
  - `contact_conversion_rate = contact_submit(lead_context=lead_magnet_diagnosis) / lead_magnet_email_sent_user`
- 보조 KPI를 아래로 고정한다.
  - `home_to_start_rate = lead_magnet_start / lp_view(page_key=home)`
  - `grade_distribution = count(grade=A/B/C)`
- 이벤트 파라미터 표준을 고정한다.
  - 필수 키: `event_name`, `page_key`, `lead_source`
  - 진단 키: `score`, `grade`
  - 컨텍스트 키: `inquiry_type`, `lead_context`
  - 유입 키: `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`
- 메일 이벤트는 운영 목적에 따라 분리한다.
  - `lead_magnet_email_sent_user`: 사용자 결과 메일 성공 이벤트 (KPI 분자용)
  - `lead_magnet_email_sent_admin`: 관리자 알림 메일 성공 이벤트 (운영 모니터링용)
- KPI 계산에서 관리자 알림 메일 이벤트는 제외한다(성공률 100% 초과 방지).
- GA4 커스텀 디멘션 대상 키를 고정한다.
  - `grade`, `lead_source`, `page_key`, `inquiry_type`, `lead_context`
- 운영 리포트(주간) 기준 뷰를 고정한다.
  - 퍼널 5단계 요약
  - `utm_campaign`/`lead_source`별 전환 비교
  - `grade`별 전환 비교

### MVP Dashboard (Immediate Setup)

- 내부 대시보드에 아래 4개 카운트를 단일 카드 묶음으로 노출한다.
  - `start`: `lead_magnet_start`
  - `submit`: `lead_magnet_submit`
  - `mail_sent`: `lead_magnet_email_sent`
  - `contact_submit`: `contact_submit(lead_source=founder_contact_from_diagnosis)`
- 내부 대시보드에서 아래 3개 비율을 즉시 계산해 노출한다.
  - `submit_rate = submit / start`
  - `mail_success_rate = mail_sent / submit`
  - `contact_conversion_rate = contact_submit / mail_sent`
- 분모 0인 경우 비율은 `0.0%`로 처리한다(에러/NaN 금지).
- 1차 목표는 “의사결정용 간단 확인 대시보드”이며, 실험/세그먼트 심화는 후속 단계로 분리한다.

### Rollout Plan (Practical)

1. 이벤트 명/파라미터 키를 고정하고 문서화한다.
2. 관리자 대시보드에 퍼널 카운트+비율을 먼저 배치한다.
3. 주간 리뷰 2회 운영 후, 병목 구간(제출 전/메일 전/상담 전)을 우선순위로 확정한다.
4. 그 다음에만 GA4 탐색 리포트/실험 메타 확장을 진행한다.

### Security & Privacy Guardrails

- GA4/내부 이벤트 메타에는 이메일/이름/연락처 등 직접 식별자(PII)를 포함하지 않는다.
- 전환 리포트는 집계 단위로만 공유하고, 개별 문의 원문/개인정보는 관리자 권한에서만 조회한다.
- KPI 계산 대상 이벤트(`*_user`)와 운영 알림 이벤트(`*_admin`)를 분리해 지표 왜곡과 데이터 오남용을 방지한다.

## Capabilities

### New Capabilities
- `lead-magnet-conversion-measurement`: 리드마그넷 퍼널 지표 정의, 수집, 비교 리포트 기준

### Modified Capabilities
- `founder-lead-magnet-capture`: 진입/제출 이벤트 메타를 전환 분석 가능한 형태로 확장
- `lead-magnet-result-bridging`: 결과 노출에서 CTA 브리지 단계의 전환 추적 기준 보강
- `lead-magnet-email-followup`: 메일 성공/실패 및 후속 액션 전환 지표 계약 보강
- `lead-magnet-admin-segmentation`: 관리자 preview/대시보드에서 전환 관점 집계와 비교 기준 추가

## Impact

- Backend:
  - `landing/views.py`
  - `landing/mailers.py`
  - `landing/analytics.py`
- Admin/Template:
  - `landing/templates/landing/lead_magnet_report_preview.html`
  - `landing/templates/landing/admin_dashboard.html`
- Documentation:
  - `codex-document/ga4-setup-manual.md` (측정 정의/운영 기준)
- Tests:
  - `landing/tests/test_landing_pages.py`
  - `landing/tests/test_contact_form.py`
  - `landing/tests/test_lead_magnet_sections.py`
  - `landing/tests/test_views.py`
- Spec delta:
  - `openspec/changes/measure-and-optimize-lead-magnet-conversion/specs/**/spec.md`
