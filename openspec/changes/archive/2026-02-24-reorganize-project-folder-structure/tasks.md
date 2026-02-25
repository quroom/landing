## 1. Target structure definition

- [x] 1.1 Define target layout with `landing/` as the single project code root and document current-to-target mapping
- [x] 1.2 Identify move candidates (`quroom_landing/`, `templates/`, `static/`) to relocate under `landing/`

## 2. Code and path migration

- [x] 2.1 Move project code into `landing/` while preserving behavior
- [x] 2.2 Update Python imports and Django settings module/static/template paths impacted by moves
- [x] 2.3 Update template/static/image references to match `landing/`-centric paths

## 3. Documentation alignment

- [x] 3.1 Update `README.md` with `landing/`-single-root folder map and navigation guidance
- [x] 3.2 Update relevant OpenSpec/operation docs to reference the new structure

## 4. Verification and stabilization

- [x] 4.1 Run compile/import checks (`python3 -m compileall`) and fix path-related issues
- [x] 4.2 Run local server and verify key routes/templates/static assets load correctly
- [x] 4.3 Verify no orphaned paths remain in code/documentation and finalize migration notes
