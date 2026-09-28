# Memory Pressure and Potential Leaks

## Symptoms

- Memory usage climbing steadily over time without corresponding traffic increase
- OutOfMemory warnings or errors

## Likely Causes

- Memory leak in application code (unreleased references)
- Cache growing unbounded
- Genuine increase in working set from higher traffic or larger payloads

## Investigation Steps

- Check memory growth trend relative to traffic trend
- Take and compare heap snapshots if a leak is suspected
- Check cache size configuration and eviction policy

## Recommended Actions

- Fix identified leak (release references, close resources)
- Bound cache size with an eviction policy
- Scale memory allocation if growth matches legitimate traffic growth

## Verification

- Memory usage stabilizes or grows proportionally with traffic only

## Severity Guidance

MEDIUM while monitored; HIGH once OutOfMemory errors begin affecting availability.

## Related Signals

- OutOfMemoryError stack trace
- Cache eviction storm
