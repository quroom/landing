## Why

현재 메인 랜딩의 제공 서비스 카피는 기능 나열 중심이라 문장 톤이 단조롭고, 일부 결과물 문구는 계약/운영 범위가 불명확하게 해석될 여지가 있다. 특히 `안정화 지원`처럼 기간·범위가 고정되지 않은 표현은 기대치 불일치 리스크를 만든다.

서비스 카피를 더 읽기 쉬운 실행형 톤으로 정리하되, 결과물 문구는 실제로 책임 가능한 범위로 한정하는 기준이 필요하다.

## What Changes

- 메인 랜딩 서비스 카드 카피를 실행형 문장 리듬으로 정리한다.
- 카드별 결과물 문구를 책임 가능한 산출물 범위로 재정의한다.
- 외주용역 트랙의 후속 운영/안정화 관련 표현은 `별도 합의` 원칙으로 명시한다.
- 운영 이관 문서의 최소 포함 항목(스택/PaaS, 재시작, 점검, 지원 채널)을 정의한다.

## Capabilities

### Modified Capabilities
- `founder-ax-package-definition`: 카드별 결과물 문구에 책임 범위 명시 요구사항 추가
- `service-content-completeness`: 서비스 카드 필수 필드에 "책임 가능한 결과물 문구" 기준 추가

## Impact

- Affected specs: `founder-ax-package-definition`, `service-content-completeness`
- Affected code (expected): `landing/content.py`, `landing/templates/landing/index.html`, 관련 테스트
- Operational impact: 제안서/상담 응답과 랜딩 카피 간 결과물 용어를 일치시켜 기대치 불일치를 줄임
