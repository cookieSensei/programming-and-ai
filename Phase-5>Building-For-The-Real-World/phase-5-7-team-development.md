# 7. Team Development

## Building Software With Other Developers

So far, most of our projects have been built by one person:

```text
You
 ↓
Code
 ↓
Git
 ↓
Application
```

Real software is often different.

A project may have:

```text
Developer A
Developer B
Developer C
Designer
Product Manager
```

all working on the same codebase.

This introduces a new problem:

# How do multiple people work on the same project without destroying each other's work?

This section introduces the basics of:

```text
Git
GitHub
Branches
Pull Requests
Code Review
Issues
Merge Conflicts
Team Workflow
```

The goal is not to become a Git expert.

The goal is to understand the basic workflow used when developers collaborate.

---

# 1. Why Team Development Is Different

Imagine two developers editing:

```text
app.py
```

at the same time.

Developer A changes:

```python
def login():
    ...
```

Developer B changes:

```python
def upload_resume():
    ...
```

If both people simply replace the entire file with their own version, someone's work may disappear.

We need a system that allows developers to:

```text
Work independently
 ↓
Save their changes
 ↓
Share their changes
 ↓
Combine changes
```

Git helps us do this.

---

# 2. Git vs GitHub

These are related but different.

## Git

Git is the version control system.

It runs on your computer.

It tracks changes to files.

```text
Your computer
    ↓
Git
    ↓
History of changes
```

## GitHub

GitHub is a service that hosts Git repositories and provides collaboration features.

```text
Your computer
    ↓
Git
    ↓
GitHub
    ↓
Team
```

Git is the version-control tool.

GitHub is one platform where Git repositories can be hosted and collaborated on.

---

# 3. The Repository

A project stored with Git is called a:

# Repository

For example:

```text
ai-career-companion/
```

The repository contains:

```text
app.py
requirements.txt
services/
pages/
README.md
```

and Git also tracks the history of changes.

---

# 4. The Shared Repository

A team might have:

```text
GitHub Repository

ai-career-companion
```

Every developer can get a copy:

```text
                    GitHub
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      Developer A  Developer B  Developer C
```

Each developer can work locally.

---

# 5. Clone

To get an existing repository:

```bash
git clone <repository-url>
```

This creates a local copy.

For example:

```bash
git clone https://github.com/example/ai-career-companion.git
```

Then:

```bash
cd ai-career-companion
```

Now you are working inside the repository.

---

# 6. The Local Repository

After cloning:

```text
GitHub
   │
   │ clone
   ▼
Your computer
   │
   ├── files
   └── .git
```

The `.git` directory contains Git's local repository data.

You normally should not edit it manually.

---

# 7. Check the Repository

A useful first command is:

```bash
git status
```

It tells you what is happening in the repository.

For example:

```text
On branch main
nothing to commit, working tree clean
```

This means:

```text
Current branch:
main

Uncommitted changes:
none
```

---

# 8. The Basic Git Workflow

The workflow we learned earlier was:

```text
Experiment
 ↓
Develop
 ↓
Git Checkpoint
 ↓
Iterate
```

With a team:

```text
Create branch
 ↓
Develop
 ↓
Test
 ↓
Commit
 ↓
Push
 ↓
Pull Request
 ↓
Code Review
 ↓
Merge
```

This is the core workflow for this section.

---

# 9. Why Branches?

Suppose the application currently works.

```text
main
 ↓
Working application
```

Now you want to add:

```text
Resume upload
```

You do not want experimental code to immediately change the main version.

Create a branch:

```text
main
 │
 └── feature/resume-upload
```

Now you can work independently.

---

# 10. Create a Branch

For example:

```bash
git switch -c feature/resume-upload
```

This means:

```text
Create branch
+
Switch to it
```

Check:

```bash
git branch
```

You might see:

```text
* feature/resume-upload
  main
```

The `*` indicates the current branch.

---

# 11. Branches Are Parallel Lines of Work

Imagine:

```text
main
 │
 ●
 │
 ●
 │
 ├──────── feature/resume-upload
 │                    │
 │                    ●
 │                    ●
 │
 └──────── feature/job-matching
                      │
                      ●
```

Different developers can work on different branches.

---

# 12. Branch Naming

Use names that describe the work.

Good:

```text
feature/resume-upload
feature/job-matching
feature/login-page
fix/file-upload-error
fix/match-score
docs/setup-guide
```

Avoid:

```text
branch1
test
new
stuff
mybranch
```

The branch name should tell another developer what it is for.

---

# 13. Make Changes

Now work normally.

For example:

```text
Add resume upload
```

Then run the application:

```bash
streamlit run app.py
```

Test it.

Fix bugs.

Test again.

Git does not replace development.

It records development.

---

# 14. See What Changed

Run:

```bash
git status
```

Then:

```bash
git diff
```

`git diff` helps you inspect the changes you made.

This is especially important when working with AI coding assistants.

Before committing:

```text
What changed?
```

should have an answer.

---

# 15. The Staging Area

Git has an intermediate step called:

# Staging

The basic flow is:

```text
Working directory
       ↓
git add
       ↓
Staging area
       ↓
git commit
       ↓
Git history
```

For example:

```bash
git add app.py
```

Or:

```bash
git add .
```

The second command stages all changes in the current directory.

Beginners should understand what they are staging before committing.

---

# 16. Commit

After staging:

```bash
git commit -m "Add resume upload"
```

A commit is a checkpoint.

It says:

```text
At this point,
the project looked like this.
```

A good commit message explains what changed.

---

# 17. Good Commit Messages

Good:

```text
Add resume upload
Fix authentication redirect
Store resume metadata
Add job matching
Update setup instructions
```

Less useful:

```text
changes
update
stuff
final
done
```

A future teammate should understand the commit without opening the entire diff.

---

# 18. Push

Your commit currently exists locally.

To send your branch to GitHub:

```bash
git push -u origin feature/resume-upload
```

Now:

```text
Local branch
      ↓
GitHub
```

The team can see your work.

---

# 19. What Is Origin?

When you clone a repository, Git normally creates a remote named:

```text
origin
```

You can inspect remotes with:

```bash
git remote -v
```

You may see:

```text
origin
    https://github.com/...
```

`origin` is simply the conventional name for the remote repository you cloned from.

---

# 20. Pull Request

After pushing your branch, create a:

# Pull Request

A Pull Request, often called a PR, asks the team:

```text
I made these changes.

Please review them.

If they are acceptable,
merge them into the main project.
```

The workflow becomes:

```text
Branch
 ↓
Commit
 ↓
Push
 ↓
Pull Request
 ↓
Review
 ↓
Merge
```

---

# 21. Why Not Push Directly to Main?

A beginner-friendly team rule is:

```text
Do not directly modify main.
```

Instead:

```text
main
 ↓
feature branch
 ↓
Pull Request
 ↓
Review
 ↓
main
```

This gives the team a checkpoint before changes become part of the shared version.

---

# 22. Code Review

Another developer reviews the PR.

They might ask:

```text
Why are we doing this?

Can this function be simpler?

What happens if the file is empty?

What happens if upload fails?

Does this expose another user's resume?

Do we have a test?
```

Code review is not about proving that someone is wrong.

It is a way to improve the software before merging it.

---

# 23. Review the Problem, Not the Person

Bad review:

```text
This code is terrible.
```

Better:

```text
Could we move this database operation
into database.py?

That would keep the Streamlit page
focused on UI logic.
```

Good code review is:

```text
specific
technical
respectful
actionable
```

---

# 24. Pull Requests as Communication

A PR should explain:

```text
What changed?

Why was it changed?

How was it tested?
```

For example:

```text
Title:
Add resume upload

Description:

What:
Users can upload PDF resumes.

Why:
We need persistent resume storage.

Testing:
- Uploaded a PDF
- Confirmed it appears in Storage
- Confirmed metadata appears in PostgreSQL
- Tested with two users
```

This makes collaboration easier.

---

# 25. Issues

A GitHub Issue can represent:

```text
Bug
Feature
Task
Question
Improvement
```

For example:

```text
#42
Add resume deletion
```

Description:

```text
Users can upload resumes,
but they currently cannot delete them.

Requirements:
- Delete Storage object
- Delete database record
- Only allow users to delete their own files
```

Now a team member can work on the issue.

---

# 26. Issue → Branch

A useful workflow is:

```text
Issue
 ↓
Branch
 ↓
Implementation
 ↓
Commit
 ↓
Pull Request
 ↓
Review
 ↓
Merge
```

For example:

```text
Issue #42
Add resume deletion
```

becomes:

```text
feature/resume-delete
```

---

# 27. Small Tasks

Do not create one giant issue:

```text
Build entire AI Career Companion
```

Break it into:

```text
Add login
Add resume upload
Add resume parser
Add jobs table
Add job creation
Add similarity calculation
Add match history
Add dashboard
```

Small tasks are easier to:

```text
Understand
Assign
Implement
Review
Test
Merge
```

---

# 28. Team Roles

For a small student project, people can rotate responsibilities.

For example:

```text
Developer A
Database + Auth

Developer B
Resume Processing

Developer C
Streamlit UI
```

But everyone should understand the whole system.

The goal is learning, not permanent specialization.

---

# 29. Working on the Same Project

Suppose:

```text
Alice
```

works on:

```text
Resume upload
```

and:

```text
Bob
```

works on:

```text
Job matching
```

Their branches might be:

```text
feature/resume-upload
feature/job-matching
```

Both originate from:

```text
main
```

They can work independently.

---

# 30. Keeping Your Branch Updated

While the team is working, `main` may change.

Your branch can become outdated.

A simple workflow is:

```bash
git switch main
git pull
```

Then update your feature branch using the team's chosen workflow.

For beginners, one approach is:

```bash
git switch feature/resume-upload
git merge main
```

This brings changes from `main` into your branch.

The exact synchronization strategy can vary between teams.

The important concept is:

> **Your branch is not automatically up to date with the rest of the team.**

---

# 31. Merge Conflicts

Eventually, two developers may edit the same lines.

For example:

Alice changes:

```python
title = "AI Career Companion"
```

Bob changes the same line:

```python
title = "Career Assistant"
```

Git cannot automatically decide which one is correct.

This produces a:

# Merge Conflict

---

# 32. What a Conflict Looks Like

Git may insert markers like:

```text
<<<<<<< HEAD
title = "AI Career Companion"
=======
title = "Career Assistant"
>>>>>>> main
```

This means:

```text
<<<<<<<
Your version

=======
Other version

>>>>>>>
```

The developer must decide what the final code should be.

---

# 33. Resolving a Conflict

The process is:

```text
Read both versions
 ↓
Understand why each changed
 ↓
Choose the correct result
 ↓
Remove conflict markers
 ↓
Run the application
 ↓
Test
 ↓
Stage resolved file
 ↓
Continue merge
```

Do not blindly choose:

```text
ours
```

or:

```text
theirs
```

without understanding the change.

---

# 34. Conflict Resolution Is a Reasoning Problem

Suppose:

```text
Developer A
added authentication

Developer B
changed the login page
```

A conflict may actually require combining both:

```text
Authentication logic
+
New login UI
```

The correct solution may not be either original version.

It may be:

```text
A + B
```

This is why developers need to understand their code.

---

# 35. AI Can Help With Conflicts

AI can explain a conflict.

Give it:

```text
Original code
Our branch
Incoming branch
```

and ask:

```text
Explain what each side changed.

Do not resolve it yet.

Tell me what behavior
each version is trying to achieve.
```

Then decide yourself.

AI should not blindly resolve conflicts in unfamiliar code.

---

# 36. GitHub Workflow

A simple team workflow is:

```text
             GitHub
                │
                ▼
              main
                │
       ┌────────┴────────┐
       ▼                 ▼
 feature/A           feature/B
       │                 │
       ▼                 ▼
    commits           commits
       │                 │
       └────────┬────────┘
                ▼
          Pull Requests
                │
                ▼
             Review
                │
                ▼
              Merge
                │
                ▼
              main
```

---

# 37. The Golden Rule

Before starting work:

```bash
git switch main
git pull
```

Then:

```bash
git switch -c feature/my-feature
```

Work:

```text
Code
 ↓
Test
 ↓
Commit
```

Then:

```bash
git push
```

Create:

```text
Pull Request
```

After review:

```text
Merge
```

This is the basic team loop.

---

# 38. What About Small Documentation Changes?

Not every change needs to be complicated.

Even for:

```text
README
```

or:

```text
Markdown tutorial
```

the workflow can be:

```text
branch
 ↓
edit
 ↓
commit
 ↓
push
 ↓
PR
 ↓
review
 ↓
merge
```

This teaches students that Git is part of everyday development, not just something used for large code changes.

---

# 39. Team Communication

Git cannot solve every team problem.

Developers also need to communicate.

Before starting a task, clarify:

```text
What am I changing?

Which files will I touch?

What does "done" mean?

Who depends on this work?
```

For example:

```text
Alice:
I'm changing the resumes table
and database helper.

Bob:
I'm building the resume upload UI.

Let's agree on the function
that connects them.
```

This prevents unnecessary conflicts.

---

# 40. Define Interfaces

Suppose one developer writes:

```python
upload_resume(...)
```

and another developer needs to use it.

Agree on:

```text
What arguments does it accept?

What does it return?

What errors can occur?
```

For example:

```python
upload_resume(
    user_id,
    filename,
    file_bytes
)
```

returns:

```text
storage_path
```

Now both developers can work independently.

This is an introduction to an important software engineering idea:

# Interfaces

---

# 41. Avoid Stepping on Each Other

A useful team strategy is to divide work by responsibility.

For example:

```text
Developer A
services/database.py

Developer B
services/resume_parser.py

Developer C
pages/Jobs.py
```

This reduces the chance that everyone edits:

```text
app.py
```

at the same time.

It is not always possible, but thoughtful task boundaries help.

---

# 42. Shared Conventions

Teams should agree on simple conventions.

For example:

```text
Python:
snake_case

Branches:
feature/name
fix/name

Commits:
short imperative messages

Files:
descriptive names

Secrets:
never committed
```

The exact rules can vary.

Consistency matters more than the particular convention.

---

# 43. `.gitignore`

Some files should not be committed.

For example:

```text
.env
__pycache__/
.venv/
```

A typical `.gitignore` might include:

```text
.venv/
__pycache__/
*.pyc
.env
.streamlit/secrets.toml
```

The exact entries depend on the project.

---

# 44. Why `.env` Matters

Suppose:

```text
.env
```

contains:

```text
SUPABASE_URL=...
SUPABASE_KEY=...
```

Do not commit it if it contains secrets.

Instead:

```text
.env
 ↓
.gitignore
 ↓
never committed
```

Team members can create their own local configuration.

---

# 45. Environment Variables

The application can read configuration from the environment.

For example:

```python
import os

supabase_url = os.getenv(
    "SUPABASE_URL"
)
```

This means:

```text
Code
 ↓
Environment
 ↓
Configuration
```

rather than:

```text
Code
 ↓
Hardcoded secret
```

---

# 46. README as Team Documentation

A shared project should explain how to run it.

For example:

```text
# AI Career Companion

## Setup

Create virtual environment.

Install dependencies.

Configure environment variables.

Run Streamlit.

## Project Structure

...

## Database

...

## Development Workflow

...
```

A new developer should be able to follow the README and get the project running.

---

# 47. Onboarding a Teammate

Imagine a new student joins.

They should be able to:

```text
Clone repository
 ↓
Read README
 ↓
Create environment
 ↓
Install dependencies
 ↓
Configure secrets
 ↓
Run application
 ↓
Understand project structure
 ↓
Pick an issue
 ↓
Create branch
 ↓
Start work
```

If they cannot do this, the project probably needs better documentation.

---

# 48. Code Review Checklist

Before approving a PR, ask:

```text
Does the code work?

Does it solve the issue?

Is the code understandable?

Are errors handled?

Are secrets protected?

Does it respect user permissions?

Could it break existing functionality?

Was it tested?

Does the documentation need updating?
```

For the Career Companion, also ask:

```text
Does this respect RLS?

Can one user access another user's data?

Can one user access another user's files?
```

---

# 49. AI + Team Development

We can combine the previous section with this one.

A modern workflow can look like:

```text
Issue
 ↓
Developer understands requirement
 ↓
Design
 ↓
AI assistance
 ↓
Implementation
 ↓
Testing
 ↓
AI code review
 ↓
Git commit
 ↓
Push
 ↓
Pull Request
 ↓
Human code review
 ↓
Merge
```

Notice there are still two review layers:

```text
AI review
+
Human review
```

AI does not replace the teammate.

---

# 50. Do Not Make AI the Reviewer of Its Own Code

If AI generated:

```text
500 lines
```

and then you ask the same AI:

```text
Is this code good?
```

the result may be useful, but it should not be your only review.

A human teammate can ask:

```text
Why did you choose this architecture?

Why is this query structured this way?

What happens when this fails?

Did you test this?
```

Human review adds context.

---

# 51. Team Project

Use the:

# AI Career Companion

as the team project.

Split the project into issues.

For example:

```text
#1 Authentication
#2 Resume upload
#3 Resume parsing
#4 Job creation
#5 Job listing
#6 Similarity engine
#7 Match history
#8 Dashboard
#9 Skill-gap analysis
#10 Documentation
```

Each issue should have:

```text
Goal
Requirements
Definition of done
```

---

# 52. Example Issue

## Issue: Add Resume Upload

### Goal

Allow an authenticated user to upload a PDF resume.

### Requirements

```text
- Accept PDF
- Upload to private Storage bucket
- Store metadata in PostgreSQL
- Associate file with current user
- Show upload success
- Handle errors
```

### Definition of Done

```text
✓ PDF uploads
✓ File appears in Storage
✓ Database row exists
✓ Correct user_id is stored
✓ Another user cannot access it
✓ Error is displayed if upload fails
```

This is much clearer than:

```text
Make resume upload.
```

---

# 53. Definition of Done

A task is not necessarily done because:

```text
"It works on my computer."
```

A better definition might include:

```text
Code implemented
Tests pass
Error cases considered
Security checked
Documentation updated
PR reviewed
```

For an introductory project, keep the definition simple but explicit.

---

# 54. Team Exercise

Create teams of:

```text
2–4 students
```

Give every team the same starting repository.

Each team should:

```text
1. Clone the repository.

2. Create GitHub Issues.

3. Divide the work.

4. Create feature branches.

5. Implement features.

6. Open Pull Requests.

7. Review each other's PRs.

8. Resolve at least one merge conflict.

9. Merge completed work.

10. Demonstrate the final application.
```

The goal is to practice the workflow.

---

# 55. Required Team Exercise

Every student should personally perform:

```text
git clone
git switch
git status
git diff
git add
git commit
git push
```

and participate in:

```text
Pull Request
Code Review
Merge
```

Every student should also experience at least one:

```text
Merge Conflict
```

because conflict resolution is much easier to understand after actually experiencing it.

---

# 56. Final Team Workflow

By the end of this section, students should be comfortable with:

```text
                 PROJECT
                    │
                    ▼
                  ISSUE
                    │
                    ▼
                 BRANCH
                    │
                    ▼
               DEVELOPMENT
                    │
                    ▼
                  TEST
                    │
                    ▼
                 COMMIT
                    │
                    ▼
                  PUSH
                    │
                    ▼
            PULL REQUEST
                    │
                    ▼
              CODE REVIEW
                    │
                    ▼
                  MERGE
                    │
                    ▼
                  MAIN
                    │
                    ▼
                ITERATE
```

---

# 57. What We Have Learned

Team development is not simply:

```text
"Use GitHub."
```

It is a way of organizing collaboration.

We learned:

```text
Git
 ↓
Branches
 ↓
Commits
 ↓
Push
 ↓
Pull Requests
 ↓
Code Review
 ↓
Issues
 ↓
Merge Conflicts
 ↓
Team Communication
```

And we connected it to:

```text
AI-Assisted Development
```

so that the complete workflow becomes:

```text
Problem
 ↓
Issue
 ↓
Design
 ↓
AI Assistance
 ↓
Branch
 ↓
Develop
 ↓
Test
 ↓
Commit
 ↓
Pull Request
 ↓
AI + Human Review
 ↓
Merge
 ↓
Iterate
```

---

# 58. The Bigger Lesson

At the beginning of the curriculum, we learned to write:

```python
1 + 2
```

in a notebook.

Then:

```text
app.py
```

Then:

```text
Git
```

Then:

```text
Machine Learning
Deep Learning
Computer Vision
NLP
```

Then:

```text
SQL
Database
Authentication
Storage
```

Now we reach another important transition:

```text
Individual Developer
        ↓
Team Developer
```

Software is rarely only about writing code.

It is also about:

```text
Communicating
Planning
Reviewing
Testing
Sharing
Maintaining
```

That is the foundation of professional software development.

---

# 59. Final Challenge

Work with a small team to extend the AI Career Companion.

Your team must:

```text
Choose 3–5 features
        ↓
Create GitHub Issues
        ↓
Assign work
        ↓
Create branches
        ↓
Implement features
        ↓
Use AI where useful
        ↓
Test
        ↓
Open Pull Requests
        ↓
Review teammates' code
        ↓
Merge
```

At the end, demonstrate:

```text
The application
+
The GitHub repository
+
The issues
+
The pull requests
+
The development history
```

The repository history is part of the project.

It tells the story of how the software was built.

---

# 60. Phase 5 Final Workflow

We can now put the entire Phase 5 together:

```text
                    IDEA
                     │
                     ▼
                  DESIGN
                     │
                     ▼
                 DATABASE
                     │
                     ▼
              AUTH + STORAGE
                     │
                     ▼
             APPLICATION LOGIC
                     │
                     ▼
              AI INTELLIGENCE
                     │
                     ▼
                 STREAMLIT
                     │
                     ▼
              AI ASSISTANCE
                     │
                     ▼
                  TESTING
                     │
                     ▼
                    GIT
                     │
                     ▼
                  BRANCH
                     │
                     ▼
              PULL REQUEST
                     │
                     ▼
               CODE REVIEW
                     │
                     ▼
                   MERGE
                     │
                     ▼
                 ITERATE
```

This is the bridge from:

```text
Learning programming
```

to:

```text
Building software with other developers.
```

---

# 61. Takeaway

You have now learned enough to build a small application, store its data, authenticate users, handle files, add intelligent behavior, use AI during development, and collaborate with other developers.

The next step is not another library.

It is to take what you have learned and **build something of your own**.
