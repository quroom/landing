## Context

현재 언어 전환 UI는 `base.html`에서 `fixed right-4 top-4 z-50`로 전역 배치되어 있어,
헤더(`z-40`) 우측 CTA와 뷰포트 조건에 따라 겹칠 수 있다.

## Goals / Non-Goals

**Goals:**
- 언어 전환 UI와 헤더 CTA 충돌 제거
- 공통 베이스 템플릿 사용 페이지에서 일관된 동작 보장
- 기존 언어 전환 동작(set_language POST) 유지

**Non-Goals:**
- 카피라이팅/CTA 문안 개편
- 헤더 정보 구조 전면 개편

## Decisions

### Decision 1: Language switcher를 헤더 흐름에 맞춘 위치로 재배치

전역 fixed 오버레이를 피하고, 헤더/내비 구조를 해치지 않는 위치로 배치한다.
필요 시 브레이크포인트별로 표시 위치를 나눠 CTA 영역과 분리한다.

### Decision 2: 회귀 방지 테스트 추가

기존 랜딩 페이지 테스트에 언어 전환 UI 존재/클래스 및 CTA 노출 관련 검증을 추가해,
추후 스타일 변경 시 겹침 회귀를 조기에 탐지한다.
