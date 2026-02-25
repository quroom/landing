## 1. Spec and content source updates

- [x] 1.1 Update `openspec/changes/consolidate-codex-docs-into-openspec/docs/quroom-landing-spec.md` to remove Hero KPI text and define page role split (`/`, `/for-founders/`, `/for-foreign-developers/`)
- [x] 1.2 Add service completeness rules to the landing spec (required fields: service name, audience, scope summary, CTA mapping)
- [x] 1.3 Refactor `landing/content.py` into shared + persona-specific content blocks and remove active use of `hero_kpi_text`
- [x] 1.4 Ensure service data includes all required fields and no missing core service item across main/founder/foreign-developer pages

## 2. Routing and view implementation

- [x] 2.1 Add dedicated routes for `/for-founders/` and `/for-foreign-developers/` in `landing/urls.py`
- [x] 2.2 Implement corresponding views in `landing/views.py` using shared layout context with persona-specific overrides
- [x] 2.3 Keep `/` as trust-oriented hub and ensure it no longer renders internal KPI support text

## 3. Template implementation

- [x] 3.1 Update `templates/landing/index.html` to remove Hero KPI line and keep common trust-first narrative
- [x] 3.2 Create `templates/landing/founders.html` with founder-focused messaging, service framing, and CTA
- [x] 3.3 Create `templates/landing/foreign_developers.html` with foreign-developer-focused messaging, onboarding/career CTA
- [x] 3.4 Ensure service cards in all pages are consistent with spec-required fields and mapped CTAs

## 4. Verification

- [x] 4.1 Verify all three routes render successfully and navigation/entry links work as intended
- [x] 4.2 Verify contact form flow still works from each page (validation + submission response)
- [x] 4.3 Verify no public page displays internal KPI phrase and service content has no missing core item
- [x] 4.4 Run a quick syntax/health check (`python3 -m compileall`) and confirm no template/view import errors
