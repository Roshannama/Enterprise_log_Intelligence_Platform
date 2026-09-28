# Database Timeout: Overview of Possible Causes (Distractor/Overview Document)

## Symptoms

- Generic symptom: any operation against the database exceeds its expected time budget

## Likely Causes

- This is a broad overview; specific causes are covered in dedicated runbooks: database availability issues, network problems between app and database, connection pool exhaustion, and general resource exhaustion on the database host. Consult the specific runbook matching your observed evidence rather than this overview alone.

## Investigation Steps

- Use this document only to decide which specific runbook to consult next
- Do not treat this overview as sufficient evidence for a specific root cause

## Recommended Actions

- Route to Database Connection Timeout, Database Connection Pool Exhaustion, Database Resource Exhaustion, or Connection Reset and Packet Loss depending on evidence

## Verification

- N/A — this is a routing document, not a resolution runbook

## Severity Guidance

Severity depends entirely on which specific cause applies; this document alone does not determine severity.

## Related Signals

- Database Connection Timeout
- Database Connection Pool Exhaustion
- Database Resource Exhaustion
- Connection Reset and Packet Loss
