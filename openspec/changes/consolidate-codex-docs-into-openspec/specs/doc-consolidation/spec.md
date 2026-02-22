## ADDED Requirements

### Requirement: Centralize codex docs under the change folder
All existing landing/vibe-coding markdown 문서를 SHALL be relocated to `openspec/changes/consolidate-codex-docs-into-openspec/docs/` so that a single OpenSpec change owns their history and archival.

#### Scenario: Doc relocation completed
- **WHEN** the listed docs are moved with `git mv`
- **THEN** the files exist under `openspec/changes/consolidate-codex-docs-into-openspec/docs/`
- **AND** their git history is preserved

### Requirement: Leave pointers at old codex-document location
The original `codex-document/` path SHALL contain a concise pointer README that lists the moved files and links to their new locations.

#### Scenario: Pointer README present
- **WHEN** a user opens `codex-document/README.md`
- **THEN** they see each migrated filename and the new path under `openspec/changes/consolidate-codex-docs-into-openspec/docs/`
- **AND** there are no stale copies of the moved files in `codex-document/`

### Requirement: Update root README with new doc locations
The repository root README SHALL describe where the landing/vibe-coding docs live after consolidation and how to access them.

#### Scenario: Root README navigation
- **WHEN** a user reads `README.md`
- **THEN** they find a section linking to the consolidated docs path
- **AND** the section notes that `codex-document/` now contains only pointers

### Requirement: Keep static assets in place
Image and asset paths (e.g., `images/portfolio/...`) SHALL remain unchanged; no asset copies or moves are performed during this consolidation.

#### Scenario: Asset paths unaffected
- **WHEN** the docs are opened after the move
- **THEN** image references still resolve because asset paths are unchanged
- **AND** no duplicate assets are introduced
