## 1. Attribution Contract

- [x] 1.1 네이버 광고 URL 표준을 UTM + 커스텀 랜딩 파라미터 조합으로 정의한다.
- [x] 1.2 `homepage` 동적 랜딩은 `src=naver`, `group`, `creative`, `kw`를 기준으로 동작하도록 유지한다.
- [x] 1.3 광고 소재별 문구는 `group + creative` 우선, 광고그룹 variant fallback으로 설계한다.

## 2. Naver Output Alignment

- [x] 2.1 `ad-for-everthing/naver/inputs/ad_creatives.csv`의 소재 URL을 UTM 포함 형태로 통일한다.
- [x] 2.2 키워드 최종 URL 생성기에 `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`를 추가한다.
- [x] 2.3 네이버 업로드용 소재 CSV와 키워드 CSV를 재생성하고 URL 누락을 검증한다.

## 3. Landing Verification

- [x] 3.1 `homepage` 문의 폼 hidden field와 `FunnelEvent.metadata`에 `ad_creative`를 저장한다.
- [x] 3.2 소재별 랜딩 미리보기 HTML과 스크린샷을 재생성한다.
- [x] 3.3 광고 제목, 랜딩 H1, CTA가 클릭 후 문의 관점에서 자연스러운지 검수한다.

## 4. Follow-up

- [ ] 4.1 실제 네이버 집행 후 소재별 CTR, 문의율, 유효 문의율을 주간 단위로 비교한다.
- [ ] 4.2 필요 시 `ContactInquiry.ad_creative` DB 컬럼과 관리자 필터를 별도 변경으로 추가한다.
- [ ] 4.3 성과가 쌓이면 FAQ, 서비스 카드 우선순위, 문의 폼 placeholder의 소재별 개인화를 검토한다.
