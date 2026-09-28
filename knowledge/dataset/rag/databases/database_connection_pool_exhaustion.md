# Database Connection Pool Exhaustion

## Symptoms

- New requests blocked waiting for a connection
- Pool utilization at or near 100%

## Likely Causes

- Traffic spike beyond provisioned pool size
- Connection leak in application code
- Slow queries holding connections longer than expected

## Investigation Steps

- Check for connection leaks (connections not released)
- Correlate with recent traffic spikes
- Review recent deploys for pooling configuration changes

## Recommended Actions

- Increase pool size within database capacity limits
- Fix connection leak in application code
- Add timeout-and-release logic for stuck connections

## Verification

- Pool utilization returns below 80%
- No requests blocked waiting for connections

## Severity Guidance

MEDIUM by default; escalate to HIGH if it causes cascading request failures.

## Related Signals

- Database Connection Timeout
- API Latency
