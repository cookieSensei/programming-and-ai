# Tutorial 26 — Reading Deployment Errors

## Why This Matters

Deployment failures are normal; students need a method for investigating them.

## Common Categories

```text
Dependency error       → requirements / package
Environment error      → missing variable
Migration error        → database schema
Host error             → ALLOWED_HOSTS / CSRF
Static-file error      → static configuration
```

## Process

```text
Deployment failed
 ↓
Read logs
 ↓
Find first meaningful error
 ↓
Identify category
 ↓
Check configuration/code
 ↓
Fix
 ↓
Redeploy
```

## Do Not Panic

Logs can be long. Look for `ERROR`, `Exception`, `Failed`, `ModuleNotFoundError`, `OperationalError`, and the first meaningful failure.

## Using ChatGPT

Give ChatGPT the exact error, relevant configuration, hosting platform, expected result, and recent change. Ask it to identify the root cause rather than suggest unrelated changes.
