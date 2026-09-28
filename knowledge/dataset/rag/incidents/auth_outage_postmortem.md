# Postmortem: Authentication Backend Outage (Synthetic)

## Symptoms

- Platform-wide login failures for 12 minutes

## Likely Causes

- Third-party auth provider experienced an upstream outage

## Investigation Steps

- Confirmed via provider status page and correlated failure timeline
- Confirmed no internal changes correlated with the onset

## Recommended Actions

- Added a secondary auth fallback path for critical internal tools
- Added provider status-page monitoring to alerting pipeline

## Verification

- Login success rate returned to 99.9%+ post-recovery

## Severity Guidance

CRITICAL — full platform authentication impact.

## Related Signals

- Auth backend outage runbook
- Circuit breaker activation
