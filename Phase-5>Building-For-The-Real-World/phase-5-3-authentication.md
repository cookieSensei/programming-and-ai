# 3. Authentication

## Teaching Our Application Who Its Users Are

We now have:

```text
Python
   ↓
Supabase
   ↓
PostgreSQL
```

Our application can store data.

But we have a new problem.

Imagine:

```text
Alice
```

uploads:

```text
alice_resume.pdf
```

and:

```text
Bob
```

uploads:

```text
bob_resume.pdf
```

How does the application know which resume belongs to whom?

We need:

# Authentication

Supabase Auth provides authentication and authorization features, including email/password, magic links, OTP, social login, and SSO. For this introductory project, we will start with the simplest model: **email + password**. citeturn0search3turn1search2

---

# 1. Authentication vs Authorization

These two words are often confused.

### Authentication

Authentication asks:

> **Who are you?**

For example:

```text
Alice logs in
       ↓
Application verifies Alice
       ↓
Alice is authenticated
```

### Authorization

Authorization asks:

> **What are you allowed to access?**

For example:

```text
Alice
 ↓
Can access Alice's resumes

Bob
 ↓
Can access Bob's resumes
```

A useful mental model is:

```text
Authentication
     ↓
Who are you?

Authorization
     ↓
What can you access?
```

We will learn both in this section.

---

# 2. Why We Need Authentication

Without authentication, our application might look like:

```text
User
 ↓
Upload resume
 ↓
Store resume
```

But the database does not know which human uploaded it.

With authentication:

```text
User
 ↓
Login
 ↓
Authenticated identity
 ↓
Upload resume
 ↓
Store resume
 ↓
Associate with user
```

Now the application can remember ownership.

---

# 3. User Identity

Supabase Auth creates a user identity.

Conceptually:

```text
Alice
 ↓
User ID
```

and:

```text
Bob
 ↓
Different User ID
```

The ID is what our database should use to associate records with a user.

We should not rely on:

```text
name
email
```

as the database relationship.

Instead:

```text
auth user ID
```

becomes the stable identity used by application data.

---

# 4. Authentication Flow

A simplified flow is:

```text
User
 ↓
Sign Up
 ↓
Supabase Auth
 ↓
User Account
 ↓
Sign In
 ↓
Session / Access Token
 ↓
Authenticated Requests
```

Supabase Auth uses JWT-based authentication, and its SDKs send the user's auth token with database requests so that Row Level Security can make row-by-row authorization decisions. citeturn0search3

We do not need to understand every JWT field yet.

We only need the basic idea:

```text
Login
 ↓
Proof of identity
 ↓
Authenticated request
```

---

# 5. Enable Email Authentication

For our first application, use:

```text
Email
+
Password
```

Supabase supports email/password authentication through its Auth system. citeturn0search3

Before writing code, inspect the Auth settings in your Supabase project.

Pay attention to:

```text
Email provider
Confirm email
Site URL
Redirect URLs
```

The exact settings can affect what happens immediately after sign-up.

---

# 6. Sign Up

The Supabase Python client provides:

```python
supabase.auth.sign_up()
```

A basic example is:

```python
response = supabase.auth.sign_up({
    "email": "alice@example.com",
    "password": "strong-password"
})
```

This is the current Python API documented by Supabase. citeturn1search2

---

# 7. Email Confirmation

There is an important detail.

Depending on your project's configuration, a new user may need to confirm their email before logging in.

With email confirmation enabled:

```text
Sign Up
   ↓
User created
   ↓
Confirmation email
   ↓
User confirms
   ↓
Can sign in
```

With confirmation disabled for a development experiment:

```text
Sign Up
   ↓
User created
   ↓
Can sign in
```

Supabase documents that when email confirmation is enabled, the sign-up response can contain a user while the session is null; when confirmation is disabled, both user and session can be returned. citeturn1search2

This is useful to understand because students may see different results depending on their project settings.

---

# 8. Do Not Store Passwords Yourself

This is a major real-world lesson.

Do **not** create a table like:

```text
users
---------------------
email
password
```

and store passwords yourself.

Authentication is a security-sensitive problem.

We are using a dedicated authentication system:

```text
Our application
      ↓
Supabase Auth
      ↓
User identity
```

Our application does not need to implement password storage itself.

---

# 9. Sign In

Once a user has an account, they can sign in.

The current Supabase Python API provides:

```python
supabase.auth.sign_in_with_password()
```

For email/password:

```python
response = supabase.auth.sign_in_with_password({
    "email": "alice@example.com",
    "password": "strong-password"
})
```

citeturn1search0

---

# 10. What Does Sign In Return?

A successful authentication flow gives the application access to a session.

Conceptually:

```text
Email
+
Password
      ↓
Supabase Auth
      ↓
Session
      ↓
Authenticated user
```

The session contains authentication information including a JWT.

For our course, think of the session as:

> **The application's current authenticated state.**

---

# 11. Session vs User

These are related but different concepts.

### User

Represents:

```text
Who is this person?
```

### Session

Represents:

```text
The current authenticated interaction.
```

Conceptually:

```text
User
 ↓
has a session
 ↓
session contains authentication information
```

Supabase's Python client exposes both session retrieval and user retrieval. citeturn1search6turn1search1

---

# 12. Get the Current Session

The Python client provides:

```python
response = supabase.auth.get_session()
```

This retrieves the current local session. citeturn1search6

It is useful for understanding whether the client currently has session information.

But there is an important security distinction.

---

# 13. Get the Current User

Supabase also provides:

```python
response = supabase.auth.get_user()
```

The documented `get_user()` call fetches the user using the current session's access token and validates that token against the Auth server. citeturn1search1

Conceptually:

```text
Session
   ↓
Access token
   ↓
Supabase Auth
   ↓
Verified user
```

This is the method to understand when you need trustworthy user identity.

---

# 14. Find the User ID

Suppose:

```python
response = supabase.auth.get_user()

user = response.user
```

The user object contains an ID.

Conceptually:

```python
user.id
```

That ID is what we will eventually use in our database.

For example:

```text
Alice
 ↓
auth.users
 ↓
UUID
 ↓
resumes.user_id
```

---

# 15. Our Database Needs to Know the User

Previously, we imagined:

```text
resumes

id
user_id
filename
extracted_text
```

Now:

```text
user_id
```

can refer to the authenticated user's ID.

The relationship becomes:

```text
Supabase Auth User
        │
        │ user ID
        ▼
    resumes.user_id
```

---

# 16. A Better Resume Table

For our application, a PostgreSQL table can use the Auth user's ID:

```sql
CREATE TABLE public.resumes (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    filename TEXT NOT NULL,
    extracted_text TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

Now the database understands:

```text
This resume belongs to this Auth user.
```

Supabase's documentation recommends referencing the managed `auth.users` table carefully and using `ON DELETE CASCADE` when appropriate for user-owned data. citeturn0search5

---

# 17. Why UUID?

Supabase Auth user IDs are UUIDs.

So instead of:

```sql
user_id INTEGER
```

we use:

```sql
user_id UUID
```

The important lesson is:

> **The type of a foreign key should match the type of the key it references.**

---

# 18. Authentication Is Not Enough

We have now connected:

```text
User
 ↓
Auth
 ↓
User ID
 ↓
Resume
```

But there is still a security problem.

Suppose Alice sends:

```text
SELECT *
FROM resumes;
```

Why should she be allowed to see Bob's rows?

Authentication tells us:

```text
This is Alice.
```

It does not automatically mean:

```text
Alice can access everything.
```

That is authorization.

---

# 19. Row Level Security

Supabase uses PostgreSQL Row Level Security, commonly called:

```text
RLS
```

RLS allows us to create policies controlling which rows a user can access. Supabase recommends enabling RLS for exposed tables, and policies can use `auth.uid()` to compare the authenticated user's ID with a row's `user_id`. citeturn0search1

Think of an RLS policy as:

```text
An invisible WHERE clause
```

that the database applies to queries.

---

# 20. Enable RLS

For our resume table:

```sql
ALTER TABLE public.resumes
ENABLE ROW LEVEL SECURITY;
```

Now we can create policies.

---

# 21. SELECT Policy

We want:

```text
Users can read their own resumes.
```

A simple policy is:

```sql
CREATE POLICY "Users can view their own resumes"
ON public.resumes
FOR SELECT
TO authenticated
USING (
    (SELECT auth.uid()) = user_id
);
```

The important part is:

```sql
auth.uid() = user_id
```

That means:

```text
Current authenticated user
        =
Row owner
```

Supabase documents this pattern for RLS policies. citeturn0search1

---

# 22. INSERT Policy

Now we need to control who can create rows.

We want:

```text
Alice can only create a resume
whose user_id is Alice's ID.
```

A policy can use `WITH CHECK`:

```sql
CREATE POLICY "Users can create their own resumes"
ON public.resumes
FOR INSERT
TO authenticated
WITH CHECK (
    (SELECT auth.uid()) = user_id
);
```

Supabase documents `WITH CHECK` as the mechanism for validating newly inserted rows against a policy. citeturn0search1

---

# 23. UPDATE Policy

For updates, we want to make sure:

```text
The existing row belongs to the user.
```

and:

```text
The updated row still belongs to the user.
```

For example:

```sql
CREATE POLICY "Users can update their own resumes"
ON public.resumes
FOR UPDATE
TO authenticated
USING (
    (SELECT auth.uid()) = user_id
)
WITH CHECK (
    (SELECT auth.uid()) = user_id
);
```

Supabase recommends using both `USING` and `WITH CHECK` for this kind of update policy. citeturn0search1

---

# 24. DELETE Policy

Finally:

```text
Users can delete their own resumes.
```

```sql
CREATE POLICY "Users can delete their own resumes"
ON public.resumes
FOR DELETE
TO authenticated
USING (
    (SELECT auth.uid()) = user_id
);
```

Now the database itself enforces ownership. citeturn0search1

---

# 25. The Complete Security Model

Our application now looks like:

```text
                    USER
                      │
                      ▼
                 LOGIN / SIGNUP
                      │
                      ▼
                 SUPABASE AUTH
                      │
                      ▼
                   USER ID
                      │
                      ▼
              DATABASE REQUEST
                      │
                      ▼
                    RLS
                      │
              ┌───────┴───────┐
              ▼               ▼
        Own row?          Other row?
              │               │
             YES              NO
              │               │
              ▼               ▼
            Allow            Deny
```

This is a major real-world concept.

---

# 26. Why RLS Is So Important

Imagine our application contains:

```text
Alice's resume
Bob's resume
Carol's resume
```

We should not rely entirely on Python code like:

```python
if resume["user_id"] == current_user.id:
    ...
```

The database can enforce the rule too.

That gives us another layer of protection.

Supabase describes RLS as a PostgreSQL authorization mechanism that can protect data row by row and integrate directly with Supabase Auth. citeturn0search1turn0search2

---

# 27. A Very Important Mental Model

Think of:

```sql
USING (
    (SELECT auth.uid()) = user_id
)
```

as approximately:

```sql
WHERE user_id = CURRENT_USER_ID
```

except that `auth.uid()` gives us the authenticated Supabase user's ID.

This makes RLS much easier to understand.

---

# 28. Anonymous vs Authenticated

Supabase distinguishes between requests made with:

```text
anon
```

and:

```text
authenticated
```

The `authenticated` role represents a logged-in user. The RLS policy can explicitly target that role with:

```sql
TO authenticated
```

Supabase recommends specifying roles in policies. citeturn0search1

For this project, our user-owned data will be accessible only to authenticated users.

---

# 29. What Happens If Nobody Is Logged In?

Supabase documents that:

```text
auth.uid()
```

returns:

```text
null
```

when there is no authenticated user.

Therefore:

```sql
auth.uid() = user_id
```

does not match a normal UUID for an unauthenticated request.

This is one reason the `TO authenticated` policy target is useful. citeturn0search1

---

# 30. Streamlit Authentication UI

Now we can create a simple Streamlit application with two modes:

```text
[ Sign Up ]
[ Login ]
```

After login:

```text
Welcome, Alice

[ Upload Resume ]
[ View Resumes ]
[ Logout ]
```

The UI changes depending on whether a user is authenticated.

---

# 31. Simple Sign-Up Form

A conceptual Streamlit form:

```python
email = st.text_input("Email")
password = st.text_input(
    "Password",
    type="password"
)

if st.button("Sign Up"):
    response = supabase.auth.sign_up({
        "email": email,
        "password": password
    })

    st.success(
        "Check your email if confirmation is required."
    )
```

The exact user experience depends on your Supabase Auth settings. citeturn1search2

---

# 32. Simple Login Form

```python
email = st.text_input("Email")
password = st.text_input(
    "Password",
    type="password"
)

if st.button("Login"):
    response = (
        supabase
        .auth
        .sign_in_with_password({
            "email": email,
            "password": password
        })
    )

    st.success("Logged in!")
```

The current Python API for password login is `sign_in_with_password()`. citeturn1search0

---

# 33. Get the Logged-In User

After login:

```python
response = supabase.auth.get_user()

user = response.user

if user:
    st.write(
        f"Logged in as {user.email}"
    )
```

The important information for our database is:

```python
user.id
```

That is the ownership ID.

---

# 34. Insert User-Owned Data

Suppose we extracted a resume.

We can store:

```python
user = supabase.auth.get_user().user

supabase.table("resumes").insert({
    "user_id": user.id,
    "filename": "resume.pdf",
    "extracted_text": extracted_text
}).execute()
```

The application explicitly associates the row with the current user.

The RLS policy then independently checks that:

```text
user.id == resumes.user_id
```

---

# 35. Read User-Owned Data

We can query:

```python
user = supabase.auth.get_user().user

response = (
    supabase
    .table("resumes")
    .select("*")
    .eq("user_id", user.id)
    .execute()
)
```

The `.eq()` filter is useful because it tells the database which user's rows we are asking for.

RLS still protects the table.

This gives us:

```text
Application filter
+
Database authorization
```

---

# 36. Why Use Both?

We might ask:

> If RLS already knows the user's ID, why filter by `user_id` in Python?

Because the filter tells PostgreSQL which rows the application wants.

RLS enforces which rows the user is allowed to access.

Think:

```text
Application filter
      ↓
"What do I want?"

RLS
      ↓
"What am I allowed to have?"
```

These are different questions.

Supabase's RLS performance guidance also recommends adding filters to queries rather than relying only on policies. citeturn0search1

---

# 37. Sign Out

The Python client provides:

```python
supabase.auth.sign_out()
```

For example:

```python
if st.button("Logout"):
    supabase.auth.sign_out()
    st.rerun()
```

The current Supabase documentation provides `sign_out()` for ending the authenticated session. citeturn1search4

---

# 38. What Does Logout Do?

Conceptually:

```text
User
 ↓
Logout
 ↓
Session removed / revoked appropriately
 ↓
Application no longer treats user as signed in
```

Supabase notes that the access-token JWT can remain valid until it expires even after logout, while the refresh token is revoked and removed from the client. citeturn1search4

For this introductory course, the key idea is simply:

> Logging out ends the application's active authenticated session.

---

# 39. Profile Data

Supabase Auth manages authentication users.

But our application may need additional profile information:

```text
first name
last name
bio
job title
```

We should not try to expose or manipulate the internal Auth schema directly from the application.

Instead, create our own table:

```text
profiles
```

linked to:

```text
auth.users
```

Supabase recommends creating application-owned user tables in the `public` schema when additional user information is needed. citeturn0search5

---

# 40. Example Profiles Table

```sql
CREATE TABLE public.profiles (
    id UUID PRIMARY KEY
        REFERENCES auth.users(id)
        ON DELETE CASCADE,

    first_name TEXT,
    last_name TEXT,
    job_title TEXT
);
```

Now:

```text
auth.users
    │
    │ id
    ▼
profiles
```

The Auth system owns authentication information.

Our application owns profile information.

---

# 41. Authentication vs Application Data

This distinction is important.

### Supabase Auth

Handles:

```text
Identity
Email
Password
Sessions
Authentication
```

### Our `profiles` table

Handles:

```text
First name
Last name
Job title
Preferences
```

### Our `resumes` table

Handles:

```text
Resume metadata
Extracted text
Ownership
```

This separation keeps responsibilities clear.

---

# 42. Mini Project — User Notes

Before connecting authentication to resumes, build:

# User Notes

The application should allow a user to:

```text
Sign up
Login
Create notes
View their notes
Update notes
Delete notes
Logout
```

The database should contain:

```text
profiles
notes
```

and each note should have:

```text
user_id
```

---

# 43. User Notes Architecture

```text
                    USER
                      │
                      ▼
                  AUTHENTICATE
                      │
                      ▼
                   USER ID
                      │
                      ▼
                    NOTES
                      │
                      ▼
                     RLS
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
      User's notes            Other notes
          │                       │
        ALLOW                    DENY
```

This is a small application, but it contains a real authorization system.

---

# 44. Suggested Database

```sql
CREATE TABLE public.notes (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    content TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

Enable RLS:

```sql
ALTER TABLE public.notes
ENABLE ROW LEVEL SECURITY;
```

Then create policies for:

```text
SELECT
INSERT
UPDATE
DELETE
```

using:

```sql
(SELECT auth.uid()) = user_id
```

---

# 45. Test Authorization

Create two accounts:

```text
Alice
Bob
```

Alice creates:

```text
Alice's note
```

Bob creates:

```text
Bob's note
```

Now test:

```text
Alice → sees Alice's note
Alice → cannot see Bob's note

Bob → sees Bob's note
Bob → cannot see Alice's note
```

This is one of the most important experiments in the entire section.

You have now demonstrated:

```text
Authentication
+
Authorization
+
Database
```

working together.

---

# 46. Common Mistakes

### Mistake 1 — Treating authentication as authorization

Being logged in does not mean:

```text
access to every row
```

You need authorization rules.

---

### Mistake 2 — Storing passwords yourself

Do not build your own password system for this project.

Use the Auth provider.

---

### Mistake 3 — Not enabling RLS

If an exposed table contains user-specific data, RLS needs to be part of the design. Supabase specifically recommends enabling RLS on exposed tables. citeturn0search1

---

### Mistake 4 — Using names as ownership

Do not use:

```text
user_name = "Alice"
```

as the ownership mechanism.

Use the authenticated user's ID.

---

### Mistake 5 — Exposing service keys

Service/secret keys can bypass RLS and must not be exposed to users or browser-side code. citeturn0search1

---

# 47. The Complete Mental Model

At this point, think of our application as:

```text
                         USER
                           │
                           ▼
                     AUTHENTICATION
                           │
                           ▼
                        USER ID
                           │
                           ▼
                    APPLICATION DATA
                           │
                           ▼
                       POSTGRESQL
                           │
                           ▼
                          RLS
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
        User-owned rows             Other rows
              │                         │
            ALLOW                      DENY
```

This is the basic architecture behind many multi-user applications.

---

# 48. Our Phase 5 Project Is Taking Shape

We started with:

```text
Python
 ↓
Supabase
 ↓
Database
```

Now:

```text
User
 ↓
Authentication
 ↓
User ID
 ↓
Database
 ↓
RLS
 ↓
User-owned data
```

Soon we will add:

```text
File Storage
```

Then:

```text
Resume Intelligence
```

Then:

```text
Dashboard
```

---

# 49. Phase 4 vs Phase 5

### Phase 4

```text
Upload resume
 ↓
Analyze resume
 ↓
Show result
```

### Phase 5

```text
Create account
 ↓
Login
 ↓
Upload resume
 ↓
Store resume
 ↓
Analyze resume
 ↓
Store analysis
 ↓
Return later
 ↓
See previous analysis
```

The AI didn't necessarily become dramatically smarter.

The **application became real software**.

---

# 50. Takeaway

We have learned three related ideas:

```text
Authentication
    ↓
Who are you?

Authorization
    ↓
What are you allowed to access?

Persistence
    ↓
What should the application remember?
```

Together:

```text
User
 ↓
Authentication
 ↓
User ID
 ↓
Database
 ↓
RLS
 ↓
User-owned data
```

This is the foundation for the next part of our application.

---

# 51. Next Step

Our users can now:

```text
Sign up
Login
Logout
Own database records
```

But resumes are files.

We still need a place to store:

```text
resume.pdf
```

while keeping its metadata in PostgreSQL.

The next section introduces:

# File Storage
