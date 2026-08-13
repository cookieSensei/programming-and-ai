# Tutorial 21 — Environment Variables and Secrets

## Why This Matters

Production applications need configuration and secrets without exposing them in source code.

## Never Hard-Code Secrets

Avoid:

```python
API_KEY = "real-secret"
```

A public repository could expose it.

## Environment Variables

Conceptually:

```text
Environment
   ↓
SECRET_KEY / API_KEY
   ↓
Django
```

## .env

During local development you may use:

```text
SECRET_KEY=local-secret
DEBUG=True
```

Do not commit the real `.env` file.

## .env.example

You can commit an example showing required variables without real values:

```text
SECRET_KEY=
DEBUG=
```

## Try It

Search your project for passwords, API keys, and secret values. Ask whether you would be comfortable publishing the repository.

## Safety

Never paste real credentials into ChatGPT. Replace them with placeholders such as `YOUR_API_KEY`.
