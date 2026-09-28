# Multi-Tenant Data Boundary Violations

## Symptoms

- A request for tenant A's data authenticated as tenant B's user
- Cross-tenant identifiers appearing together in a single request

## Likely Causes

- Missing tenant-scoping check in a query or endpoint
- Client-side bug sending wrong tenant identifier

## Investigation Steps

- Check whether the endpoint enforces tenant scoping consistently
- Trace the specific request path to find where scoping was missed

## Recommended Actions

- Add or fix tenant-scoping checks at the data-access layer
- Audit similar endpoints for the same gap

## Verification

- No further cross-tenant boundary violations found in audit

## Severity Guidance

CRITICAL — any confirmed cross-tenant data exposure is a serious incident regardless of frequency.

## Related Signals

- Restricted endpoint access
- Sensitive data exposure
