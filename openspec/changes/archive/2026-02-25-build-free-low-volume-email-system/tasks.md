## 1. SMTP Configuration

- [x] 1.1 Add and validate SMTP environment-driven settings in `landing/project/settings.py`
- [x] 1.2 Update `.env.sample` with required SMTP variables and secure defaults

## 2. Contact Delivery Integration

- [x] 2.1 Verify contact form send path uses configured SMTP recipient (`QUROOM_CONTACT_EMAIL`)
- [x] 2.2 Ensure delivery status persistence behavior remains correct on success and failure

## 3. Verification and Runbook

- [x] 3.1 Add or update operational notes for SMTP setup and test command usage
- [x] 3.2 Execute check/test and perform one end-to-end SMTP send verification
