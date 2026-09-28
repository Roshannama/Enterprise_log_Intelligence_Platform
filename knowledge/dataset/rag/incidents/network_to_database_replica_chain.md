# Signal Chain: Network Degradation to Database Replica Issues

## Symptoms

- Packet loss on database subnet
- Followed by replication lag increase
- Followed by replica connection resets
- Followed by fallback read traffic on primary

## Likely Causes

- Network degradation is the initiating event; replica issues and primary load increase are downstream consequences

## Investigation Steps

## Signal Chain

Network packet loss
→ replication lag
→ replica connection reset
→ fallback reads on primary
→ increased primary load

## Investigation

- Confirm packet loss timing precedes replication lag onset
- Check whether primary load increase matches fallback traffic volume

## Recommended Actions

- Resolve underlying network issue
- Consider temporary read failover strategy while resolving

## Verification

- Replication lag and primary load return to baseline once network issue resolves

## Severity Guidance

MEDIUM to HIGH depending on how long fallback load is sustained on primary.

## Related Signals

- Database Replica Lag
- Connection Reset and Packet Loss
