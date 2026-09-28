# Signal Chain: Database Timeout to API Failure

## Symptoms

- Database connection timeout errors
- Followed by application request timeouts
- Followed by HTTP 503 spikes
- Followed by client retry storm

## Likely Causes

- Database connection timeout is the initiating event in this chain; downstream symptoms are consequences, not independent causes

## Investigation Steps

## Signal Chain

Database connection timeout
→ connection pool exhaustion
→ application request timeout
→ HTTP 503
→ retry storm

## Investigation

- Confirm database timeout precedes the other symptoms in time
- Confirm pool exhaustion metric rises before request timeouts
- Rule out an independent cause for the 503 spike

## Recommended Actions

- Resolve the database timeout at its source (see Database Connection Timeout runbook)
- Cap retries to prevent amplification while root cause is addressed

## Verification

- All downstream symptoms clear once database timeout is resolved

## Severity Guidance

Severity tracks the most severe downstream impact; typically HIGH given payment/API impact.

## Related Signals

- Database Connection Timeout
- Retry Amplification
