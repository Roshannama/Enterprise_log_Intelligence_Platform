# Database Deadlock and Transaction Contention

## Symptoms

- Transactions rolled back with deadlock errors
- Increased transaction retry rate

## Likely Causes

- Two or more transactions acquiring locks in conflicting order
- High contention on hot rows
- Long-running transactions holding locks

## Investigation Steps

- Review deadlock graph from database logs
- Identify hot tables/rows involved
- Check for transactions that hold locks across multiple statements

## Recommended Actions

- Reorder lock acquisition consistently across code paths
- Shorten transaction scope
- Add retry-with-backoff for deadlock victims

## Verification

- Deadlock rate returns to baseline
- No repeated rollbacks on same transaction pattern

## Severity Guidance

LOW to MEDIUM depending on frequency; HIGH if deadlocks block critical write paths repeatedly.

## Related Signals

- Transaction rollback
- Retry storm
