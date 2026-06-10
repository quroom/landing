# GA4 Attribution Setup

## 목적

네이버 광고 유입의 `contact_submit` 전환을 GA4에서 소재, 키워드, 광고그룹 기준으로 분석한다. 메일 수신은 알림이고, 성과 판단의 기준은 GA4 key event와 event-scoped custom dimensions로 둔다.

## 전송 이벤트

브라우저는 HTMX 문의 제출 성공 후 다음 이벤트를 GA4로 전송한다.

- `contact_submit`: 문의 폼 제출 성공
- `lead_magnet_submit_user`: 리드마그넷 제출 성공

전송 위치:

- `landing/static/landing/js/site.js`

광고 링크로 유입된 값은 `sessionStorage`에 보존하고, 폼 hidden field가 비어 있으면 자동으로 채운다. 사용자가 광고 랜딩 후 같은 세션에서 다른 화면을 거쳐 문의해도 전환 이벤트에 광고 문맥이 붙도록 하기 위함이다.

## GA4 Custom Dimensions

GA4에서 아래 항목을 `Event` scope custom dimension으로 생성한다. Parameter name은 코드에서 보내는 이름과 정확히 같아야 한다.

| Dimension name | Event parameter | 용도 |
| --- | --- | --- |
| Lead source | `lead_source` | 네이버 광고/일반 문의/리드마그넷 유입 구분 |
| Ad campaign | `ad_campaign` | 네이버 캠페인 코드 |
| Ad group | `ad_group` | 광고그룹 코드 |
| Ad creative | `ad_creative` | 소재 코드 |
| Ad keyword | `ad_keyword` | 키워드 또는 구매 키워드 |
| Landing variant | `landing_variant` | 랜딩 문구 variant |
| UTM content | `utm_content` | 소재/그룹 분석 보조축 |

`utm_source`, `utm_medium`, `utm_campaign`, `utm_term`은 GA4 기본 유입 차원으로 먼저 확인한다. 이벤트 단위로 꼭 필요할 때만 custom dimension을 추가해 quota를 아낀다.

## GA4 설정 순서

1. GA4 Admin에서 `contact_submit` 이벤트를 key event로 표시한다.
2. Admin > Custom definitions에서 위 custom dimensions를 생성한다.
3. 광고 링크로 접속해 문의 테스트를 1건 보낸다.
4. Admin > DebugView 또는 Reports > Realtime에서 `contact_submit` 이벤트와 파라미터가 들어오는지 확인한다.
5. Explore > Free form에서 rows에 `Ad group`, `Ad creative`, `Ad keyword`, `UTM content`를 두고 metric은 `Key events` 또는 `Event count`를 본다.

## 운영 기준

- GA4에는 이름, 이메일, 전화번호, 문의 본문을 보내지 않는다.
- `ad_keyword`에는 광고 운영 키워드만 넣는다.
- 소재 성과 비교는 최소 주 1회, `contact_submit` key event 기준으로 본다.
- 유효 문의율은 GA4만으로 판단하기 어렵기 때문에 메일/CRM에서 별도 태깅해 후속 지표로 관리한다.
