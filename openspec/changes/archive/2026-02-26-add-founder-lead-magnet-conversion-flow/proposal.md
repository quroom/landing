## Why

유료 상담/외주 문의는 첫 방문자에게 진입장벽이 높아 전환 손실이 발생한다. 창업자가 부담 없이 시작할 수 있는 무료 리드마그넷을 도입해 초기 신뢰를 만들고, 이후 상담 전환으로 연결할 필요가 있다.
현재 `무료 AX 진단` 문구는 추상도가 높아 즉시 행동 유도가 약하므로, 시간/비용 손실 기준의 구체적 결과물을 전면에 제시하도록 개선이 필요하다.

## What Changes

- 메인 랜딩에 `무료 AX 진단` CTA를 추가한다.
- `3분/8문항 셀프 진단` 폼을 제공하고 결과를 즉시 보여준다.
- 결과 리포트는 `2주 실행 백로그`와 `자동화 우선순위 Top 5` 형태로 제공한다.
- 결과 일부는 즉시 노출하고, 전체 리포트/체크리스트는 이메일 입력 후 제공하는 리드 수집 흐름을 추가한다.
- 외주 문의 오퍼는 `동시 1개사 진행`으로 명시한다.
- 리드 유형을 기존 문의와 분리해 운영자가 대시보드/관리자에서 구분 가능하게 한다.
- 폼 동의 UX는 기존 구조(필수/선택/전체 동의)를 재사용하되, 리드마그넷 목적 문구로 조정한다.
- 진단 결과를 A/B/C 등급으로 분류하고, 등급별 다음 액션 CTA를 분기한다.
  - A/B: 단발성 생산성 개선 상담
  - C: 외주 집중 트랙 상담(동시 1개사 정책 안내)

## Capabilities

### New Capabilities
- `founder-lead-magnet-capture`: 창업자 대상 무료 AX 진단 리드 수집 및 결과 제공
- `lead-magnet-email-followup`: 리드마그넷 신청자에게 자료/후속 안내 메일 발송
- `lead-magnet-admin-segmentation`: 관리자 화면에서 리드마그넷 리드를 기존 문의와 분리 조회
- `lead-magnet-result-bridging`: 진단 결과에서 유료 전환으로 자연스럽게 연결하는 브릿지 오퍼 분기

### Modified Capabilities
- `contact-email-delivery`: 리드마그넷 관련 메일 유형(진단 결과/자료 전달)을 기존 메일 전달 체계에 포함
- `admin-inquiry-dashboard`: 대시보드 필터/표시에서 리드마그넷 리드 식별 및 확인 지원

## Impact

- `landing/templates/landing/index.html`: 무료 진단 CTA/섹션 추가
- `landing/forms.py`: 리드마그넷 폼(또는 기존 폼 확장) 필드 추가
- `landing/views.py`: 진단 제출/결과 계산/후속 메일 트리거 로직
- `landing/models.py`: 리드 유형 구분 및 진단 결과 저장 필드(필요 시)
- `landing/templates/landing/admin_dashboard.html`: 리드마그넷 필터/지표 노출
- `landing/tests/`: 폼 제출, 결과 계산, 메일 발송, 관리자 분류 테스트 추가
- 실험/검증 지표:
  - 진단 CTA 클릭률
  - 진단 완료율
  - 이메일 제출율
  - 리드마그넷 → 상담 전환율
