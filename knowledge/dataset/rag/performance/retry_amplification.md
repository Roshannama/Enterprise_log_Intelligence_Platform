# Retry Amplification and Retry Storms

## Symptoms

- Retry volume far exceeding original request volume
- Downstream load appearing multiplied relative to client traffic

## Likely Causes

- Aggressive retry policy without backoff
- Retries triggered on non-retryable errors
- Multiple layers each independently retrying the same failed call

## Investigation Steps

- Measure retry-to-original-request ratio
- Check retry policy configuration at each layer
- Check whether retries are triggered on errors that should not be retried

## Recommended Actions

- Add exponential backoff with jitter
- Cap maximum retry attempts
- Coordinate retry policy across layers to avoid compounding

## Verification

- Retry ratio returns to an expected, bounded level

## Severity Guidance

HIGH if retry amplification is actively worsening an ongoing outage; MEDIUM otherwise.

## Related Signals

- Circuit breaker activation
- Thread pool exhaustion
