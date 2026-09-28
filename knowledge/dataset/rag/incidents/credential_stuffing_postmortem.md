# Postmortem: Credential Stuffing Attempt (Synthetic)

## Symptoms

- Sharp increase in failed login attempts from a distributed set of IPs

## Likely Causes

- Automated credential-stuffing attempt using a leaked (unrelated, external) credential list

## Investigation Steps

- Confirmed failed attempts used random distinct credentials per IP, consistent with stuffing
- Confirmed no successful account takeovers occurred

## Recommended Actions

- Enabled rate limiting per IP and per account
- Enforced MFA on all accounts
- Notified security team and monitored for account takeover indicators

## Verification

- Failed login rate returned to baseline after mitigations

## Severity Guidance

HIGH — no confirmed compromise, but wide blast radius attempted.

## Related Signals

- Authentication failures / brute-force pattern
