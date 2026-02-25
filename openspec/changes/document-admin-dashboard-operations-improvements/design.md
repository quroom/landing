## Context

문의 데이터 persistence와 메일 전송 상태 저장은 이미 구현되어 있다. 운영 효율을 높이기 위해 관리자 관점에서 실패건/최근건 확인, 재전송, 그리고 `/admin`에서의 빠른 진입 동선을 강화했다.

## Goals / Non-Goals

**Goals:**
- staff 전용 대시보드로 문의 운영 지표를 빠르게 확인한다.
- 상태/기간 필터로 운영 triage 속도를 높인다.
- `/admin`에서 대시보드 진입 링크를 제공한다.
- 재전송 액션으로 실패건 처리 시간을 단축한다.

**Non-Goals:**
- 별도 BI 도구 연동
- 비동기 큐 기반 대량 재전송 시스템
- 권한 체계 세분화(role-based custom permissions)

## Decisions

### Decision 1: Separate staff dashboard route
- `/admin-dashboard/`를 별도 route로 두고 `@staff_member_required` 적용.
- 이유: 기존 랜딩 페이지 코드와 관리자 운영 UI 관심사를 분리.

### Decision 2: Use Django Admin template extension for navigation
- `landing/templates/admin/base_site.html`의 `userlinks` 블록 확장으로 `/admin` 상단에 링크 노출.
- 이유: admin core 코드를 건드리지 않고 동선 개선 가능.

### Decision 3: Use admin action for resend
- `ModelAdmin.actions` 기반 재전송으로 일괄 처리.
- 이유: 운영자 사용성이 높고 표준 admin flow와 일치.

## Risks / Trade-offs

- [재전송 시 동기 처리 지연] → 선택 건수는 운영자가 적정 규모로 실행
- [필터 오해 가능성] → UI에 현재 상태/기간 선택값 표시 유지
- [로그아웃 GET 오류 재발] → 대시보드에서 POST form 고정

## Migration Plan

1. 대시보드/네비게이션/재전송 액션 코드 반영
2. staff 접근/필터 테스트 추가
3. `django check` + `django test` 실행
4. 운영 문서 반영 및 커밋

## Open Questions

- 실패건만 빠르게 재전송하는 전용 버튼을 대시보드에 둘지 여부
- 날짜 필터를 주/월 단위로 확장할지 여부
