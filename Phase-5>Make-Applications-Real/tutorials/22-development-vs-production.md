# Tutorial 22 — Development vs Production

## Why This Matters

An application working locally is not automatically ready for real users.

## Development

Your laptop may use:

```text
runserver
DEBUG
SQLite
automatic reload
```

## Production

Production needs more careful configuration and a proper application server. `runserver` is for development.

## Important Settings

Understand the role of:

```text
DEBUG
ALLOWED_HOSTS
SECRET_KEY
DATABASE
STATIC FILES
```

## Mental Model

```text
Local computer
   ↓
Development

Server
   ↓
Production
```

## Try It

Look through your settings and identify what should differ between local development and production.

## Remember

> **“It works on my laptop” is not the same as “it is ready for users.”**
