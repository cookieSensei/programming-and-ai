# Tutorial 04 - Prepare Your Application for Production

## Phase 5 - Make Applications Real

### The big idea

Your application can work perfectly on your laptop and still not be ready for real users.

Development and production are different environments.

The official Phase 5 project frames the outcome as understanding the basic changes required before putting a Django application online: environment variables, secrets, debug settings, allowed hosts, static files, dependencies, and production configuration. fileciteturn13file3L437-L458

---

# 1. Development vs production

During development, you may have:

```text
Your laptop
 ↓
Django development server
 ↓
Browser
```

You control everything.

Production looks more like:

```text
Real user
 ↓
Internet
 ↓
Hosted server
 ↓
Django
 ↓
Database
```

There are more moving parts.

---

# 2. Why development settings are different

Development prioritizes:

```text
speed
convenience
debugging
experimentation
```

Production prioritizes:

```text
security
reliability
correct configuration
controlled access
```

A setting that helps you debug locally may expose information in production.

The important rule is:

> **Do not assume that a setting that is convenient for development is safe for public users.**

---

# 3. Debug mode

Django has a debug setting.

During development:

```python
DEBUG = True
```

can make errors easier to diagnose.

But a public application should not expose detailed internal error information to strangers.

Therefore production configuration needs appropriate debug behavior.

Do not think of:

```text
DEBUG = False
```

as the entire production checklist.

It is one part of a larger configuration change.

---

# 4. Secret keys

Django uses a secret key.

Sensitive values can also include:

```text
database passwords
API keys
service credentials
third-party tokens
```

These should not be casually committed into public source code.

The Phase 5 project explicitly says not to put sensitive values directly into source code and recommends environment configuration. fileciteturn13file3L471-L492

---

# 5. Why hard-coded secrets are dangerous

Imagine:

```python
STRIPE_SECRET_KEY = "actual-secret-value"
```

and then:

```bash
git add .
git commit
git push
```

Now the secret may exist in:

```text
Git history
remote repository
clones
backups
logs
```

Even deleting the line later may not remove it from history.

The safer pattern is:

```text
Environment
     ↓
Secret value
     ↓
Django
```

---

# 6. Environment variables

An environment variable allows configuration to live outside your source code.

Conceptually:

```text
Operating environment
       ↓
SECRET_KEY
DATABASE_URL
API_KEY
       ↓
Django settings
```

Your source code can use a value supplied by the environment.

A common development pattern uses a `.env` file, but remember:

> A `.env` file containing real secrets should normally not be committed.

Instead, provide something like:

```text
.env.example
```

with placeholders.

---

# 7. `.env.example`

For example:

```text
SECRET_KEY=replace-me
DATABASE_URL=replace-me
API_KEY=replace-me
```

This tells another developer what configuration is required without exposing your actual values.

Think:

```text
.env.example
= instructions

.env
= local secret configuration
```

---

# 8. Allowed hosts

Django can restrict which host/domain names are allowed to serve the application.

During deployment, your application may need:

```text
yourdomain.com
www.yourdomain.com
```

rather than only:

```text
localhost
127.0.0.1
```

The important concept is:

> Production configuration needs to know which hostnames the application is expected to serve.

---

# 9. Dependencies

Your laptop may already have many Python packages installed.

The deployment server does not.

That means the project needs a reproducible dependency list.

For example:

```bash
python -m pip freeze > requirements.txt
```

The Phase 5 project explicitly uses `requirements.txt` to help another environment recreate the packages needed by the application. fileciteturn13file3L494-L503

---

# 10. Why requirements matter

Suppose your application uses:

```text
Django
pillow
some-api-client
```

Your laptop has them.

A fresh server may have none.

Deployment needs a way to install the required dependencies.

Conceptually:

```text
requirements.txt
       ↓
install dependencies
       ↓
application can start
```

---

# 11. Static files

Your application may use:

```text
CSS
JavaScript
images
fonts
```

These are static assets.

Development can make static files feel automatic.

Production requires deliberate handling.

The question is:

> When a real user's browser requests `/static/...`, where does that file come from?

You do not need to become a web-server administrator.

You need to understand the deployment problem.

---

# 12. Database configuration

Locally you may use:

```text
SQLite
```

A hosted application may use another database setup.

The exact database choice is less important than understanding:

```text
Application
    ↓
Database configuration
    ↓
Production database
```

Your production application must connect to the correct database.

---

# 13. The application must start without your laptop

This is a powerful test.

Ask:

> If I give the project to another computer, can it start?

The other computer does not have:

```text
your installed packages
your environment variables
your local database
your file paths
```

Your project must define what it needs.

This is why deployment preparation is partly an exercise in making assumptions explicit.

---

# 14. Production checklist

Use this checklist:

```text
□ Secrets are not committed
□ Debug mode is configured correctly
□ Allowed hosts are configured
□ Dependencies are listed
□ Static files are prepared
□ Database configuration is ready
□ Environment variables are documented
□ Application can start without your development machine
```

This matches the Phase 5 project's core production checklist. fileciteturn13file3L514-L524

---

# 15. Security exercise: find the secrets

Search your project for:

```text
SECRET_KEY
password
API_KEY
TOKEN
DATABASE
credential
```

Ask:

> Would I be comfortable publishing this repository publicly?

If not, investigate the value.

Move real secrets into environment configuration.

---

# 16. What should go into Git?

Generally:

```text
source code
templates
migration files
requirements.txt
.env.example
README
configuration templates
```

Generally not:

```text
.env
real secrets
passwords
private credentials
local machine-specific files
```

The exact ignore list depends on your stack.

---

# 17. Common production-preparation mistakes

### "It works locally, so deployment will work."

Not necessarily.

### "I will add the API key directly into settings.py."

Dangerous if committed.

### "The CSS works locally, so static files are solved."

Production may serve static assets differently.

### "The database is on my laptop."

The hosted application needs access to the production database.

### "I can fix security later."

Do not publish known secrets or unsafe configuration just to move faster.

---

# 18. Using ChatGPT

Ask:

> Review this Django settings file for production readiness. Identify secrets, debug configuration, allowed-host configuration, static-file configuration, and database configuration. Do not change anything yet.

Then:

> Give me a production checklist specific to this project. Separate required changes from optional improvements.

This is better than asking:

> Make my Django project production-ready.

The second request is too broad.

---

# 19. Completion exercise

Create a file:

```text
PRODUCTION-CHECKLIST.md
```

Include:

```text
Application:
____________________

Production domain:
____________________

Required environment variables:
____________________

Database:
____________________

Static files:
____________________

Dependencies:
____________________

Debug setting:
____________________

Allowed hosts:
____________________
```

Then review the project before deployment.

---

# Remember

The most important mental model is:

```text
Local application
      ↓
Production configuration
      ↓
Hosted application
      ↓
Real users
```

Your application running on your laptop is **not automatically ready to be shared with the internet**. fileciteturn13file3L542-L550
