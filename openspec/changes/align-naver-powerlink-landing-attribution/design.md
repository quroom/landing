## BMAD Context

### Business

목표는 저비용 롱테일 키워드와 검색 의도별 광고 소재를 연결해, 클릭 후 첫 화면에서 사용자의 기대 메시지를 바로 맞추는 것이다. 성공 기준은 단순 클릭 수가 아니라 문의 전환, 유효 문의율, 전환당 비용이다.

### Market

초기 광고군은 앱 개발/제작, 홈페이지 제작/개발, 랜딩페이지, 상세페이지, 쇼핑몰, 유지보수다. 사용자는 보통 비용, 견적, 업체, 외주, 유지보수처럼 당장 의사결정에 가까운 단어로 검색한다. 따라서 랜딩은 포괄적인 브랜드 소개보다 “범위 정리, 비용 구간, 완료 기준, 운영 이관” 같은 구체 메시지를 우선해야 한다.

### Architecture

두 종류의 URL 파라미터를 분리한다.

분석용 UTM:

- `utm_source=naver`
- `utm_medium=cpc`
- `utm_campaign`: 네이버 캠페인 코드
- `utm_content`: 소재 URL은 `{ad_group}_{creative}`, 키워드 URL은 `{ad_group}`
- `utm_term`: 키워드 URL에서 키워드 원문

랜딩 제어용 커스텀 파라미터:

- `src=naver`
- `campaign`: 네이버 캠페인 코드
- `group`: 광고그룹 코드
- `intent`: 검색 의도
- `creative`: 광고 소재 코드
- `kw`: 키워드 원문

`homepage`는 `src=naver`일 때만 동적 랜딩을 적용한다. `group + creative` 조합이 있으면 소재별 문구를 우선 적용하고, 없으면 광고그룹 기본 variant로 fallback한다.

### Delivery

소재 문안과 URL은 `ad-for-everthing/naver/inputs/ad_creatives.csv`에서 관리한다. 업로드 CSV와 랜딩 미리보기는 스크립트로 다시 생성한다. `homepage` 쪽에서는 파라미터 수신, 문구 매핑, 문의/이벤트 저장만 책임진다.

## Decisions

### 1. UTM과 커스텀 파라미터를 모두 유지한다

- 결정: 광고 URL에 UTM과 커스텀 파라미터를 함께 둔다.
- 이유: UTM은 GA4와 분석 표준에 유리하고, 커스텀 파라미터는 `homepage` 내부 랜딩 제어에 명확하다.
- 리스크: URL이 길어진다. 네이버 URL 입력 제한과 브라우저 호환성 범위에서는 현재 문제가 없다.

### 2. 소재별 개인화는 히어로 영역부터 시작한다

- 결정: 1차 범위는 H1, 서브카피, CTA, 문의 hidden field, 이벤트 metadata다.
- 이유: 첫 화면 일치도가 광고 전환에 가장 직접적이고, 본문 전체 개인화보다 유지보수 비용이 낮다.
- 후속: 성과가 쌓이면 FAQ, 서비스 카드 우선순위, 문의 폼 placeholder까지 확장한다.

### 3. `ad_creative`는 우선 이벤트 metadata로 추적한다

- 결정: `ad_creative` DB 컬럼은 즉시 추가하지 않고, hidden field와 `FunnelEvent.metadata`로 저장한다.
- 이유: 초기에는 소재별 문의 수가 적을 수 있으므로 스키마 변경보다 이벤트 metadata가 충분하다.
- 후속: 관리자 필터/CSV export에서 소재별 분석이 필요해지면 `ContactInquiry.ad_creative` 컬럼을 별도 migration으로 추가한다.

### 4. 검수 기준은 실제 렌더링 스크린샷이다

- 결정: 광고 소재별 URL을 로컬 서버에서 열고 Playwright screenshot으로 비교 HTML을 생성한다.
- 이유: CSV만 보면 랜딩 문구가 실제로 바뀌는지 확인하기 어렵다.
- 산출물: `/home/quroom/workspace/ad-for-everthing/naver/results/landing_previews/index.html`

## Risks / Trade-offs

- [파라미터 누락] 광고 URL에 `src=naver`가 빠지면 동적 랜딩이 적용되지 않는다. 생성 스크립트 검증으로 잡는다.
- [분석 축 불일치] UTM과 커스텀 `campaign/group` 값이 다르면 리포트 해석이 깨진다. `ad_creatives.csv`를 단일 원본으로 유지한다.
- [소재 문구 과최적화] 소재마다 본문을 과하게 바꾸면 어떤 요소가 전환에 영향을 줬는지 알기 어렵다. 1차는 히어로만 바꾼다.
- [개인정보/보안] 검색어와 광고 파라미터는 문의 본문에 과도하게 노출하지 않고, 운영 분석 metadata로만 활용한다.

## Verification

1. `homepage`에서 관련 랜딩 테스트를 실행한다.
2. `ad-for-everthing`에서 `python3 naver/scripts/build_ad_creative_upload.py`를 실행해 소재 CSV를 재생성한다.
3. `ad-for-everthing`에서 `python3 naver/scripts/build_all_low_bid_candidates.py`를 실행해 키워드 URL을 재생성한다.
4. `homepage` 개발 서버를 띄운 뒤 `python3 naver/scripts/capture_landing_previews.py --base-url http://127.0.0.1:8018/`로 소재별 스크린샷을 생성한다.
5. `naver/results/landing_previews/index.html`에서 광고 제목, H1, CTA가 서로 맞는지 확인한다.
