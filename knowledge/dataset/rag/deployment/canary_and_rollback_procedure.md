# Canary Deployment and Rollback Procedure

## Symptoms

- Canary release showing errors or degraded metrics on a small traffic percentage
- Rollback triggered after canary failure

## Likely Causes

- Regression introduced in the new release
- Canary metrics threshold too strict/loose for normal variance

## Investigation Steps

- Compare canary metrics against the stable baseline cohort
- Review the diff introduced in the canary release

## Recommended Actions

- Roll back the canary immediately on confirmed regression
- Fix the regression and re-attempt canary
- Tune canary thresholds if they were miscalibrated

## Verification

- Canary metrics within acceptable variance of baseline before promoting

## Severity Guidance

MEDIUM for a caught-and-rolled-back regression; HIGH if it reached full rollout before detection.

## Related Signals

- Missing configuration after deploy
- Crash loop
