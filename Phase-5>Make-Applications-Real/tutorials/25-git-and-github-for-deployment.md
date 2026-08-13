# Tutorial 25 — Git and GitHub for Deployment

## Why This Matters

Git provides checkpoints and often becomes part of the deployment workflow.

## Basic Commands

```bash
git status
git add .
git commit -m "Add booking form"
git log
```

## GitHub

A repository can contain source code, templates, CSS, JavaScript, requirements, and documentation.

It should not contain:

```text
.venv/
.env
passwords
API keys
large generated files
```

## Deployment Flow

```text
Local project
 ↓
Git
 ↓
GitHub
 ↓
Deployment platform
 ↓
Live application
```

## Try It

Create a repository, commit a small change, push it, and inspect the repository to make sure secrets and `.venv` were not committed.
