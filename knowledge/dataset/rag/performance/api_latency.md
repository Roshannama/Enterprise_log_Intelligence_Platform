# API Latency Degradation

## Symptoms

- p95/p99 latency significantly above baseline
- User-visible slowness on affected endpoints

## Likely Causes

- Slow downstream dependency (database, cache, third-party API)
- Resource contention (CPU/memory) on the service
- Retry amplification multiplying load on a degraded dependency

## Investigation Steps

- Break down latency by dependency to isolate the slow hop
- Check resource utilization on the service during the window
- Check retry counts and amplification factor

## Recommended Actions

- Optimize or scale the identified slow dependency
- Add caching for expensive repeated calls
- Cap retries and add jitter/backoff to prevent amplification

## Verification

- Latency returns to within historical baseline band
- No retry amplification observed

## Severity Guidance

MEDIUM for a moderate, contained spike; HIGH if it breaches SLA on a critical path like checkout.

## Related Signals

- Slow database query
- Retry storm
- Thread pool exhaustion
