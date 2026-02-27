## Context

현재 진단 결과 생성 경로는 `핵심 보완 포인트`와 `2주 내 끝낼 작업 1개`를 서로 다른 우선순위 기준에서 뽑을 수 있어, 사용자에게 같은 리포트 안에서 상충되는 가이드를 줄 수 있다.  
또한 `q1~q8` 구조임에도 `q1,q3,q5,q7`만 필수인 경로가 남아 있어 quick/detailed 분기가 발생하고, preview/이메일/웹 결과 검증 포인트가 늘어나 유지보수 비용이 커진 상태다.

## Goals / Non-Goals

**Goals:**
- 보완 포인트와 2주 실행 과제가 동일한 질문 근거에서 생성되도록 결과 매핑을 단일화한다.
- 진단 입력 계약을 8문항 전체 필수로 고정해 quick mode 경로를 제거한다.
- preview와 이메일이 동일한 섹션 계약(요약/보완 포인트/2주 과제/CTA)을 유지하도록 검증 지점을 단순화한다.
- 테스트를 통해 매칭 불일치 회귀를 방지한다.

**Non-Goals:**
- 설문 문항 텍스트 자체를 대폭 재작성하는 작업
- 축(axis) 개수/구조를 변경하는 정보 구조 개편
- 추천 툴 알고리즘의 대규모 재설계

## Decisions

### 1) 2주 실행 과제 선택을 `핵심 보완 포인트` 근거에 정렬
- 선택: weakest axis/anchor question을 먼저 확정하고, 2주 실행 과제는 해당 anchor와 같은 intent 기반으로 생성한다.
- 이유: 사용자 입장에서 "무엇이 문제인지"와 "그래서 지금 뭘 해야 하는지"가 같은 문맥으로 이어져야 신뢰도가 높다.
- 대안: 기존처럼 전역 `(2-score)*impact_weight` 최댓값을 단독 사용.
  - 미채택 이유: weakest insight와 action intent가 쉽게 분리되어 문구 충돌이 재발한다.

### 2) 입력 계약을 8문항 필수로 고정하고 quick mode 제거
- 선택: `DIAGNOSIS_QUESTION_META`의 `required`를 전 문항 `True`로 맞추고, 커버리지 라벨/분기에서 quick 경로를 제거한다.
- 이유: 결과 해석 기준을 단일화하고, preview/email 스냅샷 복잡도를 줄일 수 있다.
- 대안: core 4개 필수 + optional 4개 유지.
  - 미채택 이유: 4문항/8문항 결과 계약을 병행하면 테스트/카피/로직 드리프트가 누적된다.

### 3) preview/email 동일 섹션 계약을 강제
- 선택: 결과 생성 경로에서 공통 section AST를 기준으로 preview/email를 렌더링하고, perfect score 예외도 동일 계약 내에서 최소 분기만 유지한다.
- 이유: 채널별 문구 드리프트를 줄이고, QA 시 비교 기준을 명확하게 유지할 수 있다.
- 대안: 채널별 별도 문자열 템플릿 유지.
  - 미채택 이유: 같은 intent라도 채널별 문장 불일치가 반복된다.

## Risks / Trade-offs

- [Risk] 8문항 전부 필수로 전환 시 이탈률 증가 가능  
  → Mitigation: 폼 안내 문구를 명확히 하고, 라디오 선택 문구를 간결하게 유지한다.

- [Risk] weakest anchor 기준으로 과제를 고정하면 전역 임팩트 최적화가 약해질 수 있음  
  → Mitigation: weakest axis 내부에서는 기존 impact_weight/score 우선순위를 유지해 실행 효율을 보존한다.

- [Risk] preview 시나리오 수가 줄어 기존 리뷰 흐름이 바뀔 수 있음  
  → Mitigation: 그룹화 카드에서 시나리오 제목 목록을 유지해 검토 추적성을 확보한다.

## Migration Plan

1. 메타데이터/폼 계약 변경
   - `q1~q8 required=True`로 통일
   - 진단 폼/페이지 안내 문구를 8문항 필수 기준으로 변경
2. 결과 생성 로직 정렬
   - weakest insight anchor와 one-action intent를 동일 근거로 생성
   - quick mode 분기 및 관련 라벨 제거
3. preview/email 계약 동기화
   - shared section AST를 기준으로 비교 시그니처를 유지
   - perfect score 예외 출력도 동일 계약 내에서 검증
4. 테스트 갱신
   - 4문항 허용 테스트 제거/수정
   - 매칭 정합성 및 8문항 필수 검증 추가

Rollback:
- required 플래그와 coverage 분기 로직을 이전 상태로 되돌리면 기능 롤백 가능하다.

## Open Questions

- 없음 (이번 변경에서는 결정 완료)
