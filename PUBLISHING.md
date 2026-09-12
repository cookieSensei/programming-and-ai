# CookieSensei LMS publishing

This repository is the authoring source for the public CookieSensei learning platform.

- `main` is the authoring branch. Changes here are drafts until published.
- `published` is the student-facing curriculum branch. CookieSensei resolves it to a commit SHA and renders only that revision at `/learn`.
- Publishing means fast-forwarding `published` to an approved commit from `main` through the authenticated CookieSensei admin workflow.
- Students never fetch GitHub directly. CookieSensei reads course content server-side and serves lessons/resources under CookieSensei URLs.
- `course.json` is the machine-readable curriculum manifest. Keep phase paths stable; lesson ordering is derived naturally from numbered filenames and directories.

Do not put secrets, answer keys, instructor-only notes, or unpublished private material in paths intended for the public curriculum. If this repository becomes private later, configure the CookieSensei server with a GitHub token that has read access, plus write access only if admin publishing should continue from the website.
