# Database Connection Failure Runbook

## Problem

The application is repeatedly failing to establish a connection to the database.

## Common Causes

Possible causes include:

1. Database server unavailable.
2. Network connectivity problems.
3. Database connection pool exhaustion.
4. Authentication or authorization failure.
5. Incorrect database configuration.
6. Database resource exhaustion.

## Investigation Steps

1. Check whether the database server is reachable.
2. Verify database connection configuration.
3. Check active database connections.
4. Check connection pool utilization.
5. Verify database credentials and permissions.
6. Review database server logs.
7. Check whether the problem affects other services.

## Recommended Actions

If the database is unavailable, investigate database health and availability.

If connection pool exhaustion is suspected, inspect connection pool utilization and active connections.

If authentication failure is suspected, verify credentials and database permissions.

## Evidence to Collect

Collect:

- Timestamp of failures.
- Service name.
- Number of failures.
- Database error messages.
- Connection pool information.
- Database server status.