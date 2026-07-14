---
title: '한국 B2B 외주 홈페이지 리뉴얼'
type: 'feature'
created: '2026-07-14'
status: 'done'
review_loop_iteration: 0
baseline_commit: '8619c7b8598791d79abfd5b7e1a8e744e7195f5d'
context:
  - 'AGENTS.md'
  - 'codex-document/homepage-landing-copy-master.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** 현재 메인 페이지는 자동화 진단과 여러 소형 서비스가 섞여 있어, 한국 기업이 외주 개발 파트너의 역량과 책임 범위를 빠르게 판단하기 어렵다. 카드, 장식 효과, 영문 라벨 중심의 표현도 외주 회사보다 AI가 만든 에세이형 포트폴리오처럼 보인다.

**Approach:** 메인 `/`를 한국 B2B 외주 의사결정 흐름에 맞춰 서비스 범위, 외주 사례, 자체 제품, 진행 방식, 대표 경력, FAQ, 문의 순으로 재구성한다. 핵심 약속은 “기획부터 개발, 배포와 운영 이관까지 책임집니다.”로 고정하고, 기존 Django 운영 기능은 그대로 연결한다.

## Boundaries & Constraints

**Always:** Django 문의 폼과 HTMX 제출, GA4 및 네이버 광고 유입 추적, 동적 광고 문구, SEO 구조화 데이터, KO/EN 전환, 동적 경력 계산, 승인 후기, 법적 고지와 별도 랜딩 경로를 보존한다. Pretendard 기반의 한국어 우선 타이포그래피를 사용하고 메인 전용 스타일로 격리한다. ArtTrip은 대표 외주 사례, 나머지 6개는 자체 제품 경험으로 구분한다.

**Ask First:** 외주 기본 가격인 4~8주·1,000만원 이상을 변경하거나, 문의 필드·데이터 모델·추적 이벤트 계약을 변경하거나, 다른 랜딩 페이지의 디자인을 함께 변경해야 할 경우 사용자 승인을 받는다.

**Never:** 자동화 실행 진단·자동화 실행 구축·무료 진단·비즈니스 메일·기업 홈페이지 부가 서비스를 메인 서비스로 노출하지 않는다. 기존 사용자 변경을 되돌리거나 운영 경로를 삭제하지 않는다. 과도한 그라디언트, 블러 장식, 중첩 카드, 대형 썸네일, 에세이형 장문을 사용하지 않는다.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|---------------|----------------------------|----------------|
| 기본 방문 | 일반 `/` 요청 | 승인된 외주 메시지와 전체 섹션, 실제 문의 폼이 표시됨 | 콘텐츠 누락 없이 서버 렌더링 |
| 광고 방문 | 네이버 광고 파라미터 포함 요청 | 광고 헤드라인과 CTA를 사용하되 새 레이아웃과 추적 필드를 유지 | 유효하지 않은 값은 기존 빌더가 기본 콘텐츠로 처리 |
| 영문 방문 | EN 활성화 | 탐색과 핵심 콘텐츠가 번역되고 레이아웃이 깨지지 않음 | 미번역 문자열을 테스트로 탐지 |
| 후기 부족 | 공개 기준 미달 | 후기 영역만 렌더링하지 않고 다음 섹션 흐름 유지 | 빈 컨테이너 미출력 |

</frozen-after-approval>

## Code Map

- `landing/templates/landing/index.html` -- 메인 페이지 정보 구조와 Django 운영 기능 연결 지점
- `landing/content.py` -- 서비스, 프로젝트, 경력, FAQ의 KO/EN 콘텐츠 소스
- `landing/static/landing/css/home-renewal.css` -- 다른 랜딩과 분리된 메인 전용 반응형 스타일
- `landing/static/landing/fonts/` -- 한국어 우선 화면에 사용하는 로컬 Pretendard 웹폰트
- `landing/forms.py` -- 일반 방문자용 문의 선택지와 기존 진단 링크 호환 계약
- `landing/tests/test_landing_pages.py` -- 페이지 콘텐츠와 동적 광고 렌더링 회귀 계약
- `landing/tests/test_content_i18n.py` -- 신규 핵심 콘텐츠 번역 계약

## Tasks & Acceptance

**Execution:**
- [x] `landing/content.py` -- 메인 외주 서비스, 사례, 프로필, 절차, FAQ 콘텐츠를 명시적으로 구성하고 KO/EN 번역을 추가한다.
- [x] `landing/forms.py` -- 메인에서 자동화 서비스를 숨기고 명시적으로 유입된 기존 진단 문의는 계속 처리한다.
- [x] `landing/templates/landing/index.html` -- 승인된 섹션 순서로 교체하고 문의·추적·광고·후기 계약을 연결한다.
- [x] `landing/static/landing/css/home-renewal.css`, `landing/static/landing/fonts/` -- 한국어 중심의 절제된 B2B 레이아웃과 반응형·접근성 상태를 구현한다.
- [x] `locale/en/LC_MESSAGES/` -- 신규 정적 UI 문구의 영문 번역 카탈로그를 갱신한다.
- [x] `landing/tests/` -- 핵심 문구, 제외 문구, 사례 구분, 광고·영문·문의 렌더링을 검증한다.

**Acceptance Criteria:**
- Given 일반 한국어 방문자, when `/`를 열면, then 첫 화면에서 책임 범위·대표 경력·기간·가격·직접 수행 여부를 확인할 수 있다.
- Given 메인 전체 페이지, when 아래로 탐색하면, then 서비스→ArtTrip 외주 사례→자체 제품 6개→진행 방식→대표 경력→FAQ→문의 순서로 보인다.
- Given 기존 문의 또는 광고 유입, when 폼을 제출하거나 광고 URL로 방문하면, then 기존 추적 데이터와 HTMX 동작이 유지된다.
- Given 모바일과 데스크톱 화면, when 주요 뷰포트로 렌더링하면, then 텍스트·버튼·이미지가 겹치거나 컨테이너를 넘지 않는다.

## Spec Change Log

## Design Notes

시안은 최종 형태가 아니라 검증된 정보 구조와 시각 방향의 기준이다. Django 템플릿에는 정적 시안 링크를 복사하지 않고 실제 URL, 콘텐츠 객체, 폼 partial, 광고 분기를 사용한다. 공용 `site.css`는 폼과 비메인 화면 계약을 계속 담당하고 새 파일은 `.home-renewal` 아래에서만 시각 속성을 재정의한다.

## Verification

**Commands:**
- `./scripts/verify.sh` -- 전체 포맷, Django 검사와 테스트 성공
- 메인 페이지 대상 Django 테스트 -- 기본·광고·영문·후기 조건 성공
- Playwright 기반 데스크톱·모바일 스크린샷 -- 레이아웃 겹침과 빈 이미지 없음

## Suggested Review Order

**정보 구조와 메시지**

- 메인 진입점에서 합의된 외주 의사결정 흐름을 한 번에 확인합니다.
  [`index.html:57`](../landing/templates/landing/index.html#L57)

- 한국어·영문 카피와 외주 서비스 조건의 단일 소스를 확인합니다.
  [`content.py:392`](../landing/content.py#L392)

- ArtTrip과 자체 제품을 데이터 기준으로 분리하는 경계를 확인합니다.
  [`content.py:1242`](../landing/content.py#L1242)

**전환과 호환성**

- 일반 문의에서는 자동화를 숨기고 기존 진단 유입만 호환합니다.
  [`forms.py:201`](../landing/forms.py#L201)

- 내부 상담 링크가 광고 파라미터를 보존하며 문의 유형을 바꿉니다.
  [`site.js:86`](../landing/static/landing/js/site.js#L86)

- 실제 HTMX 문의 폼이 새 문의 영역에 그대로 연결됩니다.
  [`index.html:295`](../landing/templates/landing/index.html#L295)

**시각과 검증**

- 절제된 데스크톱 레이아웃과 썸네일 크기 기준을 확인합니다.
  [`home-renewal.css:5`](../landing/static/landing/css/home-renewal.css#L5)

- 모바일 메뉴와 문의 폼의 반응형 규칙을 확인합니다.
  [`home-renewal.css:124`](../landing/static/landing/css/home-renewal.css#L124)

- 핵심 카피·제외 항목·섹션 순서의 회귀 계약을 확인합니다.
  [`test_landing_pages.py:399`](../landing/tests/test_landing_pages.py#L399)
