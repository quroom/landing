## Context

메인 랜딩은 founder-first 구조와 CTA 위계는 이미 정리되어 있다. 최근 사용자 피드백 기준으로도 문제는 `메시지 구조`보다 `문장 결`에 더 가깝다. 실제 코드 변경도 전면 재작성보다는 `Official` 제거, 몇몇 번역투 문구 교정, 문의 섹션 톤 완화 수준에서 끝났다.

따라서 이 change는 더 이상 `섹션 역할 재설계`가 아니라, 현재 founder 홈페이지 톤을 유지하면서도 읽히는 감각을 해치지 않는 `micro-copy polish`로 보는 것이 맞다.

## Goals / Non-Goals

**Goals:**
- founder 홈페이지에서 어색한 표현만 좁은 범위로 다듬는다.
- `Official`처럼 불필요한 보조 표기를 제거한다.
- 미세 수정에 맞춰 테스트를 동기화한다.
- 현재 구조와 톤을 유지한 채 문장 가독성만 개선한다.

**Non-Goals:**
- 서비스 구성 자체를 추가/삭제하지 않는다.
- Hero/About/Services/Contact를 전면 재작성하지 않는다.
- trust narrative를 새로 설계하지 않는다.
- CTA 구조나 라우팅을 다시 설계하지 않는다.
- 데이터 모델, 관리자 기능, 폼 구조는 변경하지 않는다.

## Decisions

### 1. change 범위는 `전면 재작성`이 아니라 `micro-copy polish`로 제한한다
- 이유: 실제 반영과 사용자 선호가 모두 작은 수정에 맞춰져 있다.
- 대안: 기존 broad rewrite 방향을 유지한다.
- 기각 이유: 현재 코드 상태와 맞지 않고, 사용자가 불편해한 톤 변경을 다시 키울 가능성이 높다.

### 2. 구조와 메시지 방향은 유지하고, 문장 결만 다듬는다
- 이유: 현재 founder homepage의 정보 구조 자체는 이미 충분히 안정적이다.
- 대안: 섹션 역할이나 신뢰 흐름까지 다시 설계한다.
- 기각 이유: 이번 범위를 불필요하게 키운다.

### 3. 변경은 homepage에 보이는 문장과 관련 테스트까지만 포함한다
- 이유: 실제 변경 파일도 `content.py`, `index.html`, `test_landing_pages.py` 수준으로 제한됐다.
- 대안: founder route나 추가 spec capability까지 연쇄 수정한다.
- 기각 이유: 이번 change를 다시 broad scope로 되돌린다.

## Risks / Trade-offs

- [리스크] 너무 많이 다듬으려다 다시 전면 개편으로 커질 수 있다.
  - 완화: 문장 수 기준으로 작업 범위를 제한한다.
- [리스크] change 문서가 코드보다 더 큰 상태로 남을 수 있다.
  - 완화: proposal/design/tasks를 실제 반영 수준에 맞게 축소한다.

## Migration Plan

1. active change 범위를 micro-copy polish 수준으로 재정의한다.
2. 실제 반영된 homepage 문장 수정과 테스트 범위를 문서에 맞춘다.
3. 더 이상의 broad rewrite 의도가 없다면, 이 change를 작은 polish change로 닫을 준비를 한다.

## Open Questions

현재 상태에서 homepage copy work를 종료하고, 이 change는 micro-copy polish change로 archive한다. broad delta specs는 main specs로 sync하지 않는다.
