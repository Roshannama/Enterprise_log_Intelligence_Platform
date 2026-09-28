# Signal Chain: Credential Stuffing to Elevated Gateway Load

## Symptoms

- Spike in failed login attempts from an IP range
- Followed by elevated gateway CPU handling the rejected traffic

## Likely Causes

- The credential stuffing attempt itself is the initiating event; gateway load is a side effect of processing the attack traffic

## Investigation Steps

## Signal Chain

Failed login burst
→ rate limiter engaged
→ elevated gateway CPU
→ load normalizes after IP block

## Investigation

- Confirm gateway CPU rise correlates with the volume of rejected auth requests, not with legitimate traffic growth

## Recommended Actions

- Block the offending IP range
- Tune rate limiter to reject cheaply before hitting more expensive code paths

## Verification

- Gateway CPU returns to baseline once the IP range is blocked

## Severity Guidance

HIGH — treat as a security incident with a secondary performance impact.

## Related Signals

- Authentication Failures and Brute-Force Patterns
