# Phase 2 - Building Software
# Tutorial 1: Regular Expressions (Regex) in Python

> **Path:** `programming-and-ai/Phase-2/Building-Softwares/1 - REGEX.md`

---

# Table of Contents

1. [Why Regex Exists](#1-why-regex-exists)
2. [Learning Objectives](#2-learning-objectives)
3. [What Is a Regular Expression?](#3-what-is-a-regular-expression)
4. [Regex in Python](#4-regex-in-python)
5. [Your First Regex](#5-your-first-regex)
6. [Literal Matching](#6-literal-matching)
7. [Character Classes](#7-character-classes)
8. [Ranges](#8-ranges)
9. [Negated Character Classes](#9-negated-character-classes)
10. [Shorthand Character Classes](#10-shorthand-character-classes)
11. [The Dot](#11-the-dot)
12. [Quantifiers](#12-quantifiers)
13. [Greedy vs Non-Greedy Matching](#13-greedy-vs-non-greedy-matching)
14. [Anchors](#14-anchors)
15. [Alternation](#15-alternation)
16. [Groups](#16-groups)
17. [Named Groups](#17-named-groups)
18. [Capturing vs Non-Capturing Groups](#18-capturing-vs-non-capturing-groups)
19. [Backreferences](#19-backreferences)
20. [Lookahead](#20-lookahead)
21. [Lookbehind](#21-lookbehind)
22. [Flags](#22-flags)
23. [`match()` vs `search()` vs `fullmatch()`](#23-match-vs-search-vs-fullmatch)
24. [`findall()`](#24-findall)
25. [`finditer()`](#25-finditer)
26. [`split()`](#26-split)
27. [`sub()` and `subn()`](#27-sub-and-subn)
28. [Compiled Patterns](#28-compiled-patterns)
29. [Escaping Regex Characters](#29-escaping-regex-characters)
30. [Raw Strings in Python](#30-raw-strings-in-python)
31. [Common Validation Patterns](#31-common-validation-patterns)
32. [Regex for Text Extraction](#32-regex-for-text-extraction)
33. [Regex for Cleaning Data](#33-regex-for-cleaning-data)
34. [Regex for Log Parsing](#34-regex-for-log-parsing)
35. [Regex for URLs](#35-regex-for-urls)
36. [Regex for File Names](#36-regex-for-file-names)
37. [Regex for Structured IDs](#37-regex-for-structured-ids)
38. [Regex for Password Rules](#38-regex-for-password-rules)
39. [Regex for Dates and Times](#39-regex-for-dates-and-times)
40. [Regex for Data Pipelines](#40-regex-for-data-pipelines)
41. [Project 1 - Extract Information](#41-project-1--extract-information)
42. [Project 2 - Contact Information Extractor](#42-project-2--contact-information-extractor)
43. [Project 3 - Log Analyzer](#43-project-3--log-analyzer)
44. [Project 4 - Data Cleaner](#44-project-4--data-cleaner)
45. [Project 5 - URL and Link Scanner](#45-project-5--url-and-link-scanner)
46. [Project 6 - Input Validator](#46-project-6--input-validator)
47. [Project 7 - Markdown Scanner](#47-project-7--markdown-scanner)
48. [Project 8 - Mini Search Engine](#48-project-8--mini-search-engine)
49. [Project 9 - PII Detection](#49-project-9--pii-detection)
50. [Project 10 - Final Regex Toolkit](#50-project-10--final-regex-toolkit)
51. [Debugging Regex](#51-debugging-regex)
52. [Performance and Safety](#52-performance-and-safety)
53. [When Not to Use Regex](#53-when-not-to-use-regex)
54. [Regex Design Principles](#54-regex-design-principles)
55. [Final Assessment](#55-final-assessment)
56. [Final Cheat Sheet](#56-final-cheat-sheet)

---

# 1. Why Regex Exists

Regular expressions are one of the most useful tools for working with **structured text**.

Software constantly receives text such as:

```text
hello@example.com
+91-9876543210
2026-08-23
ERROR [2026-08-23 14:42:01] database unavailable
https://example.com/products?id=42
ORD-2026-000184
```

A human can look at these strings and recognize patterns.

A program needs explicit instructions.

Regex gives us a compact language for describing those patterns.

For example:

```text
\d{4}-\d{2}-\d{2}
```

describes a common `YYYY-MM-DD` shape.

Regex can be used to:

- search text
- extract information
- validate input
- clean messy data
- replace text
- tokenize text
- parse logs
- identify structured IDs
- detect potentially sensitive information
- build text-processing tools

However:

> **Regex is a pattern-matching tool, not a replacement for every parser.**

Learning when to use regex is just as important as learning regex syntax.

---

# 2. Learning Objectives

By the end of this tutorial, you should be able to:

- understand regex syntax
- write simple and complex patterns
- use Python's `re` module
- search text for patterns
- extract values using capture groups
- validate structured input
- replace matching text
- split text using regex
- use named groups
- use lookaheads and lookbehinds
- understand greedy and non-greedy matching
- use regex flags
- debug patterns systematically
- parse semi-structured logs
- clean text with regex
- build reusable regex utilities
- recognize regex limitations
- avoid common performance problems

The ultimate goal is not:

> "I memorized regex syntax."

The goal is:

> **"I can look at a text-processing problem and design an appropriate pattern or decide that regex is the wrong tool."**

---

# 3. What Is a Regular Expression?

A regular expression is a pattern describing a set of strings.

For example:

```regex
cat
```

matches:

```text
cat
```

It can also match the substring `cat` inside:

```text
The cat is sleeping.
concatenate
copycat
```

A regex can become more general.

For example:

```regex
c.t
```

means:

```text
c
any character
t
```

So it can match:

```text
cat
cut
cot
c9t
c-t
```

The pattern describes a **structure**, not one specific string.

---

# 4. Regex in Python

Python provides regex functionality through the standard-library `re` module.

```python
import re
```

No external package is required.

Let's start with a simple example:

```python
import re

text = "I love Python."

result = re.search(r"Python", text)

print(result)
```

If a match exists, Python returns a `Match` object.

If no match exists:

```python
None
```

---

## Why use `r"..."`?

Python raw strings are strongly recommended for regex patterns.

Prefer:

```python
r"\d+"
```

instead of:

```python
"\\d+"
```

Both can work, but raw strings make regex patterns easier to read.

More on this later.

---

# 5. Your First Regex

Let's search for a word.

```python
import re

text = "Python is powerful."

match = re.search(r"Python", text)

if match:
    print("Found!")
else:
    print("Not found.")
```

Output:

```text
Found!
```

A match object contains useful information.

```python
print(match.group())
print(match.start())
print(match.end())
```

Possible output:

```text
Python
0
6
```

The match occupies:

```text
[0, 6)
```

Python's `end()` is exclusive.

---

# 6. Literal Matching

Literal matching is the simplest form of regex.

```regex
python
```

matches the exact sequence:

```text
python
```

But regex matching is case-sensitive by default.

```python
re.search(r"python", "Python")
```

returns:

```python
None
```

We can change this with a flag:

```python
re.search(r"python", "Python", re.IGNORECASE)
```

---

## Exercise

Write a regex that finds:

```text
apple
```

inside:

```text
I bought an apple today.
```

Then test it against:

```text
APPLE
Apple
pineapple
```

Observe what happens.

---

# 7. Character Classes

A character class lets us specify a set of allowed characters.

Syntax:

```regex
[abc]
```

means:

> Match one character that is either `a`, `b`, or `c`.

Examples:

```regex
[aeiou]
```

matches a vowel.

```regex
[0123456789]
```

matches a digit.

```regex
[abc123]
```

matches one character from the listed set.

---

## Example

```python
text = "cat bat hat mat"

matches = re.findall(r"[cbhm]at", text)

print(matches)
```

Output:

```text
['cat', 'bat', 'hat', 'mat']
```

---

# 8. Ranges

Writing:

```regex
[0123456789]
```

is cumbersome.

Use:

```regex
[0-9]
```

Similarly:

```regex
[a-z]
```

means lowercase English letters.

```regex
[A-Z]
```

means uppercase English letters.

```regex
[a-zA-Z]
```

means either uppercase or lowercase English letters.

You can combine ranges:

```regex
[a-zA-Z0-9]
```

---

## Important

A hyphen inside a character class often defines a range.

```regex
[a-z]
```

But outside a character class, `-` is generally a literal hyphen.

---

# 9. Negated Character Classes

Put `^` immediately after `[` to negate a character class.

```regex
[^0-9]
```

means:

> Match one character that is not a digit.

Example:

```python
text = "abc123"

print(re.findall(r"[^0-9]", text))
```

Output:

```text
['a', 'b', 'c']
```

Another example:

```regex
[^a-zA-Z]
```

matches characters that are not English letters.

---

# 10. Shorthand Character Classes

Regex provides shortcuts for common classes.

## `\d`

Digit.

Usually equivalent to a Unicode-aware digit class in Python:

```regex
\d
```

Example:

```python
re.findall(r"\d", "Room 42")
```

returns:

```text
['4', '2']
```

---

## `\D`

Not a digit.

```regex
\D
```

---

## `\w`

Word character.

In Python, this is Unicode-aware and includes letters, digits, and underscore.

```regex
\w
```

---

## `\W`

Not a word character.

---

## `\s`

Whitespace.

Includes characters such as:

- spaces
- tabs
- newlines

---

## `\S`

Non-whitespace.

---

## Summary

| Pattern | Meaning |
|---|---|
| `\d` | digit |
| `\D` | non-digit |
| `\w` | word character |
| `\W` | non-word character |
| `\s` | whitespace |
| `\S` | non-whitespace |

---

# 11. The Dot

The dot:

```regex
.
```

means:

> Match almost any character.

Example:

```regex
c.t
```

can match:

```text
cat
cot
cut
c9t
c-t
```

By default, `.` does not match newline characters.

The `DOTALL` flag changes this behavior.

```python
re.search(r"a.b", "a\nb", re.DOTALL)
```

---

## Be careful

A dot is extremely broad.

If you write:

```regex
.*
```

you are saying:

> Match almost anything, as much as possible.

This can be useful, but it can also cause:

- overly broad matches
- confusing behavior
- poor performance
- incorrect extraction

Specific patterns are usually safer.

---

# 12. Quantifiers

Quantifiers describe **how many times** something can occur.

## `*`

Zero or more.

```regex
a*
```

Matches:

```text
""
"a"
"aa"
"aaa"
```

---

## `+`

One or more.

```regex
a+
```

Matches:

```text
a
aa
aaa
```

but not an empty string.

---

## `?`

Zero or one.

```regex
colou?r
```

matches:

```text
color
colour
```

---

## Exact repetition

```regex
a{3}
```

matches exactly:

```text
aaa
```

---

## Range

```regex
a{2,5}
```

matches between 2 and 5 `a` characters.

---

## At least N

```regex
a{2,}
```

means:

> two or more `a`s.

---

## Example

Phone-like digits:

```regex
\d{10}
```

matches exactly ten digits.

---

# 13. Greedy vs Non-Greedy Matching

Regex quantifiers are generally **greedy**.

Consider:

```python
text = "<title>Hello</title><title>World</title>"

re.findall(r"<title>.*</title>", text)
```

You might expect:

```text
['<title>Hello</title>', '<title>World</title>']
```

But a greedy `.*` can consume too much.

A non-greedy quantifier uses `?`:

```regex
.*?
```

So:

```python
re.findall(r"<title>.*?</title>", text)
```

can produce:

```text
['<title>Hello</title>', '<title>World</title>']
```

---

## Greedy

```regex
.*
```

means:

> Take as much as possible while still allowing the entire pattern to succeed.

## Non-greedy

```regex
.*?
```

means:

> Take as little as possible while still allowing the entire pattern to succeed.

---

# 14. Anchors

Anchors describe **positions**, not characters.

## `^`

Beginning of string/line depending on flags.

```regex
^Hello
```

matches:

```text
Hello world
```

but not:

```text
Say Hello
```

---

## `$`

End of string/line depending on flags.

```regex
world$
```

matches:

```text
Hello world
```

but not:

```text
world today
```

---

## `\b`

Word boundary.

```regex
\bcat\b
```

matches:

```text
cat
the cat
cat!
```

but not:

```text
concatenate
copycat
```

---

## `\B`

Not a word boundary.

---

## Why anchors matter

Suppose you want to validate a three-digit code.

This is not enough:

```regex
\d{3}
```

because it could match part of:

```text
12345
```

For a whole-string validation:

```regex
^\d{3}$
```

or, preferably in Python:

```python
re.fullmatch(r"\d{3}", value)
```

---

# 15. Alternation

The pipe character:

```regex
|
```

means OR.

Example:

```regex
cat|dog
```

matches either:

```text
cat
```

or:

```text
dog
```

---

## Grouping alternation

This:

```regex
cat|doghouse
```

means:

```text
cat
```

OR:

```text
doghouse
```

If you want:

```text
cat
```

or:

```text
dog
```

followed by:

```text
house
```

use:

```regex
(cat|dog)house
```

which matches:

```text
cathouse
doghouse
```

---

# 16. Groups

Parentheses create groups.

```regex
(\d{4})-(\d{2})-(\d{2})
```

can capture:

```text
2026-08-23
```

as:

```text
2026
08
23
```

Example:

```python
text = "2026-08-23"

match = re.search(
    r"(\d{4})-(\d{2})-(\d{2})",
    text
)

print(match.group(1))
print(match.group(2))
print(match.group(3))
```

Output:

```text
2026
08
23
```

---

## `group(0)`

The entire match:

```python
match.group(0)
```

is equivalent to:

```python
match.group()
```

---

# 17. Named Groups

For complex regex patterns, numeric group references become difficult to understand.

Instead of:

```regex
(\d{4})-(\d{2})-(\d{2})
```

use:

```regex
(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})
```

Python example:

```python
pattern = re.compile(
    r"(?P<year>\d{4})-"
    r"(?P<month>\d{2})-"
    r"(?P<day>\d{2})"
)

match = pattern.search("2026-08-23")

print(match.group("year"))
print(match.group("month"))
print(match.group("day"))
```

This is much more readable.

---

# 18. Capturing vs Non-Capturing Groups

Normal parentheses capture:

```regex
(...)
```

Non-capturing groups use:

```regex
(?:...)
```

Example:

```regex
(?:cat|dog)
```

This groups alternatives without creating a captured result.

Use non-capturing groups when you need grouping logic but do not need the group's value later.

This becomes especially important in large patterns.

---

# 19. Backreferences

A backreference says:

> Match the same text that was captured earlier.

Example:

```regex
\b(\w+)\s+\1\b
```

can detect repeated words:

```text
this this
hello hello
very very
```

Example:

```python
text = "This is is a test."

match = re.search(r"\b(\w+)\s+\1\b", text, re.IGNORECASE)

print(match.group())
```

Potential output:

```text
is is
```

Backreferences are powerful but can make patterns harder to understand.

---

# 20. Lookahead

A lookahead checks what comes next without consuming it.

## Positive lookahead

Syntax:

```regex
(?=...)
```

Example:

```regex
\d+(?=USD)
```

matches digits only when followed by `USD`.

Given:

```text
100USD
200EUR
300USD
```

it matches:

```text
100
300
```

The `USD` text is not part of the match.

---

## Negative lookahead

Syntax:

```regex
(?!...)
```

Example:

```regex
\d+(?!USD)
```

means:

> Match digits not immediately followed by `USD`.

Lookaheads are useful for conditions such as:

- must contain
- must not contain
- followed by
- not followed by

---

# 21. Lookbehind

Lookbehind checks what comes before the current position.

## Positive lookbehind

```regex
(?<=\$)\d+
```

matches digits preceded by `$`.

For:

```text
$100
€200
$300
```

it can extract:

```text
100
300
```

The dollar sign is not included in the match.

---

## Negative lookbehind

```regex
(?<!\$)\d+
```

matches digits not immediately preceded by `$`.

---

## Important Python note

Python's `re` module has restrictions around lookbehind width. Fixed-width lookbehind is the safest pattern to use.

---

# 22. Flags

Flags modify regex behavior.

Common Python flags include:

| Flag | Purpose |
|---|---|
| `re.IGNORECASE` | Case-insensitive matching |
| `re.MULTILINE` | `^` and `$` work per line |
| `re.DOTALL` | `.` matches newlines |
| `re.VERBOSE` | Allows readable multi-line patterns |
| `re.ASCII` | ASCII-oriented shorthand behavior |

---

## Case-insensitive matching

```python
re.search(r"python", "PYTHON", re.IGNORECASE)
```

---

## Multiline

```python
text = """first
second
third"""

re.findall(r"^.*$", text, re.MULTILINE)
```

---

## DOTALL

```python
re.search(r"start.*end", text, re.DOTALL)
```

allows `.` to cross line boundaries.

---

# 23. `match()` vs `search()` vs `fullmatch()`

This distinction is essential.

## `re.match()`

Checks the beginning of the string.

```python
re.match(r"Python", "Python is great")
```

works.

```python
re.match(r"Python", "I use Python")
```

does not.

---

## `re.search()`

Finds the pattern anywhere.

```python
re.search(r"Python", "I use Python")
```

works.

---

## `re.fullmatch()`

Requires the entire string to match.

```python
re.fullmatch(r"\d{5}", "12345")
```

works.

```python
re.fullmatch(r"\d{5}", "123456")
```

does not.

---

## Rule of thumb

Use:

- `match()` when the beginning matters
- `search()` when you need to find something anywhere
- `fullmatch()` for strict validation

For validation, `fullmatch()` is often clearer than manually adding `^` and `$`.

---

# 24. `findall()`

Use `findall()` when you want all matches.

```python
text = "Order 123, order 456, order 789"

numbers = re.findall(r"\d+", text)

print(numbers)
```

Output:

```text
['123', '456', '789']
```

---

## Important behavior with groups

If your regex contains capture groups, `findall()` may return group contents rather than the entire match.

Example:

```python
re.findall(r"ID-(\d+)", "ID-123 ID-456")
```

returns:

```text
['123', '456']
```

This is useful, but it can surprise beginners.

---

# 25. `finditer()`

`finditer()` returns an iterator of match objects.

This is useful when you need:

- positions
- groups
- matched text
- surrounding context

Example:

```python
text = "ID-123 ID-456"

for match in re.finditer(r"ID-(\d+)", text):
    print(match.group())
    print(match.group(1))
    print(match.span())
```

This is often preferable to `findall()` for serious text processing.

---

# 26. `split()`

Regex can be used for splitting.

```python
text = "apple,banana;orange|grape"

parts = re.split(r"[,;|]", text)

print(parts)
```

Output:

```text
['apple', 'banana', 'orange', 'grape']
```

You can also handle variable whitespace:

```python
re.split(r"\s*,\s*", "apple, banana,   orange")
```

---

# 27. `sub()` and `subn()`

Use `sub()` for replacement.

```python
text = "My phone is 9876543210."

cleaned = re.sub(r"\d", "X", text)

print(cleaned)
```

Output:

```text
My phone is XXXXXXXXXX.
```

---

## Replacement with groups

Suppose:

```text
2026-08-23
```

needs to become:

```text
23/08/2026
```

Use:

```python
text = "2026-08-23"

result = re.sub(
    r"(\d{4})-(\d{2})-(\d{2})",
    r"\3/\2/\1",
    text
)

print(result)
```

---

## `subn()`

Returns both:

- modified text
- number of replacements

```python
result, count = re.subn(r"\d+", "[NUMBER]", "10 cats and 20 dogs")

print(result)
print(count)
```

---

# 28. Compiled Patterns

If you repeatedly use the same regex, compile it.

```python
pattern = re.compile(r"\d+")
```

Then:

```python
pattern.findall("10 20 30")
pattern.search("abc123")
```

Compilation makes the intent clearer and can be useful when the same pattern is reused many times.

---

# 29. Escaping Regex Characters

Some characters have special meaning:

```text
. ^ $ * + ? { } [ ] \ | ( )
```

If you want to match them literally, escape them.

For example:

```regex
\.
```

matches a literal period.

```regex
\+
```

matches a literal plus sign.

```regex
\?
```

matches a literal question mark.

---

## Example

To find:

```text
example.com
```

a precise regex could use:

```regex
example\.com
```

Without escaping the dot:

```regex
example.com
```

the `.` can match another character.

---

# 30. Raw Strings in Python

Python itself uses backslashes for escapes.

For example:

```python
"\n"
```

is a newline.

Regex also uses backslashes:

```regex
\d
```

Raw strings reduce the escaping confusion.

Prefer:

```python
r"\d+"
```

instead of:

```python
"\\d+"
```

Prefer:

```python
r"\."
```

instead of:

```python
"\\."
```

This is one of the most important Python regex habits.

---

# 31. Common Validation Patterns

Regex is commonly used for lightweight validation.

## Digits only

```regex
\d+
```

For strict validation:

```python
bool(re.fullmatch(r"\d+", value))
```

---

## Exactly 10 digits

```python
bool(re.fullmatch(r"\d{10}", value))
```

---

## Letters only

```python
bool(re.fullmatch(r"[A-Za-z]+", value))
```

---

## Alphanumeric ID

```python
bool(re.fullmatch(r"[A-Za-z0-9]+", value))
```

---

## Simple username

```regex
[A-Za-z0-9_]{3,20}
```

---

## Simple hexadecimal value

```regex
[0-9A-Fa-f]+
```

---

# 32. Regex for Text Extraction

Regex is particularly useful when information is embedded in prose.

Example:

```text
Customer Alice purchased product ABC-123 for $499.
```

We can extract:

- customer name
- product ID
- price

Example pattern:

```regex
Customer (?P<name>[A-Za-z]+) purchased product (?P<product>[A-Z]{3}-\d+) for \$(?P<price>\d+)
```

Then:

```python
match = pattern.search(text)

if match:
    print(match.groupdict())
```

Potential output:

```python
{
    "name": "Alice",
    "product": "ABC-123",
    "price": "499"
}
```

Named groups make extraction code significantly easier to maintain.

---

# 33. Regex for Cleaning Data

Real-world data is messy.

Examples:

```text
"  John Smith  "
"JOHN SMITH"
"john   smith"
"+91 98765-43210"
```

Regex can normalize certain structural problems.

Remove repeated whitespace:

```python
re.sub(r"\s+", " ", text).strip()
```

Remove non-digits:

```python
re.sub(r"\D", "", phone)
```

Normalize separators:

```python
re.sub(r"[-\s]+", "", phone)
```

But be careful:

> Cleaning is a semantic operation.

Removing characters blindly can destroy meaningful information.

---

# 34. Regex for Log Parsing

Logs are a classic regex use case.

Example:

```text
2026-08-23 14:32:10 [ERROR] user=alice request_id=abc123 message="Database timeout"
```

We might want:

```text
timestamp
level
username
request_id
message
```

A named-group pattern:

```regex
(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})
\s+\[(?P<level>[A-Z]+)\]
\s+user=(?P<user>\w+)
\s+request_id=(?P<request_id>\w+)
\s+message="(?P<message>.*?)"
```

Then:

```python
match.groupdict()
```

produces a structured dictionary.

---

# 35. Regex for URLs

A URL can have many forms.

A simplistic pattern might be:

```regex
https?://[^\s]+
```

This is often enough for extraction from ordinary text.

Example:

```python
text = """
Read https://example.com/docs
and https://example.org/tutorial
"""

urls = re.findall(r"https?://[^\s]+", text)

print(urls)
```

Output:

```text
['https://example.com/docs', 'https://example.org/tutorial']
```

Do not assume this is a complete URL validator.

URLs have complex grammar and edge cases.

For serious URL parsing, Python's `urllib.parse` is often a better choice.

---

# 36. Regex for File Names

Suppose you have:

```text
report_2026.csv
sales_2025.xlsx
notes.txt
image.png
```

To extract the extension:

```regex
\.([A-Za-z0-9]+)$
```

Example:

```python
match = re.search(r"\.([A-Za-z0-9]+)$", "report_2026.csv")

if match:
    print(match.group(1))
```

Output:

```text
csv
```

For filesystem work, however, Python's `pathlib` is often preferable.

Regex is useful when file names are part of a larger text-processing workflow.

---

# 37. Regex for Structured IDs

Suppose your company uses IDs like:

```text
ORD-2026-000001
ORD-2026-000002
USR-2026-000381
```

Pattern:

```regex
(?P<type>ORD|USR)-(?P<year>\d{4})-(?P<number>\d{6})
```

This lets us extract:

```python
{
    "type": "ORD",
    "year": "2026",
    "number": "000381"
}
```

This is a great example of why groups matter.

---

# 38. Regex for Password Rules

Regex can check structural requirements.

Suppose a password must:

- contain at least 8 characters
- contain a lowercase letter
- contain an uppercase letter
- contain a digit

A lookahead-based pattern can be:

```regex
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$
```

Python:

```python
pattern = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
)

print(bool(pattern.fullmatch("Password1")))
```

---

## Important security note

Password validation is not the same as password security.

Regex can check syntax.

It does not make passwords secure.

A production authentication system should also consider:

- secure password hashing
- rate limiting
- account protection
- password policies
- breached-password detection
- secure storage

---

# 39. Regex for Dates and Times

A common date pattern:

```regex
\d{4}-\d{2}-\d{2}
```

matches:

```text
2026-08-23
```

But it also matches invalid dates such as:

```text
9999-99-99
```

This is an important lesson:

> **Pattern validity is not necessarily semantic validity.**

Regex can check the shape.

A date library should check whether the date actually exists.

Example:

```python
from datetime import datetime

datetime.strptime("2026-08-23", "%Y-%m-%d")
```

Regex and parsers can work together.

---

# 40. Regex for Data Pipelines

A typical text-processing pipeline might look like:

```text
Raw text
   ↓
Normalize
   ↓
Find candidate patterns
   ↓
Extract structured values
   ↓
Validate values
   ↓
Transform values
   ↓
Store structured data
```

For example:

```text
log line
   ↓
regex extraction
   ↓
dictionary
   ↓
Pandas DataFrame
   ↓
analysis
```

Regex is often one component of a larger software system.

---

# 41. Project 1 - Extract Information

## Difficulty: Beginner

Given:

```python
text = """
Alice paid $120 for order ORD-2026-000123.
Bob paid $89 for order ORD-2026-000124.
Charlie paid $450 for order ORD-2026-000125.
"""
```

Extract all:

- names
- prices
- order IDs

---

## Step 1 - Extract order IDs

Expected:

```text
ORD-2026-000123
ORD-2026-000124
ORD-2026-000125
```

Use:

```regex
ORD-\d{4}-\d{6}
```

---

## Step 2 - Extract prices

Use:

```regex
\$\d+
```

---

## Step 3 - Extract names

Use an appropriate word-based pattern.

---

## Step 4 - Combine the extraction

Try to create structured records:

```python
[
    {
        "name": "Alice",
        "price": 120,
        "order_id": "ORD-2026-000123"
    },
    ...
]
```

---

# 42. Project 2 - Contact Information Extractor

## Difficulty: Beginner → Intermediate

Given:

```python
text = """
Contact Alice at alice@example.com or +91-98765-43210.
Contact Bob at bob@example.org or +1-202-555-0147.
"""
```

Build a utility that extracts:

- email addresses
- phone numbers
- names

---

## Requirements

Create:

```python
def extract_contacts(text):
    ...
```

Return:

```python
[
    {
        "name": "...",
        "email": "...",
        "phone": "..."
    }
]
```

---

## Extension

Handle:

```text
Alice <alice@example.com>
Bob <bob@example.org>
```

and:

```text
alice@example.com
```

without a phone number.

The important lesson is that real text is rarely perfectly uniform.

---

# 43. Project 3 - Log Analyzer

## Difficulty: Intermediate

Use this dataset:

```python
logs = """
2026-08-23 10:01:12 [INFO] user=alice request_id=req001 message="Login successful"
2026-08-23 10:02:18 [ERROR] user=bob request_id=req002 message="Database timeout"
2026-08-23 10:03:44 [WARNING] user=alice request_id=req003 message="Rate limit approaching"
2026-08-23 10:04:51 [ERROR] user=charlie request_id=req004 message="Payment failed"
"""
```

Build a parser.

---

## Requirements

Extract:

```text
timestamp
level
user
request_id
message
```

Return a list of dictionaries.

---

## Bonus

Convert the result into a Pandas DataFrame.

Then answer:

- How many errors?
- Which users generated errors?
- Which error messages occurred?
- How many events occurred at each severity?

This demonstrates how regex can become part of a data-analysis pipeline.

---

# 44. Project 4 - Data Cleaner

## Difficulty: Intermediate

Build a text-cleaning utility.

Requirements:

```python
def clean_text(text):
    ...
```

It should:

1. remove leading/trailing whitespace
2. collapse repeated whitespace
3. normalize line endings
4. optionally remove URLs
5. optionally remove punctuation
6. preserve meaningful words

Example:

```text
"   Hello    world!\n\nVisit https://example.com   "
```

could become:

```text
"Hello world! Visit"
```

depending on your chosen options.

---

## Design challenge

Do not create one giant regex.

Prefer several small, understandable transformations.

For example:

```python
text = re.sub(...)
text = re.sub(...)
text = ...
```

Readable pipelines are easier to debug.

---

# 45. Project 5 - URL and Link Scanner

## Difficulty: Intermediate

Given a large block of text, find URLs.

Requirements:

- detect `http://`
- detect `https://`
- extract the entire URL
- remove trailing punctuation when appropriate

Example:

```text
Read https://example.com/docs.
Then visit https://example.org/tutorial!
```

Potential output:

```text
https://example.com/docs
https://example.org/tutorial
```

---

## Extension

Write:

```python
def extract_urls(text):
    ...
```

Then test it against:

- parentheses
- punctuation
- query strings
- fragments
- URLs on separate lines

Think carefully about where a URL ends.

---

# 46. Project 6 - Input Validator

## Difficulty: Intermediate

Create validators for:

```python
is_valid_username()
is_valid_order_id()
is_valid_email()
is_valid_phone()
is_valid_date_format()
```

Each should return:

```python
True
```

or:

```python
False
```

---

## Example

```python
def is_valid_order_id(value):
    pattern = r"ORD-\d{4}-\d{6}"
    return bool(re.fullmatch(pattern, value))
```

---

## Test-driven requirement

For every validator, create:

### Valid examples

At least five.

### Invalid examples

At least five.

This is an important software-engineering habit:

> A regex is not finished when it matches the first example. It is finished when its behavior has been tested against representative cases and edge cases.

---

# 47. Project 7 - Markdown Scanner

## Difficulty: Intermediate → Advanced

Build a simple Markdown scanner.

Given:

```markdown
# Introduction

This is a paragraph.

## Python

Learn Python at https://python.org.

- item one
- item two

**important**
```

Extract:

- headings
- links
- bullet points
- bold text

---

## Heading pattern

A simple starting point:

```regex
^#{1,6}\s+(.+)$
```

Use:

```python
re.MULTILINE
```

---

## Link pattern

Markdown links look like:

```markdown
[Python](https://python.org)
```

A basic pattern:

```regex
\[([^\]]+)\]\(([^)]+)\)
```

Capture:

1. link text
2. URL

---

## Extension

Return structured data:

```python
{
    "headings": [...],
    "links": [...],
    "bullets": [...],
    "bold": [...]
}
```

---

# 48. Project 8 - Mini Search Engine

## Difficulty: Advanced

Build a small text-search utility.

Given a collection of documents:

```python
documents = {
    "doc1": "Python is useful for data science.",
    "doc2": "Regex is useful for text processing.",
    "doc3": "Python and regex can work together."
}
```

Create:

```python
search_documents(query)
```

The function should:

1. search case-insensitively
2. return matching documents
3. highlight matching terms
4. count occurrences
5. return match positions

---

## Extension

Allow simple wildcard-like queries.

For example:

```text
pyth*
```

could be converted into an appropriate regex.

Be careful about regex injection and unintended patterns.

---

# 49. Project 9 - PII Detection

## Difficulty: Advanced

Build a basic detector for potentially sensitive information.

Look for patterns resembling:

- email addresses
- phone numbers
- dates
- IP addresses
- credit-card-like sequences

Example:

```python
text = """
User: alice@example.com
Phone: +91-98765-43210
IP: 192.168.1.25
"""
```

Return:

```python
{
    "emails": [...],
    "phones": [...],
    "ips": [...]
}
```

---

## Extension: Redaction

Replace detected values with placeholders.

Example:

```text
User: [EMAIL]
Phone: [PHONE]
IP: [IP]
```

---

## Important

A regex detector should not be described as a perfect security system.

False positives and false negatives are possible.

Sensitive-data handling also requires:

- access control
- secure logging
- retention policies
- encryption
- appropriate privacy practices

---

# 50. Project 10 - Final Regex Toolkit

## Difficulty: Advanced

Build a reusable Python module.

Suggested structure:

```text
regex_toolkit/
│
├── patterns.py
├── extractors.py
├── validators.py
├── cleaners.py
├── tests/
│   └── test_regex_toolkit.py
└── README.md
```

---

## `patterns.py`

Store reusable compiled patterns.

Example:

```python
EMAIL_PATTERN = re.compile(...)
ORDER_ID_PATTERN = re.compile(...)
PHONE_PATTERN = re.compile(...)
```

---

## `extractors.py`

Functions:

```python
extract_emails()
extract_phones()
extract_order_ids()
extract_urls()
extract_dates()
```

---

## `validators.py`

Functions:

```python
is_valid_email()
is_valid_phone()
is_valid_order_id()
```

---

## `cleaners.py`

Functions:

```python
normalize_whitespace()
remove_urls()
redact_emails()
normalize_phone()
```

---

## Tests

Write tests for:

- normal input
- empty input
- malformed input
- Unicode text
- repeated matches
- edge cases
- unexpected punctuation

This is where regex becomes software engineering rather than syntax practice.

---

# 51. Debugging Regex

Regex debugging is a skill.

When a pattern fails, do not immediately make it more complicated.

Use a systematic process.

---

## Step 1 - Start with the smallest possible example

Instead of:

```text
a 500-line log file
```

start with:

```text
ERROR
```

---

## Step 2 - Test one requirement

If you need:

```text
ORD-2026-000123
```

first test:

```regex
ORD
```

Then:

```regex
ORD-\d+
```

Then:

```regex
ORD-\d{4}
```

Then:

```regex
ORD-\d{4}-\d{6}
```

Build incrementally.

---

## Step 3 - Inspect match spans

Use:

```python
match.span()
```

to understand exactly what matched.

---

## Step 4 - Inspect groups

Use:

```python
match.groups()
```

or:

```python
match.groupdict()
```

---

## Step 5 - Test negative examples

A good regex should not only match valid examples.

It should reject or avoid incorrect examples.

---

## Step 6 - Add comments

For complex patterns, use `re.VERBOSE`.

Example:

```python
pattern = re.compile(
    r"""
    (?P<year>\d{4})      # year
    -
    (?P<month>\d{2})     # month
    -
    (?P<day>\d{2})       # day
    """,
    re.VERBOSE
)
```

This is much easier to maintain.

---

# 52. Performance and Safety

Regex can be extremely fast.

It can also become surprisingly expensive.

One important issue is **catastrophic backtracking** in patterns with ambiguous nested repetition.

Patterns involving combinations like:

```regex
(a+)+
```

or:

```regex
(.*)+
```

can become problematic on carefully chosen input.

---

## Practical rules

Prefer:

```regex
\d+
```

over:

```regex
.*
```

when you know the content is numeric.

Prefer:

```regex
[^"]*
```

when extracting text inside quotes rather than:

```regex
.*?
```

when the structure gives you a clear delimiter.

---

## Principle

> **The more specific the pattern, the easier it is to reason about.**

Specific patterns are generally easier to:

- test
- maintain
- debug
- optimize
- trust

---

# 53. When Not to Use Regex

This is one of the most important sections.

Regex is not the correct tool for every text problem.

---

## Do not use regex to parse complex HTML

HTML has nesting and grammar.

Use an HTML parser.

---

## Do not use regex as a full JSON parser

Use:

```python
import json
```

and:

```python
json.loads(...)
```

---

## Do not use regex as a full URL parser

Use:

```python
from urllib.parse import urlparse
```

---

## Do not use regex to validate real calendar semantics

Regex can check:

```text
YYYY-MM-DD
```

A date library can determine whether the date actually exists.

---

## Do not create giant regexes unnecessarily

If your pattern becomes hundreds of characters long and contains deeply nested logic, ask:

> "Would a parser or ordinary Python code be clearer?"

---

# 54. Regex Design Principles

## Principle 1 - Start from the data

Do not start by writing symbols.

First understand the input.

Ask:

- What does the text look like?
- Is it structured?
- Is the structure consistent?
- What variations exist?
- What should count as a match?
- What should not count as a match?

---

## Principle 2 - Define examples first

Before writing the pattern, make a test table.

| Input | Should match? |
|---|---|
| `ORD-2026-000001` | Yes |
| `ORD-2026-123456` | Yes |
| `ORD-26-123456` | No |
| `USER-2026-000001` | No |
| `ORD-2026-ABCDEF` | No |

Then build the regex.

---

## Principle 3 - Prefer readable patterns

This:

```regex
(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})
```

is easier to understand than an unnecessarily clever equivalent.

---

## Principle 4 - Separate extraction and validation

Finding:

```text
2026-99-99
```

and validating:

```text
2026-99-99
```

are different tasks.

Regex can extract.

A date parser can validate semantics.

---

## Principle 5 - Use named groups for important fields

Prefer:

```regex
(?P<email>...)
```

over relying on:

```python
group(7)
```

in complex patterns.

---

## Principle 6 - Test edge cases

Think about:

- empty strings
- whitespace
- punctuation
- Unicode
- very long strings
- missing fields
- duplicate values
- unexpected separators
- malformed input

---

# 55. Final Assessment

Complete the following without copying examples directly.

---

## Part A - Syntax

Write regex patterns for:

1. exactly five digits
2. one or more lowercase letters
3. a word beginning with `A`
4. a string ending with `.csv`
5. an ID such as `USR-2026-123456`
6. either `cat` or `dog`
7. a repeated word
8. a number immediately followed by `USD`
9. a number immediately preceded by `$`
10. a string containing at least one digit

---

## Part B - Python API

Explain the difference between:

```python
re.match()
re.search()
re.fullmatch()
re.findall()
re.finditer()
re.split()
re.sub()
```

Give one example for each.

---

## Part C - Extraction

Given:

```text
Alice <alice@example.com> placed order ORD-2026-000123 for $599.
```

Extract:

```text
Alice
alice@example.com
ORD-2026-000123
599
```

Use named groups.

---

## Part D - Validation

Build:

```python
is_valid_order_id()
is_valid_username()
is_valid_phone()
```

Each must have at least ten tests.

---

## Part E - Parsing

Parse:

```text
2026-08-23 14:42:01 [ERROR] user=alice request_id=req-192 message="Payment failed"
```

into:

```python
{
    "timestamp": "2026-08-23 14:42:01",
    "level": "ERROR",
    "user": "alice",
    "request_id": "req-192",
    "message": "Payment failed"
}
```

---

## Part F - Architecture

Design a small package called:

```text
text_tools
```

that provides:

```python
extract_emails()
extract_urls()
extract_order_ids()
redact_emails()
normalize_whitespace()
is_valid_order_id()
parse_log_line()
```

Explain:

- file structure
- responsibilities
- testing strategy
- error handling
- performance considerations

---

# 56. Final Cheat Sheet

## Character classes

```regex
[abc]       # a, b, or c
[a-z]       # lowercase range
[A-Z]       # uppercase range
[0-9]       # digit range
[^abc]      # anything except a, b, c
```

---

## Shorthand classes

```regex
\d          # digit
\D          # non-digit
\w          # word character
\W          # non-word character
\s          # whitespace
\S          # non-whitespace
.           # almost any character
```

---

## Quantifiers

```regex
*           # zero or more
+           # one or more
?           # zero or one
{3}         # exactly 3
{3,}        # 3 or more
{3,7}       # 3 through 7
```

---

## Anchors

```regex
^           # beginning
$           # end
\b          # word boundary
\B          # non-word boundary
```

---

## Groups

```regex
(...)           # capture
(?:...)         # non-capturing group
(?P<name>...)   # named group
\1              # backreference
```

---

## Alternation

```regex
cat|dog
```

---

## Lookarounds

```regex
(?=...)         # positive lookahead
(?!...)         # negative lookahead
(?<=...)        # positive lookbehind
(?<!...)        # negative lookbehind
```

---

## Python functions

```python
re.match()
re.search()
re.fullmatch()
re.findall()
re.finditer()
re.split()
re.sub()
re.subn()
re.compile()
```

---

## Flags

```python
re.IGNORECASE
re.MULTILINE
re.DOTALL
re.VERBOSE
re.ASCII
```

---

# The Regex Mental Model

When you see a text-processing problem, think in this order:

```text
1. What exactly am I trying to find?
              ↓
2. What does a valid example look like?
              ↓
3. What invalid examples must be rejected?
              ↓
4. What parts are fixed?
              ↓
5. What parts vary?
              ↓
6. What character classes describe the variation?
              ↓
7. How many characters can occur?
              ↓
8. Where must the match begin/end?
              ↓
9. Do I need groups?
              ↓
10. Do I need lookarounds?
              ↓
11. Can I test the pattern against edge cases?
              ↓
12. Is regex actually the right tool?
```

---

# Final Takeaway

Regex is best understood as a **small language for describing text structure**.

You should be able to look at:

```text
ORD-2026-000123
```

and reason:

```text
ORD
+
-
+
four digits
+
-
+
six digits
```

which becomes:

```regex
ORD-\d{4}-\d{6}
```

Then you should be able to move from:

```text
pattern
```

to:

```text
search
```

to:

```text
extract
```

to:

```text
validate
```

to:

```text
transform
```

to:

```text
structured software
```

That progression is the real purpose of this tutorial.

The objective of Phase 2 is not merely to learn another Python library.

It is to learn how to turn **messy real-world text into reliable software inputs**.

Regex is one of the foundational tools for doing exactly that.

---

# Recommended Practice Loop

For every regex problem you encounter:

```text
Understand the input
        ↓
Write examples
        ↓
Define expected matches
        ↓
Write the smallest pattern
        ↓
Test positive cases
        ↓
Test negative cases
        ↓
Add complexity gradually
        ↓
Name important groups
        ↓
Measure/debug behavior
        ↓
Ask whether a parser is better
        ↓
Document the pattern
```

If you can consistently follow this process, you are no longer merely memorizing regex syntax.

You are **engineering text-processing systems**.
