## ADDED Requirements

### Requirement: Admin entry page MUST expose dashboard shortcut
The admin interface MUST include a visible shortcut to inquiry dashboard so operators do not need to memorize direct URLs.

#### Scenario: Admin user enters /admin
- **WHEN** a logged-in admin user loads `/admin/`
- **THEN** the top user links area MUST include a navigation link to the inquiry dashboard
- **AND** link target MUST resolve to the staff dashboard route

### Requirement: Inquiry resend operation MUST be available in admin list
The contact inquiry admin list MUST provide a batch action to resend selected inquiry notification emails.

#### Scenario: Admin runs resend action
- **WHEN** admin selects inquiries and executes resend action
- **THEN** the system MUST attempt email delivery for each selected inquiry
- **AND** each inquiry delivery status and error field MUST be updated based on result
