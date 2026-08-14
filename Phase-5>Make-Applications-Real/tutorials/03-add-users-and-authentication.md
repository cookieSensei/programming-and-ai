# Tutorial 03 — Add Users and Authentication

## Phase 5 — Make Applications Real

### The big idea

A Phase 4 application may work for a generic visitor.

A real product often needs to answer:

> **Who is using the application?**

Once users exist, a second question appears:

> **What is this user allowed to see or do?**

These are related but different problems.

The official Phase 5 project introduces registration, login, logout, sessions, protected pages, and associating application data with users. It explicitly distinguishes authentication from authorization. fileciteturn13file2L291-L323

---

# 1. Authentication vs authorization

Memorize these questions.

### Authentication

> **Who are you?**

Examples:

```text
Enter username
Enter password
```

The system verifies the identity.

### Authorization

> **What are you allowed to do?**

Examples:

```text
Can this user view this booking?
Can this user edit this profile?
Can this user delete this record?
Can this user access Admin?
```

A user can be authenticated but not authorized to perform a particular action.

---

# 2. The basic user journey

A common flow:

```text
Register
   ↓
Login
   ↓
Use application
   ↓
Logout
```

After login:

```text
Browser
   ↓
Authenticated session
   ↓
Django knows the user
```

The user's browser can then make requests associated with that signed-in session.

---

# 3. Registration

Registration creates an account.

A basic registration form might ask for:

```text
Username
Email
Password
Password confirmation
```

A real registration system must consider:

- required fields
- invalid input
- duplicate accounts
- password handling
- validation

Do not create your own password-storage system.

The Phase 5 project explicitly recommends using Django's built-in authentication features instead of creating a custom password system. fileciteturn13file2L337-L349

---

# 4. Passwords are special data

A password is not ordinary application information.

Do not design:

```python
password = models.CharField(...)
```

and simply store the user's password as plain text.

Instead, use Django's authentication framework.

The framework handles password hashing and related authentication behavior.

Your responsibility is to understand:

```text
User enters password
       ↓
Authentication system
       ↓
Password verification
       ↓
Authenticated user
```

---

# 5. Login

A login flow looks like:

```text
User enters credentials
        ↓
Django authentication
        ↓
Credentials valid?
       / \
     yes  no
      ↓    ↓
   session  error
      ↓
logged-in user
```

The session lets subsequent requests be associated with the authenticated user.

---

# 6. Sessions

HTTP requests are separate requests.

Without some mechanism for remembering authentication state, the server would have difficulty knowing that:

```text
Request 1
```

and:

```text
Request 2
```

belong to the same signed-in user.

A session provides a mechanism for maintaining state across requests.

Conceptually:

```text
Login
 ↓
Session established
 ↓
Request
 ↓
Django recognizes user
 ↓
Personalized response
```

You do not need to understand every implementation detail.

---

# 7. Logout

Logout ends the authenticated session.

The flow becomes:

```text
Login
 ↓
Authenticated
 ↓
Use application
 ↓
Logout
 ↓
No longer authenticated
```

Test this deliberately.

---

# 8. Protected pages

Suppose you have:

```text
/my-bookings/
```

It should not necessarily be visible to anonymous users.

The desired behavior might be:

```text
Not logged in
     ↓
Try /my-bookings/
     ↓
Redirect to login
```

while:

```text
Logged in
     ↓
/my-bookings/
     ↓
Show my bookings
```

This is an authorization/access-control problem.

---

# 9. Associating data with users

This is where authentication becomes useful to the business application.

Suppose:

```text
User A
 ├── Booking 1
 └── Booking 5

User B
 ├── Booking 2
 └── Booking 8
```

The database must know which booking belongs to which user.

Conceptually:

```text
User
  ↓
their records
```

This is usually represented through a relationship between your application model and the user model.

---

# 10. The critical security question

Never assume that because a user is logged in, they can access any record.

Imagine:

```text
User A is logged in.
```

The URL is:

```text
/bookings/42/
```

But booking 42 belongs to User B.

A vulnerable application might simply do:

```python
Booking.objects.get(id=42)
```

and show it.

A secure application must enforce ownership or another authorization rule.

The important question is:

> **Does this record belong to the current user, and is the current user allowed to access it?**

---

# 11. Server-side authorization

Do not rely on hiding buttons.

Suppose you remove:

```html
<button>Delete</button>
```

from the page for unauthorized users.

That improves the interface.

But it does not create security.

A user can potentially send a request directly.

Therefore:

```text
UI restriction
     ≠
security boundary
```

The server must enforce access rules.

The Phase 5 project explicitly uses the exercise of attempting to access another user's data to introduce this idea. fileciteturn13file2L395-L406

---

# 12. Two-user testing

Do not test authentication only with one account.

Create:

```text
User A
User B
```

Then:

### Test A

Login as User A.

Create a record.

### Test B

Logout.

Login as User B.

Check whether User A's record is visible.

### Test C

Try to access User A's record directly.

Ask:

> What should happen?

This is much more useful than simply testing "login works."

---

# 13. Common authentication mistakes

### Protecting the page but not the object

You might correctly require login for:

```text
/bookings/
```

but accidentally allow any logged-in user to open:

```text
/bookings/17/
```

Authorization needs to apply at the record level when appropriate.

### Trusting user-provided IDs

Never assume:

```text
id=17
```

means the current user owns record 17.

Verify ownership.

### Building custom password logic

Do not reinvent password hashing and authentication when Django already provides the system.

### Forgetting logout testing

A system that can login but never properly logs out is incomplete.

---

# 14. Authentication and your MWP

Ask whether your product actually needs accounts.

Some products do.

Examples:

```text
Personal expense tracker
Private dashboard
Booking history
Customer portal
```

Others may not.

Examples:

```text
Public landing page
Simple calculator
Public document reader
```

Do not add registration just because Phase 5 teaches it.

Use it when it supports the product.

---

# 15. Data ownership exercise

For your application, fill this in:

```text
My main user:
____________________

My main record:
____________________

Should each record belong to a user?
Yes / No

If yes:
How is ownership represented?
____________________

Who can read the record?
____________________

Who can edit it?
____________________

Who can delete it?
____________________
```

---

# 16. Security exercise

Create:

```text
User A
User B
```

Then test:

```text
□ A can register
□ A can login
□ A can logout
□ B can register
□ B can login
□ Protected page blocks anonymous users
□ A sees A's data
□ B sees B's data
□ A cannot access B's private data
□ B cannot access A's private data
```

This is your first meaningful authorization test.

---

# 17. Using ChatGPT

Good prompt:

> I have a Django application where users should only see their own bookings. Explain how authentication and authorization should work. Show me where the ownership check belongs and why. Do not assume that hiding a button is sufficient security.

For debugging:

> User A can currently access User B's record by changing the ID in the URL. Explain the security flaw and identify the smallest server-side change needed.

---

# 18. Completion model

You should be able to explain:

```text
User
 ↓
Login
 ↓
Session
 ↓
Authenticated request
 ↓
Authorization check
 ↓
Personalized data
```

And distinguish:

```text
Authentication
= Who are you?

Authorization
= What are you allowed to do?
```

The Phase 5 project treats this as the bridge from a generic application to an application that supports individual users. fileciteturn13file2L408-L426
