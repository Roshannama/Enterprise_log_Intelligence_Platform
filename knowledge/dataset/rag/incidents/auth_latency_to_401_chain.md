# Signal Chain: Auth Latency to Spurious 401 Errors

## Symptoms

- Token validation latency increase
- Followed by a wave of 401 responses
- Followed by downstream service errors referencing auth dependency

## Likely Causes

- Slow token introspection is the initiating event; 401s are a side-effect of validation timeouts being treated as invalid tokens

## Investigation Steps

## Signal Chain

Token introspection latency
→ validation timeouts
→ spurious 401 responses
→ downstream error propagation

## Investigation

- Confirm 401 spike coincides with introspection latency, not with a credential change
- Distinguish this from a genuine brute-force pattern by checking whether failures cluster on distinct users, not distinct IPs targeting a few accounts

## Recommended Actions

- Resolve auth backend latency
- Add a distinct error code for validation-timeout vs invalid-credential to avoid confusion

## Verification

- 401 rate returns to baseline as introspection latency normalizes

## Severity Guidance

MEDIUM typically, unless it blocks a large share of legitimate users.

## Related Signals

- Auth Backend Outage
- Authentication Failures
