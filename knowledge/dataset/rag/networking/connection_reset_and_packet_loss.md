# Connection Resets and Packet Loss

## Symptoms

- Connection reset by peer errors
- Elevated packet loss on a network segment

## Likely Causes

- Network hardware or link degradation
- Overloaded network path (congestion)
- Misconfigured firewall/security-group dropping legitimate connections

## Investigation Steps

- Check packet loss metrics on the relevant network segment
- Check firewall/security-group rule changes
- Check for correlated congestion from other traffic

## Recommended Actions

- Engage network team for hardware/link issues
- Revert or fix problematic firewall rule changes
- Add retry with backoff for transient resets

## Verification

- Packet loss and reset rate return to baseline

## Severity Guidance

MEDIUM typically; HIGH if it causes replica lag or payment path instability.

## Related Signals

- Database replica lag
- DNS resolution failure
