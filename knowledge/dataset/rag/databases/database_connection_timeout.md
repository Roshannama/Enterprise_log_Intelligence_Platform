# Database Connection Timeout

## Symptoms

- Requests fail with connection timeout errors
- Elevated latency on database-dependent endpoints
- Connection pool utilization near maximum

## Likely Causes

- Database host unreachable or overloaded
- Network partition between app and database
- Connection pool undersized for current load
- Long-running queries holding connections

## Investigation Steps

- Check database host health and load
- Inspect connection pool metrics (active/idle/max)
- Review slow query log for long-running queries
- Check network path between app and database

## Recommended Actions

- Scale connection pool if undersized
- Kill or optimize long-running queries
- Add read replicas to offload read traffic
- Add circuit breaker on database-dependent calls

## Verification

- Confirm connection success rate returns to baseline
- Confirm pool utilization drops below 70%

## Severity Guidance

Escalate to HIGH if sustained beyond 5 minutes or affecting checkout/payment paths; MEDIUM if isolated and brief.

## Related Signals

- Connection pool exhaustion
- Elevated query_time_ms
- Downstream 503s on dependent services
