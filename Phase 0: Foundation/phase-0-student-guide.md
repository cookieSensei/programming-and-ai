# Phase 0 — Your First Developer Workflow

Welcome to your first step into software development.

In this phase, we are **not trying to learn a lot of Python syntax**.

Instead, we are going to understand something more important:

> **How does a developer turn an idea into working software?**

We will discover this by doing.

Our workflow will be:

**Experiment → Develop → Git Checkpoint → Iterate**

---

## 1. Experimenting with Jupyter Notebooks

We will start with a **Jupyter Notebook**.

A notebook lets us write small pieces of code and immediately see what happens.

A notebook is made up of **cells**. A cell can contain code, text, or other content.

For our first experiment, put this into a code cell:

```python
1 + 2
```

Run the cell.

You should see:

```text
3
```

Congratulations — you just ran your first piece of code.

### Try changing it

Change the code to:

```python
10 + 20
```

Run the cell again.

Then try:

```python
100 + 200
```

Notice what is happening:

1. We write some code.
2. We run the code.
3. The computer executes it.
4. We see the output.
5. We change the code.
6. We run it again.

This is **experimentation**.

We can quickly try an idea, observe what happens, and change our code.

### The important idea

For now, don't worry about understanding every part of Python.

The important thing is:

> **Code is a set of instructions that a computer can execute.**

And a notebook gives us a convenient place to experiment with those instructions.

---

# 2. From Notebook to Script

Notebooks are great for experimentation.

But software is often written as files that can be run again and again.

Let's create our first Python file.

Create a file called:

```text
app.py
```

Put this inside it:

```python
1 + 2
```

You have now written a **Python script**.

A script is simply a file containing code that we can run.

Our notebook allowed us to experiment with code inside a cell.

Our Python script allows us to keep our code in a file.

---

# 3. Running a Script from the Terminal

Now we are going to run `app.py` from the **terminal**.

Open your terminal and run:

```bash
python app.py
```

Python will read the code inside `app.py` and execute it.

The basic picture is:

```text
app.py
  ↓
python app.py
  ↓
Python runs the code
  ↓
output
```

## What is the terminal?

The terminal is a way of communicating with your computer by typing commands.

Instead of clicking buttons and menus, we can tell the computer what to do by entering commands.

For example:

```bash
python app.py
```

means:

> "Python, run the code inside `app.py`."

You don't need to memorize lots of terminal commands right now.

The important thing is to understand the relationship between:

- **Code** — the instructions we write
- **File** — where we keep our code
- **Terminal** — where we can give commands to the computer
- **Python** — the program that executes our Python code

---

# 4. Change Your Program

Now let's make a change.

Change `app.py` to:

```python
10 + 20
```

Run it again:

```bash
python app.py
```

Now change it again:

```python
100 + 200
```

Run it again.

We are doing something very normal in software development:

> **We change the code, run it, observe what happens, and change it again.**

This is development.

We don't write perfect software in one attempt.

We experiment, make changes, test our ideas, and improve the program.

---

# 5. What Happens When We Make Lots of Changes?

Imagine that we have been working on a project for several hours.

We make changes:

```text
Version 1
   ↓
Change something
   ↓
Version 2
   ↓
Change something
   ↓
Version 3
   ↓
Change something
   ↓
Version 4
```

Now imagine that Version 4 doesn't work.

We might want to know:

- What did we change?
- What did the code look like before?
- Which change caused the problem?
- Can we go back to an earlier version?

This is one of the problems that **Git** helps us solve.

---

# 6. Git — Checkpoints for Your Code

Git is a tool for tracking changes to files.

One useful way to think about Git is:

> **Git lets us create checkpoints for our project.**

Imagine playing a video game.

You play for an hour and reach a difficult level.

Before trying something risky, you save the game.

If things go badly, you can return to that save point.

Git gives us a similar idea for our code.

We make some changes, then create a **commit**.

A commit is a checkpoint that records the state of our project at that point in time.

For now, you don't need to learn everything Git can do.

We only need to understand the basic idea:

```text
Make changes
     ↓
Create a Git checkpoint
     ↓
Make more changes
     ↓
Create another checkpoint
```

---

# 7. The Developer Workflow

We have now seen several different tools and ideas.

Let's put them together.

```text
             EXPERIMENT
                  ↓
             Write some code
                  ↓
             See what happens
                  ↓
              DEVELOP
                  ↓
             Change the code
                  ↓
             Run and test it
                  ↓
           GIT CHECKPOINT
                  ↓
             Save our progress
                  ↓
               ITERATE
                  ↓
        Make the next experiment
                  ↓
                  ↺
```

This cycle is at the heart of software development.

We don't simply:

> "Write the code once and finish."

Instead, we repeatedly:

> **Experiment → Develop → Checkpoint → Iterate**

---

# 8. Your Mental Model

By the end of this phase, you should be able to explain these ideas in your own words.

### Jupyter Notebook

A place where we can experiment with code interactively.

### Code

Instructions that a computer can execute.

### Script

A file containing code that can be run.

### Terminal

A way to communicate with the computer using commands.

### Python

The program that executes Python code.

### Git

A tool that tracks changes to our project and lets us create checkpoints.

### Commit

A saved checkpoint of our project.

---

# 9. Your First Challenge

Now try the workflow yourself.

## Step 1 — Experiment

In a Jupyter Notebook, experiment with simple expressions:

```python
1 + 2
```

Try changing the numbers.

Try multiplication:

```python
5 * 10
```

Try division:

```python
100 / 4
```

Don't worry about memorizing syntax.

Just observe what happens.

---

## Step 2 — Create a Script

Create:

```text
app.py
```

Put some of your experiments into the file.

For example:

```python
5 * 10
```

---

## Step 3 — Run It

Run:

```bash
python app.py
```

Change the code and run it again.

---

## Step 4 — Make a Git Checkpoint

Once you have a version you want to keep, create a Git commit.

Think of the commit as:

> **"This is a version of my project that I want to remember."**

---

## Step 5 — Iterate

Make another change.

Run the program.

Observe the result.

Then create another checkpoint.

---

# The Big Idea

You have just encountered a tiny version of a real developer workflow.

```text
Experiment
    ↓
Develop
    ↓
Test
    ↓
Git Checkpoint
    ↓
Iterate
    ↓
Experiment again
```

The tools will become more powerful as we progress.

The projects will become more complicated.

The code will become much longer.

But this basic loop will keep appearing:

> **Try something. Build something. Check your work. Save your progress. Try again.**

That's what we're going to learn to do throughout CookieSensei.
