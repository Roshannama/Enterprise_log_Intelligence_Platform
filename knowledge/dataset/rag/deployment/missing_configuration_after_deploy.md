# Missing Configuration After Deployment

## Symptoms

- Service fails to start after a new deployment
- Errors referencing a missing environment variable or config key

## Likely Causes

- New configuration requirement not added to deployment manifest
- Config value present in one environment but not another
- Secret/config store misconfigured for the new release

## Investigation Steps

- Diff the configuration between the failing and last-known-good revision
- Check deployment manifest for the missing key
- Check config/secret store for the target environment

## Recommended Actions

- Add the missing configuration value
- Roll back to the last-known-good revision if urgent
- Add a pre-deploy configuration validation check

## Verification

- Service starts successfully with the configuration present

## Severity Guidance

MEDIUM if caught quickly with rollback available; HIGH if it causes extended downtime.

## Related Signals

- Crash loop
- Rollback event
