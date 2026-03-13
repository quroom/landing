# Capability: django-gettext-localization

## ADDED Requirements

### Requirement: Landing text MUST be managed through Django gettext catalogs
The system MUST manage user-facing landing text through Django gettext catalogs under `locale/<lang>/LC_MESSAGES/` for supported languages.

#### Scenario: Template strings are extractable by makemessages
- **WHEN** maintainers run `django-admin makemessages -l ko -l en`
- **THEN** landing template and form/view strings are extracted into catalog files
- **AND** extracted keys are available for translation updates without code changes

### Requirement: Language switching MUST use Django set_language flow
The system MUST switch landing language using Django `set_language` endpoint and language cookie handling.

#### Scenario: User toggles language via set_language
- **WHEN** a user submits language selection for `ko` or `en`
- **THEN** the response sets Django language cookie to the selected value
- **AND** subsequent landing requests render in the selected locale

### Requirement: Translation resources MUST be compile-verified before release
The system MUST verify translation resources compile successfully before release.

#### Scenario: compilemessages check succeeds
- **WHEN** maintainers run `django-admin compilemessages`
- **THEN** translation catalogs compile without errors
- **AND** deployment verification treats compile failures as blocking issues
