# Injection Attempt Detection (SQL/Command/Path Traversal)

## Symptoms

- Request parameters containing SQL syntax fragments
- Path segments containing traversal sequences
- Input containing shell metacharacters

## Likely Causes

- Automated vulnerability scanner probing endpoints
- Targeted exploitation attempt
- Legitimate but unusual input incorrectly flagged (false positive)

## Investigation Steps

- Confirm whether WAF or input validation blocked the request
- Check if the pattern repeats across many endpoints (scanning) or targets one (exploitation)
- Review whether any request actually succeeded despite the suspicious payload

## Recommended Actions

- Ensure parameterized queries are used everywhere
- Ensure path inputs are canonicalized and validated
- Block the source IP if clearly malicious and confirmed not a false positive

## Verification

- No successful exploitation confirmed
- Repeat attempts blocked at WAF/edge

## Severity Guidance

HIGH if any request succeeded; MEDIUM if consistently blocked with no impact.

## Related Signals

- Unusual user agent
- WAF block event
