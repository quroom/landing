## 1. Priority and CTA Logic Refinement

- [x] 1.1 Update result priority selection in `landing/views.py` to expose only top 3 items in UI/report output
- [x] 1.2 Enforce single-CTA policy per result and map CTA label/link by grade (A/B/C) in `landing/views.py`
- [x] 1.3 Ensure preview generation path uses the same grade/priority/CTA output logic as live submission flow

## 2. Report Readability Improvements

- [x] 2.1 Refactor report text blocks in `landing/views.py` for concise CTA-first flow (summary -> top 3 -> next action)
- [x] 2.2 Improve web result layout spacing/line breaks in `landing/templates/landing/partials/lead_magnet_form.html`
- [x] 2.3 Improve preview readability presentation in `landing/templates/landing/lead_magnet_report_preview.html`

## 3. Email Formatting Improvements

- [x] 3.1 Update lead-magnet email text format in `landing/mailers.py` to include cleaner paragraph spacing and concise sections
- [x] 3.2 Update lead-magnet HTML email in `landing/mailers.py` with improved line-height, block spacing, and one primary CTA

## 4. Verification

- [x] 4.1 Update/add tests for top-3 priority output, single CTA behavior, and preview consistency (`landing/tests/test_contact_form.py`, `landing/tests/test_landing_pages.py`)
- [x] 4.2 Run `./scripts/verify.sh` and confirm all checks pass
