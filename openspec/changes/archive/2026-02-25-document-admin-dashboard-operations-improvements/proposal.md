## Why

문의 데이터가 저장되더라도 운영자가 실패 건과 최근 문의를 빠르게 점검하지 못하면 대응 지연이 발생한다. `/admin` 진입 후 즉시 대시보드로 이동하고, 상태/기간 기준으로 문의를 확인할 수 있는 운영 화면이 필요하다.

## What Changes

- staff 전용 문의 운영 대시보드(`/admin-dashboard/`)를 제공한다.
- 대시보드에 상태 KPI, 상태 필터, 기간 필터, 최근 문의 목록, 문의 유형 통계를 제공한다.
- Django Admin 화면에서 대시보드로 바로 이동할 수 있는 링크를 추가한다.
- 대시보드에서 POST 기반 로그아웃 동작을 제공한다.
- Django Admin 액션으로 실패/선택 문의 메일 재전송 기능을 제공한다.

## Capabilities

### New Capabilities
- `admin-inquiry-dashboard`: 문의 운영 현황을 staff가 실시간으로 점검하는 대시보드 기능
- `admin-dashboard-navigation`: `/admin`에서 대시보드로 빠르게 이동하는 네비게이션 기능

### Modified Capabilities
- None.

## Impact

- `landing/views.py`: 관리자 대시보드 집계/필터 로직
- `landing/urls.py`: 대시보드 URL 노출
- `landing/admin.py`: 메일 재전송 admin action
- `landing/templates/landing/admin_dashboard.html`: 운영 UI/필터/로그아웃 버튼
- `landing/templates/admin/base_site.html`: `/admin` 상단 대시보드 링크
- `landing/tests/test_landing_pages.py`: staff 접근/필터 동작 테스트
