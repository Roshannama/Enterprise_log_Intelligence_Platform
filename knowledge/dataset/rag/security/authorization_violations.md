# Authorization Violations and Privilege Escalation Indicators

## Symptoms

- 403 Forbidden responses to restricted resources
- Repeated attempts to reach an admin or sensitive endpoint
- Unexpected role changes outside change-management process

## Likely Causes

- Compromised low-privilege account probing for access
- Legitimate user hitting a misconfigured permission
- Insider attempting unauthorized privilege escalation

## Investigation Steps

- Review the identity and role of the requesting account
- Check whether the endpoint accessed is genuinely sensitive
- Check audit trail for related role changes

## Recommended Actions

- Block or suspend the account if malicious intent is likely
- Correct any permission misconfiguration
- Require review/approval for any privilege escalation

## Verification

- No further unauthorized access attempts
- Role changes reviewed and confirmed legitimate

## Severity Guidance

HIGH for confirmed privilege escalation attempts; MEDIUM for isolated 403s pending review.

## Related Signals

- Repeated 403 Forbidden
- Unreviewed role change
