## ADDED Requirements

### Requirement: Career timeline MUST communicate capability progression
The system MUST present career timeline copy that clearly connects prior field operations experience to current automation execution positioning.

#### Scenario: Timeline progression is readable at a glance
- **WHEN** a visitor scans the career timeline section
- **THEN** the timeline MUST present entries in chronological order
- **AND** the copy MUST make progression understandable as qualification, execution, expansion, and current operation

#### Scenario: Timeline wording follows a consistent format
- **WHEN** maintainers add or edit timeline entries
- **THEN** each label MUST follow a consistent style using year-oriented action wording
- **AND** key entries related to automation execution MUST preserve action and outcome context

### Requirement: Key legacy-business milestones MUST be represented
The system MUST include 2015~2017 milestone entries to preserve business context before current company operation.

#### Scenario: Required milestones are present
- **WHEN** timeline data is rendered on landing page
- **THEN** it MUST include `2015: 공인중개사 자격 취득`
- **AND** it MUST include `2016: 중개업 활동, 매물 수집 자동화로 운영 시간 단축`
- **AND** it MUST include `2017: 쉐어하우스 창업 및 확장`
