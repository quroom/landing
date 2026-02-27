## 1. Question Model and Metadata

- [x] 1.1 q1~q8 질문 문구를 대중적인 표현으로 통일하고 질문별 intent key를 정의한다.
- [x] 1.2 `landing/ax_tool_stack.py`에 질문 메타(축 매핑, 표시 순서, `impact_weight`, 필수/선택 여부)를 정리한다.
- [x] 1.3 핵심 4문항 `q1,q3,q5,q7`을 필수로, 추가 4문항 `q2,q4,q6,q8`을 선택으로 고정한다.

## 2. Survey Flow and Validation

- [x] 2.1 설문 UI를 카테고리 헤더 없는 질문 중심 렌더링으로 바꾸고 8문항을 항상 노출한다.
- [x] 2.2 폼 검증에서 핵심 4문항 필수 규칙과 추가 4문항 미응답 허용 규칙을 반영한다.
- [x] 2.3 각 문항 응답을 개별 필드로 저장해 점수 계산/카피 매핑에서 직접 참조 가능하게 만든다.
- [x] 2.4 응답 개수 기준으로 `quick(4)`/`detailed(8)` 커버리지 상태를 생성한다.

## 3. Scoring and Priority Recommendation

- [x] 3.1 총점과 축 점수를 응답한 문항 수 기준 분모로 정규화한다(선택 미응답은 분모에서 제외).
- [x] 3.2 정규화 점수 기준으로 A/B/C 등급 계산이 유지되도록 임계값/회귀를 점검한다.
- [x] 3.3 우선순위 추천 로직에 `(2 - answer_score) * impact_weight` 공식을 적용한다.
- [x] 3.4 동점일 때 `하고 있지 않음`을 `어느 정도 하고 있음`보다 우선 추천하도록 정렬 규칙을 반영한다.
- [x] 3.5 결과에 2주 우선 과제 1개, 완료 기준 1문장, 추천 도구를 함께 출력한다.

## 4. Result Copy and Cross-Channel Contract

- [x] 4.1 결과 시뮬레이션(요약/카테고리/우선과제/CTA) 문구를 질문 intent와 1:1로 매핑되게 재작성한다.
- [x] 4.2 `landing/lead_magnet_sections.py` 공통 섹션 생성 경로에서 preview/email 공통 카피 계약을 유지한다.
- [x] 4.3 preview/email 출력에 `quick`/`detailed` 상태 표시를 포함하고 섹션 순서와 제목을 동일하게 유지한다.
- [x] 4.4 추천 도구 문구가 중복/충돌 없이 우선 과제 블록과 일치하도록 정리한다.

## 5. Tests and Verification

- [x] 5.1 `landing/tests/test_landing_pages.py`에서 카테고리 비노출 + 8문항 상시 노출 + 필수/선택 동작을 검증한다.
- [x] 5.2 `landing/tests/test_contact_form.py`에서 핵심 4문항 필수/추가 4문항 선택 제출 케이스를 검증한다.
- [x] 5.3 `landing/tests/test_lead_magnet_sections.py`에서 정규화 점수, 우선 과제 1개, 추천 도구 정합을 검증한다.
- [x] 5.4 preview/email 동등성(공통 섹션, 카피, CTA 링크, 커버리지 표시) 회귀 테스트를 갱신한다.
- [x] 5.5 `./scripts/verify.sh`를 실행해 전체 검증을 통과시킨다.
