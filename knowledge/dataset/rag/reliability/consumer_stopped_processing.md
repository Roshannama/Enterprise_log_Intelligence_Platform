# Consumer Stopped Processing Messages

## Symptoms

- No messages consumed for an extended period
- Consumer group coordinator errors

## Likely Causes

- Consumer group rebalance failure
- Unhandled exception in consumer loop
- Broker connectivity issue

## Investigation Steps

- Check consumer group state and rebalance history
- Check consumer process logs for exceptions
- Check broker connectivity from consumer host

## Recommended Actions

- Restart affected consumer instances
- Fix unhandled exception causing consumer exit
- Address broker connectivity issue if present

## Verification

- Messages actively being consumed again
- Consumer lag decreasing

## Severity Guidance

HIGH if the queue backs critical, time-sensitive processing (e.g., order fulfillment).

## Related Signals

- Queue backlog
- Retry exhaustion
