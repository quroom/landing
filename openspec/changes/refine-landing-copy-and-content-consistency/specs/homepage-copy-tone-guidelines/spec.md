## MODIFIED Requirements

### Requirement: Founder homepage copy MUST use pragmatic and non-promotional tone
The system MUST present founder homepage copy in a pragmatic tone that avoids exaggerated promises, translation-like phrasing, policy-style sections, and brochure-style wording.

#### Scenario: User scans homepage primary copy
- **WHEN** a user reads the Hero, About, Services, and Contact sections on `/`
- **THEN** the copy uses short, judgment-oriented sentences
- **AND** the copy avoids vague promotional claims such as unspecified end-to-end guarantees
- **AND** the copy keeps founder trust grounded in scope, priority, delegation criteria, and execution boundaries
- **AND** public-facing copy does not render internal policy language that is better kept in source documents or maintainers' notes

### Requirement: Founder homepage copy MUST preserve meaning while reducing abstraction
The system MUST keep the existing service meaning and CTA structure while rewriting copy to reduce abstract nouns and improve direct readability.

#### Scenario: Maintainer reviews rewritten homepage copy
- **WHEN** homepage founder copy is updated
- **THEN** the service lineup, CTA hierarchy, and section flow remain unchanged
- **AND** rewritten sentences use more direct verbs and fewer abstract framing terms
- **AND** the copy remains understandable to a non-technical founder audience
- **AND** Hero and About copy align around work that can be trusted and delegated, not only discussion or strategy framing
