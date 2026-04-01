## 1. Canonical and Robots Structure

- [x] 1.1 대표 사이트 URL 기준을 확인하고 canonical 또는 관련 메타 구성을 정리한다.
- [x] 1.2 `robots.txt` 하단에 운영자가 추가 문구를 넣을 수 있는 구조 또는 반영 절차를 정리한다.

## 2. Indexing Readiness Routes

- [x] 2.1 `robots.txt` route와 응답을 추가한다.
- [x] 2.2 `sitemap.xml` route와 응답을 추가하고 핵심 landing URL을 포함한다.

## 3. Documentation

- [x] 3.1 README 또는 운영 runbook에 검색엔진 등록 준비 절차를 추가한다.
- [x] 3.2 Google/Bing/Naver/Daum 등록 순서, 입력값, sitemap 제출 기준을 문서화한다.

## 4. Verification

- [x] 4.1 테스트를 추가 또는 갱신해 `robots.txt`, `sitemap.xml`, canonical 관련 응답 또는 렌더를 검증한다.
- [x] 4.2 `./scripts/verify.sh` 를 실행해 회귀가 없는지 확인한다.
