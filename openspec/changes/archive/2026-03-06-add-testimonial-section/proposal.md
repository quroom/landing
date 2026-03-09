## Why

신뢰 신호를 강화하려면 실제 사용자 후기가 필요하지만, 현재 랜딩에는 후기를 수집/관리하는 기본 흐름이 없습니다. 특히 대면 무료 상담 직후에만 전달 가능한 비공개 후기 링크가 필요하므로, 초기에는 공개 모집이 아닌 "초대형 후기 작성 페이지"를 먼저 구축해야 합니다.

## What Changes

- 공개 진입이 불가능한 후기 작성 전용 페이지를 추가하고, 운영자가 개별 전달한 초대 링크(토큰)로만 접근 가능하게 한다.
- 사용자는 이름/직군/후기 본문/공개 동의 항목을 제출할 수 있게 한다.
- 제출된 후기는 운영 검토 전 상태로 저장하고, 기본적으로 랜딩 메인에는 노출하지 않는다.
- 후기 공개 섹션은 "승인 후기 최소 N건" 기준을 만족할 때만 노출 가능하도록 정책을 정의한다.
- 초기 기본값은 `N=3`으로 제안하되, 운영 설정으로 조정 가능하게 한다.
- 내일 상담 등 즉시 활용을 위해 "상담 종료 후 개별 링크 전달 -> 작성 -> 검토 대기 저장"의 운영 흐름을 우선 지원한다.

## Capabilities

### New Capabilities

- `testimonial-collection-and-gating`: 후기 작성 페이지, 후기 저장/검토 상태, 최소 공개 건수 게이트 정책을 정의한다.
- `testimonial-invite-link`: 비공개 초대 링크(토큰), 만료/사용 제한, 링크 기반 접근 통제를 정의한다.

### Modified Capabilities

- `founder-first-homepage-positioning`: 메인 페이지 신뢰 요소에 후기 섹션 노출 조건(최소 건수 충족 시)을 추가한다.

## Impact

- Affected code: `landing/views.py`, `landing/forms.py`, `landing/templates/landing/*`, `landing/models.py`, `landing/admin.py`, `landing/urls.py`
- Data impact: 후기 엔티티(작성/검토/노출 상태)와 초대 링크 엔티티(토큰/만료/사용 여부) 저장 구조 추가 가능
- Ops impact: 상담 직후 링크 발급/전달, 관리자 승인 프로세스, 최소 노출 건수 운영 기준 필요
