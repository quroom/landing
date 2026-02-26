# founder-lead-magnet-capture Specification

## Purpose
Define the founder-focused free AX diagnosis capture flow and immediate result behavior on the main landing page.

## Requirements
### Requirement: Founder landing MUST provide a free AX diagnosis lead magnet flow
The system MUST provide a founder-focused free diagnosis flow on the main landing page that can be completed within a short interaction.

#### Scenario: User starts diagnosis from main landing
- **WHEN** a visitor clicks the free diagnosis CTA on the main landing page
- **THEN** the system MUST display a diagnosis form with 8 questions and required contact fields
- **AND** the flow MUST be labeled as a free founder-oriented AX diagnosis

### Requirement: Diagnosis submission MUST return immediate partial result
The system MUST calculate and show an immediate partial result after valid diagnosis submission.

#### Scenario: Valid diagnosis is submitted
- **WHEN** a user submits all required diagnosis fields
- **THEN** the system MUST calculate a diagnosis score and grade (A/B/C)
- **AND** the system MUST show immediate partial result summary including top priorities
