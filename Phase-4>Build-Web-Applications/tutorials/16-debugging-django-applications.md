# Tutorial 16 — Debugging Django Applications

## Why This Matters

Beginners need confidence reading errors more than they need memorization.

## Start With the Error

Read the bottom of a traceback first. For example:

```text
django.db.utils.OperationalError:
no such table: main_product
```

That immediately identifies a database-table problem.

## Common Problems

```text
SyntaxError       → Python cannot parse code
ImportError       → something cannot be imported
Template error    → template/path problem
404               → URL pattern problem
500               → application error
no such table     → migration/database problem
```

## Migration Checks

```bash
python manage.py showmigrations
python manage.py migrate
```

After changing a model:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Debugging Process

```text
What did I expect?
What happened?
What is the exact error?
Which file and line are mentioned?
What changed recently?
Can I reproduce it?
What is the smallest fix?
```

## Using ChatGPT

Give it the exact error, relevant code, expected result, actual result, and recent change. Ask: **“Explain the root cause before giving me the fix.”**
