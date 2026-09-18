# 빌드노트 SEO 개선 검토

운영 배포 전 검토용. 정부지원사업 글은 발행 대상에서 제외하며 DB 내용은 변경하지 않는다.

## 대표 이미지

- 7개 주제별 자체 제작 흐름도, PNG 1200×630. 이미지 생성 API와 외부 사진 미사용.
- 본문, OG, BlogPosting.image에서 같은 파일을 사용한다. 이미지 노출이나 순위는 검색엔진이 결정한다.
- `landing/build_note_images.py`에 slug별 주제와 단계를 정의한다. 신규 글은 관련 도식이 등록된 경우에만 Article 이미지가 추가된다.
- `python3 scripts/build-note-covers.py`로 재생성한다. 제작 환경에 Pillow와 Noto Sans CJK가 필요하며 서버 런타임 의존성은 없다. 한국어 face(index 1)의 Bold 제목/단계명과 Regular 설명을 사용한다.

## 측정

- GA4 로딩과 이벤트 전송 제거. PostHog와 기존 서버 문의 이벤트를 유지한다.
- `build_note_viewed`: article_slug.
- `build_note_cta_clicked`: article_slug, destination.
- 기존 `contact_submit`은 성공 응답에서 발생한다. PostHog 세션 속성 article_slug로 마지막 열람 글과 연결한다. 계약 성사나 이메일 전달 성공을 의미하지 않는다.
- 자동 상호작용 수집과 세션 녹화를 비활성화한다. 명시한 이벤트와 페이지 조회만 사용한다. 기존 IP 제외를 유지한다.
- 운영 PostHog 프로젝트의 실제 보관 기간 및 개인정보처리방침 최종 확인이 필요하다. 이번 작업은 계정 설정을 변경하지 않는다.

## 검색 신호와 배포 후 확인

- 빌드노트 공통 Organization/WebSite 컨텍스트 복구, 절대 OG URL, BlogPosting, 안전한 JSON 직렬화.
- 빌드노트 lastmod는 DB 발행일/수정일 중 나중 값이다. 본문 재동기화 시 변경 없는 저장으로 updated_at을 갱신하지 않도록 운영한다. 정확한 날짜가 없는 고정 페이지에는 lastmod를 만들지 않는다.
- www GET/HEAD는 대표 호스트로 301 이동하며 경로와 쿼리를 보존한다. POST는 변경하지 않는다.
- 운영 배포 후 이미지 HTTP 200, Google Rich Results Test와 Search Console URL 검사, PostHog Live events를 확인한다.
- 현재 로컬 테스트 통과는 실제 검색결과 이미지 노출이나 운영 PostHog 수신 검증을 대신하지 않는다.
