## 1. Core Copy Cleanup

- [x] 1.1 `landing/views.py`에서 핵심 보완 포인트 보조 문구 생성 시 `우선 항목` 노출을 제거한다.
- [x] 1.2 진단 결과 메시지(요약/보완 포인트/완료 기준)에서 중복·부연 표현을 정리하고 intent별 핵심 문장만 남긴다.
- [x] 1.3 `2주 내 끝낼 작업` 완료 기준 문구를 intent별 단문 기준으로 재작성해 반복 접두 문장을 제거한다.

## 2. Preview Simplification and Grouping

- [x] 2.1 `landing/templates/landing/lead_magnet_report_preview.html`에서 4개 분류형 상세 블록(전체 4개 항목 보기)을 제거한다.
- [x] 2.2 `landing/views.py` preview 데이터 구성에서 제목 제외 본문 기준 시그니처를 만들고 동일 본문 시나리오를 그룹화한다.
- [x] 2.3 그룹화된 preview 카드에서 묶인 시나리오 제목을 검토 가능한 형태(목록/요약)로 노출한다.

## 3. Cross-Channel Contract Sync

- [x] 3.1 `landing/lead_magnet_sections.py` 공통 섹션 AST 계약이 정리된 카피를 그대로 반영하도록 점검한다.
- [x] 3.2 `landing/mailers.py`에서 웹/preview와 동일하게 핵심 보완 포인트 문구 및 완료 기준 문구 계약을 맞춘다.
- [x] 3.3 CTA/섹션 순서/핵심 보완 포인트 헤더가 채널별로 달라지지 않도록 출력 경로를 정렬한다.

## 4. Regression Tests and Verification

- [x] 4.1 `landing/tests/test_landing_pages.py`에서 preview 상세 블록 제거 및 그룹화 노출 기준을 검증한다.
- [x] 4.2 `landing/tests/test_lead_magnet_sections.py` 스냅샷을 갱신해 `우선 항목` 미노출과 새 완료 기준 문구를 검증한다.
- [x] 4.3 `landing/tests/test_contact_form.py` 이메일 본문/HTML이 갱신된 공통 카피 계약을 따르는지 검증한다.
- [x] 4.4 필요 시 `landing/tests/test_views.py`에 preview 그룹화 시그니처 회귀 테스트를 추가한다.
- [x] 4.5 `./scripts/verify.sh`를 실행해 전체 검증을 통과시킨다.
