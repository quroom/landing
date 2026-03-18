## Context

현재 foreign-developer 랜딩은 `/for-foreign-developers/`에서 동작하는 전용 템플릿, 페이지 전용 콘텐츠, 단계형 intake, community waitlist, 영어 기본 노출 구조를 이미 갖추고 있습니다. 운영 초점은 취업 전략, 매칭 준비, 정착 가이드가 필요한 외국인 소프트웨어 개발자입니다.

하지만 명함 방향이 바뀌면서 두 가지 제약이 추가됩니다.

- QR로 들어온 첫인상과 랜딩 메시지가 `Work in Korea with practical support`, `For international talent`, `Especially foreign software engineers`와 맞아야 합니다.
- 전남대 등 오프라인에서 만나는 사람은 학생, 디자이너, 연구자, 예비 창업자 등 비개발자일 수 있으므로, 첫 화면에서 너무 이른 자기 배제가 일어나면 안 됩니다.

따라서 이번 설계는 기존 niche와 staged funnel을 버리지 않으면서도, entry framing만 한 단계 상위 개념으로 넓히는 방향을 택합니다.

## Goals / Non-Goals

**Goals:**

- 기존 foreign-developer 페이지를 계속 운영 주체로 유지하고, 반쯤 겹치는 여러 페이지로 트래픽을 쪼개지 않는다.
- 랜딩 hero, 서비스 구획, QR/share URL을 명함 문구와 맞춘다.
- 더 넓은 국제 인재 유입이 들어와도 첫 화면과 1차 intake에서 현재 지원 적합도를 이해할 수 있게 만든다.
- 기존 경계 조건인 비보장 취업, 비자·법률 직접 대행 없음, 프로필 적합도 검토 후 소개를 유지한다.
- staged funnel analytics는 유지하되, 외국인 소프트웨어 엔지니어 경로와 lighter community/referral 경로를 구분할 수 있게 한다.

**Non-Goals:**

- 완전히 별도인 global-network 사이트나 범용 국제 인재 서비스 라인을 새로 만드는 것
- 현재 가장 강한 약속 범위를 외국인 소프트웨어 엔지니어 바깥으로 과도하게 넓히는 것
- founder 중심 홈페이지를 다시 손보거나 국제 인재 상세 메시지를 `/`로 섞어 넣는 것
- 실제 live community 플랫폼을 이번 변경에서 출시하는 것

## Decisions

### 1. 기존 foreign-developer 페이지를 유지하고 entry framing만 현 위치에서 넓힌다

구현은 현재 foreign-developer 페이지, view, content pipeline을 그대로 운영 주체로 유지합니다. 대신 hero와 서비스 framing은 `foreign developers only` 표현에서 `international talent` 진입 표현으로 넓히고, 바로 이어지는 보조 문구에서 현재 가장 강한 지원 대상이 `foreign software engineers`임을 명시합니다.

이 방식은 신뢰와 운영 책임을 여러 페이지로 분산시키지 않으면서도, 오프라인에서 만난 비개발자 국제 인재가 QR 진입 단계에서 배제감을 느끼지 않게 합니다.

Alternatives considered:

- 새로운 global-network 페이지를 별도 생성: 콘텐츠 중복과 운영 초점 분산 때문에 제외
- 현재 developer-only framing 유지: 명함 메시지와 어긋나고 인접 국제 인재가 스스로 이탈할 가능성이 커서 제외

### 2. 오프라인 인쇄물용 share-friendly alias 경로를 추가한다

설계상 `/it/`를 명함/공유용 진입 URL로 추가하되, 기존 `/for-foreign-developers/` 경로는 유지합니다. alias는 동일한 랜딩 경험으로 연결되어야 하며, locale/query parameter와 analytics context를 잃지 않아야 합니다.

이렇게 하면 기존 스펙과 테스트를 깨지 않으면서도, 명함과 구두 공유, QR에서는 더 짧고 설명하기 쉬운 URL을 쓸 수 있습니다.

Alternatives considered:

- 기존 경로를 완전히 교체: 이미 많은 스펙, 테스트, 레퍼런스가 `/for-foreign-developers/`를 전제로 하고 있어 제외
- `/gn/` 사용: 이번 방향은 `global talent`보다 `international talent` 표현을 기준으로 잡았고, `/it/`가 명함과 설명 문맥에 더 자연스럽기 때문에 보류

### 3. staged funnel은 유지하되, 1차 intake에서 더 넓은 유입을 분기할 수 있게 한다

현재의 2단계 funnel 자체는 여전히 적절합니다. 다만 Step 1이 모든 유입자를 이미 개발자로 가정하면 안 됩니다. 1차 intake는 가볍게 유지하되, 방문자가 현재 foreign software engineer 지원 경로에 맞는지, 아니면 lighter community/referral 경로로 보내야 하는지를 구분할 수 있어야 합니다.

Step 2는 foreign software engineer 경로를 위한 상세 matching profile로 유지합니다. 개발자가 아닌 국제 인재에게도 다음 액션은 분명해야 하지만, 너무 일찍 소프트웨어 엔지니어 전용 필드를 강제하면 안 됩니다.

Alternatives considered:

- staged funnel을 일반 문의 폼으로 교체: 기존 qualification과 analytics 가치가 사라져 제외
- 모든 유입자를 현재 developer-specific 2단계로 강제: 더 넓은 오프라인 유입과 어긋나고 friction이 커서 제외

### 4. 서비스 구획은 명함 약속에 맞춰 재표현하되, 실제 범위를 과장하지 않는다

랜딩은 명함과 맞는 세 가지 지원 축으로 보이게 구성합니다.

- career strategy
- resume/portfolio readiness
- Korea guidance

이 세 축은 새로운 범용 서비스가 아니라 현재 운영 범위를 다시 묶어 표현한 것입니다. `Korea guidance` 역시 실무 가이드와 파트너 연결을 뜻하며, 비자·법률 직접 대행을 의미하지 않습니다.

Alternatives considered:

- 넓은 `international talent support` 메뉴로 일반화: 현재 실제 제공 강도보다 약속이 커져 제외
- 현재 서비스 wording 유지: 오프라인 명함 메시지보다 지나치게 좁아서 제외

## Risks / Trade-offs

- [상단 퍼널 문구를 넓히면 지원 불가능한 프로필도 유입될 수 있음] -> Mitigation: hero 근처와 intake 분기 카피에서 `especially for foreign software engineers`를 명확히 표기한다.
- [하나의 페이지에 URL이 두 개면 canonical 혼선이 생길 수 있음] -> Mitigation: 템플릿/QR에서는 하나의 선호 share URL을 정하고, 다른 경로는 일관되게 처리한다.
- [더 넓은 entry copy가 기존 foreign-developer 특수성을 약하게 만들 수 있음] -> Mitigation: 상세 섹션, matching profile 필드, 지원 경계를 software engineer 경로에 계속 고정한다.
- [qualification 로직이 카피/폼 복잡도를 높일 수 있음] -> Mitigation: Step 1은 최대한 가볍게 두고, 세부 분기는 후속 메시지나 Step 2 노출 단계로 미룬다.

## Migration Plan

1. entry framing, share-link routing, funnel qualification 관련 스펙을 먼저 확정한다.
2. `/it/` alias를 추가하고 기존 경로를 유지한다.
3. 랜딩 카피, 서비스 라벨, community/intake 안내 문구를 새 framing에 맞게 조정한다.
4. 1차 intake qualification 확장에 맞춰 form, test, analytics 기대값을 수정한다.
5. alias 경로와 랜딩 카피가 검증된 뒤 명함 QR에 최종 URL을 반영한다.

rollback은 비교적 단순합니다. alias 경로를 남기더라도, broadened messaging과 intake qualification 카피만 기존 developer 중심 흐름으로 되돌리면 됩니다.

## Open Questions

- `/it/`는 단순 redirect가 좋은가, 아니면 두 URL이 직접 같은 페이지를 서빙하는 편이 좋은가?
- 보조 문구는 `Especially for foreign software engineers`가 좋은가, 아니면 `Currently strongest for foreign software engineers`가 더 정확한가?
- 인접 국제 인재에 대한 fallback은 community waitlist만 둘 것인가, 아니면 가벼운 manual referral/contact 경로도 함께 둘 것인가?
