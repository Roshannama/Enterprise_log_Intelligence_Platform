# Latency Issues: General Overview (Distractor/Overview Document)

## Symptoms

- Generic symptom: response times higher than expected for one or more endpoints

## Likely Causes

- Elevated latency can stem from many unrelated causes: slow database queries, thread pool saturation, retry amplification, memory pressure causing GC pauses, or genuine traffic growth outpacing capacity. This document does not itself diagnose which applies.

## Investigation Steps

- Identify which specific dependency or resource correlates with the latency before consulting a specific runbook

## Recommended Actions

- Route to the specific matching runbook rather than acting on this overview alone

## Verification

- N/A — overview document

## Severity Guidance

Not applicable directly; severity depends on the specific underlying cause identified.

## Related Signals

- API Latency Degradation
- Slow Database Query Patterns
- Retry Amplification
- Memory Pressure and Leaks
