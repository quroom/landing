# Capability: service-content-completeness

## MODIFIED Requirements

### Requirement: Service content SHALL include required fields per card
Each service card MUST include service name, target audience, scope summary, CTA mapping, and accountable deliverable wording.

#### Scenario: Service card deliverable wording is bounded
- **WHEN** service content is updated in source data
- **THEN** each card keeps deliverable wording within verifiable and transferable scope
- **AND** ambiguous commitments (e.g., unspecified stabilization support period) are avoided or explicitly marked as separately agreed
- **AND** outsourcing-track handover content includes operational minimums (stack/PaaS context, restart basics, troubleshooting/log entry points, support channels)
