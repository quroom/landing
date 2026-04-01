## Why

`quroom.kr`는 Google Search Console과 Bing Webmaster Tools는 DNS 소유권 인증을 마쳤고, Naver Search Advisor도 verification을 진행한 상태다. 이제 남은 작업은 검색엔진 공통 준비물과 Daum 등록 대응을 정리하는 것이다. 현재 코드 기준으로는 `robots.txt`, `sitemap.xml`, canonical 기준, Daum 등록용 운영 절차 문서가 없다.

이 상태에서는 운영자가 각 콘솔에 사이트를 등록하더라도 소유권 인증 방식이 분산되고, sitemap 제출과 수집 상태 점검도 일관되게 하기 어렵다.

## What Changes

- 사이트가 `robots.txt`와 `sitemap.xml`을 제공하도록 준비한다.
- 기본 canonical 사이트 URL과 sitemap URL을 운영 문서에서 명확히 정의한다.
- Daum 등록 시 필요한 robots 하단 문구 또는 운영자가 요구받은 추가 라인을 반영할 수 있게 한다.
- Google/Bing/Naver/Daum 등록 현황과 남은 수동 절차를 정리한 운영 runbook을 추가한다.
- 이번 변경은 검색엔진 등록 준비 상태를 만드는 것이 목적이며, 실제 각 콘솔 계정에서의 최종 제출/승인 자체는 운영자 수동 절차로 남긴다.

## Capabilities

### New Capabilities
- `search-engine-indexing-readiness`: 사이트가 검색엔진 등록과 색인 준비를 위해 `robots.txt`, `sitemap.xml`, canonical 기준, 운영 runbook을 제공하도록 정의한다.

### Modified Capabilities
- `developer-navigation-and-runbook`: 개발/운영 문서가 검색엔진 등록 준비 절차와 관련 env/config 위치를 안내하도록 확장한다.

## Impact

- 영향 코드: `landing/project/urls.py`, `landing/views.py`, 필요 시 `landing/templates/landing/base.html`, `landing/project/settings.py`
- 영향 문서: `README.md`, `codex-document/` 또는 동일 성격의 운영 runbook
- 외부 의존성: 없음. 각 검색엔진 콘솔 등록은 운영자가 수동으로 수행
