# Service Crash and Automatic Restart

## Symptoms

- Unhandled exception followed by process exit
- Service instance restarted automatically
- Brief gap in availability for affected instance

## Likely Causes

- Unhandled edge case in application logic
- Out-of-memory condition
- Bad deployment introducing a regression

## Investigation Steps

- Review stack trace at crash time
- Check recent deploy history
- Check memory usage trend leading up to crash

## Recommended Actions

- Patch the unhandled exception path
- Add memory limits and alerting
- Roll back recent deploy if correlated

## Verification

- No further crashes of same type for 24h
- Memory usage stable post-fix

## Severity Guidance

MEDIUM for a single isolated crash; HIGH if crash-looping repeatedly.

## Related Signals

- OutOfMemoryError
- Deployment configuration error
