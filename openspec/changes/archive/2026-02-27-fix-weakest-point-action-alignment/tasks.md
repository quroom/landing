## 1. 입력 계약(8문항 필수) 정렬

- [x] 1.1 `landing/ax_tool_stack.py`에서 `q1~q8` `required` 메타데이터를 전부 필수로 통일한다.
- [x] 1.2 `landing/forms.py`와 `lead_magnet_submit` 검증 흐름에서 8문항 미응답 제출이 실패하도록 정렬한다.
- [x] 1.3 `landing/templates/landing/partials/lead_magnet_form.html` 및 `free_diagnosis.html`의 안내 문구를 8문항 필수 기준으로 갱신한다.

## 2. 보완 포인트-2주 과제 매칭 로직 정렬

- [x] 2.1 `landing/views.py`에서 weakest insight anchor 질문 키를 기준으로 one-action 선택 로직을 단일화한다.
- [x] 2.2 `landing/views.py`에서 weakest insight와 one-action이 동일 `question_key/intent_key` 계보를 가지는지 보장하는 가드 로직을 추가한다.
- [x] 2.3 completion/execution 문구 매핑이 weakest anchor intent와 충돌하지 않도록 title/execution 생성 경로를 정리한다.

## 3. preview/email 공통 섹션 계약 동기화

- [x] 3.1 `landing/lead_magnet_sections.py`의 공통 section AST를 기준으로 preview/email가 같은 보완 포인트/2주 과제를 사용하도록 정렬한다.
- [x] 3.2 `landing/views.py` preview 시나리오 생성에서 quick mode 분기를 제거하고 8문항 상세 모드 기준으로만 시뮬레이션을 구성한다.
- [x] 3.3 `landing/mailers.py`에서 mode/본문/CTA 출력이 preview와 동일 계약을 따르도록 갱신한다.

## 4. 회귀 테스트 및 검증

- [x] 4.1 `landing/tests/test_contact_form.py`에서 4문항 제출 허용 테스트를 8문항 필수 실패/성공 케이스로 대체한다.
- [x] 4.2 `landing/tests/test_lead_magnet_sections.py`, `test_landing_pages.py`, `test_views.py` 기대값을 detailed(8문항) 기준으로 갱신한다.
- [x] 4.3 weakest insight와 one-action 매칭 정합성을 검증하는 테스트를 추가한다.
- [x] 4.4 `./scripts/verify.sh`를 실행해 전체 테스트/체크 통과를 확인한다.
