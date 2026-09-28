# Credential Exposure Guidance

## Problem

Sensitive credentials such as API keys, passwords, bearer tokens, and authentication secrets may accidentally appear in application logs.

## Sensitive Information

Examples include:

- API keys.
- Passwords.
- Bearer tokens.
- Authentication tokens.
- Database credentials.
- Private access tokens.

## Risks

Credential exposure in logs may allow unauthorized users to access systems or services if the exposed credential remains valid.

Potential consequences include:

- Unauthorized access.
- Data exposure.
- Account compromise.
- Service misuse.
- Security incidents.

## Investigation Steps

1. Identify the type of credential exposed.
2. Determine where the credential was logged.
3. Determine whether the credential is still active.
4. Identify systems or services that can be accessed using the credential.
5. Review access logs for suspicious activity.
6. Check whether the credential was exposed to unauthorized users.

## Recommended Actions

1. Revoke or rotate the exposed credential.
2. Remove sensitive information from future application logs.
3. Review logging configuration.
4. Investigate whether the credential was used after exposure.
5. Restrict access to logs containing sensitive information.

## Prevention

Applications should avoid writing credentials and authentication secrets to logs.

Sensitive values should be detected and redacted before logs are stored or processed.