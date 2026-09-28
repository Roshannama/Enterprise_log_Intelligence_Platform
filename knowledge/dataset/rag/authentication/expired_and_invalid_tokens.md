# Expired and Invalid Token Handling

## Symptoms

- Requests failing with expired-token errors
- Invalid signature errors on token validation

## Likely Causes

- Normal token lifecycle expiry (expected)
- Clock skew between issuing and validating services
- Forged or tampered token (security concern)

## Investigation Steps

- Check whether failures are expiry-only (expected) or signature-mismatch (concerning)
- Check clock synchronization across services
- Check source diversity of invalid-signature attempts

## Recommended Actions

- No action needed for routine expiry (client should refresh)
- Fix clock sync if skew detected
- Investigate as possible forgery if signature mismatches are widespread

## Verification

- Failure type distribution returns to routine-expiry-only pattern

## Severity Guidance

LOW for routine expiry; HIGH if signature forgery is suspected.

## Related Signals

- Invalid token signature
- Brute-force pattern
