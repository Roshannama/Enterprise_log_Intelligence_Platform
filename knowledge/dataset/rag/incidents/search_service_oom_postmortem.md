# Postmortem: Search Service Memory Exhaustion (Synthetic)

## Symptoms

- search-service instances repeatedly restarting under load

## Likely Causes

- An unbounded in-memory cache grew without eviction, eventually exhausting heap

## Investigation Steps

- Reviewed heap snapshots showing continual growth
- Identified the unbounded cache as the growth source

## Recommended Actions

- Added a bounded LRU eviction policy to the cache
- Added heap-usage alerting ahead of OOM thresholds

## Verification

- Heap usage stabilized at a sustainable plateau after the fix

## Severity Guidance

HIGH — degraded search availability during peak hours.

## Related Signals

- Memory pressure and leaks
- OutOfMemoryError stack trace
