## Why

현재 리드마그넷 Preview와 실제 발송 이메일이 같은 의도를 가지더라도 렌더링 경로가 분리되어 있어 섹션 순서, 문구, CTA 링크가 쉽게 드리프트할 수 있다.  
변경이 잦은 구간이므로 채널 간 출력 계약을 공통화해 회귀 리스크를 구조적으로 줄여야 한다.

## What Changes

- Preview와 이메일이 공통 섹션 빌더(요약, 최약 카테고리 1개, 2주 실행 1개, CTA 1개)를 공유하도록 요구사항을 명시한다.
- 섹션 순서/제목/CTA 카피와 링크 정규화(`/#contact`)가 채널 간 동일하게 유지되도록 계약을 강화한다.
- 채널별 텍스트/HTML 출력이 같은 데이터 계약을 따르도록 하여 포맷 변경 시 단일 수정 지점을 보장한다.
- 회귀 방지를 위해 Preview-Email 동등성 검증(스냅샷 또는 동등성 테스트) 요구를 추가한다.

## Capabilities

### New Capabilities
- 없음

### Modified Capabilities
- `lead-magnet-email-followup`: 이메일 본문 생성이 Preview와 동일한 섹션 계약을 공유하도록 요구사항을 확장한다.
- `lead-magnet-cta-report-format`: 리포트/Preview/이메일 간 섹션 구성과 CTA 링크 정규화 결과가 일치하도록 채널 일관성 요구를 강화한다.

## Impact

- Backend:
  - `landing/mailers.py`
  - `landing/views.py`
  - 필요 시 공통 렌더 유틸 파일(신규 또는 기존 함수 정리)
- Test:
  - `landing/tests/test_contact_form.py`
  - `landing/tests/test_landing_pages.py`
  - Preview/Email 동등성 검증 테스트(신규 또는 기존 확장)
- Spec:
  - `openspec/specs/lead-magnet-email-followup/spec.md`
  - `openspec/specs/lead-magnet-cta-report-format/spec.md`
