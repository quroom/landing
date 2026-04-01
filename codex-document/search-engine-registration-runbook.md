# Search Engine Registration Runbook

## 1) Canonical indexing 기준값

- Canonical site URL: `https://quroom.kr`
- Robots URL: `https://quroom.kr/robots.txt`
- Sitemap URL: `https://quroom.kr/sitemap.xml`

모든 콘솔 등록/제출 입력값은 위 canonical 기준으로 통일한다.

## 2) 배포 전 설정 확인

`landing/project/settings.py` 기준:
- `DJANGO_SITE_BASE_URL`: canonical URL과 동일하게 설정 (`https://quroom.kr`)
- `SEARCH_ROBOTS_EXTRA_LINES`: 검색엔진 운영 중 추가 요청 문구가 있을 때만 사용

예시(여러 줄):

```env
SEARCH_ROBOTS_EXTRA_LINES="User-agent: Daumoa
Allow: /"
```

## 3) 등록 순서 (운영 권장)

1. Google Search Console
2. Bing Webmaster Tools
3. Naver Search Advisor
4. Daum 검색등록

Google/Bing/Naver는 verification 기반 콘솔 흐름이고, Daum은 등록 신청 흐름으로 별도 취급한다.

## 4) 서비스별 입력값과 제출 기준

### Google Search Console
- 속성 URL: `https://quroom.kr/`
- 확인: DNS verification 완료 상태 유지
- 제출: `https://quroom.kr/sitemap.xml`
- 점검: 색인 생성 > 사이트맵에서 처리 상태 확인

### Bing Webmaster Tools
- 사이트 URL: `https://quroom.kr/`
- 확인: DNS verification 완료 상태 유지
- 제출: `https://quroom.kr/sitemap.xml`
- 점검: Sitemaps 메뉴에서 fetch/처리 결과 확인

### Naver Search Advisor
- 사이트 URL: `https://quroom.kr/`
- 확인: 소유확인(verification) 완료 상태 유지
- 제출: `https://quroom.kr/sitemap.xml`
- 점검: 웹마스터도구 수집 현황/사이트맵 처리 결과 확인

### Daum 검색등록
- URL: `https://quroom.kr/`
- 절차: 검색등록 신청(verification code 삽입 자동화 대상 아님)
- 요청 대응: 운영 중 `robots.txt` 하단 문구 추가 요구가 오면 `SEARCH_ROBOTS_EXTRA_LINES`에 반영 후 재배포
- 점검: 등록 결과/반려 사유를 운영 기록에 남기고 필요 시 robots 추가 문구 조정

## 5) 운영 체크리스트

1. `https://quroom.kr/robots.txt`에서 `Sitemap: https://quroom.kr/sitemap.xml` 라인 확인
2. `https://quroom.kr/sitemap.xml`에서 핵심 공개 랜딩 URL 포함 확인
3. 대표 페이지 HTML에서 canonical 링크(`https://quroom.kr/...`) 확인
4. Google/Bing/Naver에 sitemap 제출 완료 확인
5. Daum 등록 신청/보완 요청 상태 기록
