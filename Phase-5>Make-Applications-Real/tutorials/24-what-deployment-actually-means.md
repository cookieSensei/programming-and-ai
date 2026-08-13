# Tutorial 24 — What Deployment Actually Means

## Why This Matters

Deployment becomes less mysterious when broken into its required pieces.

## Local vs Deployed

```text
Local:
Your laptop → Django → Browser

Deployed:
Code → Server → Internet → User
```

## What the Server Needs

At a basic level:

```text
Python
Django
Dependencies
Application code
Environment variables
Database
Static files
Application server
```

## Typical Flow

```text
Write code
 ↓
Test locally
 ↓
Commit
 ↓
Push
 ↓
Configure server
 ↓
Install dependencies
 ↓
Configure environment
 ↓
Run migrations
 ↓
Collect static files
 ↓
Start application
 ↓
Public URL
```

## Try It

For your MWP, draw:

```text
Browser → Internet → ? → Django → Database
```

Fill in what each component will be after deployment.
