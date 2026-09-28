# TLS Handshake Failures

## Symptoms

- Certificate verify failed errors
- Handshake failures concentrated after a certain date

## Likely Causes

- Expired TLS certificate
- Certificate chain misconfiguration
- Client/server TLS version mismatch

## Investigation Steps

- Check certificate expiry date
- Check certificate chain completeness
- Check supported TLS versions on both ends

## Recommended Actions

- Rotate/renew the expired certificate
- Fix certificate chain configuration
- Align supported TLS versions
- Automate certificate renewal to prevent recurrence

## Verification

- Handshakes succeed consistently post-fix

## Severity Guidance

MEDIUM typically; HIGH if it blocks a critical external integration.

## Related Signals

- Upstream connection reset
