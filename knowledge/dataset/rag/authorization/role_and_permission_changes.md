# Unexpected Role and Permission Changes

## Symptoms

- Role changed to a higher-privilege role outside change windows
- Permission grants without corresponding approval record

## Likely Causes

- Legitimate but unlogged administrative action
- Compromised admin account making unauthorized changes
- Automation/script bug granting incorrect roles

## Investigation Steps

- Identify the actor who made the change
- Check for a corresponding approved change ticket
- Check actor's account for other suspicious activity

## Recommended Actions

- Revert the role change if unauthorized
- Require MFA and review for admin role changes going forward
- Fix any automation bug identified

## Verification

- All privileged roles reconciled against approved change records

## Severity Guidance

HIGH for any unreviewed privilege escalation to admin-level roles.

## Related Signals

- Restricted endpoint access
- Brute-force pattern
