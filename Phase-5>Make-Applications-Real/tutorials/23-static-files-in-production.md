# Tutorial 23 — Static Files in Production

## Why This Matters

Students need to understand why CSS and images sometimes disappear after deployment.

## Static Files

Static files include CSS, JavaScript, images, and fonts.

## Collecting Files

Django provides:

```bash
python manage.py collectstatic
```

This gathers static files into the configured location for deployment.

## Why It Matters

A deployed page can have working HTML but missing CSS. Static-file configuration is one of the first things to check.

## WhiteNoise

A simple Django deployment may use WhiteNoise to help serve static files without requiring a separate static-file server. Students only need to understand its role, not its internals.

## Try It

Run `collectstatic` in a suitable project and inspect what it does. Then identify the project's static settings.
