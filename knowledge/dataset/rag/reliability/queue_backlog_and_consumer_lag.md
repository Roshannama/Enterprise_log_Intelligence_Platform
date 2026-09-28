# Queue Backlog and Consumer Lag

## Symptoms

- Growing queue depth
- Consumer lag exceeding threshold
- Delayed downstream processing

## Likely Causes

- Producer rate exceeding consumer throughput
- Consumer crashed or stalled
- Downstream dependency slowing consumer processing

## Investigation Steps

- Check consumer instance count and health
- Check for errors in consumer processing logic
- Check whether a downstream dependency is slowing consumers

## Recommended Actions

- Scale consumer instances
- Fix stalled/crashed consumers
- Add backpressure or rate limiting on producers if appropriate

## Verification

- Queue depth trending back to baseline
- Consumer lag below threshold

## Severity Guidance

LOW if brief and self-resolving; MEDIUM to HIGH if backlog causes user-visible delay.

## Related Signals

- Consumer stopped
- Retry exhaustion
