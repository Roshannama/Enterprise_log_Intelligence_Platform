# Thread Pool and Connection Pool Saturation

## Symptoms

- Requests rejected due to full thread pool
- Connection pool utilization near 100%

## Likely Causes

- Traffic burst beyond provisioned capacity
- Slow downstream calls holding threads/connections longer than expected
- Pool size misconfigured for current workload

## Investigation Steps

- Check pool utilization trend leading up to saturation
- Check whether downstream latency is holding resources longer
- Check recent traffic volume changes

## Recommended Actions

- Increase pool size within safe limits
- Reduce downstream call duration (timeouts, caching)
- Add load shedding for non-critical requests during saturation

## Verification

- Pool utilization returns below a safe threshold
- Request rejection rate returns to zero

## Severity Guidance

MEDIUM typically; HIGH if it causes cascading rejections across dependent services.

## Related Signals

- API latency
- Retry amplification
