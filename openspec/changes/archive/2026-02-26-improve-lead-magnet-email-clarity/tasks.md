## 1. Founder-Focused Report Structure

- [x] 1.1 Update lead-magnet result payload to expose a default summary view with only the weakest category visible.
- [x] 1.2 Add optional "show all categories" data path for preview/report consumers.
- [x] 1.3 Ensure report text sections stay concise: summary, weakest category, one 2-week action, one CTA.

## 2. Email Copy and Sender Branding

- [x] 2.1 Refactor follow-up email builder to use simple founder-friendly language in both text and HTML.
- [x] 2.2 Remove foreign-developer positioning from free diagnosis follow-up email content.
- [x] 2.3 Enforce sender display name as `큐룸` via environment-backed from-email configuration.

## 3. CTA and Preview Consistency

- [x] 3.1 Normalize CTA links so `#contact` always resolves to homepage contact URL (`/#contact`) in email and preview.
- [x] 3.2 Sync preview rendering with the same default visibility policy used in email/report output.
- [x] 3.3 Verify preview continues to provide optional full-category detail access.

## 4. Validation

- [x] 4.1 Update/add tests for founder-only copy, weakest-category default visibility, CTA normalization, and sender branding.
- [x] 4.2 Run `./.venv/bin/python manage.py test landing.tests.test_contact_form landing.tests.test_landing_pages`.
- [x] 4.3 Run `./scripts/verify.sh` and confirm apply-ready baseline is clean.
