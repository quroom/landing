## 1. Django I18n Infrastructure Alignment

- [x] 1.1 Ensure `LANGUAGES`, `LOCALE_PATHS`, and `LocaleMiddleware` are configured for `ko/en`.
- [x] 1.2 Wire Django `set_language` route and confirm language cookie-based switching behavior.
- [x] 1.3 Add/update developer runbook notes for gettext tooling prerequisites.

## 2. String Migration to gettext

- [x] 2.1 Replace landing template hardcoded strings with `{% trans %}`/`{% blocktrans %}` where appropriate.
- [x] 2.2 Refactor form/view user-facing messages to `gettext_lazy`/`gettext`.
- [x] 2.3 Reduce legacy locale-key dictionaries to only data fields that are not translation strings.

## 3. Translation Catalog and Verification

- [x] 3.1 Generate `locale/ko` and `locale/en` catalogs via `makemessages`.
- [x] 3.2 Fill critical conversion-path translations (hero/menu/CTA/contact/FAQ/error/success).
- [x] 3.3 Run `compilemessages` and `./scripts/verify.sh`, then fix regressions until all checks pass.

## 4. Post-Implementation Gap Fixes

- [x] 4.1 Fill remaining root-page English gaps in footer/company fields (company/address/registration value formatting).
- [x] 4.2 Localize career timeline labels and duration format for English mode on the root page.
- [x] 4.3 Complete second-pass English copy coverage for portfolio duration/price/description strings and base meta tags.
