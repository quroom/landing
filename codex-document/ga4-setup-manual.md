# GA4 측정 정보 매뉴얼 (리드마그넷 전환 최적화용)

이 문서는 “설치 방법”이 아니라, **무엇을 측정하고 어떤 기준으로 판단할지**를 정리합니다.
현재 코드는 내부 이벤트(`FunnelEvent`)를 이미 저장하고 있으므로, GA4는 채널/캠페인 분석 중심으로 병행합니다.

## 1) 측정 목표 (Primary KPI)

리드마그넷 퍼널의 핵심 KPI는 아래 3개로 고정합니다.

1. `submit_rate` = `lead_magnet_submit / lead_magnet_start`
2. `mail_success_rate` = `lead_magnet_email_sent_user / lead_magnet_submit`
3. `contact_conversion_rate` = `contact_submit(lead_context=lead_magnet_diagnosis) / lead_magnet_email_sent`

권장 보조 KPI:
- `home_to_start_rate` = `lead_magnet_start / lp_view(page_key=home)`
- 등급 분포: `grade(A/B/C)`
- 제출 후 이탈률: `1 - mail_success_rate`

주의:
- `lead_magnet_email_sent`를 관리자 알림 메일까지 포함해 집계하면 성공률이 100%를 초과할 수 있습니다.
- KPI 산식에서는 반드시 **사용자 발송 성공 이벤트(`lead_magnet_email_sent_user`)만** 분자로 사용합니다.

## 2) 현재 이벤트 소스(코드 기준)

현재 서버 코드에서 수집되는 핵심 이벤트:

- `lp_view`
- `lead_magnet_start`
- `lead_magnet_submit` (metadata: `score`, `grade`)
- `lead_magnet_email_sent` (metadata: `grade`)
- `contact_submit` (metadata: `inquiry_type`, `marketing_opt_in`)

UTM 파라미터(`utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`)는 `track_event()`에서 자동 병합됩니다.

## 3) GA4에서 관리할 측정 정보 (권장 Event Schema)

GA4에는 아래 이벤트를 최소 반영합니다.

- `lead_magnet_start`
  - params: `page_key`, `lead_source`, `utm_source`, `utm_medium`, `utm_campaign`
- `lead_magnet_submit`
  - params: `score`, `grade`, `lead_source`, `utm_*`
- `lead_magnet_email_sent_user`
  - params: `grade`, `lead_source`, `utm_*`
- `lead_magnet_email_sent_admin`
  - params: `lead_source`, `utm_*`
- `lead_magnet_contact_submit`
  - params: `inquiry_type`, `lead_context`, `lead_source`, `utm_*`

주의:
- GA4 이벤트명은 영문 스네이크/소문자 유지
- `grade`는 `A/B/C`로 고정
- `lead_source` 값셋은 운영 중 변경 금지(리포트 분산 방지)

## 4) 커스텀 정의 (GA4 Admin)

GA4에서 커스텀 디멘션 등록 권장:

- Event-scoped:
  - `grade`
  - `lead_source`
  - `page_key`
  - `inquiry_type`
  - `lead_context`

등록 후 실시간/탐색 리포트에서 필터 가능 여부 확인합니다.

## 5) 대시보드 기준 뷰 (주간 운영)

주간 리뷰에서는 아래 4개 표만 고정 운영합니다.

1. 퍼널 요약: `lp_view -> lead_magnet_start -> lead_magnet_submit -> lead_magnet_email_sent -> contact_submit`
2. 채널별 전환: `utm_source/medium/campaign`별 `submit_rate`, `contact_conversion_rate`
3. 등급별 전환: `grade`별 `mail_success_rate`, `contact_conversion_rate`
4. 리드소스별 성과: `lead_source`별 볼륨/전환

## 6) 운영 규칙 (중요)

- 이벤트명/파라미터 키는 월간 1회만 변경 검토
- 지표 정의 수식은 문서 고정(임의 변경 금지)
- GA4 수치와 내부 DB 수치가 다르면 내부 DB를 기준으로 원인 분석
- 실험(카피/CTA) 전에는 반드시 비교 대상 기간과 성공 KPI를 먼저 고정
- 사용자 KPI는 `*_user` 이벤트만 기준으로 계산하고, 관리자 알림 이벤트는 운영 알림 지표로 분리한다.

## 7) 보안/개인정보 가드레일

- GA4 이벤트 파라미터에는 이메일/이름/연락처 등 직접 식별자(PII)를 전송하지 않는다.
- `lead_source`, `grade`, `inquiry_type`, `lead_context`, `utm_*` 같은 비식별 메타만 사용한다.
- 관리자 대시보드는 스태프 권한에서만 접근 가능하도록 유지한다.
- 전환 분석 원본(내부 DB) 조회 권한은 최소 권한 원칙으로 제한한다.
- 외부 공유 리포트에는 집계값만 포함하고 개별 문의 데이터는 제외한다.

## 8) 바로 적용할 체크리스트

- [ ] GA4 커스텀 디멘션 등록 (`grade`, `lead_source`, `page_key`, `inquiry_type`, `lead_context`)
- [ ] 탐색 보고서에 퍼널 5단계 템플릿 생성
- [ ] 채널(utm_campaign) 필터 기준 통일
- [ ] 주간 리뷰용 KPI 표(위 3개 Primary KPI) 템플릿 확정
- [ ] `lead_magnet_email_sent_user` / `lead_magnet_email_sent_admin` 이벤트 분리 적용 여부 점검
