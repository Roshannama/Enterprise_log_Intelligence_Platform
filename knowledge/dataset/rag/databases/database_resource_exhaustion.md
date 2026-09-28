# Database Resource Exhaustion (CPU/Memory/Disk)

## Symptoms

- High CPU or memory utilization on database host
- Disk usage approaching capacity
- Query latency increasing without code changes

## Likely Causes

- Inefficient queries or missing indexes
- Unexpected traffic growth
- Background maintenance jobs (vacuum, backup) competing for resources
- Disk filling due to log or WAL growth

## Investigation Steps

- Check top queries by CPU/IO consumption
- Check disk usage trend over recent days
- Check for concurrent maintenance jobs

## Recommended Actions

- Add missing indexes
- Schedule maintenance jobs during low-traffic windows
- Provision additional disk or clean up old WAL/log files
- Scale database vertically or add replicas

## Verification

- Resource utilization returns to sustainable range
- Query latency returns to baseline

## Severity Guidance

Escalate to CRITICAL if disk usage exceeds 95% or CPU sustained above 95% affecting all queries.

## Related Signals

- Slow Database Query
- Database Connection Timeout
