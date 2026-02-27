## 1. KPI Contract and Event Metadata

- [x] 1.1 Align lead-magnet event schema (`event_name`, `page_key`, `lead_source`, `score`, `grade`, `lead_context`, `utm_*`) across tracking points.
- [x] 1.2 Implement and document fixed KPI formulas (`submit_rate`, `mail_success_rate`, `contact_conversion_rate`) with denominator-zero handling (`0.0%`).
- [x] 1.3 Add tests to verify event metadata presence for lead-magnet submit/email/contact conversion paths.

## 2. MVP Internal Dashboard

- [x] 2.1 Add lead-magnet funnel count cards (`start`, `submit`, `mail_sent`, `contact_submit`) to admin dashboard.
- [x] 2.2 Add derived KPI rate cards using fixed formulas and one-decimal percentage formatting.
- [x] 2.3 Ensure dashboard rendering remains stable for empty periods (no events) and filtered views.

## 3. Conversion Review Readiness

- [x] 3.1 Update documentation with measurement definitions, weekly review checklist, and GA4/internal role separation.
- [x] 3.2 Add regression tests for dashboard KPI block visibility and baseline conversion values.
- [x] 3.3 Verify lead-magnet result/bridge/email changes do not break existing report/section parity contracts.
