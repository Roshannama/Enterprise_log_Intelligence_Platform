# Signal Chain: Deployment to Configuration-Driven Crash Loop

## Symptoms

- Deployment start event
- Followed immediately by missing-configuration errors
- Followed by repeated crash-restart cycles

## Likely Causes

- The deployment introducing a new configuration requirement is the initiating event

## Investigation Steps

## Signal Chain

Deployment started
→ missing config error
→ crash
→ restart
→ crash (loop)
→ rollback

## Investigation

- Confirm the crash-loop onset aligns exactly with the deployment timestamp
- Diff configuration between the new and previous revision

## Recommended Actions

- Roll back immediately to stop the loop
- Add the missing configuration and add a pre-deploy validation gate

## Verification

- Service stable on either the fixed revision or the rollback

## Severity Guidance

HIGH — full service outage until rollback or fix.

## Related Signals

- Missing Configuration After Deployment
