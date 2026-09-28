# Incident Severity Classification Policy

## Symptoms

- Ambiguity in assigning LOW/MEDIUM/HIGH/CRITICAL to a given finding

## Likely Causes

- Severity is not a direct function of log level alone; a single ERROR line is not automatically HIGH

## Investigation Steps

- Assess blast radius (how many users/services affected)
- Assess persistence (transient vs sustained)
- Assess whether a critical business path (payments, auth, checkout) is involved
- Assess confidence in the evidence supporting the finding

## Recommended Actions

- CRITICAL: sustained, wide blast radius, critical path, high confidence
- HIGH: significant impact or critical path involvement, most confidence factors present
- MEDIUM: contained impact, moderate confidence, non-critical path
- LOW: isolated, brief, low confidence, or self-resolving

## Verification

- Severity assignments reviewed against actual user/business impact after the fact

## Severity Guidance

This document itself defines the severity guidance used across the knowledge base.

## Related Signals

- Applies to every runbook and postmortem in this knowledge base
