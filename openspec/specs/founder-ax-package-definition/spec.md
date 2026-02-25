# Capability: founder-ax-package-definition

## Purpose
창업자 대상 AX 서비스를 패키지 단위로 명확히 정의한다.

## Requirements

### Requirement: AX offerings MUST be package-defined
The system MUST define founder AX offerings as fixed packages with scope, duration, and expected deliverables.

#### Scenario: Package structure is explicit
- **WHEN** maintainers review service content for founder pages
- **THEN** each AX package includes name, duration, and deliverable summary
- **AND** package cards use a consistent field structure to support comparison

### Requirement: Default founder core packages MUST include baseline options
The system MUST provide baseline founder core package options: AX 진단(90분), AX 구축(2주~4주), and 외주용역 집중 트랙(4주~8주).

#### Scenario: Baseline founder core packages are present
- **WHEN** founder core package data is rendered
- **THEN** AX 진단, AX 구축, and 외주용역 집중 트랙 are present as distinct cards
- **AND** each card maps to a consultation CTA
