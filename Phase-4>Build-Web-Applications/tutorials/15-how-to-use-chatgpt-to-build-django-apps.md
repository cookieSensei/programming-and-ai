# Tutorial 15 — How to Use ChatGPT to Build Django Apps

## Why This Matters

Students are encouraged to use AI; this tutorial teaches them to remain the builder.

## Bad Pattern

```text
“Build my entire website.”
        ↓
Copy everything
        ↓
Something breaks
        ↓
“I don't understand Django.”
```

## Better Pattern

```text
Idea
 ↓
Small problem
 ↓
Ask ChatGPT
 ↓
Understand
 ↓
Implement
 ↓
Test
 ↓
Debug
 ↓
Improve
```

## Give Context

Include:

```text
What I am building
What I already have
What I want to change
What went wrong
```

Ask for one change at a time.

## Ask for Understanding

Useful prompts:

```text
Explain this code.
Why is this migration necessary?
Which file handles this request?
Where does this data reach the database?
What is the smallest fix?
```

## Verify AI Code

Before accepting code, ask:

1. What files change?
2. Does it add a package?
3. Does it change the database?
4. Does it require environment variables?
5. Does it introduce security concerns?

## Principle

> **Use AI to increase your building ability, not to replace your understanding.**
