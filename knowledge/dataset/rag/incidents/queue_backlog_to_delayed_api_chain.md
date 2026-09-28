# Signal Chain: Queue Backlog to Delayed API Responses

## Symptoms

- Queue depth growth
- Followed by reduced worker processing rate
- Followed by user-visible delay in dependent API responses

## Likely Causes

- Insufficient consumer capacity relative to producer rate is the initiating event

## Investigation Steps

## Signal Chain

Queue depth growth
→ processing rate drop
→ delayed dependent API responses

## Investigation

- Confirm queue depth growth precedes the API delay reports
- Check whether consumer count changed (e.g., a crash) around the same time

## Recommended Actions

- Scale consumer capacity
- Investigate any consumer crash or slowdown separately

## Verification

- Queue depth and API delay both return to baseline together

## Severity Guidance

MEDIUM typically; HIGH if it delays time-sensitive processing like order confirmation.

## Related Signals

- Queue Backlog and Consumer Lag
