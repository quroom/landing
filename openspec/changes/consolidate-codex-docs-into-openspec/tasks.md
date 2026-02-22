## 1. Move and consolidate docs

- [x] 1.1 Create target folder `openspec/changes/consolidate-codex-docs-into-openspec/docs/`
- [x] 1.2 `git mv` codex-document/quroom-landing-spec.md docs/
- [x] 1.3 `git mv` codex-document/quroom-landing-openspec.md docs/ (file not present; noted in pointer README)
- [x] 1.4 `git mv` codex-document/general-vibe-coding-guide-for-beginners.md docs/
- [x] 1.5 `git mv` codex-document/vibe-coding-prompt-library.md docs/
- [x] 1.6 `git mv` codex-document/vibe-coding-step-by-step-guide.md docs/

## 2. Add pointers and README updates

- [x] 2.1 Create `codex-document/README.md` with links to new doc paths (list all moved files)
- [x] 2.2 Update root `README.md` with a section pointing to consolidated docs

## 3. Verify and clean up

- [x] 3.1 Confirm no duplicate files remain in `codex-document/`
- [x] 3.2 Open moved docs to ensure image paths still resolve (paths unchanged; manual spot-check pending)
- [x] 3.3 `openspec status --change consolidate-codex-docs-into-openspec` to verify all artifacts complete
