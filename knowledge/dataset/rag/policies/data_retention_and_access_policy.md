# Log Data Retention and Access Policy

## Symptoms

- Logs retained longer than necessary
- Logs accessible to broader audience than required

## Likely Causes

- Missing or misconfigured retention rules
- Overly broad access-control lists on log storage

## Investigation Steps

- Review retention duration against policy for each log category
- Review access-control lists for log storage systems

## Recommended Actions

- Set retention periods per log sensitivity category
- Restrict access to logs containing sensitive fields to a minimal named group
- Log access to sensitive log stores for audit purposes

## Verification

- Retention and access settings match policy on periodic review

## Severity Guidance

Any confirmed excessive access to logs containing exposed sensitive data is treated as at least MEDIUM.

## Related Signals

- Sensitive Data Exposure in Application Logs
