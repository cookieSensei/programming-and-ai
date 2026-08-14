# Tutorial 06 - Build Your Minimum Working Product

## Phase 5 - Make Applications Real

## Final Phase 5 Project

### The big idea

This is the point where the separate technical pieces become one product.

You started with an idea.

You built an early application.

You learned databases.

You learned SQL.

You added users where appropriate.

You prepared the application for production.

You deployed it.

Now you need to answer:

> **Can another person actually experience the core value of this idea?**

The official Phase 5 project defines a Minimum Working Product as the simplest working version of an idea that allows another person to experience its core value. It explicitly says that it is not a perfect startup, complete product, production-scale system, or finished business. fileciteturn14file0L9-L35

---

# 1. Do not start from scratch

Return to your Phase 4 application.

The intended progression is:

```text
Phase 4 application
       ↓
Database
       ↓
Users, if needed
       ↓
Persistent data
       ↓
Production configuration
       ↓
Deployment
       ↓
Real user
```

The Phase 5 project explicitly asks you to take the small application from Phase 4 and move it toward something another person can actually try. fileciteturn14file0L37-L65

---

# 2. What is an MWP?

MWP means:

> **Minimum Working Product**

Break the phrase apart.

### Minimum

Only the smallest necessary scope.

### Working

The core experience actually functions.

### Product

Another person can use it to experience some meaningful value.

---

# 3. What an MWP is not

It is not:

```text
Perfect UI
Complete startup
Huge feature set
Enterprise architecture
Mobile app
AI everywhere
Payment integration
Advanced analytics
```

You can build those later.

The first goal is to test whether the core idea works.

---

# 4. Why "minimum" is difficult

Builders naturally add features.

Suppose your idea is:

> People can book a consultation online.

The core product might only need:

```text
Customer
 ↓
Choose service
 ↓
Submit booking
 ↓
Booking stored
 ↓
Confirmation
```

You might be tempted to add:

```text
Payments
Coupons
Calendar synchronization
SMS
Email automation
AI assistant
Analytics
Reviews
Referral system
Mobile app
```

Those may eventually be valuable.

But they are not necessarily required to test the core idea.

---

# 5. Define the core user journey

Write this:

```text
User
 ↓
Action
 ↓
Application
 ↓
Result
```

For example:

```text
Customer
 ↓
Books a consultation
 ↓
Application stores booking
 ↓
Customer sees confirmation
```

The official Phase 5 project treats this core journey as the center of the MWP and says everything outside it is secondary. fileciteturn14file0L67-L93

---

# 6. Your one-sentence product test

Complete:

> A ______ can use my application to ______ and receive ______.

Examples:

> A customer can use my application to book a consultation and receive a confirmation.

> A small business owner can upload an invoice and receive extracted text.

> A student can enter an assignment and receive a structured study plan.

> A local buyer can browse available products and submit an inquiry.

If you cannot write this sentence clearly, the product scope is probably still unclear.

---

# 7. Must Have vs Later

Create two lists.

## Must Have

Features required for the core value.

## Later

Features that would improve the product but are not necessary for the first real test.

For example:

```text
MUST HAVE

□ Landing page
□ Service list
□ Booking form
□ Save booking
□ Confirmation
□ Public URL
```

Later:

```text
□ Payments
□ Notifications
□ Analytics
□ Admin dashboard
□ Mobile application
□ Recommendations
```

The official project uses this exact Must Have/Later distinction as a scope-control exercise. fileciteturn14file0L95-L124

---

# 8. Build the smallest complete flow

An MWP should be complete around its core action.

A bad MVP can contain:

```text
Beautiful homepage
+
half-finished form
+
unfinished database
```

A better MWP might be visually simple but complete:

```text
User arrives
 ↓
Understands purpose
 ↓
Performs core action
 ↓
Application processes it
 ↓
Data is stored if needed
 ↓
User gets useful result
```

Completion is more important than feature count.

---

# 9. Use the Phase 5 pieces selectively

You do not have to use every Phase 5 feature in every product.

### Database

Use it if the application needs persistent information.

### Users

Use them if the application needs accounts, private data, or user-specific workflows.

### SQL

Use it for understanding and inspecting your data.

### Production configuration

Use it before public deployment.

### Deployment

Use it if another person needs to test the product.

This is why the project says to use previous Phase 5 projects to add the pieces your product actually needs. fileciteturn14file0L44-L65

---

# 10. Does your MWP need AI?

Ask:

> **Does AI create meaningful value in my product?**

If yes, use it.

If no, do not force it.

This is explicitly part of the Phase 5 final project. fileciteturn14file0L126-L148

Examples where AI might create meaningful value:

```text
User feedback
 ↓
Sentiment analysis
```

```text
Long text
 ↓
AI summary
```

```text
Description
 ↓
Suggested category
```

But a normal booking form does not become better merely because an AI chatbot is placed beside it.

---

# 11. Product before technology

Ask:

```text
What problem?
Who has it?
What action do they need?
What result matters?
```

Only then ask:

```text
What technology should I use?
```

Avoid:

> I learned feature X, so I need to put feature X into my product.

Instead:

> My user needs Y. Does feature X help achieve Y?

---

# 12. User testing

Find at least one person who did not build the application.

Give them the public URL.

Do not immediately explain the interface.

Observe.

Ask:

1. What do you think this application does?
2. What would you expect to happen next?
3. What was confusing?
4. Did you complete the main task?
5. What would you change?

These questions are directly aligned with the final project's user-testing exercise. fileciteturn14file0L150-L167

---

# 13. Watch instead of explaining

Suppose the user asks:

> Where do I click?

Your instinct may be to tell them.

Instead, record:

```text
User could not find the action.
```

That is product feedback.

You want to discover:

```text
What users naturally understand
```

not:

```text
What users understand after the founder explains it.
```

---

# 14. Prioritize feedback

Do not treat every comment equally.

Classify feedback.

### Critical

The user cannot complete the core task.

### Important

The user can complete it but becomes confused.

### Nice to have

The user suggests an enhancement.

Example:

```text
"I couldn't submit the form."
→ Critical

"I wasn't sure what this field meant."
→ Important

"Could you add dark mode?"
→ Nice to have
```

Fix the core problems first.

---

# 15. The MWP build loop

Use this cycle:

```text
Define core journey
       ↓
Build smallest version
       ↓
Test yourself
       ↓
Deploy
       ↓
Give to real user
       ↓
Observe
       ↓
Fix biggest problem
       ↓
Test again
```

This is product development.

---

# 16. Do not endlessly polish

A common trap:

```text
Build
 ↓
Polish
 ↓
Polish
 ↓
Polish
 ↓
Never show anyone
```

A better loop:

```text
Build enough
 ↓
Show someone
 ↓
Learn
 ↓
Improve
```

Real user behavior is more informative than your imagination.

---

# 17. Technical completion checklist

Your MWP should be checked from multiple layers.

## Product

```text
□ Clear purpose
□ Defined user
□ Core journey written
```

## Application

```text
□ Main page works
□ Core action works
□ Result is useful
□ Errors are handled reasonably
```

## Data

```text
□ Required data is stored
□ Data can be retrieved
□ User ownership works if required
```

## Authentication

```text
□ Login works if needed
□ Logout works if needed
□ Private data is protected if needed
```

## Production

```text
□ Secrets are protected
□ Production configuration is set
□ Dependencies are listed
```

## Deployment

```text
□ Public URL works
□ Another person can access it
□ Core flow works remotely
```

---

# 18. The final demonstration

Prepare a short demonstration.

The official project suggests covering:

### The Problem

What problem are you solving?

### The User

Who is it for?

### The Product

What does the application do?

### The Core Flow

What can the user actually do?

### The Technology

What did you use?

### AI Decision

Did you use AI?

If yes:

> Why?

If no:

> Why not?

### What You Learned

What could you build next?

These are the final project's demonstration categories. fileciteturn14file0L169-L201

---

# 19. Five-minute demonstration structure

Use:

```text
0:00–0:45
Problem + user

0:45–1:15
What the product does

1:15–3:30
Live core user journey

3:30–4:15
Technology + architecture

4:15–4:45
AI decision

4:45–5:00
What comes next
```

Do not spend the entire demonstration talking about code.

Show the product.

---

# 20. Architecture explanation

Be able to draw your system:

```text
User
 ↓
Browser
 ↓
Django
 ↓
Authentication
 ↓
Business logic
 ↓
Database
 ↓
Response
```

If AI is involved:

```text
User
 ↓
Django
 ↓
AI service
 ↓
Structured result
 ↓
Database
 ↓
User
```

You do not need to explain every implementation detail.

Explain the role of each component.

---

# 21. AI-assisted building workflow

Use ChatGPT strategically.

### Step 1 - Explain the goal

> I am building an MWP for [user] who needs to [problem]. The core flow is [flow].

### Step 2 - Ask for architecture

> Identify the minimum files/components required.

### Step 3 - Implement one feature

> Add the smallest implementation for [feature].

### Step 4 - Test

> Here is what happened.

### Step 5 - Debug

> Explain the root cause before proposing the fix.

### Step 6 - Review

> Check whether this change introduces security, data ownership, or deployment issues.

---

# 22. Do not outsource product decisions

AI can suggest:

```text
database schema
UI
code
validation
architecture
tests
```

But you decide:

```text
Who is the user?
What problem matters?
What is the core value?
What should be excluded?
What trade-offs are acceptable?
```

AI is an implementation assistant.

You are the product builder.

---

# 23. Scope-control exercise

Write:

```text
My idea:
________________________

Target user:
________________________

Core problem:
________________________

Core action:
________________________

Useful result:
________________________
```

Then:

```text
MUST HAVE

1.
2.
3.
4.

LATER

1.
2.
3.
4.
```

If your Must Have list contains 20 items, reduce it.

Ask:

> What is the smallest version that still demonstrates the idea?

---

# 24. Final success criteria

The official Phase 5 project expects the MWP to have:

```text
□ Clear purpose
□ Defined user
□ Working core flow
□ Required information stored
□ User handling if accounts are required
□ Public URL
□ Another person able to try it
```

It does not need to be perfect. fileciteturn14file0L203-L215

---

# 25. Final reflection

Answer these questions honestly:

### Product

> What problem did I attempt to solve?

### User

> Who is the product for?

### Technical

> What did I build?

### Data

> What does the application remember?

### Security

> What should users be allowed to access?

### Deployment

> Can another person use it?

### AI

> Did AI create meaningful value?

### Learning

> What part was hardest?

### Next step

> What would I build next if I had another week?

---

# 26. The deeper outcome

The final goal of the program is not mastery of Django.

It is not mastery of SQL.

It is not mastery of deployment.

It is not mastery of AI.

The deeper outcome is builder confidence.

The official curriculum expresses this as the ability to look at an idea and think:

> **"I may not know how to build everything yet, but I know enough to start."** fileciteturn14file0L217-L229

That is exactly what Phase 5 should produce.

---

# Remember

The MWP is:

```text
Idea
 ↓
User
 ↓
Core problem
 ↓
Smallest useful flow
 ↓
Working application
 ↓
Persistent data
 ↓
Production configuration
 ↓
Public URL
 ↓
Real person
 ↓
Feedback
```

The objective is not to prove that you can build everything.

The objective is to prove that you can build **enough to learn from reality**.
