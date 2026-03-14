## Why

현재 외국인 개발자 랜딩은 "네트워크 연결 문의" 중심으로 설계되어 있어, 초기 방문자의 정보 입력 부담과 기대치 불일치(취업 보장 오해, 범위 오해)로 전환 효율이 제한됩니다. 취업 준비 단계가 다양한 사용자군을 수용하려면, 저마찰 1차 CTA로 접점을 만들고 라포 형성 후 2차 프로필 수집으로 이어지는 단계형 인재풀 운영 모델이 필요합니다.

## What Changes

- 외국인 개발자 랜딩의 핵심 목적을 단일 문의 전환에서 `인재풀 구축 + 단계형 매칭 준비`로 전환한다.
- 1차 CTA를 "간단 등록(닉네임/이메일/희망직무 + 추가 메모 선택)"으로 단순화하고, 2차 CTA를 "매칭 프로필 완성(CV/링크, GitHub/포트폴리오, 스택/경력, 비자/근무조건)"으로 분리한다.
- 랜딩 카피에서 고정 기간 약속(예: 4주)을 제거하고, 단계/상태 기반 지원 메시지로 변경한다.
- 광주/전남 후보자에게는 대면 우선 지원, 타지역 후보자에게는 온라인 매칭/원격 가이드를 기본으로 하는 지역 운영 원칙을 명시한다.
- 서비스 메시지를 취업 알선이 아닌 `취업 전략 설계 + 지원 실행 지원 + 네트워크 브릿지 + 커뮤니티 정보 공유`로 재구성한다.
- 커뮤니티는 즉시 채널 오픈이 아닌 `대기열 CTA`로 시작하고, 임계치 충족 시 채널을 개설한다.
- 취업 보장 아님, 비자/법률 직접 대행 아님, 프로필 핏 기반 소개 진행 원칙을 랜딩/FAQ/CTA 근처에서 일관되게 노출한다.
- 관리자 관점에서 1차/2차 데이터 상태를 구분 가능한 운영 상태값(신규, 전략중, 매칭대기, 소개진행, 종료)을 정의한다.
- 메인 창업가 페이지 Hero는 창업자 상담을 주 CTA로 유지하고, 보조 CTA 수를 줄여 우선 행동을 선명하게 한다.

## Capabilities

### New Capabilities
- `foreign-developer-talent-pool-funnel`: 외국인 개발자 랜딩에서 1차 간단 등록과 2차 매칭 프로필 완성을 분리한 단계형 수집/전환 흐름을 정의한다.
- `foreign-developer-community-sharing`: 외국인 개발자 간 채용/면접/정착 정보 공유를 위한 커뮤니티 안내 및 참여 유도 기준을 정의한다.

### Modified Capabilities
- `foreign-developer-practical-linkage`: 실무 연계 메시지를 단순 네트워크 연결에서 취업 전략/준비/소개 가능성 중심으로 확장하고, 소개 진행 전제(프로필 핏 확인)를 요구사항에 반영한다.
- `persona-landing-pages`: 외국인 개발자 페이지 전환 목표를 단일 문의 제출에서 단계형 퍼널(1차 등록 -> 2차 프로필)로 수정하고 KPI 경계를 반영한다.
- `contact-inquiry-persistence`: 외국인 개발자 문의 데이터에 단계형 수집 상태와 후속 매칭 준비 정보를 저장/추적할 수 있도록 요구사항을 확장한다.
- `founder-first-homepage-positioning`: 메인 페이지 Hero CTA를 창업자 상담 중심으로 우선순위화하고 보조 CTA를 하향 조정하는 요구사항을 반영한다.

## Impact

- Affected code:
  - `landing/templates/landing/foreign_developers.html`
  - `landing/templates/landing/partials/contact_form.html`
  - `landing/forms.py`
  - `landing/views.py`
  - `landing/models.py` (필요 시 단계 상태 필드)
  - `landing/content.py`
- Affected analytics/KPI:
  - 기존 `foreign_linkage_inquiry_submit` 외에 1차 등록/2차 프로필 완료 이벤트 추적 필요
  - 커뮤니티 대기열 제출 이벤트(`foreign_community_waitlist_submit`) 추적 필요
- Ops/process impact:
  - 관리자 운영에서 1차 리드와 2차 매칭 후보를 구분해 후속 액션 우선순위를 관리해야 함
