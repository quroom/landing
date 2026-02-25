# Capability: evidence-link-governance

## Purpose
신뢰 문구가 검증 가능한 출처와 공개 정책을 따르도록 통제한다.

## ADDED Requirements

### Requirement: Credibility claims MUST have evidence-link type mapping
The system MUST define evidence-link types for credibility claims (LinkedIn, portfolio, GitHub) where public proof is available.

#### Scenario: Evidence-link policy review
- **WHEN** a contributor updates trust claims
- **THEN** each claim can be mapped to an allowed evidence-link type or marked as non-public with rationale

### Requirement: Network claims MUST follow disclosure policy
The system MUST avoid unauthorized company-name disclosure and use category-level wording by default.

#### Scenario: Network claim rendering
- **WHEN** network strength is described on landing pages
- **THEN** category-level wording is used unless explicit permission exists for named disclosure
