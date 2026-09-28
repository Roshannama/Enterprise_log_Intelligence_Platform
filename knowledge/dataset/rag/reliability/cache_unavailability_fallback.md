# Cache Unavailability and Database Fallback

## Symptoms

- Cache connection errors
- Increased database load
- Elevated request latency

## Likely Causes

- Cache node failure or restart
- Network issue between app and cache
- Cache eviction storm due to memory pressure

## Investigation Steps

- Check cache node health and restart history
- Check cache memory usage and eviction rate
- Check database load correlated with cache errors

## Recommended Actions

- Restart or replace failed cache node
- Increase cache memory or adjust eviction policy
- Add graceful fallback with request coalescing to protect database

## Verification

- Cache error rate returns to zero
- Database load returns to baseline

## Severity Guidance

MEDIUM typically; HIGH if database cannot sustain fallback load without further failures.

## Related Signals

- Eviction storm
- Elevated database CPU
