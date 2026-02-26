## 1. Lead Magnet Capture Flow

- [x] 1.1 Add founder lead-magnet section/CTA and diagnosis form rendering on `landing/templates/landing/index.html`.
- [x] 1.2 Implement lead-magnet form schema and validation in `landing/forms.py`.
- [x] 1.3 Add submission endpoint and result scoring/grade logic in `landing/views.py`.

## 2. Persistence and Email Follow-up

- [x] 2.1 Persist lead-magnet submissions using `ContactInquiry` with a distinct inquiry type and structured result summary.
- [x] 2.2 Extend mail delivery flow to send operations notification + submitter follow-up report email.
- [x] 2.3 Track lead-magnet funnel events (`start/submit/email_sent`) using internal analytics.

## 3. Admin Segmentation and UX Bridging

- [x] 3.1 Add dashboard segmentation/filtering for lead-magnet inquiries in `landing/views.py` and `landing/templates/landing/admin_dashboard.html`.
- [x] 3.2 Add grade-based bridge CTA blocks (A/B/C) and policy text (`동시 1개사 진행`) in the result UI.

## 4. Verification

- [x] 4.1 Add/extend tests for lead-magnet submission, scoring, email delivery status, and dashboard filtering.
- [x] 4.2 Run `./scripts/verify.sh` and confirm all checks/tests pass.
