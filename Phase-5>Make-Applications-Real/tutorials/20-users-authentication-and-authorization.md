# Tutorial 20 — Users, Authentication and Authorization

## Why This Matters

Applications often need to know who a user is and what they are allowed to do.

## Authentication

Authentication asks:

> **Who are you?**

Examples: register, login, logout.

## Authorization

Authorization asks:

> **What are you allowed to do?**

For example, User A should not automatically see User B's private bookings.

## Sessions

After login, the application needs to remember the authenticated user across requests.

```text
Login → Session → Next request → Django knows the user
```

## Server-Side Protection

Hiding a button is not enough. The server must enforce permissions when a protected URL or action is requested.

## Try It

Create two users and verify that each user sees only the data they should be allowed to access.

## Using ChatGPT

Ask: **“Does this Django view actually protect the data on the server, or does it only hide the button in HTML?”**
