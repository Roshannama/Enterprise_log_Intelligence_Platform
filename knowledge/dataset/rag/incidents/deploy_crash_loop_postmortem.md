# Postmortem: Deployment Crash Loop (Synthetic)

## Symptoms

- New release entered a crash loop immediately after rollout

## Likely Causes

- A required environment variable was omitted from the new deployment manifest

## Investigation Steps

- Diffed configuration between revisions
- Identified the missing environment variable
- Confirmed rollback restored service

## Recommended Actions

- Added a pre-deploy configuration validation gate
- Added automated rollback on crash-loop detection

## Verification

- Subsequent deploys passed the new validation gate without incident

## Severity Guidance

HIGH — full service outage until rollback, contained to one service.

## Related Signals

- Missing configuration after deploy
