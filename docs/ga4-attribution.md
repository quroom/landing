# GA4 Attribution and UTM Setup

## 목적

네이버, 구글, 링크드인, 스레드 등 모든 유입을 같은 UTM 규칙으로 태깅하고 `contact_submit` 전환을 GA4에서 채널, 캠페인, 키워드, 소재 기준으로 분석한다. 메일 수신은 알림이고, 성과 판단의 기준은 GA4 key event와 traffic-source dimensions, event-scoped custom dimensions로 둔다.

공식 기준:

- GA4는 광고/캠페인 URL에 붙은 UTM 값을 traffic-source dimensions로 처리한다.
- 수동 태깅을 쓰면 `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`가 GA4의 manual source/medium/campaign/term/content 계열 차원으로 들어간다.
- 커스텀 이벤트 파라미터를 리포트와 Explore에서 쓰려면 GA4 Admin에서 custom dimension으로 등록해야 한다.

참고:

- https://support.google.com/analytics/answer/10917952
- https://support.google.com/analytics/answer/11242870
- https://developers.google.com/analytics/devguides/collection/ga4/event-parameters

## UTM 기본 규칙

모든 외부 유입 링크에는 아래 5개 UTM을 우선 붙인다.

| UTM parameter | 필수 | 의미 | 예시 |
| --- | --- | --- | --- |
| `utm_source` | 필수 | 유입 플랫폼/매체명 | `naver`, `google`, `linkedin`, `threads`, `newsletter` |
| `utm_medium` | 필수 | 유입 방식 | `cpc`, `organic_social`, `paid_social`, `referral`, `email`, `dm` |
| `utm_campaign` | 필수 | 캠페인 코드 | `app_dev`, `homepage_dev`, `founder_network_2026q2` |
| `utm_term` | 선택 | 검색 키워드/타깃 키워드 | `앱개발비용`, `{keyword}` |
| `utm_content` | 선택 | 소재/버튼/게시물/광고그룹 구분 | `app_cost_scope_first`, `linkedin_post_20260610_a` |

운영 원칙:

- 값은 가능하면 소문자 snake_case로 쓴다. 예: `app_dev`, `paid_social`.
- 한글 키워드는 `utm_term`에만 허용한다. 캠페인/소재 코드는 영문 코드로 둔다.
- 같은 의미를 여러 값으로 나누지 않는다. 예: `naver`, `Naver`, `naver_search`를 섞지 않는다.
- `utm_source`는 플랫폼, `utm_medium`은 방식이다. 예: 네이버 검색광고는 `utm_source=naver`, `utm_medium=cpc`.
- 이름, 이메일, 전화번호, 개인 식별 가능한 값은 UTM에 넣지 않는다.

## 채널별 태깅 표준

| 채널 | `utm_source` | `utm_medium` | `utm_campaign` | `utm_term` | `utm_content` |
| --- | --- | --- | --- | --- | --- |
| 네이버 파워링크 | `naver` | `cpc` | 캠페인 코드 | 키워드 URL이면 키워드 원문 | `{ad_group}_{creative}` 또는 `{ad_group}` |
| 구글 검색광고 | `google` | `cpc` | 캠페인 코드 또는 Google Ads campaign id | `{keyword}` | `{adgroupid}_{creative}` |
| 링크드인 유료 광고 | `linkedin` | `paid_social` | 캠페인 코드 | 타깃 세그먼트 코드 | 소재/게시물 코드 |
| 링크드인 일반 포스트 | `linkedin` | `organic_social` | 콘텐츠 캠페인 코드 | 비움 | 포스트 코드 |
| 스레드 일반 포스트 | `threads` | `organic_social` | 콘텐츠 캠페인 코드 | 비움 | 포스트 코드 |
| 창업가 네트워크 DM | `founder_network` | `dm` | 아웃리치 캠페인 코드 | 비움 | 메시지/세그먼트 코드 |
| 뉴스레터 | `newsletter` | `email` | 발송 캠페인 코드 | 비움 | 버튼/섹션 코드 |

## URL 예시

### 네이버 파워링크 소재 URL

```text
https://quroom.kr/?utm_source=naver&utm_medium=cpc&utm_campaign=app_dev&utm_content=app_cost_scope_first&src=naver&campaign=app_dev&group=app_cost&intent=cost&creative=scope_first
```

### 네이버 키워드 URL

```text
https://quroom.kr/?utm_source=naver&utm_medium=cpc&utm_campaign=app_dev&utm_term=%EC%95%B1%EA%B0%9C%EB%B0%9C%EB%B9%84%EC%9A%A9&utm_content=app_cost&src=naver&campaign=app_dev&group=app_cost&intent=cost&kw=%EC%95%B1%EA%B0%9C%EB%B0%9C%EB%B9%84%EC%9A%A9
```

### 구글 검색광고 URL

Google Ads와 GA4를 연결했다면 auto-tagging의 `gclid`가 Google Ads 성과 분석의 1차 기준이다. 그래도 네이버/링크드인과 같은 UTM 리포트 축을 유지하려면 Google Ads tracking template 또는 final URL suffix에 아래처럼 ValueTrack을 붙인다.

```text
utm_source=google&utm_medium=cpc&utm_campaign={campaignid}&utm_term={keyword}&utm_content={adgroupid}_{creative}
```

Google Ads ValueTrack 공식 문서:

- https://support.google.com/google-ads/answer/6305348

### 링크드인 일반 포스트

```text
https://quroom.kr/?utm_source=linkedin&utm_medium=organic_social&utm_campaign=founder_story_2026q2&utm_content=post_20260610_builder_investor_parent
```

### 스레드 일반 포스트

```text
https://quroom.kr/?utm_source=threads&utm_medium=organic_social&utm_campaign=founder_story_2026q2&utm_content=thread_20260610_build_in_public
```

## 전송 이벤트

브라우저는 HTMX 문의 제출 성공 후 다음 이벤트를 GA4로 전송한다.

- `contact_submit`: 문의 폼 제출 성공
- `lead_magnet_submit_user`: 리드마그넷 제출 성공

전송 위치:

- `landing/static/landing/js/site.js`

광고 링크로 유입된 값은 `sessionStorage`에 보존하고, 폼 hidden field가 비어 있으면 자동으로 채운다. 사용자가 광고 랜딩 후 같은 세션에서 다른 화면을 거쳐 문의해도 전환 이벤트에 광고 문맥이 붙도록 하기 위함이다.

## GA4에서 UTM 확인하기

### 기본 리포트

1. GA4 > Reports > Acquisition > Traffic acquisition으로 간다.
2. 기본 dimension을 `Session source / medium` 또는 `Session campaign`으로 바꾼다.
3. `naver / cpc`, `google / cpc`, `linkedin / organic_social`, `threads / organic_social`이 분리되어 보이는지 확인한다.
4. 전환은 metric에서 `Key events`를 보고, 드롭다운에서 `contact_submit`만 선택한다.

### Explore에서 상세 확인

1. GA4 > Explore > Free form을 만든다.
2. Dimensions에 아래를 추가한다.
   - `Session manual source`
   - `Session manual medium`
   - `Session manual campaign name`
   - `Session manual term`
   - `Session manual ad content`
   - custom dimension으로 등록한 `Ad group`, `Ad creative`, `Ad keyword`
3. Metrics에 아래를 추가한다.
   - `Sessions`
   - `Event count`
   - `Key events`
   - 가능하면 `Session key event rate`
4. Rows에 `Session manual source`, `Session manual medium`, `Session manual campaign name`을 둔다.
5. 세부 분석이 필요하면 Rows에 `Ad creative`, `Ad keyword`, `Session manual ad content`를 추가한다.
6. Filter에서 `Event name exactly matches contact_submit` 또는 key event를 `contact_submit`으로 제한한다.

### DebugView에서 테스트

1. Google Tag Assistant 또는 GA4 DebugView 설정으로 debug mode를 켠다.
2. UTM이 붙은 테스트 URL로 접속한다.
3. 문의 폼을 제출한다.
4. GA4 > Admin > Data display > DebugView에서 `page_view`와 `contact_submit`을 확인한다.
5. `contact_submit` 이벤트 파라미터에 `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`, `ad_creative`, `ad_keyword`가 들어오는지 확인한다.

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

`utm_source`, `utm_medium`, `utm_campaign`, `utm_term`은 GA4 기본 유입 차원으로 먼저 확인한다. 이벤트 단위로 꼭 필요할 때만 custom dimension을 추가해 quota를 아낀다. 다만 `utm_content`는 소재 성과 비교에 자주 필요하므로 custom dimension으로 등록한다.

## GA4 설정 순서

1. GA4 Admin에서 `contact_submit` 이벤트를 key event로 표시한다.
2. Admin > Custom definitions에서 위 custom dimensions를 생성한다.
3. 광고 링크로 접속해 문의 테스트를 1건 보낸다.
4. Admin > DebugView 또는 Reports > Realtime에서 `contact_submit` 이벤트와 파라미터가 들어오는지 확인한다.
5. Explore > Free form에서 rows에 `Ad group`, `Ad creative`, `Ad keyword`, `UTM content`를 두고 metric은 `Key events` 또는 `Event count`를 본다.

## `naver`인지 `google`인지 구분하는 기준

GA4에서 가장 먼저 보는 축은 `Session source / medium`이다.

| 보고 싶은 것 | GA4 dimension | 기대값 |
| --- | --- | --- |
| 네이버 검색광고 유입 | `Session source / medium` | `naver / cpc` |
| 구글 검색광고 유입 | `Session source / medium` | `google / cpc` |
| 링크드인 일반 포스트 | `Session source / medium` | `linkedin / organic_social` |
| 스레드 일반 포스트 | `Session source / medium` | `threads / organic_social` |
| 캠페인별 성과 | `Session campaign` 또는 `Session manual campaign name` | `app_dev`, `homepage_dev` |
| 키워드별 성과 | `Session manual term` 또는 `Ad keyword` | `앱개발비용`, `{keyword}` |
| 소재별 성과 | `Session manual ad content`, `UTM content`, `Ad creative` | `app_cost_scope_first` |

실무 판단 순서:

1. `Session source / medium`으로 채널 성과를 본다.
2. `Session campaign`으로 캠페인 성과를 본다.
3. `utm_content` 또는 `Ad creative`로 소재 성과를 본다.
4. `utm_term` 또는 `Ad keyword`로 키워드 성과를 본다.
5. 마지막에 실제 문의 품질은 메일/CRM에서 유효 문의 여부로 보정한다.

## URL 생성 체크리스트

- `utm_source`, `utm_medium`, `utm_campaign`이 모두 있는가?
- 검색광고라면 `utm_term`이 있는가?
- 소재가 2개 이상이면 `utm_content`가 서로 다른가?
- 네이버 동적 랜딩이라면 `src=naver`, `campaign`, `group`, `intent`, `creative` 또는 `kw`가 있는가?
- URL에 이름, 이메일, 전화번호, 회사명 등 PII가 없는가?
- 최종 URL을 브라우저에서 열었을 때 파라미터가 redirect 과정에서 사라지지 않는가?
- 테스트 제출 후 GA4 Realtime 또는 DebugView에서 `contact_submit`이 보이는가?

## 운영 기준

- GA4에는 이름, 이메일, 전화번호, 문의 본문을 보내지 않는다.
- `ad_keyword`에는 광고 운영 키워드만 넣는다.
- 소재 성과 비교는 최소 주 1회, `contact_submit` key event 기준으로 본다.
- 유효 문의율은 GA4만으로 판단하기 어렵기 때문에 메일/CRM에서 별도 태깅해 후속 지표로 관리한다.
- UTM 값 표준을 바꾸면 과거 데이터와 리포트가 갈라지므로 새 값은 캠페인 시작 전에만 추가한다.
