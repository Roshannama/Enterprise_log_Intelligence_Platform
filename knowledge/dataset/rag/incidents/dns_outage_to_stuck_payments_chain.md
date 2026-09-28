# Signal Chain: DNS Outage to Stuck Payment State

## Symptoms

- DNS resolution failures for a payment gateway hostname
- Followed by payment-service unable to reach the gateway
- Followed by orders stuck in a pending-payment state

## Likely Causes

- The DNS resolution failure is the initiating event

## Investigation Steps

## Signal Chain

DNS failure for payment-gateway.internal
→ payment-service unreachable
→ orders stuck pending_payment
→ DNS restored
→ backlog drains

## Investigation

- Confirm the DNS failure timestamp precedes the first stuck-order report
- Confirm backlog drains automatically once DNS resolves, without manual intervention needed for most orders

## Recommended Actions

- Resolve the DNS issue at its source
- Add a secondary resolution path or cached fallback IP for critical hostnames

## Verification

- No orders remain stuck in pending_payment after backlog drains

## Severity Guidance

HIGH — direct revenue-path impact.

## Related Signals

- DNS Resolution Failures
