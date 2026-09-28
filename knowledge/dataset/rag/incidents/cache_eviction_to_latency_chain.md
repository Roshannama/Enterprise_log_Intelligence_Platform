# Signal Chain: Cache Eviction Storm to Latency Degradation

## Symptoms

- Cache eviction rate increase
- Followed by increased database load
- Followed by request latency degradation

## Likely Causes

- Cache memory pressure causing eviction storm is the initiating event

## Investigation Steps

## Signal Chain

Cache eviction storm
→ cache miss increase
→ increased database load
→ latency degradation

## Investigation

- Confirm eviction rate rose before database load and latency did
- Rule out an independent database-side cause for the latency

## Recommended Actions

- Increase cache memory or adjust eviction policy
- Add request coalescing to reduce redundant database load during cache misses

## Verification

- Latency returns to baseline once eviction rate normalizes

## Severity Guidance

MEDIUM, escalate if database cannot sustain the fallback load.

## Related Signals

- Cache Unavailability and Fallback
- Memory Pressure and Leaks
