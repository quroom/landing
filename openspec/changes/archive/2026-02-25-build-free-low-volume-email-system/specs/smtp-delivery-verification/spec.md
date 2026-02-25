## ADDED Requirements

### Requirement: Operators can verify SMTP delivery with a deterministic command
The system MUST provide an operator-verifiable command path to test SMTP delivery after environment setup.

#### Scenario: Operator runs SMTP test command
- **WHEN** environment variables are loaded and test mail command is executed
- **THEN** the command MUST return success on delivery acceptance by SMTP provider
- **AND** operators MUST be able to identify failures from the command output or exception

### Requirement: Delivery failures remain auditable
The system MUST preserve inquiry records and delivery status when mail sending fails.

#### Scenario: SMTP delivery fails at runtime
- **WHEN** contact form submission triggers a mail send error
- **THEN** the inquiry MUST remain persisted
- **AND** delivery status and error summary MUST be stored for follow-up
