# Restricted Endpoint Access Patterns

## Symptoms

- Repeated 403 responses to a single restricted endpoint
- Access attempts from an account without the required role

## Likely Causes

- Compromised account probing for sensitive data
- Legitimate user with a genuinely missing permission
- Frontend bug requesting an endpoint it shouldn't

## Investigation Steps

- Check requesting account's role and recent activity
- Check if access attempts are automated (rate, pattern) vs manual
- Check whether a recent frontend change introduced the errant calls

## Recommended Actions

- Escalate to security review if compromise is suspected
- Grant permission if legitimately missing
- Fix frontend bug if that is the cause

## Verification

- 403 rate for the endpoint returns to near zero

## Severity Guidance

HIGH if pattern suggests probing by a compromised account; LOW if traced to a frontend bug.

## Related Signals

- Privilege escalation indicator
