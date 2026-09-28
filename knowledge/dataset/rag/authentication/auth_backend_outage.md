# Authentication Backend Outage

## Symptoms

- Authentication backend unreachable
- Widespread login failures across many users simultaneously

## Likely Causes

- Auth provider infrastructure outage
- Network partition to auth backend
- Auth backend overloaded

## Investigation Steps

- Check auth backend health/status directly
- Check network path from app to auth backend
- Check whether failures correlate with a specific auth backend instance

## Recommended Actions

- Fail over to backup auth backend if available
- Engage auth provider if third-party
- Add graceful degradation messaging for users during outage

## Verification

- Login success rate returns to baseline across all users

## Severity Guidance

HIGH given broad user impact; CRITICAL if it blocks all authentication platform-wide.

## Related Signals

- Widespread 401 responses
- Circuit breaker activation
