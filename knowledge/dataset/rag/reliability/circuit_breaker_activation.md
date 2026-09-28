# Circuit Breaker Activation

## Symptoms

- Circuit breaker opened for a downstream dependency
- Requests short-circuited without calling dependency

## Likely Causes

- Downstream dependency degraded or unavailable
- Misconfigured breaker thresholds triggering prematurely

## Investigation Steps

- Check downstream dependency health during the window
- Review breaker configuration (error threshold, window size)
- Check whether breaker closed again once dependency recovered

## Recommended Actions

- Address root cause in downstream dependency
- Tune breaker thresholds if premature
- Add fallback behavior for short-circuited requests

## Verification

- Breaker remains closed with dependency healthy
- Error rate to dependency below threshold

## Severity Guidance

MEDIUM typically; escalate if the dependency is on a critical path like payments.

## Related Signals

- Upstream latency elevation
- HTTP 503 spike
