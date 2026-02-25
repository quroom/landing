# Capability: hero-kpi-suppression

## Purpose
외부 랜딩에 내부 운영 KPI 문구가 노출되지 않도록 통제한다.

## ADDED Requirements

### Requirement: Internal KPI text SHALL NOT be shown on public hero
The system MUST suppress the internal KPI message (`hero_kpi_text`) from externally visible hero sections.

#### Scenario: Hero renders without KPI text
- **WHEN** the main landing page hero is rendered
- **THEN** no internal target phrase is displayed in hero support copy

#### Scenario: Persona pages render without KPI text
- **WHEN** persona landing pages are rendered
- **THEN** no internal KPI text is displayed in hero or equivalent top section
