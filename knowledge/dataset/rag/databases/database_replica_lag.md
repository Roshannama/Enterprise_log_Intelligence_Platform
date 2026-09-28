# Database Replica Lag and Read Failures

## Symptoms

- Read replica returning stale data
- Replica connection resets
- Increasing replication lag metric

## Likely Causes

- Network degradation between primary and replica
- Replica under-provisioned for write volume
- Long-running transactions on primary delaying replication

## Investigation Steps

- Check replication lag metric trend
- Check network health between primary and replica
- Check for long-running transactions on primary

## Recommended Actions

- Failover reads to primary temporarily
- Scale replica resources
- Investigate and resolve network path issues

## Verification

- Replication lag returns to near-zero
- Reads return fresh data consistently

## Severity Guidance

MEDIUM typically; HIGH if application correctness depends on read freshness (e.g., financial data).

## Related Signals

- Network packet loss
- Increased primary load from fallback reads
