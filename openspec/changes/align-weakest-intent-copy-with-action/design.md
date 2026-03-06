## Context

무료 진단 결과는 8문항(`q1~q8`) 응답을 기반으로 `weakest_insight`(핵심 보완 포인트)와 `one_action`(2주 실행 작업 1개)을 생성한다. 현재 구현은 내부적으로 같은 anchor 질문을 사용하지만, 사용자 노출 문구는 보완 포인트가 축(axis) 중심, 실행 작업이 intent 중심으로 표현되어 의미 해상도가 다르게 보인다. 이 차이로 preview 검토 시 "보완 포인트와 실행 작업이 안 맞는다"는 피드백이 반복되고 있다.

관련 모듈은 `landing/views.py`(스코어링/문구 생성), `landing/lead_magnet_sections.py`(채널 중립 섹션 계약), `landing/mailers.py`(메일 렌더링), `landing/templates/landing/lead_magnet_report_preview.html`(관리자 검토 UI)다.

## Goals / Non-Goals

**Goals:**
- 핵심 보완 포인트와 2주 실행 작업을 동일 anchor intent 기준으로 1:1 정렬한다.
- preview/메일/텍스트 렌더링에서 intent 정렬 계약을 공통으로 강제한다.
- 관리자 preview에서 그룹화된 카드도 동일 intent 기반인지 빠르게 검토할 수 있게 한다.

**Non-Goals:**
- 진단 점수 계산식(예: impact_weight, 등급 임계값) 자체 변경
- 8문항 설문 구조 변경
- CTA 퍼널/이벤트 이름/집계 로직 변경

## Decisions

- 선택: 핵심 보완 포인트의 대표 문구를 축(axis) 템플릿 우선에서 anchor intent 템플릿 우선으로 전환한다.
  - 이유: 사용자에게 보이는 "문제 진단"과 "2주 실행"이 같은 단위를 참조해야 신뢰도와 이해도가 올라간다.
  - 대안: 축 문구 유지 + 실행문만 intent 유지.
  - 미채택 이유: 해상도 차이로 불일치 체감이 계속 발생한다.

- 선택: `weakest_insight.intent_key == one_action.intent_key`를 결과 계약 필드로 명시하고 테스트로 고정한다.
  - 이유: 구현 리팩터링 중에도 정합성 회귀를 즉시 감지할 수 있다.
  - 대안: 질문 키(`question_key`)만 비교.
  - 미채택 이유: 질문 키는 같아도 사용자 노출 문구 매핑에서 intent 레벨 불일치가 숨겨질 수 있다.

- 선택: preview 그룹화는 기존 "본문 동일" 기준을 유지하되, 카드 내에 intent 기반 정렬 검토 정보(예: 대표 intent, 묶인 intent 수)를 노출한다.
  - 이유: 운영자 검토 편의와 실제 메일 노출 단순성을 동시에 만족한다.
  - 대안: preview를 메일과 동일 포맷으로 제한.
  - 미채택 이유: 검토 효율이 크게 떨어진다.

## Risks / Trade-offs

- [위험] intent 중심 문구가 과도하게 세분화되어 카피 일관성이 약해질 수 있음
  → Mitigation: intent별 기본 카피 템플릿을 단일 맵으로 관리하고 회귀 테스트에 스냅샷을 추가한다.

- [위험] 기존 축 중심 메시지를 기대하던 내부 검토 기준과 충돌할 수 있음
  → Mitigation: preview에 축 정보는 보조 정보로 유지하되, 주표현은 intent 기준으로 명확히 안내한다.

- [위험] preview 그룹화 시 서로 다른 축이 하나로 묶여 오해를 줄 수 있음
  → Mitigation: 그룹 카드에 대표 intent/연관 시나리오 타이틀을 함께 노출한다.

## Migration Plan

1. 결과 생성 경로(`_category_grade_insights`, `_best_single_action`, 섹션 빌더)에 intent 정렬 계약 필드 추가
2. preview/메일 공통 섹션 출력이 새 계약을 사용하도록 조정
3. 기존 테스트를 intent 정렬 기준으로 갱신하고 새 회귀 테스트 추가
4. 관리자 preview에서 그룹화 검토 정보 노출 확인
5. 스모크 테스트: 16점 시나리오 + 8개 intent 취약 시나리오

롤백 전략:
- 필요 시 축 기반 문구 선택기를 feature flag 없이 즉시 되돌릴 수 있도록 기존 축 메시지 맵을 유지한다.
- 회귀 발생 시 이전 정렬 기준(질문키 비교)로 임시 복귀 후 원인 분석한다.

## Open Questions

- preview에서 intent 검토 정보를 어떤 형태(라벨/배지/요약문)로 노출할지?
- 축 정보 표시를 완전히 숨길지, 운영자용 보조 정보로 최소 유지할지?
- intent별 카피 템플릿을 현재 파일 내 상수로 유지할지 별도 모듈로 분리할지?
