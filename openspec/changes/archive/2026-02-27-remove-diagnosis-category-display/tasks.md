## 1. Survey Rendering Alignment

- [x] 1.1 진단 설문 템플릿에서 카테고리명/카테고리 설명 노출을 제거하고 질문 리스트 렌더링만 유지한다.
- [x] 1.2 질문 카드 UI에서 필수/선택 표시만 남기고 카테고리 기반 그룹 마크업을 정리한다.
- [x] 1.3 설문 진입/제출 화면에서 카테고리 용어가 노출되는 텍스트를 질문 중심 문구로 교체한다.

## 2. Question Intent Consistency

- [x] 2.1 `ax_tool_stack` 질문 메타에서 q1~q8 intent key와 문구 결(행동 단위/시간 기준)을 점검하고 불일치 항목을 수정한다.
- [x] 2.2 같은 축의 문항 쌍(q1/q2, q3/q4, q5/q6, q7/q8)이 동일한 질문 관점으로 읽히도록 문항 표현을 통일한다.
- [x] 2.3 질문-의도 매핑이 누락되지 않도록 메타 접근 경로를 정리하고 기본 fallback 동작을 명확히 한다.

## 3. Result Interpretation Mapping

- [x] 3.1 결과 생성 로직에서 1차 해석/우선과제가 category label이 아니라 intent key 기반으로 선택되도록 정리한다.
- [x] 3.2 축별 메시지 생성 시 anchor 문항 선택 규칙(우선순위/동점 처리)을 고정하고 보조 문장에 anchor 맥락을 반영한다.
- [x] 3.3 one-action과 추천 툴이 동일 intent에서 파생되도록 매핑 경로를 단일화한다.
- [x] 3.4 사용자 노출 요약 문구에서 내부 axis key/카테고리 기술 용어가 직접 노출되지 않도록 정리한다.

## 4. Cross-Channel Contract Sync

- [x] 4.1 공통 섹션 AST(summary/weakest/one_action/tools/next_action) 구조를 유지하면서 intent 기반 카피로 갱신한다.
- [x] 4.2 preview 화면 출력이 웹 결과와 같은 intent 매핑/섹션 순서를 따르도록 정합성을 맞춘다.
- [x] 4.3 follow-up 이메일(text/html)에서 웹/preview와 동일한 intent 기반 해석이 출력되도록 동기화한다.
- [x] 4.4 CTA 링크/주석/추천툴 표기가 채널별로 달라지지 않도록 공통 계약 테스트 포인트를 정리한다.

## 5. Regression Tests and Verification

- [x] 5.1 `test_landing_pages`에서 설문 카테고리 비노출과 질문 중심 렌더링 동작을 검증한다.
- [x] 5.2 `test_lead_magnet_sections`에서 섹션 텍스트 스냅샷을 intent 기반 결과로 갱신하고 회귀를 검증한다.
- [x] 5.3 `test_contact_form`에서 이메일 본문/HTML이 intent 기반 문구와 동일 계약을 따르는지 검증한다.
- [x] 5.4 preview/email/web 섹션 동등성(헤더/순서/CTA/추천툴)을 회귀 테스트로 보강한다.
- [x] 5.5 `./scripts/verify.sh`를 실행해 전체 검증을 통과시킨다.
