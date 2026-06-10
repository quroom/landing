## Why

네이버 파워링크에서 유입되는 사용자는 검색어, 광고그룹, 광고 소재마다 기대하는 메시지가 다르다. 현재 `homepage`는 `src/campaign/group/intent/creative/kw` 파라미터로 히어로 문구를 바꾸고 문의 이벤트에 광고 정보를 남길 수 있지만, 광고 업로드 URL과 분석 기준이 흔들리면 소재별 전환 판단이 어렵다.

이 변경은 `ad-for-everthing/naver`의 광고 운영 데이터와 `homepage`의 동적 랜딩/문의 추적을 하나의 운영 흐름으로 맞추기 위한 BMAD 실행 문서다.

## What Changes

- 네이버 광고 URL은 분석용 UTM과 랜딩 제어용 커스텀 파라미터를 함께 사용한다.
- `homepage`는 커스텀 파라미터로 랜딩 문구를 결정하고, UTM은 GA4 및 내부 이벤트 분석 축으로 보존한다.
- 소재별 랜딩 문구 변경은 히어로 H1, 서브카피, CTA, 문의 hidden field, `FunnelEvent.metadata` 범위에서 시작한다.
- 광고 소재와 랜딩 문구의 단일 운영 원본은 `/home/quroom/workspace/ad-for-everthing/naver/inputs/ad_creatives.csv`로 둔다.
- 실제 화면 검수는 `/home/quroom/workspace/ad-for-everthing/naver/results/landing_previews/index.html`을 기준으로 한다.

## Capabilities

### New Capabilities

- `naver-powerlink-dynamic-landing-attribution`: 네이버 광고 유입이 광고 소재별 랜딩 문구와 분석 파라미터를 일관되게 전달해야 한다.

### Modified Capabilities

- `lead-magnet-conversion-measurement`: 기존 UTM 보존 원칙을 네이버 파워링크 유입에도 적용한다.
- `contact-inquiry-persistence`: 문의 저장과 이벤트 metadata가 네이버 광고 소재 문맥을 잃지 않도록 한다.

## Impact

- 영향 코드: [`landing/ad_landing.py`](/home/quroom/workspace/homepage/landing/ad_landing.py), [`landing/forms.py`](/home/quroom/workspace/homepage/landing/forms.py), [`landing/views.py`](/home/quroom/workspace/homepage/landing/views.py)
- 영향 템플릿: [`landing/templates/landing/index.html`](/home/quroom/workspace/homepage/landing/templates/landing/index.html), [`landing/templates/landing/partials/contact_form.html`](/home/quroom/workspace/homepage/landing/templates/landing/partials/contact_form.html)
- 영향 데이터: `FunnelEvent.metadata`, `ContactInquiry` 광고 attribution 필드, 네이버 광고 URL 파라미터
- 외부 산출물: `/home/quroom/workspace/ad-for-everthing/naver/results/naver_powerlink_ads.csv`, `/home/quroom/workspace/ad-for-everthing/naver/results/all_low_bid_candidates_naver.csv`

## Non-Goals

- 네이버 광고 API 자동 등록은 포함하지 않는다.
- 소재별 본문 전체 개인화는 1차 범위가 아니다.
- GA4 대시보드 구축이나 쿠키 동의 정책 변경은 별도 변경으로 분리한다.
