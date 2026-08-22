# Git & GitHub: Version Control for Real Projects

## Why Are We Learning This?

So far, you have learned how to write code, run programs, and use the terminal.

Now we are going to learn one of the tools that professional developers use every day:

**Git.**

Git helps you keep track of changes to your code.

**GitHub** lets you store Git repositories online, collaborate with other developers, and share your projects.

By the end of this tutorial, you should be comfortable taking a project from:

```text
A folder on your computer
        ↓
A Git repository
        ↓
A series of meaningful commits
        ↓
A GitHub repository
        ↓
A project you can share with others
```

More importantly, you should understand **why** each step exists.

---

# 1. The Problem Git Solves

Imagine that you are building a Python application.

On Monday, your project works:

```python
print("Hello!")
```

On Tuesday, you add some features.

On Wednesday, you change several things.

On Thursday, your program stops working.

You now have a problem.

You might start making copies:

```text
project/
project-backup/
project-final/
project-final-2/
project-final-new/
project-final-new-working/
project-final-new-working-2/
```

This becomes a mess very quickly.

You need a way to answer questions such as:

- What changed?
- Who changed it?
- When did it change?
- Why did we change it?
- What did the project look like yesterday?
- Can we go back to an earlier version?
- Which changes belong together?
- Can I experiment without destroying the working version?

Git solves this problem.

---

# 2. What Is Version Control?

**Version control** is a system for keeping track of changes to files over time.

Instead of thinking about your project as one constantly changing folder, think about it as a sequence of snapshots:

```text
Version 1
   ↓
Version 2
   ↓
Version 3
   ↓
Version 4
```

Each version represents a meaningful point in the project's history.

Git is a **distributed version control system**.

That sounds complicated, but the basic idea is simple:

> Git records the history of your project.

---

# 3. Git Is Not a Programming Language

Git is a tool.

You do not write Python code with Git.

You use Git from the terminal.

For example:

```bash
git status
```

or:

```bash
git commit -m "Add calculator"
```

Git works with almost any kind of text-based project:

- Python
- JavaScript
- Java
- C++
- HTML
- CSS
- SQL
- configuration files
- documentation
- data-processing projects

---

# 4. Git vs. GitHub

This distinction is extremely important.

## Git

Git is the version-control software running on your computer.

It tracks your project's history.

You can use Git without GitHub.

---

## GitHub

GitHub is an online platform built around Git repositories.

GitHub provides things such as:

- remote repository hosting
- collaboration
- pull requests
- code review
- issue tracking
- project documentation
- public project sharing
- automated workflows
- GitHub Actions
- project management

A useful analogy:

> **Git is the technology that tracks your project's history. GitHub is an online service where Git repositories can be stored and collaborated on.**

---

# 5. A Mental Model for Git

Imagine your project is a notebook.

You work on it every day.

Every so often, you create a photograph of the notebook.

That photograph represents a checkpoint.

Git gives you a much more powerful version of this idea.

Your history might look like:

```text
Initial project
      ↓
Add calculator
      ↓
Add input validation
      ↓
Fix division bug
      ↓
Add command-line interface
```

Each checkpoint is called a **commit**.

---

# 6. Install Git

Open your terminal and run:

```bash
git --version
```

You should see something similar to:

```text
git version 2.x.x
```

The exact version will depend on your computer.

If the command is not found, install Git before continuing.

After installation, run the command again:

```bash
git --version
```

---

# 7. Configure Git

Before making commits, Git needs to know who you are.

Set your name:

```bash
git config --global user.name "Your Name"
```

Set your email:

```bash
git config --global user.email "you@example.com"
```

You can check your configuration with:

```bash
git config --global --list
```

You should see your name and email.

Your email becomes part of the metadata associated with your commits.

---

# 8. Create a Practice Project

Let's create a small project.

Create a folder:

```text
git-practice
```

Inside it, create:

```text
app.py
```

Put this into `app.py`:

```python
print("Hello, Git!")
```

Your project should look like:

```text
git-practice/
└── app.py
```

Open the terminal in the project folder.

Run:

```bash
python app.py
```

You should see:

```text
Hello, Git!
```

---

# 9. Create a Git Repository

Right now, `git-practice` is just an ordinary folder.

We can turn it into a Git repository.

Run:

```bash
git init
```

Git will create a hidden `.git` directory.

Your project now conceptually looks like:

```text
git-practice/
├── .git/
└── app.py
```

The `.git` directory contains the information Git needs to track your repository.

Do not manually modify `.git`.

Let Git manage it.

---

# 10. What Is a Repository?

A **repository**, often shortened to **repo**, is a project whose history is managed by Git.

You can think of a repository as:

```text
Project files
+
Git history
+
Git configuration
```

A repository can exist:

- locally on your computer
- remotely on GitHub
- in both places

---

# 11. Your First Git Command: `status`

Run:

```bash
git status
```

Git will tell you what is happening in your repository.

You should see that `app.py` is untracked.

That means Git sees the file, but it is not currently part of a commit.

This is an important concept:

> A file existing in your folder does not automatically mean Git has recorded it.

---

# 12. The Three Important Areas of Git

One of the most important concepts in Git is understanding that your files can exist in different states.

Think about three areas:

```text
Working Directory
       ↓
Staging Area
       ↓
Repository
```

Let's understand each one.

---

## Working Directory

This is the project you are actively editing.

For example:

```text
app.py
```

You open it in your editor and make changes.

Those changes exist in your working directory.

---

## Staging Area

The staging area is where you prepare changes for the next commit.

You put a file into the staging area with:

```bash
git add app.py
```

Think:

> "I want this change included in my next checkpoint."

---

## Repository

When you commit staged changes:

```bash
git commit -m "Create first Python program"
```

Git records them in the repository's history.

---

# 13. The Basic Git Workflow

This is the workflow you will use constantly:

```text
Edit files
   ↓
git status
   ↓
git add
   ↓
git commit
```

In more detail:

```text
Change code
    ↓
Check what changed
    ↓
Select changes
    ↓
Create a checkpoint
```

The commands are:

```bash
git status
git add app.py
git commit -m "Describe the change"
```

Memorize these three commands first.

---

# 14. Stage Your First File

Run:

```bash
git add app.py
```

Then:

```bash
git status
```

The file should now appear as staged.

You have moved it from:

```text
Untracked
```

to:

```text
Staged
```

---

# 15. Create Your First Commit

Now run:

```bash
git commit -m "Create first Python program"
```

Congratulations.

You have created your first Git commit.

You can think of the commit as:

```text
Checkpoint #1
```

Git now remembers this state of your project.

---

# 16. What Is a Commit?

A commit is a recorded set of changes.

It contains information such as:

- which files changed
- what those changes were
- who created the commit
- when it was created
- the commit message
- a unique commit identifier

A commit is not just "save."

It is a meaningful point in the project's history.

---

# 17. Good Commit Messages

A commit message should explain what the commit did.

Good:

```text
Add calculator function
```

```text
Fix invalid user input
```

```text
Create homepage
```

```text
Add password validation
```

Less useful:

```text
stuff
```

```text
changes
```

```text
asdf
```

```text
final
```

A useful commit message should make sense when you read it six months later.

---

# 18. Make Another Change

Change `app.py`:

```python
print("Hello, Git!")
print("I am learning version control.")
```

Save the file.

Run:

```bash
python app.py
```

Then run:

```bash
git status
```

Git will tell you that `app.py` has been modified.

Git is comparing:

```text
Current project
       ↓
Last commit
```

and noticing that they are different.

---

# 19. Inspect Your Changes

Run:

```bash
git diff
```

Git will show the changes you have made since the last commit.

This is incredibly useful.

Before committing, you can inspect what you are about to record.

A common workflow is:

```bash
git status
git diff
git add app.py
git commit -m "Add learning message"
```

---

# 20. Create Your Second Commit

Stage the file:

```bash
git add app.py
```

Commit it:

```bash
git commit -m "Add learning message"
```

You now have two commits.

Conceptually:

```text
Commit 1
Create first Python program
        ↓
Commit 2
Add learning message
```

---

# 21. View Your History

Run:

```bash
git log
```

You will see your commits.

A shorter version is:

```bash
git log --oneline
```

You might see:

```text
91ab32f Add learning message
73c9d11 Create first Python program
```

Each commit has a unique identifier.

This identifier is called a **commit hash**.

---

# 22. Why Commits Matter

Suppose your program works perfectly.

You then make five changes.

Suddenly it breaks.

If those changes were committed separately, you have a history:

```text
Working version
      ↓
Add feature
      ↓
Refactor code
      ↓
Change input handling
      ↓
Add validation
      ↓
Bug appears
```

You can inspect the history and determine what happened.

This is much better than having one giant:

```text
final.py
```

file with no history.

---

# 23. Git Is About History, Not Just Backup

Git is often described as a backup system.

That is incomplete.

Git gives you:

- history
- comparisons
- experimentation
- collaboration
- branching
- merging
- rollback
- accountability
- code review

The important idea is:

> Git lets you manage change.

---

# 24. What Is a Remote Repository?

So far, our repository exists only on our computer.

We can create a second copy somewhere else.

This is called a **remote repository**.

For this tutorial, the remote will be GitHub.

The relationship looks like:

```text
Your computer
┌──────────────────┐
│ Local Git repo   │
└──────────────────┘
         │
         │ push / pull
         ↓
┌──────────────────┐
│ GitHub repo      │
└──────────────────┘
```

---

# 25. Create a GitHub Account

Go to GitHub and create an account if you do not already have one.

Once your account is ready, you can create repositories online.

Important:

**GitHub is not required to use Git locally.**

You can learn Git entirely on your computer.

GitHub becomes useful when you want to:

- back up your repository
- share your code
- collaborate
- work from multiple computers
- contribute to open-source projects

---

# 26. Create a GitHub Repository

On GitHub, create a new repository.

For this tutorial, call it:

```text
git-practice
```

GitHub may ask whether you want to initialize it with:

- a README
- a `.gitignore`
- a license

For this first exercise, create the repository without adding extra files.

We already have a local repository.

We will connect the two.

---

# 27. Local vs. Remote

You now have:

```text
LOCAL

git-practice/
├── .git/
└── app.py
```

and:

```text
REMOTE

GitHub
└── git-practice
```

They are two repositories.

We need to tell Git that the GitHub repository is the remote associated with our local repository.

---

# 28. Add the GitHub Remote

GitHub will provide commands for connecting your local repository.

Conceptually, the command looks like:

```bash
git remote add origin <repository-url>
```

For example:

```bash
git remote add origin https://github.com/YOUR-USERNAME/git-practice.git
```

The word:

```text
origin
```

is simply the conventional name for the default remote repository.

You can check your remote with:

```bash
git remote -v
```

You should see your GitHub repository listed.

---

# 29. What Does `origin` Mean?

`origin` is not a special Git command.

It is a name.

When you run:

```bash
git remote add origin ...
```

you are saying:

> "Call this remote repository `origin`."

You could technically use another name.

But `origin` is the standard convention.

You will see it everywhere.

---

# 30. Push Your Code to GitHub

Your local repository contains commits.

GitHub does not have those commits yet.

We need to **push** them.

Run:

```bash
git push -u origin main
```

Depending on your Git configuration, your default branch may be named `master` instead of `main`.

If your branch is called `master`, use:

```bash
git push -u origin master
```

The `-u` sets the upstream relationship between your local branch and the remote branch.

After the first push, you can usually simply run:

```bash
git push
```

---

# 31. What Does `push` Mean?

`push` means:

> Send local commits to a remote repository.

Think:

```text
Your computer
     │
     │ git push
     ↓
GitHub
```

It does not mean "upload every file blindly."

Git pushes Git history and the objects associated with your commits.

---

# 32. Refresh GitHub

Open your repository on GitHub.

You should now see:

```text
app.py
```

You should also be able to see your commit history.

Your project now exists in two places:

```text
Your computer
      ↕
   GitHub
```

---

# 33. The Complete Workflow

At this point, you know the basic local-to-GitHub workflow:

```text
Write code
    ↓
Save code
    ↓
git status
    ↓
git diff
    ↓
git add
    ↓
git commit
    ↓
git push
    ↓
GitHub
```

A typical session might look like:

```bash
git status
git diff
git add .
git commit -m "Add user greeting"
git push
```

---

# 34. What Does `git add .` Mean?

You may see developers use:

```bash
git add .
```

The `.` means the current directory.

It tells Git to stage changes throughout the current directory.

This can be convenient.

However, beginners should understand what they are staging before committing.

Use:

```bash
git status
```

after staging to verify what will be included.

For example:

```bash
git add .
git status
```

Read the result before committing.

---

# 35. Be Careful With `git add .`

Imagine your project contains:

```text
project/
├── app.py
├── notes.txt
├── secret.txt
└── data.csv
```

You only intended to commit `app.py`.

If you run:

```bash
git add .
```

you may stage everything that Git considers relevant.

This is why `.gitignore` is important.

---

# 36. What Is `.gitignore`?

A `.gitignore` file tells Git which files it should ignore.

For example:

```text
__pycache__/
.env
*.pyc
```

This tells Git not to track certain files.

This is particularly important for:

- passwords
- API keys
- environment variables
- temporary files
- generated files
- operating-system files
- Python cache files
- virtual environments

---

# 37. Never Commit Secrets

This is one of the most important rules in this tutorial.

Do **not** commit:

```text
API keys
passwords
private keys
database credentials
secret tokens
```

For example, never do this:

```python
API_KEY = "my-real-secret-key"
```

inside a file that you intend to push publicly to GitHub.

Instead, use environment variables.

For example:

```python
import os

api_key = os.environ.get("API_KEY")
```

We will study environment variables in more detail later.

---

# 38. A Typical Python `.gitignore`

A Python project often has a `.gitignore` resembling:

```gitignore
__pycache__/
*.pyc
.venv/
.env
.DS_Store
```

Each line represents something Git should ignore.

You do not need to memorize this yet.

The important idea is:

> **Not every file in your project should be committed.**

---

# 39. What Is a Branch?

Now we move into one of Git's most powerful concepts.

A **branch** is an independent line of development.

Imagine your main project is:

```text
main
  │
  ●
  │
  ●
  │
  ●
```

You want to experiment with a new feature.

Instead of changing `main` directly, you can create a branch:

```text
main
  │
  ●
  │
  ●──────────── feature-login
  │                  │
  ●                  ●
                     │
                     ●
```

You can work on the feature without disturbing the main branch.

---

# 40. Why Branches Exist

Suppose your application works.

You want to add:

```text
AI chatbot
```

This could involve many changes.

You don't want unfinished work to interfere with the stable version.

So you create:

```text
feature-chatbot
```

Then work there.

Your branches might look like:

```text
main
feature-chatbot
feature-login
bugfix-payment
```

---

# 41. See Your Branch

Run:

```bash
git branch
```

The current branch will usually be marked with `*`.

For example:

```text
* main
```

---

# 42. Create a Branch

Run:

```bash
git branch feature-greeting
```

This creates the branch.

But it does not switch you to it.

To switch:

```bash
git switch feature-greeting
```

You can combine the two operations:

```bash
git switch -c feature-greeting
```

This means:

> Create a new branch and switch to it.

---

# 43. Branch Workflow

Your workflow becomes:

```text
main
  ↓
create branch
  ↓
feature-greeting
  ↓
write code
  ↓
commit
  ↓
push
```

The main branch remains separate.

---

# 44. Make a Change on Your Branch

On `feature-greeting`, change `app.py`:

```python
print("Hello, Git!")
print("Welcome to CookieSensei.")
```

Then:

```bash
git status
git add app.py
git commit -m "Add CookieSensei greeting"
```

Your commit belongs to the feature branch.

---

# 45. Push a Branch to GitHub

You can push your branch:

```bash
git push -u origin feature-greeting
```

Now GitHub can see the branch.

You may see:

```text
main
feature-greeting
```

as separate branches.

---

# 46. What Is a Pull Request?

A **pull request**, often called a PR, is a request to merge changes from one branch into another.

For example:

```text
feature-greeting
        │
        │ Pull Request
        ↓
      main
```

A pull request allows people to:

- inspect changes
- discuss code
- suggest improvements
- run tests
- review the implementation
- approve the change
- merge it

Pull requests are one of the main ways professional teams collaborate.

---

# 47. Why Not Just Change `main`?

For a tiny personal project, you can.

But imagine a company with ten developers.

If everyone directly modifies `main`, you can quickly get conflicts and unstable code.

Instead:

```text
main
 │
 ├── feature-login
 ├── feature-dashboard
 ├── bugfix-payment
 └── feature-search
```

Each developer can work independently.

Then changes are reviewed and merged.

---

# 48. Merging

When a feature is complete, its changes can be merged into `main`.

Conceptually:

```text
feature-greeting
       │
       ●
       │
       ●
        \
         \
main -----●----------●
```

After the merge, the feature becomes part of the main development line.

Git handles the mechanics of combining the histories.

---

# 49. What Is a Merge Conflict?

Sometimes two people modify the same part of the same file.

For example:

Developer A writes:

```python
print("Hello from Alice")
```

Developer B writes:

```python
print("Hello from Bob")
```

Git cannot automatically decide which line is correct.

This creates a **merge conflict**.

Git will mark the conflicting section.

You must manually decide what the final code should be.

---

# 50. Merge Conflicts Are Normal

Do not think:

> "A merge conflict means I broke Git."

It doesn't.

A conflict means:

> "Git found two changes that it cannot safely combine automatically."

The normal process is:

```text
Conflict
   ↓
Open the file
   ↓
Understand both changes
   ↓
Choose the correct result
   ↓
Save the file
   ↓
git add
   ↓
Complete the merge
```

Learning to resolve conflicts is part of becoming comfortable with Git.

---

# 51. `git pull`

Now imagine another computer or another developer has pushed changes to GitHub.

Your local repository is now behind.

You can retrieve the latest changes with:

```bash
git pull
```

Conceptually:

```text
GitHub
   ↓
git pull
   ↓
Your computer
```

`git pull` generally retrieves remote changes and integrates them into your current branch.

---

# 52. `git fetch` vs. `git pull`

These commands are related but different.

### `git fetch`

Downloads information about remote changes without automatically integrating them into your current branch.

```bash
git fetch
```

### `git pull`

Fetches remote changes and then integrates them into your current branch.

```bash
git pull
```

A beginner can start with:

```bash
git pull
```

As you become more advanced, understanding `git fetch` becomes useful.

---

# 53. The Four Commands You Will Use Constantly

A very common workflow is:

```bash
git status
git add .
git commit -m "Describe the change"
git push
```

And when starting work:

```bash
git pull
```

So a typical development cycle is:

```text
git pull

     ↓

Write code

     ↓

git status

     ↓

git diff

     ↓

git add .

     ↓

git commit

     ↓

git push
```

---

# 54. Inspecting History

Useful history commands include:

```bash
git log
```

```bash
git log --oneline
```

```bash
git log --oneline --graph --all
```

The last one can give you a visual representation of branches.

For example:

```text
* 91ab Add login
* 73cd Add homepage
|\
| * 51ef Experiment with chatbot
| * 48ac Add chatbot UI
|/
* 21aa Initial project
```

---

# 55. Viewing a Commit

You can inspect a particular commit with:

```bash
git show COMMIT_HASH
```

For example:

```bash
git show 91ab32f
```

This lets you see what happened in that commit.

---

# 56. Comparing Changes

To see unstaged changes:

```bash
git diff
```

To see staged changes:

```bash
git diff --staged
```

This distinction is useful.

Think:

```text
Working directory
       │
       │ git diff
       ↓
What have I changed?

Staging area
       │
       │ git diff --staged
       ↓
What am I about to commit?
```

---

# 57. Undoing Changes

Git gives you many ways to undo things.

This is powerful, but it is also where beginners should slow down.

There is an important difference between:

- undoing an uncommitted change
- undoing a staged change
- undoing a commit
- undoing a commit that has already been pushed

These are different situations.

---

# 58. Discarding an Uncommitted Change

Suppose you edit:

```text
app.py
```

and decide:

> "I don't want these changes."

If the changes have not been committed, Git can restore the file to its last committed state.

One modern command is:

```bash
git restore app.py
```

Be careful.

This discards the current uncommitted changes to that file.

---

# 59. Unstaging a File

Suppose you ran:

```bash
git add app.py
```

but then realize you don't want it included in the next commit.

You can unstage it with:

```bash
git restore --staged app.py
```

This does **not** necessarily delete your changes.

It removes the file from the staging area.

---

# 60. Reverting a Commit

Suppose you already committed a change and want to undo its effect.

A safe approach for shared history is:

```bash
git revert COMMIT_HASH
```

Git creates a new commit that reverses the earlier commit.

This preserves the history.

For example:

```text
Commit A
   ↓
Commit B
   ↓
Commit C
   ↓
Revert B
```

The history remains visible.

---

# 61. Why `revert` Is Important

Imagine you pushed a commit to GitHub.

Other developers may already have based their work on it.

You generally do not want to rewrite shared history.

Instead, create a new commit that undoes the old one.

That is what `git revert` is designed for.

---

# 62. Be Careful With `reset`

You may encounter:

```bash
git reset
```

and especially:

```bash
git reset --hard
```

These commands can rewrite or discard history and changes.

They are useful in certain situations, but beginners should not use them casually.

The important rule for now is:

> **If you are unsure what a Git command will destroy, stop and inspect it before running it.**

---

# 63. GitHub as Your Public Portfolio

GitHub can become more than storage.

It can become part of your developer portfolio.

A good repository can show:

- what you built
- how you structured the project
- how you documented it
- how you use Git
- how you test code
- how you collaborate
- how you solve problems

For a student learning to code, this can become very valuable.

---

# 64. The README

Most GitHub repositories should have a `README.md`.

The README explains the project.

A simple README might contain:

```markdown
# My First Python Project

A small Python project I built while learning programming.

## What It Does

The program prints a greeting.

## How to Run

```bash
python app.py
```

## What I Learned

- Python basics
- Git
- GitHub
```

The README is often the first thing another person sees when visiting your repository.

---

# 65. What Makes a Good Repository?

A good beginner project might look like:

```text
my-project/
├── README.md
├── app.py
├── requirements.txt
├── .gitignore
└── src/
```

The exact structure depends on the project.

The goal is clarity.

Someone else should be able to understand:

1. What the project does.
2. How to install it.
3. How to run it.
4. What technologies it uses.
5. What you learned.
6. Where to find the important code.

---

# 66. GitHub Issues

GitHub also provides **Issues**.

Issues can represent:

- bugs
- feature requests
- questions
- improvements
- tasks

For example:

```text
Issue #1
Add user login

Issue #2
Fix invalid email validation

Issue #3
Improve homepage design
```

This turns GitHub into a lightweight project-management system.

---

# 67. Connecting Issues and Commits

You can reference issues in commit messages.

For example:

```text
Add email validation (#12)
```

This creates a relationship between the commit and the issue.

In larger projects, this makes the history much easier to understand.

---

# 68. GitHub Pull Requests

A pull request is not simply:

> "Please pull my code."

It is a collaborative review process.

A good pull request explains:

### What changed?

```text
Added user authentication.
```

### Why?

```text
Users need to be able to create accounts.
```

### How was it implemented?

```text
Added Django authentication views and templates.
```

### How was it tested?

```text
Tested signup, login, logout, and invalid passwords.
```

This makes code review much easier.

---

# 69. A Professional Feature Workflow

A realistic workflow might look like:

```text
git pull
        ↓
Create feature branch
        ↓
Write code
        ↓
Run tests
        ↓
git status
        ↓
git diff
        ↓
git add
        ↓
git commit
        ↓
git push
        ↓
Open Pull Request
        ↓
Code review
        ↓
Fix requested changes
        ↓
Merge
```

This is the workflow you will gradually become comfortable with.

---

# 70. Your First Complete GitHub Exercise

Create a project called:

```text
my-first-github-project
```

Create:

```text
app.py
README.md
.gitignore
```

Your `app.py` should contain a small Python program.

For example:

```python
name = input("What is your name? ")

print(f"Hello, {name}!")
```

Your README should explain:

- what the program does
- how to run it
- what you learned

Then initialize Git:

```bash
git init
```

Check the repository:

```bash
git status
```

Stage your files:

```bash
git add .
```

Commit:

```bash
git commit -m "Create first GitHub project"
```

Create a GitHub repository.

Connect it:

```bash
git remote add origin <repository-url>
```

Push:

```bash
git push -u origin main
```

Then open the repository on GitHub.

---

# 71. Your Second Exercise: Branches

Create a branch:

```bash
git switch -c add-favorite-language
```

Modify your program so it asks:

```text
What is your favorite programming language?
```

Commit the change:

```bash
git add .
git commit -m "Ask for favorite programming language"
```

Push the branch:

```bash
git push -u origin add-favorite-language
```

Open GitHub.

Create a pull request from:

```text
add-favorite-language
```

into:

```text
main
```

Read through the changes.

Then merge the pull request.

This is your first taste of a professional Git workflow.

---

# 72. Exercise: Break Something Safely

Git becomes much easier to understand when you experiment.

Create a commit where your program works.

Then deliberately change something so it breaks.

Run:

```bash
git diff
```

Look at the changes.

Then decide whether you want to:

- fix the code
- restore the file
- commit the fix

The goal is to become comfortable experimenting.

---

# 73. Exercise: Read Your Own History

Run:

```bash
git log --oneline
```

Read each commit.

Ask yourself:

> If I joined this project six months from now, would these messages help me understand what happened?

If not, improve your commit-message habits.

---

# 74. Common Beginner Mistakes

## Mistake 1: Forgetting to commit

You make changes for hours without creating a checkpoint.

Better:

```text
Small meaningful changes
        ↓
Small meaningful commits
```

---

## Mistake 2: Using terrible commit messages

Avoid:

```text
update
stuff
final
changes
```

Prefer:

```text
Add login form
Fix invalid email validation
Create database model
Add homepage navigation
```

---

## Mistake 3: Committing secrets

Never commit API keys or passwords.

---

## Mistake 4: Not checking `git status`

When confused, run:

```bash
git status
```

This is one of your best debugging tools.

---

## Mistake 5: Being afraid of branches

Branches are not scary.

They are simply separate lines of development.

---

# 75. When You Are Confused, Ask Git

A surprisingly useful rule:

> **When you don't know what is happening, run `git status`.**

For example:

```bash
git status
```

It can tell you:

- your current branch
- modified files
- staged files
- untracked files
- whether your branch is ahead
- whether your branch is behind

It is often the first command you should run when something feels wrong.

---

# 76. The Git Vocabulary You Should Know

By the end of this tutorial, you should understand these words:

### Repository

A project managed by Git.

### Commit

A recorded checkpoint in Git history.

### Working directory

The files you are currently editing.

### Staging area

The changes prepared for the next commit.

### Branch

A separate line of development.

### Merge

Combining changes from different branches.

### Remote

Another repository, usually hosted somewhere like GitHub.

### Push

Send local commits to a remote repository.

### Pull

Retrieve and integrate changes from a remote repository.

### Clone

Create a local copy of a remote repository.

### Pull request

A request to merge changes into another branch on a platform such as GitHub.

### Commit hash

The unique identifier associated with a commit.

### `.gitignore`

A file specifying things Git should not track.

---

# 77. Clone: The Opposite of Creating a Repository

So far, we started locally and pushed to GitHub.

But often you will start with an existing GitHub project.

You can download a repository with:

```bash
git clone <repository-url>
```

For example:

```bash
git clone https://github.com/example/project.git
```

This creates a local copy of the repository.

The workflow becomes:

```text
GitHub repository
       ↓
git clone
       ↓
Your computer
```

You can then:

```bash
cd project
```

and start working.

---

# 78. Clone vs. Download ZIP

You might notice that GitHub lets you download a ZIP file.

That gives you the project files.

But cloning gives you the Git history and remote configuration too.

For development work, prefer:

```bash
git clone
```

because you want the repository, not just a snapshot of the files.

---

# 79. The Most Important Mental Model

At this point, remember this picture:

```text
                    GitHub
                 Remote Repo
                     ↑
                     │
                   push
                     │
                     │
┌────────────────────┴────────────────────┐
│                                         │
│             Local Repository            │
│                                         │
│   Working       Staging       Commits   │
│   Directory       Area        History   │
│      │              │             │     │
│      │   git add    │  commit     │     │
│      └─────────────→└────────────→      │
│                                         │
└─────────────────────────────────────────┘
```

And when you receive changes:

```text
GitHub
   │
   │ git pull
   ↓
Local repository
```

---

# 80. Your Everyday Git Checklist

When starting work on a project:

```bash
git pull
```

Work on your code.

Then:

```bash
git status
```

Inspect your changes:

```bash
git diff
```

Stage them:

```bash
git add .
```

Check what will be committed:

```bash
git status
```

Commit:

```bash
git commit -m "Describe what changed"
```

Push:

```bash
git push
```

That is enough to get started.

---

# 81. Phase 0 Challenge

Build a small Python project of your choice.

It could be:

- a calculator
- a number guessing game
- a quiz
- a unit converter
- a simple text adventure
- a command-line to-do list

Your project must:

- contain at least one Python file
- have a README
- have a `.gitignore`
- be initialized as a Git repository
- contain at least five meaningful commits
- have a GitHub remote
- be pushed to GitHub
- contain at least one feature branch
- contain at least one pull request
- have the feature merged into `main`

Your commit history might look something like:

```text
Create initial Python application
Add input validation
Add score tracking
Fix invalid input bug
Add README
```

---

# 82. Reflection Questions

After completing the challenge, answer these questions in your own words.

### Question 1

What problem does Git solve?

### Question 2

What is the difference between Git and GitHub?

### Question 3

What happens when you run:

```bash
git add
```

?

### Question 4

What happens when you run:

```bash
git commit
```

?

### Question 5

Why might you create a branch?

### Question 6

What is the difference between `git push` and `git pull`?

### Question 7

Why should you never commit API keys?

### Question 8

Why are small, meaningful commits useful?

---

# 83. The Core Idea

You do not need to memorize every Git command.

You need to understand the workflow.

```text
I change my code.
        ↓
I inspect my changes.
        ↓
I stage the changes I want.
        ↓
I create a meaningful checkpoint.
        ↓
I push that history to GitHub.
        ↓
I can collaborate, review, and recover.
```

Git is not just another command-line tool.

It is a way of thinking about software development:

> **Make changes deliberately. Record meaningful checkpoints. Keep your history understandable.**

As your CookieSensei projects become larger, this habit will become increasingly important.