## ADDED Requirements

### Requirement: Internal KPI text SHALL NOT be shown on public hero
The system MUST suppress the internal KPI message (`hero_kpi_text`) from externally visible hero sections.

#### Scenario: Hero renders without KPI text
- **WHEN** the main landing page hero is rendered
- **THEN** no internal target phrase is displayed in hero support copy

#### Scenario: Persona pages render without KPI text
- **WHEN** persona landing pages are rendered
- **THEN** no internal KPI text is displayed in hero or equivalent top section
