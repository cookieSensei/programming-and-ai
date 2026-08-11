# 4. File Storage

## Storing the Actual Files

We now have:

```text
Python
 ↓
Supabase
 ↓
PostgreSQL
```

and:

```text
User
 ↓
Authentication
 ↓
User ID
 ↓
RLS
 ↓
User-owned database records
```

But a resume is not just structured data. There is an actual file:

```text
resume.pdf
```

Where should that file live?

This section introduces **Supabase Storage**.

---

# 1. Database Data vs Files

A relational database is excellent for structured information:

```text
resume_id
user_id
filename
created_at
match_score
```

But the PDF itself is a file.

We can separate the two:

```text
                 RESUME
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
     File Storage          Database
          │                   │
     resume.pdf          metadata
                         user_id
                         filename
                         score
```

Supabase Storage is designed for storing and serving files, while file metadata is represented separately from the file itself. citeturn0search9turn0search8

---

# 2. What Is Supabase Storage?

Supabase Storage provides:

```text
Buckets
Files
Uploads
Downloads
Access control
Signed URLs
```

For our project, Storage will hold:

```text
PDFs
Images
Documents
```

while PostgreSQL holds information **about** those files.

---

# 3. Buckets

Supabase organizes files into **buckets**.

Think of a bucket as a top-level container.

For example:

```text
resumes
```

could be our bucket.

Inside it we might have:

```text
resumes/
    user-id-1/
        resume-a.pdf

    user-id-2/
        resume-b.pdf
```

Buckets also define important storage behavior such as the access model and upload restrictions. citeturn0search7

---

# 4. Public vs Private Buckets

Supabase supports two important access models:

```text
Public
Private
```

Public bucket files can be served publicly when their URLs are known.

Private buckets require access control for downloads and are private by default. citeturn0search7

For resumes, use:

```text
Private
```

A resume can contain personal information, so we do not want every uploaded resume to be publicly accessible.

---

# 5. Create the Resume Bucket

In the Supabase Dashboard:

```text
Storage
   ↓
Create bucket
   ↓
Name: resumes
```

Keep the bucket private.

The bucket must exist before the application attempts an upload.

---

# 6. Storage and Database Are Different

Suppose Alice uploads:

```text
resume.pdf
```

The file could live at:

```text
resumes/<alice-user-id>/resume.pdf
```

while PostgreSQL contains:

```text
resumes
----------------
id
user_id
filename
storage_path
extracted_text
created_at
```

The relationship is:

```text
Database
   │
   └── storage_path
            │
            ▼
       Storage file
```

The database tells us **where the file is** and **who owns it**.

---

# 7. Resume Table

We can use:

```sql
CREATE TABLE public.resumes (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    filename TEXT NOT NULL,
    storage_path TEXT NOT NULL,
    extracted_text TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

The database stores metadata, not the PDF bytes.

---

# 8. Uploading With Python

The Supabase Python client exposes Storage through:

```python
supabase.storage
```

and a bucket through:

```python
supabase.storage.from_("resumes")
```

The Python Storage API provides `upload()` for uploading a file to an existing bucket. citeturn0search4

A basic example is:

```python
with open("resume.pdf", "rb") as file:
    response = (
        supabase
        .storage
        .from_("resumes")
        .upload(
            "resume.pdf",
            file
        )
    )
```

The important structure is:

```text
bucket
 ↓
path
 ↓
file
```

---

# 9. User-Specific Paths

Do not put every user's file at:

```text
resume.pdf
```

Use a path containing the authenticated user's ID:

```python
path = f"{user.id}/resume.pdf"
```

Now:

```text
resumes/
    123-user-id/
        resume.pdf

    456-user-id/
        resume.pdf
```

This gives us a natural organization scheme.

The path is useful for organization, but **the path alone is not the security boundary**. Storage policies must enforce access.

---

# 10. Avoid Filename Collisions

Suppose Alice uploads `resume.pdf` twice.

Using:

```text
alice-id/resume.pdf
```

can cause a collision.

A simple solution is a unique filename:

```python
import uuid

file_name = f"{uuid.uuid4()}-resume.pdf"
```

Then:

```text
alice-id/
    8c7...-resume.pdf

alice-id/
    91a...-resume.pdf
```

For our first project, unique paths are often simpler than overwriting files.

---

# 11. Upsert

Supabase's upload API supports an `upsert` option.

Without upsert, uploading to an existing path can fail because the object already exists. With upsert, an existing object can be overwritten. citeturn0search4turn0search11

For this project, prefer unique paths unless you specifically want replacement behavior.

---

# 12. Content Type

Files have MIME types.

For example:

```text
application/pdf
image/jpeg
image/png
```

Supabase's Storage API allows the content type to be specified during upload. citeturn0search4turn0search11

For a PDF, the intended type is:

```text
application/pdf
```

Follow the current client documentation for the exact option syntax for your installed library version.

---

# 13. Streamlit File Upload

We already know this from earlier phases:

```python
uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf"]
)
```

Now the workflow becomes:

```text
Streamlit
   ↓
Uploaded file
   ↓
Python
   ↓
Supabase Storage
```

---

# 14. Complete Upload Flow

For an authenticated user:

```text
User
 ↓
Login
 ↓
Upload resume
 ↓
Get user ID
 ↓
Generate storage path
 ↓
Upload file
 ↓
Store metadata in PostgreSQL
```

Conceptually:

```python
user = supabase.auth.get_user().user

storage_path = (
    f"{user.id}/{uploaded_file.name}"
)
```

Upload:

```python
supabase.storage \
    .from_("resumes") \
    .upload(
        storage_path,
        uploaded_file
    )
```

Then store metadata:

```python
supabase.table("resumes").insert({
    "user_id": user.id,
    "filename": uploaded_file.name,
    "storage_path": storage_path
}).execute()
```

Now:

```text
Storage
   ↓
Actual PDF

PostgreSQL
   ↓
Metadata
```

---

# 15. Why Store Metadata Separately?

Suppose the application needs to display:

```text
My Resumes

resume.pdf
Uploaded: August 11
```

We do not need to inspect the PDF just to display this information.

PostgreSQL can quickly provide:

```text
filename
created_at
user_id
```

The actual file remains in Storage.

This separation makes the application easier to reason about.

---

# 16. Private Files and Downloads

For a private bucket, files are not publicly accessible through a normal public URL.

Private files can be downloaded through an authenticated request or exposed temporarily with a signed URL. citeturn0search6turn0search7

Conceptually:

```text
User
 ↓
Request file
 ↓
Storage authorization
 ↓
File bytes
```

---

# 17. Signed URLs

Sometimes we want to give temporary access to a private file.

Use a:

# Signed URL

For example:

```python
response = (
    supabase
    .storage
    .from_("resumes")
    .create_signed_url(
        storage_path,
        60
    )
)
```

The second argument is the expiry time in seconds.

Supabase documents signed URLs as time-limited links for files in private buckets. citeturn0search3

---

# 18. Why Signed URLs?

Imagine a user clicks:

```text
View Resume
```

We do not want to make the resume public forever.

Instead:

```text
Click View
     ↓
Generate signed URL
     ↓
Valid for a short time
     ↓
Open file
```

The bucket remains private.

---

# 19. Public URL vs Signed URL

### Public URL

```text
Anyone with URL
      ↓
File
```

Suitable for genuinely public assets.

### Signed URL

```text
Application
      ↓
Temporary URL
      ↓
Private file
```

Suitable for:

```text
Resumes
Private documents
Invoices
User uploads
```

Supabase documents `get_public_url()` for public buckets and `create_signed_url()` for time-limited access to private files. citeturn0search5turn0search3

---

# 20. Storage Policies

Database tables use PostgreSQL RLS.

Storage objects also use access-control policies.

Supabase stores Storage object metadata in `storage.objects`, and Storage access can be controlled with RLS policies on that table. citeturn0search7turn0search8

Think:

```text
Database rows
    ↓
RLS policies

Storage objects
    ↓
Storage RLS policies
```

---

# 21. User-Owned Storage

We want:

```text
Alice
 ↓
Alice's files

Bob
 ↓
Bob's files
```

A useful path convention is:

```text
<user-id>/<filename>
```

For example:

```text
resumes/
    8f3.../
        resume.pdf

    a91.../
        resume.pdf
```

A policy can then use the authenticated user's ID when deciding whether an object may be accessed.

Supabase documents Storage authorization through policies on `storage.objects`. citeturn0search7

---

# 22. Storage Security Mental Model

Do not think:

```text
The folder name protects the file.
```

Think:

```text
Path
 ↓
Organization

RLS policy
 ↓
Security
```

The application should never rely on a filename or folder name alone as an authorization mechanism.

---

# 23. Deleting a Resume

Deleting a resume involves two pieces:

```text
Storage file
+
Database metadata
```

Conceptually:

```text
Delete resume
    │
    ├── Delete Storage object
    │
    └── Delete database row
```

Otherwise we could end up with a database record for a file that no longer exists, or a file with no database record.

---

# 24. Orphaned Files

An orphaned file is a file that remains in Storage even though the application no longer has a database record for it.

Example:

```text
Storage
 └── old-resume.pdf

Database
 └── no matching row
```

This can happen when one operation succeeds and the other fails.

We do not need a sophisticated distributed transaction system in this course, but students should learn to recognize the problem.

---

# 25. Handling Errors

Suppose:

```text
Storage upload succeeds
```

but:

```text
Database insert fails
```

Then:

```text
File exists
Metadata missing
```

At minimum, handle failures rather than assuming every operation succeeds:

```python
try:
    # upload
    # insert metadata
    pass
except Exception as e:
    st.error(str(e))
```

A later version can add cleanup if the second operation fails.

---

# 26. File Validation

Do not blindly accept every uploaded file.

For our first version, accept:

```text
PDF
```

and later consider:

```text
PNG
JPG
JPEG
```

Streamlit can restrict the upload control:

```python
uploaded_file = st.file_uploader(
    "Upload resume",
    type=["pdf"]
)
```

But UI filtering should not be treated as the complete security or validation strategy.

---

# 27. File Size

For small files, standard uploads are appropriate.

Supabase recommends resumable uploads for larger files, particularly files over about 6 MB, where network reliability becomes more important. citeturn0search10turn0search11

Typical resumes are small enough that our introductory project can use the standard upload flow.

We do not need to introduce resumable uploads yet.

---

# 28. The Resume Pipeline

We can now build:

```text
                USER
                  │
                  ▼
               LOGIN
                  │
                  ▼
              USER ID
                  │
                  ▼
          UPLOAD RESUME
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
     STORAGE             DATABASE
        │                   │
   resume.pdf          metadata
                          │
                          ▼
                    extracted_text
```

Then:

```text
Database
   ↓
Resume record
   ↓
Resume Intelligence
   ↓
Match score
```

---

# 29. Integrating OCR

If the uploaded file is an image or scanned document:

```text
Storage
 ↓
Read file
 ↓
OpenCV
 ↓
OCR
 ↓
Text
 ↓
Database
```

For a text-based PDF:

```text
Storage
 ↓
Read PDF
 ↓
Text extraction
 ↓
Database
```

This is where our Phase 4 work becomes part of a persistent application.

---

# 30. Full Resume Upload Architecture

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
                    STREAMLIT UPLOAD
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
            FILE STORAGE         POSTGRESQL
                 │                   │
             resume.pdf          metadata
                 │                   │
                 ▼                   ▼
            OCR / PARSER       storage_path
                 │                   │
                 └─────────┬─────────┘
                           ▼
                     RESUME DATA
                           │
                           ▼
                  RESUME INTELLIGENCE
```

This is now starting to resemble a real application.

---

# 31. Mini Project — Private Resume Vault

Before building the complete Career Companion, create:

# Private Resume Vault

The application should allow an authenticated user to:

```text
Sign up
Login
Upload a PDF
Store the PDF
Store metadata
List their resumes
Generate a temporary viewing/download link
Delete their resume
Logout
```

The application should **not** allow:

```text
Alice → Bob's resume
```

---

# 32. Database Schema

Use something like:

```sql
CREATE TABLE public.resumes (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    filename TEXT NOT NULL,
    storage_path TEXT NOT NULL,
    extracted_text TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

Enable RLS:

```sql
ALTER TABLE public.resumes
ENABLE ROW LEVEL SECURITY;
```

Then create policies so users can only access their own rows.

---

# 33. Storage Layout

Use:

```text
resumes/
    <user-id>/
        <unique-file-name>.pdf
```

For example:

```text
resumes/
    8f3e.../
        19ac...-resume.pdf
```

Store the path in PostgreSQL:

```text
storage_path =
"8f3e.../19ac...-resume.pdf"
```

---

# 34. Private Resume Vault Flow

```text
Login
 ↓
Get user ID
 ↓
Choose PDF
 ↓
Generate unique path
 ↓
Upload to private bucket
 ↓
Insert database metadata
 ↓
Display resume list
 ↓
User clicks View
 ↓
Generate signed URL
 ↓
Open temporary link
```

This is a complete mini application.

---

# 35. Test With Two Users

Create:

```text
Alice
Bob
```

Alice uploads:

```text
alice.pdf
```

Bob uploads:

```text
bob.pdf
```

Test:

```text
Alice:
✓ sees alice.pdf
✗ cannot see bob.pdf

Bob:
✓ sees bob.pdf
✗ cannot see alice.pdf
```

Then test:

```text
Alice logs out
 ↓
Bob logs in
 ↓
Alice's file remains inaccessible
```

This demonstrates authentication and storage authorization working together.

---

# 36. Common Mistakes

### Mistake 1 — Making the resume bucket public

Do not make private user documents public just to make the demo easier.

### Mistake 2 — Storing only the filename

Store the actual:

```text
storage_path
```

so the application knows exactly where the object lives.

### Mistake 3 — Forgetting ownership

Every user-owned file needs an ownership model.

Use:

```text
user ID
+
access policies
```

### Mistake 4 — Trusting Streamlit's file filter

The UI filter is useful, but it is not the complete security or validation strategy.

### Mistake 5 — Ignoring failed operations

Storage and database operations are separate operations.

Think about what happens if:

```text
upload succeeds
but database insert fails
```

---

# 37. What We Have Learned

We can now distinguish:

```text
PostgreSQL
    ↓
Structured application data
```

from:

```text
Storage
    ↓
Actual files
```

And:

```text
Authentication
    ↓
Who is the user?
```

from:

```text
Authorization
    ↓
Which files can the user access?
```

---

# 38. The Architecture So Far

```text
                         USER
                           │
                           ▼
                     AUTHENTICATION
                           │
                           ▼
                        USER ID
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
         POSTGRESQL                  STORAGE
              │                         │
       structured data              files
              │                         │
              └────────────┬────────────┘
                           ▼
                       PYTHON
                           │
                           ▼
                       STREAMLIT
```

Both database rows and Storage objects can have access-control rules.

---

# 39. Phase 4 Meets Phase 5

### Phase 4

```text
Resume
 ↓
OCR / NLP
 ↓
Matching
 ↓
Result
```

### Phase 5

```text
User
 ↓
Authentication
 ↓
Upload Resume
 ↓
Storage
 ↓
OCR / NLP
 ↓
Matching
 ↓
Database
 ↓
Persistent Result
```

The intelligent components are the same.

The surrounding software has become much more real.

---

# 40. Takeaway

We now have three layers:

```text
AUTHENTICATION
Who are you?

DATABASE
What structured data should we remember?

STORAGE
What files should we keep?
```

Together:

```text
User
 ↓
Auth
 ↓
Database
 ↓
Storage
 ↓
AI Application
```

That is enough infrastructure to build our central Phase 5 project.

---

# 41. Next Step

We now have:

```text
SQL
PostgreSQL
Supabase
Authentication
Authorization
RLS
File Storage
```

The next step is to bring the Phase 4 intelligence back into this system.

We will build:

# AI Career Companion

where a user can:

```text
Upload a resume
      ↓
Store it
      ↓
Parse it
      ↓
Analyze it
      ↓
Add jobs
      ↓
Match resume to jobs
      ↓
Store results
      ↓
Return later
      ↓
See their history
```

Now we are finally building a real persistent intelligent application.

