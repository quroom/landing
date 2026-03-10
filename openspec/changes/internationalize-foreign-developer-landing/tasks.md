## 1. Locale Resolution and Content Model

- [x] 1.1 Implement locale resolution priority (`lang` query -> persisted preference -> page default) for landing views.
- [x] 1.2 Refactor landing content structures to support locale-keyed copy (`ko`, `en`) for CTA, FAQ, and persona text.
- [x] 1.3 Add fallback handling for missing translation keys (page default -> safe site locale) and surface missing-key logs.

## 2. Persona Page Internationalization

- [x] 2.1 Set `/for-foreign-developers/` default locale to English and keep `/` default locale as Korean.
- [x] 2.2 Localize foreign developer page conversion-critical copy (headline, service CTA, FAQ, support-boundary statement) with English-first rendering.
- [x] 2.3 Localize shared contact form labels/placeholders/validation messages based on resolved locale.

## 3. Verification and Regression Coverage

- [x] 3.1 Add/adjust template and view tests for page-level `lang` behavior and locale switching precedence.
- [x] 3.2 Add tests for translation fallback behavior and missing-key safe rendering.
- [x] 3.3 Run `./scripts/verify.sh` and fix regressions until all checks pass.
