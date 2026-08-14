# Project 5 - Deploy Your Application

This is a small deployment-ready Django application.

The repository is provider-neutral. Use the hosting provider selected for your class and map its settings to the values in `.env.example`.

## Local setup

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver
```

## Production start command

```bash
gunicorn deploy_project.wsgi
```

## Deployment checklist

Configure these environment variables on the hosting provider:

```text
SECRET_KEY
DEBUG=False
ALLOWED_HOSTS
CSRF_TRUSTED_ORIGINS
DATABASE_URL (if using a hosted database)
```

After deployment, verify the public URL and inspect application logs if something fails.

This project intentionally does not hard-code a provider-specific deployment recipe. The teaching objective is understanding what deployment requires.
