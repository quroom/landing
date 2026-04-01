## Context

현재 `quroom.kr`는 기본 landing 페이지는 정상 동작하지만, 검색엔진 등록 관점에서는 공통 준비 상태가 미완성이다. Google Search Console과 Bing Webmaster Tools는 DNS 소유권 인증을 마쳤고, Naver Search Advisor verification도 진행된 상태다. 이제 운영자가 일관되게 마무리하려면 사이트 자체가 `robots.txt`, `sitemap.xml`, canonical 기준, Daum 등록 대응 문구를 제공해야 한다.

이번 변경의 목적은 SEO 대개편이나 마케팅 분석 도입이 아니라, 검색엔진 등록의 최소 준비 상태를 만드는 것이다. 즉 "등록할 수 있는 사이트 상태"와 "운영자가 따라 할 수 있는 문서"를 만드는 것이 핵심이다.

## Goals / Non-Goals

**Goals:**
- 사이트가 `robots.txt`와 `sitemap.xml`을 제공하도록 준비한다.
- canonical 기준 URL과 sitemap 제출 기준 URL을 문서화한다.
- Daum 등록 과정에서 요구받은 robots 하단 문구를 안전하게 반영할 수 있게 한다.
- 운영자가 Google/Bing/Naver/Daum 등록 현황과 남은 절차를 추적할 수 있도록 runbook을 제공한다.

**Non-Goals:**
- 각 콘솔 계정에 로그인해서 실제 등록을 자동화하지 않는다.
- 검색 노출 순위, SEO 카피, structured data 전체를 이번 범위에 포함하지 않는다.
- GA4, IndexNow, 광고 태그 등 마케팅 도구 연동은 포함하지 않는다.

## Decisions

### 1. sitemap은 핵심 landing URL만 우선 포함한다

- 결정: 첫 버전 sitemap에는 핵심 공개 landing URL만 포함한다.
- 이유: 지금 목적은 검색엔진 등록 준비이며, 모든 locale/관리 경로를 포괄하는 대형 sitemap이 아니다.
- 대안:
  - 모든 가능한 URL을 동적으로 포함: 현재 범위 대비 복잡도가 크고 유지보수 기준이 불명확해 제외

### 2. robots.txt는 최소 허용 정책으로 시작하되 하단 추가 문구를 허용한다

- 결정: 기본은 `User-agent: *`, `Allow: /`, `Sitemap:` 형식으로 두고, 운영자가 Daum 등록 과정에서 요구받은 추가 라인을 하단에 붙일 수 있는 구조를 둔다.
- 이유: 검색엔진 등록 준비의 최소 요건을 유지하면서, 검색등록 운영 중 서비스별 요구사항을 빠르게 반영할 수 있다.
- 대안:
  - 완전히 고정된 robots 응답만 제공: Daum 등록 대응 유연성이 떨어져 제외

### 3. canonical 기준은 `https://quroom.kr/`로 문서화한다

- 결정: canonical 기준 URL은 `https://quroom.kr/`로 문서화하고, sitemap과 robots도 동일 기준을 사용한다.
- 이유: 등록 콘솔별 기준 URL이 흔들리면 수집 상태와 소유권 관리가 복잡해진다.
- 대안:
  - `www`와 non-`www`를 병행 표기: 등록/색인 기준이 흔들려 제외

### 4. Daum은 코드 인증이 아니라 운영 runbook 대상이다

- 결정: Daum은 별도 verification code 삽입 대상이 아니라 검색등록 신청 절차를 문서화하는 방향으로 다룬다.
- 이유: Daum은 Google/Bing/Naver처럼 지속형 verification console 성격이 약하고 등록 신청 성격이 더 강하다.
- 대안:
  - Daum 전용 메타/인증 구조 추가: 현재 확인된 운영 흐름과 맞지 않아 제외

## Risks / Trade-offs

- [sitemap 범위가 너무 좁을 수 있음] → 첫 버전은 핵심 landing URL만 포함하고, 필요 시 후속 change에서 확장한다.
- [canonical 기준 URL이 흔들릴 수 있음] → `https://quroom.kr/`를 대표 기준으로 문서화하고 sitemap/robots도 동일 기준을 사용한다.
- [Daum이 요구하는 robots 하단 문구가 바뀔 수 있음] → 운영자가 쉽게 반영할 수 있는 추가 라인 구조와 문서 체크리스트를 둔다.
- [Daum 등록을 자동화하지 않아 잊힐 수 있음] → 운영 체크리스트에 별도 단계로 명시한다.

## Migration Plan

1. `robots.txt`, `sitemap.xml` route와 응답을 추가한다.
2. 필요 시 canonical 관련 메타 구성을 정리한다.
3. 테스트로 `robots`, `sitemap` 응답을 검증한다.
4. README/runbook에 Google/Bing/Naver 완료 현황과 Daum 남은 절차를 추가한다.
5. 운영자는 배포 후 Daum 검색등록과 sitemap 제출을 진행한다.

롤백은 `robots/sitemap/meta` 노출을 제거하고 문서 변경을 되돌리는 정도로 충분하다.

## Open Questions

없음
