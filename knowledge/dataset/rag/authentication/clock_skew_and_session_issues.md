# Clock Skew and Session Validation Issues

## Symptoms

- Tokens rejected as not-yet-valid or prematurely expired
- Session validation inconsistent across service instances

## Likely Causes

- NTP synchronization drift on one or more hosts
- Container clock not synced with host clock

## Investigation Steps

- Compare system clocks across affected hosts
- Check NTP sync status and drift magnitude

## Recommended Actions

- Resync NTP on affected hosts
- Add clock-skew tolerance in token validation logic within safe bounds

## Verification

- Clock drift within acceptable tolerance across all hosts

## Severity Guidance

LOW to MEDIUM; escalate if it causes broad authentication failures.

## Related Signals

- Expired/invalid token failures
