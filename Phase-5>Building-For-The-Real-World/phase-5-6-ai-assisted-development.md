# 6. AI-Assisted Development

## Learning to Build With AI, Not Just Learn About AI

By this point in the curriculum, we have learned how to build applications ourselves.

We have worked with:

```text
Python
SQL
PostgreSQL
Supabase
Authentication
Storage
Streamlit
NLP
Machine Learning
Deep Learning
Computer Vision
```

Now we introduce another tool that has become part of modern software development:

# AI Coding Assistants

The goal of this section is **not** to teach students how to blindly generate an entire application with AI.

The goal is to teach:

> **How to use AI to become a better developer.**

---

# 1. The Old Workflow

Earlier in the curriculum, our workflow looked like:

```text
Problem
 ↓
Think
 ↓
Search documentation
 ↓
Write code
 ↓
Run code
 ↓
Get error
 ↓
Debug
 ↓
Repeat
```

This is still a valid workflow.

AI does not replace it.

Instead, we can add another tool:

```text
Problem
 ↓
Think
 ↓
Ask AI
 ↓
Evaluate answer
 ↓
Write / modify code
 ↓
Run code
 ↓
Get error
 ↓
Ask AI / investigate
 ↓
Debug
 ↓
Repeat
```

The important new step is:

```text
Evaluate answer
```

---

# 2. AI Is a Development Assistant

Think of an AI coding assistant as:

```text
Junior developer
+
Documentation assistant
+
Code reviewer
+
Rubber duck
```

It can help us:

```text
Explain code
Generate boilerplate
Find bugs
Suggest approaches
Write tests
Refactor code
Explain error messages
Read documentation
```

But it can also:

```text
Make mistakes
Invent APIs
Use outdated syntax
Introduce security problems
Misunderstand requirements
Write code that looks correct but is wrong
```

Therefore:

> **The developer remains responsible for the code.**

---

# 3. Why Learn This After Building the Application?

Because now we have enough experience to judge AI-generated code.

Imagine asking AI:

```text
Build me a Streamlit resume application
with Supabase authentication,
PostgreSQL, Storage and
cosine similarity.
```

The model may produce hundreds of lines.

But how would we know whether the code is good?

After Phase 5, we can ask:

```text
Where is authentication?

Where is authorization?

Where is RLS?

Where is the file stored?

Where is the database record?

Who owns this row?

What happens if the upload fails?

Where is the similarity calculation?
```

Learning fundamentals makes AI much more useful.

---

# 4. The Fundamental Rule

A useful rule for this section is:

> **Never accept code you cannot explain.**

You do not need to understand every implementation detail of every library.

But you should understand:

```text
What does this function do?

Why is it here?

What data goes into it?

What comes out?

What assumptions does it make?

What could go wrong?
```

---

# 5. Bad AI-Assisted Development

Imagine asking:

```text
Build my entire application.
```

AI produces:

```text
2,000 lines of code
```

You copy it.

It runs.

You deploy it.

This feels fast.

But you may not know:

```text
How authentication works
How data is stored
Why the database is structured this way
Whether secrets are exposed
Why a particular API is used
What happens on errors
```

You have generated software.

You have not necessarily learned software development.

---

# 6. Better AI-Assisted Development

Instead, break the problem down.

Ask:

```text
How should I structure
the database for users,
resumes, jobs and matches?
```

Then:

```text
Explain the schema.
```

Then:

```text
Write the SQL.
```

Then:

```text
Explain each policy.
```

Then:

```text
Help me connect this
table from Python.
```

Then:

```text
Help me debug this error.
```

The developer remains in control.

---

# 7. Context Is Everything

AI gives better answers when we give it useful context.

Compare:

```text
Why doesn't this work?
```

with:

```text
I am using Streamlit and the Supabase Python client.

This is my upload function:

<code>

The upload succeeds, but the database
insert fails with this error:

<error>

Here is the schema:

<schema>

What is likely wrong?
```

The second prompt gives the model something concrete to reason about.

---

# 8. The Anatomy of a Good Prompt

A useful coding prompt often contains:

```text
Context
+
Goal
+
Relevant code
+
Error
+
Constraints
```

For example:

```text
Context:
I am building a Streamlit application
using Supabase.

Goal:
Upload a PDF to a private Storage bucket
and store its path in PostgreSQL.

Code:
...

Error:
...

Constraints:
The bucket must remain private.
Users should only access their own files.
```

Now the AI has a much better problem definition.

---

# 9. Ask for Explanations

Do not only ask:

```text
Give me the code.
```

Also ask:

```text
Explain why this works.
```

For example:

```text
Explain this SQL query
line by line.
```

or:

```text
Explain why this RLS policy
protects the user's rows.
```

or:

```text
Explain what this Python function
returns and what assumptions it makes.
```

This turns AI into a teaching tool.

---

# 10. Ask AI to Teach at the Right Level

You can specify:

```text
Explain this like I am a beginner.
```

or:

```text
Explain this using concepts
we have already learned.
```

For this curriculum, a useful instruction is:

```text
Do not introduce a new library
unless it is necessary.
```

This prevents AI from turning a simple problem into a complicated architecture.

---

# 11. AI and Documentation

AI should not replace documentation.

Suppose you are using:

```text
Supabase Python
```

and AI gives you:

```python
some_function(...)
```

Before trusting it, check the official documentation.

The workflow becomes:

```text
AI suggestion
      ↓
Official documentation
      ↓
Verify API
      ↓
Use code
```

This is especially important for libraries that change frequently.

---

# 12. Search vs AI

Sometimes search is better.

Use documentation/search when you need:

```text
Exact API syntax
Current version behavior
Configuration options
Official examples
Security recommendations
```

Use AI when you need:

```text
Explanation
Debugging
Reasoning
Refactoring ideas
Connecting concepts
```

Often the best workflow is:

```text
AI
+
Documentation
```

rather than:

```text
AI
instead of documentation
```

---

# 13. AI as a Debugging Partner

Suppose Python gives:

```text
TypeError:
can't multiply sequence by
non-int of type 'float'
```

Instead of asking:

```text
Fix this.
```

give AI:

```text
What does this error mean?

Here is the line producing it:

<line>

Here is the type of each variable:

<values>

Explain the root cause before suggesting
a fix.
```

This teaches you to diagnose the problem.

---

# 14. The Debugging Loop

A strong AI-assisted debugging workflow is:

```text
Error
 ↓
Read error
 ↓
Understand what failed
 ↓
Form hypothesis
 ↓
Ask AI
 ↓
Compare explanation
 ↓
Test smallest fix
 ↓
Run again
```

Do not immediately replace the entire program.

---

# 15. Ask for the Smallest Fix

Suppose a program has:

```text
500 lines
```

and one function is broken.

Do not ask:

```text
Rewrite the whole application.
```

Ask:

```text
What is the smallest change
that fixes this error?
```

This reduces accidental changes.

---

# 16. AI-Assisted Refactoring

Suppose we have:

```python
def process_resume(...):
    # 200 lines
```

We can ask AI:

```text
Refactor this function into smaller functions.

Do not change behavior.

Explain each extracted function.
```

Now AI helps us improve structure.

The important constraint is:

```text
Do not change behavior.
```

---

# 17. Code Review

AI can also act as a code reviewer.

Give it:

```text
my Python file
```

and ask:

```text
Review this code for:

1. Bugs
2. Security issues
3. Poor error handling
4. Unnecessary complexity
5. Readability
6. Performance

Do not rewrite it yet.
Explain the problems first.
```

This is often more useful than asking AI to rewrite everything.

---

# 18. Security Review

This is especially important for our Phase 5 application.

Ask:

```text
Review this application for
security problems.

Pay particular attention to:

- API keys
- Supabase credentials
- Authentication
- RLS
- File access
- User ownership
- SQL injection
- Uploaded files
```

Then manually verify the findings.

---

# 19. Secrets

One of the most important rules:

> **Never put secrets directly into source code.**

Bad:

```python
SUPABASE_KEY = "my-secret-key"
```

Better:

```text
Environment variable
```

or the appropriate secret-management mechanism for the deployment environment.

AI can help us write configuration code, but we still need to understand what a secret is and where it should live.

---

# 20. AI Can Accidentally Leak Secrets

Be careful when pasting code into an AI assistant.

Do not blindly include:

```text
API keys
Passwords
Access tokens
Private keys
Personal data
Private documents
```

Instead replace them with:

```text
YOUR_API_KEY
```

or:

```text
<REDACTED>
```

---

# 21. AI-Generated Dependencies

AI may suggest:

```bash
pip install some-package
```

Do not automatically install everything it suggests.

Ask:

```text
Why do we need this dependency?
```

Then check:

```text
Is it actually necessary?

Is there already a library we use?

Is it maintained?

Is it compatible with our Python version?
```

A simple application can become unnecessarily complicated through dependency accumulation.

---

# 22. AI and Hallucinated APIs

A common failure mode is:

```text
AI confidently invents a function.
```

For example:

```python
supabase.magic_function(...)
```

The code looks plausible.

But it may not exist.

This is why:

```text
AI output
 ↓
Documentation
```

is so important.

Never assume that syntactically plausible code corresponds to a real API.

---

# 23. Ask AI to Use Existing Code

When working on the Career Companion, prefer:

```text
Here is my current code.

Modify this code.
```

instead of:

```text
Write a new application.
```

This keeps the AI grounded in your actual project.

---

# 24. Give AI the Architecture

A useful project-level prompt might say:

```text
I am building an introductory
AI Career Companion.

Stack:
- Python
- Streamlit
- Supabase
- PostgreSQL
- Supabase Auth
- Supabase Storage
- scikit-learn

Architecture:
- Auth users own resumes
- Resumes are stored in private Storage
- Resume metadata is in PostgreSQL
- RLS protects user-owned rows
- TF-IDF + cosine similarity matches resumes to jobs

Do not introduce LLMs.
Do not introduce unnecessary frameworks.
Keep the implementation beginner-friendly.
```

This establishes constraints.

---

# 25. AI as a Pair Programmer

A useful mental model is:

```text
YOU
 │
 ├── Define requirements
 ├── Make architectural decisions
 ├── Review code
 ├── Run code
 └── Make final decisions
        │
        ▼
       AI
        │
 ├── Suggest
 ├── Explain
 ├── Generate
 ├── Debug
 └── Review
```

AI is assisting the developer.

It is not the developer.

---

# 26. Build Small, Then Ask

Suppose we need a resume upload feature.

Do not ask:

```text
Build resume upload.
```

Break it down:

```text
1. How do I read a Streamlit UploadedFile?

2. How do I generate a unique filename?

3. How do I upload bytes to Supabase Storage?

4. How do I insert metadata into PostgreSQL?

5. How do I protect the row with RLS?

6. How do I generate a signed URL?
```

Now each question has a clear boundary.

---

# 27. AI-Assisted SQL

AI is particularly useful for learning SQL.

Instead of:

```text
Give me SQL for my database.
```

try:

```text
Here is my schema:

<schema>

I want to find all jobs
that a particular resume
has been matched against.

Write the SQL and explain
the JOIN step by step.
```

Then test the query yourself.

---

# 28. AI-Assisted Regex

We already learned regex earlier.

AI can help construct a pattern.

For example:

```text
I need to find email addresses
inside extracted resume text.

Suggest a regex.

Then explain every part of the pattern.
```

Do not just copy:

```python
re.findall(...)
```

Understand what it is matching.

---

# 29. AI-Assisted Data Analysis

Suppose you have:

```text
jobs.csv
```

You can ask:

```text
What EDA would be useful
for understanding the skills
requested in this dataset?
```

AI can suggest:

```text
frequency analysis
missing values
distributions
skill counts
```

Then you implement the analysis yourself.

---

# 30. AI-Assisted Machine Learning

You can ask:

```text
I have a classification problem.

Here are my features and target.

Which metrics should I use
and why?
```

The important thing is not to ask:

```text
Which model gives the highest score?
```

without understanding:

```text
What are we measuring?

What does the metric mean?

What does the test set represent?
```

The fundamentals from Phase 3 still matter.

---

# 31. AI Does Not Remove Testing

AI-generated code still needs tests.

The workflow is:

```text
Generate
 ↓
Run
 ↓
Test
 ↓
Inspect
 ↓
Fix
```

For example:

```python
def calculate_match(...):
    ...
```

Test:

```text
Same resume + same job
 → same result

Empty resume
 → handled

Empty job
 → handled

Unrelated texts
 → low similarity
```

---

# 32. Ask AI to Generate Tests

AI is often useful for generating test cases.

For example:

```text
Here is my function.

Generate test cases for:

- normal input
- empty input
- invalid input
- boundary cases
- unexpected input
```

Then review the tests.

A test is only useful if it tests something meaningful.

---

# 33. AI and Git

AI-assisted development makes Git even more important.

Why?

Because AI can make many changes quickly.

Use:

```text
Experiment
 ↓
Run
 ↓
Review
 ↓
Git checkpoint
```

rather than:

```text
Ask AI
 ↓
Accept 500 changes
 ↓
Hope it works
```

Small commits make it easier to recover.

---

# 34. The Curriculum Workflow

This connects directly to the workflow introduced near the beginning of the curriculum:

```text
Experiment
      ↓
Develop
      ↓
Git Checkpoint
      ↓
Iterate
```

With AI:

```text
Experiment
      ↓
Ask AI
      ↓
Develop
      ↓
Test
      ↓
Git Checkpoint
      ↓
Iterate
```

AI becomes another tool inside the development loop.

---

# 35. The AI Review Loop

A particularly useful workflow is:

```text
Write code
 ↓
Ask AI to review
 ↓
Read suggestions
 ↓
Decide what is valid
 ↓
Change code
 ↓
Run tests
 ↓
Commit
```

Notice:

```text
AI suggests
Developer decides
```

---

# 36. Ask AI to Challenge Your Thinking

AI can also act as a critic.

For example:

```text
I designed the application this way.

Here is my architecture:

<architecture>

Do not redesign it.

Instead, identify assumptions
that could cause problems.
```

This is a powerful use because the AI is not immediately replacing your design.

It is helping you examine it.

---

# 37. Use AI for Alternatives

Suppose you have:

```text
Approach A
```

Ask:

```text
What are two simpler alternatives?

Compare them in terms of:

- complexity
- maintainability
- learning value
- performance
```

Then make the decision yourself.

This is much better than:

```text
What is the best architecture?
```

because "best" depends on the project's goals.

---

# 38. AI-Assisted Documentation

AI can help turn code into documentation.

For example:

```text
Here is my function.

Write a concise docstring
that describes:

- purpose
- arguments
- return value
- possible errors
```

It can also help produce:

```text
README
Setup instructions
API notes
Comments
```

But verify that the documentation matches the actual code.

---

# 39. AI-Assisted Git Messages

After a meaningful change, you can ask AI:

```text
Here is the diff.

Suggest a concise commit message.
```

For example:

```text
Add private resume upload flow
```

But students should still understand what the commit actually changed.

---

# 40. AI and Git Diff

A particularly useful workflow:

```text
git diff
    ↓
AI review
    ↓
Potential issues
    ↓
Developer inspection
```

For example:

```text
Review this diff.

Look specifically for:

- accidental changes
- security problems
- broken error handling
- unnecessary dependencies
```

This is much safer than asking AI to rewrite the entire repository.

---

# 41. Build an AI-Assisted Feature

Now let's apply the workflow.

Suppose we want:

# Resume Skill Gap Analysis

Requirement:

```text
Given a resume and a job description,
show skills that the job requests
but the resume does not contain.
```

First define the problem ourselves.

```text
Input:
resume skills
job skills

Output:
missing skills
```

Then:

```python
missing = job_skills - resume_skills
```

We may not need AI at all.

This is an important lesson:

> **Do not use AI when ordinary code solves the problem clearly.**

---

# 42. When AI Actually Helps

Suppose the problem becomes:

```text
Users write:
"Postgres"
"PostgreSQL"
"Postgres DB"
```

but our database treats them as different strings.

Now AI could help us reason about:

```text
Skill normalization
```

But even then, start simple.

Perhaps:

```python
ALIASES = {
    "postgres": "postgresql",
    "postgres db": "postgresql"
}
```

Only introduce a more sophisticated technique when the simple approach stops being useful.

---

# 43. AI Should Not Hide Complexity

A dangerous pattern is:

```text
Problem
 ↓
AI generates library
 ↓
Library hides problem
 ↓
Student never learns problem
```

Instead:

```text
Problem
 ↓
Understand fundamentals
 ↓
Use AI to accelerate implementation
```

This preserves learning.

---

# 44. A Practical AI Prompt Template

Students can use:

```text
I am building [PROJECT].

Context:
[WHAT THE APPLICATION DOES]

Current stack:
[LANGUAGES / LIBRARIES]

Current behavior:
[WHAT WORKS]

Problem:
[WHAT IS WRONG]

Relevant code:
[CODE]

Error:
[ERROR]

Constraints:
[WHAT MUST NOT CHANGE]

First explain the likely cause.

Then suggest the smallest fix.

Do not rewrite unrelated code.
```

This is a strong default template.

---

# 45. A Debugging Prompt Template

```text
I am getting this error:

[ERROR]

The error occurs here:

[CODE]

Relevant variable values/types:

[VALUES]

Explain:

1. What the error means.
2. Why it is happening.
3. How I can verify the cause.
4. The smallest fix.

Do not rewrite the entire program.
```

This encourages reasoning instead of blind copying.

---

# 46. A Code Review Prompt Template

```text
Review this code as a mentor.

Look for:

- bugs
- security issues
- poor error handling
- unnecessary complexity
- unclear naming
- maintainability problems

Do not rewrite the code yet.

First list the issues and explain why
each one matters.
```

Then fix issues one at a time.

---

# 47. A Learning Prompt Template

```text
I am learning [TOPIC].

I already understand:

[KNOWN CONCEPTS]

I do not understand:

[CONFUSION]

Explain the missing concept using
only ideas I have already learned
where possible.

Give me one small example
and one exercise.
```

This makes AI a personalized tutor rather than merely a code generator.

---

# 48. AI-Assisted Development Project

Create a small feature for the:

# AI Career Companion

Feature:

```text
Skill Gap Analyzer
```

Requirements:

```text
1. User has a stored resume.

2. User selects a job.

3. Application extracts job skills.

4. Application compares:
   resume skills
   vs
   job skills

5. Application displays:
   matched skills
   missing skills

6. Results are saved.
```

---

# 49. The AI-Assisted Workflow

### Step 1 - Design yourself

Write:

```text
Input
Output
Data needed
Database changes
Functions needed
```

### Step 2 - Ask AI for critique

```text
Here is my design.
What assumptions am I missing?
```

### Step 3 - Implement

Write the first version.

### Step 4 - Ask AI to review

```text
Review this implementation.
```

### Step 5 - Test

Create test cases.

### Step 6 - Git checkpoint

```bash
git add .
git commit -m "Add skill gap analysis"
```

### Step 7 - Iterate

Now improve it.

---

# 50. Final Challenge

Choose one feature from the Career Companion:

```text
Skill gap analysis
Resume comparison
Job categorization
Career dashboard
Resume history
```

Build it using this workflow:

```text
Design
 ↓
AI critique
 ↓
Implement
 ↓
Test
 ↓
AI code review
 ↓
Fix
 ↓
Git checkpoint
 ↓
Iterate
```

Do not ask AI to build the entire feature in one response.

---

# 51. The Developer's New Role

AI changes what developers spend time doing.

Some mechanical work becomes easier:

```text
Boilerplate
Syntax lookup
Basic refactoring
Test generation
Documentation drafts
```

But higher-level work becomes more important:

```text
Problem definition
Architecture
Requirements
Testing
Security
Tradeoffs
Debugging
Evaluation
```

This is why fundamentals remain important.

---

# 52. What You Should Be Able to Do

After this section, you should be able to:

```text
✓ Ask AI useful technical questions

✓ Provide useful context

✓ Debug with AI

✓ Review AI-generated code

✓ Verify APIs against documentation

✓ Identify hallucinated APIs

✓ Protect secrets

✓ Ask AI for tests

✓ Use AI for refactoring

✓ Use AI for documentation

✓ Keep Git checkpoints

✓ Decide when NOT to use AI

✓ Build features incrementally with AI
```

---

# 53. The Final Mental Model

The goal is not:

```text
Human
 ↓
AI
 ↓
Software
```

It is:

```text
Human
  │
  ├── Defines problem
  ├── Designs system
  ├── Evaluates solutions
  ├── Tests behavior
  └── Makes decisions
          │
          ▼
         AI
          │
  ├── Suggests
  ├── Explains
  ├── Generates
  ├── Reviews
  └── Accelerates
```

The human remains responsible for the result.

---

# 54. Phase 5 Complete

We started Phase 5 by asking:

```text
How do we turn an application
into software that can be used repeatedly?
```

We learned:

```text
SQL
 ↓
Databases
 ↓
Authentication
 ↓
Authorization
 ↓
Storage
 ↓
Persistent applications
```

Then we assembled those pieces into:

```text
AI Career Companion
```

Finally, we learned how AI can become part of our:

```text
Development Workflow
```

The complete workflow is now:

```text
IDEA
 ↓
DESIGN
 ↓
EXPERIMENT
 ↓
DEVELOP
 ↓
AI ASSISTANCE
 ↓
TEST
 ↓
REVIEW
 ↓
GIT CHECKPOINT
 ↓
ITERATE
```

That is the developer workflow we want students to carry beyond this curriculum.
