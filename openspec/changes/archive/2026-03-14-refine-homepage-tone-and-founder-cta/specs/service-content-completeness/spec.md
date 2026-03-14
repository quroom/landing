## MODIFIED Requirements

### Requirement: Service content SHALL include required fields per card
Each service card MUST include service name, target audience, scope summary, CTA mapping, and accountable deliverable wording, and the summary MUST remain understandable to a non-technical founder audience.

#### Scenario: Service card deliverable wording is bounded
- **WHEN** service content is updated in source data
- **THEN** each card keeps deliverable wording within verifiable and transferable scope
- **AND** ambiguous commitments (e.g., unspecified stabilization support period) are avoided or explicitly marked as separately agreed
- **AND** outsourcing-track handover content includes operational minimums (stack/PaaS context, restart basics, troubleshooting/log entry points, support channels)
- **AND** service summaries avoid internal-only phrasing that obscures the founder value proposition

### Requirement: Service offerings SHALL remain consistent across spec and implementation
The documented service offerings in `quroom-landing-spec.md` MUST match the implemented service content structure.

#### Scenario: Spec-to-code service consistency check
- **WHEN** maintainers compare the spec and rendered pages
- **THEN** no documented core service is missing from implementation
- **AND** no implemented core service is undocumented in the spec
- **AND** founder AX offerings and foreign-developer practical-linkage offerings stay page-scoped without cross-mixing
- **AND** founder service group structure (AX / outsourcing / startup foundation infrastructure) is consistent between spec and implementation
