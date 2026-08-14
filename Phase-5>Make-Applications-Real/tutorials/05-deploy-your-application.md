# Tutorial 05 - Deploy Your Application

## Phase 5 - Make Applications Real

### The big idea

A website is not useful to another person if it only runs on your laptop.

Deployment means moving the application from your development environment into an environment where another person can access it.

The official Phase 5 project defines the outcome simply:

> **I can put my application in front of another person.**

It focuses on hosting, remote dependencies, database configuration, environment variables, public URLs, and deployment troubleshooting. fileciteturn13file4L561-L580

---

# 1. Local application

During development:

```text
Your computer
     ↓
Django
     ↓
Browser
```

You might run:

```bash
python manage.py runserver
```

and open:

```text
http://127.0.0.1:8000/
```

That URL points to your own computer.

Someone else cannot normally use it as your public product URL.

---

# 2. Deployed application

After deployment:

```text
Your computer
     ↓
Deploy
     ↓
Hosted server
     ↓
Internet
     ↓
Another person's browser
```

Now your application has a public address.

That is the fundamental purpose of deployment.

---

# 3. What is a server?

A server is a computer/system that provides resources or services to other computers.

In this context, a hosted server runs your web application.

Conceptually:

```text
Server
 ├── application code
 ├── Python environment
 ├── dependencies
 ├── configuration
 └── access to database
```

You do not need to own a physical server.

A hosting provider can provide the infrastructure.

---

# 4. What does a hosting provider do?

A hosting provider gives you an environment where your application can run.

Different providers have different interfaces.

The exact provider is less important than understanding the questions:

1. Where is the code hosted?
2. Where does the application run?
3. Where does the database live?
4. How are environment variables configured?
5. How does the application start?
6. Where do logs appear?

These are the important deployment concepts emphasized in the Phase 5 implementation. fileciteturn13file4L621-L632

---

# 5. Before deployment

Your project should contain the important pieces:

```text
source code
requirements.txt
templates
static files
environment configuration
database configuration
```

The Phase 5 project recommends committing the project to Git before deployment. fileciteturn13file4L608-L619

---

# 6. Why Git matters

Deployment systems commonly retrieve your source code from a repository.

Git gives you:

```text
history
versions
branches
commits
```

A useful workflow is:

```text
Build locally
   ↓
Test
   ↓
Commit
   ↓
Push
   ↓
Deploy
```

Do not deploy an untested pile of changes if you can avoid it.

---

# 7. The deployment pipeline

A simplified pipeline:

```text
Git repository
       ↓
Hosting platform
       ↓
Install Python
       ↓
Install requirements
       ↓
Set environment variables
       ↓
Configure database
       ↓
Run application
       ↓
Public URL
```

The exact commands differ by hosting provider.

The architecture remains similar.

---

# 8. Requirements installation

The remote environment does not know what packages your laptop has installed.

It may run:

```bash
pip install -r requirements.txt
```

That is why the requirements file matters.

If your application imports:

```python
import django
import PIL
```

the remote environment needs those dependencies installed.

---

# 9. Environment variables

Your deployment environment needs configuration.

Examples:

```text
SECRET_KEY
DEBUG
ALLOWED_HOSTS
DATABASE_URL
API_KEY
```

These should be configured in the hosting environment rather than committed as secrets.

Conceptually:

```text
Hosting settings
       ↓
Environment variables
       ↓
Django
```

---

# 10. Database deployment

This is a common source of confusion.

Your local database might contain:

```text
Booking #1
Booking #2
Booking #3
```

The production database may initially contain nothing.

Your application code and your database are separate things.

```text
Code
 ≠
Data
```

A deployment may need:

```bash
python manage.py migrate
```

to create the required database schema.

If you need sample data, seed it deliberately.

---

# 11. Application startup

The hosting platform needs to know how to start your Django application.

The production server typically needs an application entry point.

Django projects commonly expose WSGI or ASGI application objects.

You do not need to memorize the internals.

Understand:

```text
Hosting platform
      ↓
Starts Django application
      ↓
Application listens for web requests
```

---

# 12. Logs are your friend

When deployment fails, do not guess.

Find the logs.

You may see:

```text
ModuleNotFoundError
```

This suggests a missing dependency.

Or:

```text
ImproperlyConfigured
```

This suggests a configuration problem.

Or:

```text
DisallowedHost
```

This suggests host configuration.

Or:

```text
OperationalError
```

This may indicate a database problem.

The skill is:

> **Read the deployment log and identify which layer failed.**

---

# 13. Common deployment failures

## Missing dependency

```text
ModuleNotFoundError
```

Check:

```text
requirements.txt
```

## Missing environment variable

The application expects:

```text
SECRET_KEY
```

but the hosting environment does not provide it.

## Wrong allowed host

Django rejects the incoming hostname.

## Database not configured

The application cannot connect to the expected database.

## Static files missing

The HTML loads but:

```text
CSS missing
images missing
JavaScript missing
```

## Incorrect startup command

The platform cannot start the Django application.

---

# 14. Debugging deployment systematically

Use:

```text
1. Did the build succeed?
2. Were dependencies installed?
3. Were environment variables configured?
4. Did the database connect?
5. Did migrations run?
6. Did the application start?
7. Can the server receive a request?
8. Are static files available?
```

Do not change five things at once.

---

# 15. The first public test

Once deployed:

```text
Open public URL
       ↓
Homepage
       ↓
Core user journey
       ↓
Database action
       ↓
Result
```

Test the application exactly as a user would.

---

# 16. Test with another person

This is one of the most valuable exercises in Phase 5.

Give the URL to someone who was not involved in building the application.

Do not explain the interface immediately.

Ask them to use it.

The official project recommends observing whether they understand the application, can complete the core task, and where they become confused. fileciteturn13file4L651-L663

---

# 17. Why outside testing matters

You know:

```text
where the button is
what the terminology means
what should happen
which steps are required
```

A new user does not.

That makes you a poor judge of discoverability.

Watch the user.

Do not defend the interface.

Record what actually happens.

---

# 18. Deployment exercise

Create a deployment checklist:

```text
□ Git repository ready
□ requirements.txt ready
□ environment variables identified
□ secrets excluded
□ database configured
□ migrations ready
□ static files considered
□ application start command known
□ logs accessible
□ public URL works
```

Then deploy.

---

# 19. Break-and-diagnose exercise

The Phase 5 project recommends deliberately inspecting deployment failures such as:

```text
missing environment variable
missing dependency
incorrect allowed host
static-file configuration issue
```

and asking:

> **Where did the application fail?** fileciteturn13file4L634-L649

You can simulate some failures in a controlled environment.

For example:

```text
Remove a non-sensitive test configuration value
```

Deploy.

Read the log.

Restore it.

This teaches deployment as a debugging process rather than a magical button.

---

# 20. Using ChatGPT

Good deployment prompt:

> My Django deployment fails. Here is the exact hosting log, my requirements.txt, and the relevant settings. Identify the first meaningful failure, explain why it occurs, and give me the smallest fix. Do not rewrite the deployment architecture.

If static files fail:

> The deployed HTML loads, but CSS does not. Explain how to trace the browser request, Django static configuration, and hosting configuration before changing anything.

---

# 21. Completion criteria

You have completed this project when:

```text
Another person
      ↓
opens public URL
      ↓
understands the application
      ↓
completes the core task
      ↓
gets the expected result
```

That is more meaningful than:

> "The deployment command said successful."

---

# Remember

Deployment is the transition:

```text
My laptop
   ↓
Hosted application
   ↓
Internet
   ↓
Real user
```

The Phase 5 project defines success as another person being able to open the application through a public URL and use its core functionality. fileciteturn13file4L664-L671
