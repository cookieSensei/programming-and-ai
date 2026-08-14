# Tutorial 15 - How to Use ChatGPT to Build Django Apps

## Why this tutorial exists

AI-assisted programming is part of this program.

You are encouraged to use ChatGPT to help create your MWP.

The objective is not:

> Write every line manually.

The objective is:

> Understand enough to direct AI, evaluate its output, test it, and debug it.

## 1. The bad pattern

```text
Idea
 ↓
"Build my entire website."
 ↓
Copy thousands of lines
 ↓
Something breaks
 ↓
"I don't understand anything."
```

## 2. A better pattern

```text
Business idea
 ↓
Small feature
 ↓
Ask AI
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

## 3. Start with a bounded request

Weak:

> Build me a Django booking website.

Better:

> I have a Django project with a Booking model containing name, email, and date. I want a page where users can submit a booking. Explain which files need to change and why. Keep the implementation beginner-friendly.

The second request has boundaries.

## 4. Ask for a plan first

Before generating code:

> Give me a simple implementation plan for this feature. List the files that need to change and explain the purpose of each change. Do not write code yet.

This helps you understand the architecture before accepting implementation.

## 5. Ask for one change at a time

Good:

> Add a navigation link to the existing base template.

Good:

> Add a phone number field to my Booking model.

Good:

> Add search to the Django Admin booking list.

Avoid making ten unrelated changes in one prompt.

## 6. Give AI your existing code

Instead of:

> Create a view.

provide:

```text
Here is my current views.py.

I want to add a confirmation page.

Modify only what is necessary and explain the changes.
```

This reduces accidental restructuring.

## 7. Ask "why?"

When you see unfamiliar code:

> Why is this needed?

Useful questions:

```text
Why do I need csrf_token?
Why do I need makemigrations?
Why is request passed to the view?
Why is this model registered in admin.py?
Why does this template extend base.html?
Why is this package necessary?
```

The "why" questions build understanding.

## 8. Ask AI to preserve your structure

Useful instructions:

> Do not create a new app unless necessary.

> Do not change unrelated files.

> Keep my current folder structure.

> Modify only `views.py` and the relevant template.

This makes AI-generated changes easier to inspect.

## 9. Give exact errors

Bad:

> Django doesn't work.

Better:

```text
I submitted the booking form.

Expected:
Booking confirmation.

Actual:
500 error.

Error:
[paste exact traceback]

views.py:
[paste relevant code]
```

Then:

> Explain the root cause before giving me the smallest fix.

## 10. Ask for alternatives

If AI suggests a complicated approach:

> Give me a simpler approach suitable for a beginner building an MWP, and explain the trade-offs.

You are learning to make technical decisions.

## 11. Do not blindly trust generated code

AI can produce:

- incorrect code
- unnecessary dependencies
- outdated approaches
- insecure patterns
- changes that conflict with your project

Always test.

## 12. Important things you should understand

You do not need to understand every line.

But you should understand:

```text
What does the application do?
Where is data stored?
How does a user interact with it?
Where is the important business logic?
Which model stores information?
How do I run it?
How do I debug it?
```

## 13. Never paste secrets

Do not give AI:

```text
API keys
passwords
private keys
access tokens
database passwords
```

Use:

```text
YOUR_API_KEY
YOUR_PASSWORD
YOUR_SECRET
```

instead.

## 14. A reusable prompt

```text
I am building:
[project]

My goal:
[one feature]

Current project:
[structure/code]

Expected behavior:
[what should happen]

Actual behavior:
[what happens]

Error:
[exact error]

Please:
1. Explain the problem.
2. Identify the responsible file.
3. Give the smallest fix.
4. Explain the changed code.
5. Tell me how to test it.
```

## 15. AI as pair programmer

Think of the workflow as:

```text
You
 ↓
decide what to build

AI
 ↓
helps implement

You
 ↓
test

AI
 ↓
helps debug

You
 ↓
decide what to improve
```

You remain responsible for the product.

## 16. Exercise

Take a Phase 4 project and ask ChatGPT to add one small feature.

Before accepting the answer:

1. Ask which files change.
2. Ask why.
3. Implement it.
4. Test it.
5. Explain the result in your own words.

## Remember

AI-assisted development does not mean:

> I do not need to understand anything.

It means:

> I can build faster because AI helps me write and explain code.

Your target is enough understanding to remain in control.
