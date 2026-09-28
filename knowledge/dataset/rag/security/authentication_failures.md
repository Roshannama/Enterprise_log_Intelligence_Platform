# Authentication Failures and Brute-Force Patterns

## Symptoms

- Repeated failed login attempts
- Account lockouts
- Failed attempts concentrated from one IP or IP range

## Likely Causes

- Credential stuffing or brute-force attempt
- Legitimate user with expired or forgotten credentials
- Client misconfiguration causing repeated failed auth

## Investigation Steps

- Check source IP diversity of failed attempts
- Check whether failures target one account or many
- Check for a pattern matching known credential-stuffing lists

## Recommended Actions

- Rate-limit or block the offending IP/range
- Enforce MFA for the targeted accounts
- Notify affected users if account takeover is suspected

## Verification

- Failed login rate returns to baseline
- No successful login from flagged IP

## Severity Guidance

HIGH if a wide IP range or many accounts are targeted; LOW/MEDIUM for a single user's expired credentials.

## Related Signals

- Invalid token signature
- Account lockout
