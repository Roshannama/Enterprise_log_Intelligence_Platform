# Rolling Deployment Transient Latency

## Symptoms

- Brief latency increase on instances being drained during a rolling deploy
- Latency returns to normal once rollout completes

## Likely Causes

- Expected connection draining behavior during instance replacement
- Load balancer briefly routing to draining instances

## Investigation Steps

- Confirm the latency window aligns with the deployment timeline
- Check whether latency fully resolves after rollout completion

## Recommended Actions

- Tune drain timeout to minimize overlap
- Ensure load balancer deregisters draining instances promptly

## Verification

- Latency stable and back to baseline post-rollout

## Severity Guidance

LOW — this is expected behavior unless the window is unusually long or user-impacting.

## Related Signals

- Deployment start/end markers
