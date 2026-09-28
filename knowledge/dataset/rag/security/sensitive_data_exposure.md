# Sensitive Data Exposure in Application Logs

## Symptoms

- Email addresses, phone numbers, or account IDs visible in logs
- PII fields logged at DEBUG level

## Likely Causes

- Missing field-level masking in logging middleware
- Debug logging accidentally left enabled
- New log statement added without following data-handling policy

## Investigation Steps

- Identify which fields are exposed and in which services
- Check log retention and access controls for the affected logs

## Recommended Actions

- Add field-level masking for PII in the logging pipeline
- Purge or redact already-exposed log entries where feasible
- Add a data-handling review step to the logging code-review checklist

## Verification

- No new PII fields appear in logs post-fix
- Masking verified in a staging environment

## Severity Guidance

MEDIUM typically for internal logs with restricted access; HIGH if logs are broadly accessible or exported.

## Related Signals

- Credential exposure
- Debug logging enabled in production
