# smtp-provider-configuration Specification

## Purpose
TBD - created by archiving change build-free-low-volume-email-system. Update Purpose after archive.
## Requirements
### Requirement: SMTP provider configuration via environment variables
The system MUST support SMTP-based mail delivery using environment variables so operators can configure provider settings without code changes.

#### Scenario: SMTP env values are provided
- **WHEN** `DJANGO_EMAIL_BACKEND` is set to SMTP backend and host credentials are configured
- **THEN** the application MUST attempt to send contact emails through the configured SMTP provider
- **AND** the mail sender and recipient addresses MUST be configurable through environment variables

### Requirement: Safe default behavior for local development
The system MUST keep a safe local default backend for development when SMTP values are not provided.

#### Scenario: SMTP env values are missing in local environment
- **WHEN** mail backend settings are not configured in environment
- **THEN** the application MUST use a non-delivery-safe backend for local development
- **AND** no production email MUST be sent implicitly

