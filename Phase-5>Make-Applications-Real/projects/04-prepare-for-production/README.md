# Project 4 — Prepare Your Application for Production

This project demonstrates a production-oriented Django configuration.

It is intentionally a configuration exercise rather than a large application.

## Install

```bash
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set values appropriate to your environment.

## Development

```bash
python manage.py check
python manage.py runserver
```

## Production-style checks

```bash
python manage.py check --deploy
```

The project demonstrates:

- environment variables
- secret configuration
- `DEBUG`
- `ALLOWED_HOSTS`
- CSRF trusted origins
- static files
- `requirements.txt`
- Gunicorn

Do not commit `.env`.
