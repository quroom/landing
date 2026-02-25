## 1. Spec and content source alignment

- [x] 1.1 Update `openspec/changes/consolidate-codex-docs-into-openspec/docs/quroom-landing-spec.md` with founder-first main page scope and foreign-developer page scope boundaries
- [x] 1.2 Add canonical career timeline copy (2011.01~2012.07, 2012.08~2014.10, 2020.03~present) and evidence-link policy to the landing spec
- [x] 1.3 Define founder AX package cards (AX 진단 90분, 자동화 구축 2주, 실행 코칭 4주) in `landing/content.py` with required card fields
- [x] 1.4 Define foreign-developer practical-linkage content, support boundary (visa/legal out-of-scope), and persona-specific FAQ/KPI fields in `landing/content.py`

## 2. Template and page behavior updates

- [x] 2.1 Update `landing/templates/landing/index.html` to keep founder-first narrative and remove foreign-developer practical-linkage detail
- [x] 2.2 Update `landing/templates/landing/founders.html` to align with founder AX service offers and package CTA structure
- [x] 2.3 Update `landing/templates/landing/foreign_developers.html` to emphasize practical-linkage support, credibility signals, and out-of-scope notice
- [x] 2.4 Ensure `landing/views.py` context wiring supports separated founder vs foreign-developer fields without cross-mixing

## 3. Governance and consistency checks

- [x] 3.1 Verify persona CTA ownership is separated (founder consultation CTA vs foreign practical-linkage CTA)
- [x] 3.2 Verify persona FAQ ownership is separated (founder: scope/cost/timeline, foreign: linkage process/preparation/support scope)
- [x] 3.3 Verify KPI keys are separated for each persona journey and can be tracked independently
- [x] 3.4 Verify evidence-link governance is applied (LinkedIn/portfolio/GitHub mapping, category-level network wording by default)

## 4. Validation and readiness

- [x] 4.1 Run `python3 -m compileall landing manage.py` and resolve content/template reference issues
- [x] 4.2 Run `./.venv/bin/python manage.py check` and resolve Django configuration/template errors
- [x] 4.3 Verify core routes (`/`, `/for-founders/`, `/for-foreign-developers/`) render with intended page-scoped messaging
- [x] 4.4 Final review for spec-to-implementation consistency against modified capabilities (`persona-landing-pages`, `landing-spec-persona-governance`, `service-content-completeness`)
