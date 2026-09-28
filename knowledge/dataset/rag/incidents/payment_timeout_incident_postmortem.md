# Postmortem: Payment Timeout Incident (Synthetic)

## Symptoms

- Elevated payment failures for ~7 minutes
- Customers saw checkout timeout errors

## Likely Causes

- Database CPU saturation caused connection pool exhaustion, which cascaded into payment-service timeouts

## Investigation Steps

- Reviewed database CPU and connection metrics
- Correlated with payment-service error timeline
- Confirmed recovery aligned with CPU normalization

## Recommended Actions

- Added query optimization for the identified hot query
- Added earlier alerting on database CPU thresholds
- Added circuit breaker on payment-service's database calls

## Verification

- No recurrence in the 30 days following the fix

## Severity Guidance

HIGH — checkout-path impact for several minutes.

## Related Signals

- Database CPU pressure
- Connection pool exhaustion
- Payment-service timeout
