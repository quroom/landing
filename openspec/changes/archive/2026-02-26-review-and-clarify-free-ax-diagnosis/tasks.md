## 1. Diagnosis Category and Scoring Structure

- [x] 1.1 Restructure diagnosis axes into four categories in `landing/ax_tool_stack.py`
- [x] 1.2 Update segmentation/scoring logic in `landing/views.py` to align with four-category model

## 2. Personalized Result and Action Output

- [x] 2.1 Implement category x grade (4x3) response matrix in `landing/views.py`
- [x] 2.2 Implement single best 2-week action recommendation in `landing/views.py`
- [x] 2.3 Reduce tool recommendation list to concise, high-signal tools in `landing/views.py`

## 3. Report and Email Clarity

- [x] 3.1 Refine report text structure for explicit execution guidance and CTA bridge in `landing/views.py`
- [x] 3.2 Update lead-magnet email text/HTML with grade-specific copy in `landing/mailers.py`
- [x] 3.3 Update diagnosis UI/preview templates to reflect 4-category + one-action model

## 4. Verification

- [x] 4.1 Update tests in `landing/tests/test_contact_form.py` and `landing/tests/test_landing_pages.py`
- [x] 4.2 Run `./scripts/verify.sh` and confirm all checks pass
