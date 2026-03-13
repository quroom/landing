# Capability: landing-page-internationalization

## ADDED Requirements

### Requirement: Landing pages MUST resolve locale with deterministic priority
The system MUST resolve landing-page locale in this priority order: explicit request parameter, persisted user preference, then page default locale.

#### Scenario: Explicit locale parameter overrides defaults
- **WHEN** a user requests a landing page with `lang=en` or `lang=ko`
- **THEN** the system renders content in the requested locale when translations are available
- **AND** the selected locale is persisted for subsequent requests

### Requirement: Landing pages MUST provide fallback for missing translations
The system MUST fallback to the page default locale when requested locale content is missing, and MUST fallback to a safe site locale when page default content is missing.

#### Scenario: Missing requested-locale content falls back safely
- **WHEN** a translation key is missing in the requested locale
- **THEN** the system renders the page default locale value for that key
- **AND** if the page default value is also missing, the system renders the safe site locale value

### Requirement: I18n coverage MUST include conversion-critical text
The system MUST internationalize conversion-critical text for each supported locale, including CTA labels, contact-form labels, placeholders, validation messages, and FAQ entries.

#### Scenario: Contact flow texts are localized
- **WHEN** a user opens a landing page in a supported locale
- **THEN** the contact form and CTA copy are rendered in that locale
- **AND** validation/error messages are rendered in that locale

