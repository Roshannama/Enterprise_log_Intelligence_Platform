# Signal Chain: Shared Database CPU Contention Affecting Search

## Symptoms

- Database CPU utilization increase
- Followed by index query latency increase on search-service
- Followed by search request timeouts

## Likely Causes

- Shared database resource contention is the initiating event, even though the visible symptom appears in an unrelated-seeming service

## Investigation Steps

## Signal Chain

Database CPU pressure (shared instance)
→ search index query latency
→ search timeout
→ user-visible search degradation

## Investigation

- Confirm search-service and the affected database share the same underlying instance
- Confirm CPU normalization timing matches search latency recovery

## Recommended Actions

- Identify and optimize the CPU-heavy query causing contention
- Consider isolating search's database workload onto separate resources

## Verification

- Search latency returns to baseline as shared database CPU normalizes

## Severity Guidance

MEDIUM, escalate if it recurs frequently due to persistent resource sharing.

## Related Signals

- Database Resource Exhaustion
- Slow Database Query Patterns
