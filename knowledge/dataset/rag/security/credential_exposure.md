# Credential and Secret Exposure in Logs

## Symptoms

- API keys, tokens, or passwords appearing in plaintext log output
- Sensitive values present in DEBUG-level logs

## Likely Causes

- Missing or misconfigured log sanitization/masking
- Verbose debug logging left enabled in production
- Secrets passed via URL query parameters, which get logged

## Investigation Steps

- Identify all log locations containing the exposed value
- Determine how long the exposure has been present
- Check whether logs are accessible to unauthorized parties

## Recommended Actions

- Rotate any exposed credential immediately
- Add or fix log sanitization rules for secret patterns
- Move secrets out of URL parameters into headers or secure vaults
- Disable verbose debug logging in production

## Verification

- Confirm sanitizer masks the pattern going forward
- Confirm rotated credential is in use

## Severity Guidance

HIGH by default for any real credential exposure; treat synthetic/test values as MEDIUM for process validation.

## Related Signals

- Bearer token in logs
- Password field in logs
- API key in logs
