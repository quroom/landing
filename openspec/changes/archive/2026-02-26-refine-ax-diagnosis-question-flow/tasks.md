## 1. Diagnosis Model and Question Structure

- [x] 1.1 Define five-axis diagnosis question groups and metadata in `landing/ax_tool_stack.py`
- [x] 1.2 Refactor diagnosis form fields/validation in `landing/forms.py` to support grouped axis inputs
- [x] 1.3 Add backward-safe mapping so existing grade logic still computes while new axis scores are introduced

## 2. Result Classification and Personalization

- [x] 2.1 Implement axis-level score calculation and segmentation labels in `landing/views.py`
- [x] 2.2 Update free diagnosis result context to include operation type, bottleneck type, readiness type, and two-week priorities
- [x] 2.3 Update tool recommendation mapping to use segmented diagnosis patterns

## 3. UX and Email Report Updates

- [x] 3.1 Update diagnosis form UI (`landing/templates/landing/partials/lead_magnet_form.html`) to reflect multi-axis grouped questions
- [x] 3.2 Update result UI (`landing/templates/landing/free_diagnosis.html`, `landing/templates/landing/lead_magnet_report_preview.html`) with segmented output
- [x] 3.3 Update follow-up email content generation in `landing/mailers.py` to include personalized segmented guidance

## 4. Verification

- [x] 4.1 Add/update tests for grouped question submission and segmented result output (`landing/tests/test_contact_form.py`, `landing/tests/test_landing_pages.py`)
- [x] 4.2 Run `./scripts/verify.sh` and confirm all checks pass
