# Log Sanitization Policy

## Symptoms

- Logs containing raw secrets, tokens, or passwords found in an audit

## Likely Causes

- Sanitization middleware not applied to a given log path
- New logging code added without following the policy

## Investigation Steps

- Audit representative log samples across all services quarterly
- Verify sanitization patterns cover current secret formats

## Recommended Actions

- All logging paths must pass through the central sanitization middleware
- Known secret patterns (bearer tokens, API keys, passwords, card-like numbers) must be masked before write
- New services must integrate sanitization before going to production

## Verification

- Quarterly audit finds zero unmasked secret patterns

## Severity Guidance

Any confirmed policy violation exposing a real secret is treated as HIGH regardless of exposure duration.

## Related Signals

- Credential and Secret Exposure in Logs
