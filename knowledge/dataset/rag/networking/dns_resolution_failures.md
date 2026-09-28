# DNS Resolution Failures

## Symptoms

- Failed to resolve hostname errors
- Intermittent connectivity to a specific internal hostname

## Likely Causes

- Internal DNS server outage or overload
- Misconfigured or expired DNS record
- Network partition to DNS resolver

## Investigation Steps

- Check internal DNS server health
- Check the specific DNS record for correctness
- Test resolution from multiple hosts to isolate scope

## Recommended Actions

- Restart or scale the DNS server if overloaded
- Correct the DNS record if misconfigured
- Add DNS caching with sane TTLs to reduce resolver load

## Verification

- Resolution succeeds consistently from all affected hosts

## Severity Guidance

MEDIUM if isolated to one service; HIGH if affecting many services platform-wide.

## Related Signals

- Upstream unavailable
- Payment gateway unreachable
