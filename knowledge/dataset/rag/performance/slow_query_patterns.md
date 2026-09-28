# Slow Database Query Patterns

## Symptoms

- query_time_ms significantly above baseline for specific query shapes
- Full table scans observed in query plan

## Likely Causes

- Missing index for a common query predicate
- Query plan regression after a schema or statistics change
- Data growth outpacing existing index efficiency

## Investigation Steps

- Capture and review the query plan for the slow query
- Check whether an appropriate index exists
- Check recent schema or statistics changes

## Recommended Actions

- Add or rebuild the appropriate index
- Rewrite the query to avoid unnecessary full scans
- Update table statistics if stale

## Verification

- Query time returns to baseline for the affected query shape

## Severity Guidance

LOW to MEDIUM typically; HIGH if the query backs a high-traffic critical endpoint.

## Related Signals

- Database resource exhaustion
- API latency
