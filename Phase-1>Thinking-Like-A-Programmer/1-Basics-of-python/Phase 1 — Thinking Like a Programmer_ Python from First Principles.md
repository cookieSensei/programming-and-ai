# Phase 1 - Thinking Like a Programmer

## Python from First Principles

Phase 0 taught you how to work with a computer as a developer:

- how files and folders work
- how to use the terminal
- how to run programs
- how to use Git and GitHub
- how to save meaningful checkpoints of your work

Now we are going to learn how to **think like a programmer**.

This phase is not about memorizing Python syntax.

It is about learning how to take a problem that exists in the real world and turn it into a sequence of precise instructions that a computer can execute.

The language we will use is **Python**.

Python is a good language for this because its syntax is relatively readable, but the underlying ideas you learn here apply far beyond Python.

By the end of Phase 1, you should be able to look at a problem and think:

```text
What information do I have?
        ↓
What information do I need?
        ↓
What transformations need to happen?
        ↓
What decisions need to be made?
        ↓
What should repeat?
        ↓
How should I organize the solution?
        ↓
How can I test whether it works?
```

That way of thinking is more important than any individual Python command.

---

# 1. What Is Programming?

Programming is the process of giving a computer a precise set of instructions for solving a problem.

Humans are very good at interpreting vague instructions.

Computers are not.

If you tell a person:

> "Make me some tea."

They can fill in many missing details.

They might assume:

1. Find a cup.
2. Put tea in it.
3. Boil water.
4. Pour the water into the cup.
5. Wait.
6. Add milk if appropriate.

A computer cannot safely make those assumptions.

A computer needs explicit instructions.

Programming is therefore partly the art of turning:

```text
Human intention
```

into:

```text
Precise instructions
```

---

# 2. Programming Is Problem Decomposition

Suppose you want to build a program that calculates the total price of an order.

The human-level problem is:

> "Calculate the order total."

But the computer needs smaller steps.

We might decompose it into:

```text
Get item prices
        ↓
Get quantities
        ↓
Multiply each price by its quantity
        ↓
Add the results
        ↓
Apply tax
        ↓
Display total
```

This process is called **decomposition**.

You take one large problem and break it into smaller problems.

This is one of the most important programming skills you can develop.

---

# 3. Algorithms

An **algorithm** is a sequence of steps for solving a problem.

For example, suppose we want to determine whether a number is even.

We can describe the algorithm:

```text
Take a number
      ↓
Divide it by 2
      ↓
Look at the remainder
      ↓
If remainder = 0
    → even
Otherwise
    → odd
```

In Python:

```python
number = 17

if number % 2 == 0:
    print("Even")
else:
    print("Odd")
```

The Python code is simply one representation of the underlying algorithm.

---

# 4. Programming Languages

Computers ultimately execute machine instructions.

Humans generally do not want to write programs directly as machine instructions.

Programming languages provide a more understandable way to express instructions.

For example:

```python
total = price * quantity
```

is much easier for a human to understand than the low-level instructions the computer eventually executes.

Python is one programming language.

Other languages include:

- JavaScript
- Java
- C
- C++
- C#
- Go
- Rust
- Swift
- Kotlin

The syntax differs, but many programming concepts remain the same.

---

# 5. Why Python?

Python is widely used in:

- web development
- automation
- data analysis
- artificial intelligence
- machine learning
- scientific computing
- scripting
- education
- backend systems

But the main reason we are using Python in this curriculum is its readability.

For example:

```python
if age >= 18:
    print("Adult")
```

The code is relatively close to the way a person might describe the logic.

That makes Python a useful language for learning programming concepts.

---

# 6. Your First Python Program

Create a file called:

```text
hello.py
```

Put this inside:

```python
print("Hello, world!")
```

Run it:

```bash
python hello.py
```

You should see:

```text
Hello, world!
```

You have just written a program.

The program contains one instruction:

> Print the text "Hello, world!"

---

# 7. Python Files

Python programs normally use the `.py` extension.

Examples:

```text
hello.py
calculator.py
game.py
analysis.py
server.py
```

A Python file contains Python source code.

You can execute it with:

```bash
python filename.py
```

For example:

```bash
python calculator.py
```

---

# 8. `print()`

The `print()` function displays information.

For example:

```python
print("Hello")
```

You can print multiple things:

```python
print("Hello")
print("Welcome to Python")
print("We are learning programming")
```

The output is:

```text
Hello
Welcome to Python
We are learning programming
```

Each `print()` produces output.

---

# 9. Strings

Text in Python is represented using **strings**.

Examples:

```python
"Hello"
"Python"
"CookieSensei"
"I am learning programming"
```

Strings can use either single or double quotation marks:

```python
"Hello"
```

or:

```python
'Hello'
```

Both represent strings.

Pick a style and be consistent.

---

# 10. Numbers

Python can work with numbers.

For example:

```python
10
25
3.14
-7
0
```

There are two important numeric types you will encounter immediately:

### Integers

Whole numbers:

```python
10
42
-3
```

### Floating-point numbers

Numbers containing a decimal component:

```python
3.14
9.5
0.25
```

---

# 11. Arithmetic

Python can perform arithmetic.

```python
print(10 + 5)
```

Output:

```text
15
```

Subtraction:

```python
print(10 - 5)
```

Multiplication:

```python
print(10 * 5)
```

Division:

```python
print(10 / 5)
```

Exponentiation:

```python
print(2 ** 3)
```

Output:

```text
8
```

---

# 12. Division and the Remainder

Python has a few operators for division.

Normal division:

```python
10 / 3
```

Result:

```text
3.3333333333333335
```

Floor division:

```python
10 // 3
```

Result:

```text
3
```

Remainder:

```python
10 % 3
```

Result:

```text
1
```

The `%` operator is called the **modulo operator**.

It is extremely useful.

For example:

```python
number % 2
```

can help determine whether a number is even or odd.

---

# 13. Expressions

An expression is something Python can evaluate to produce a value.

Examples:

```python
10 + 5
```

```python
price * quantity
```

```python
age >= 18
```

```python
name.upper()
```

Expressions are the building blocks of programs.

---

# 14. Variables

A variable gives a name to a value.

For example:

```python
name = "Alice"
```

Now `name` refers to the string:

```text
Alice
```

We can use it:

```python
print(name)
```

Output:

```text
Alice
```

Variables allow programs to remember information.

---

# 15. Assignment

This:

```python
age = 25
```

does not mean:

> "age is mathematically equal to 25 forever."

It means:

> "Store the value 25 under the name `age`."

We can then change it:

```python
age = 26
```

Now `age` refers to `26`.

This operation is called **assignment**.

---

# 16. Variable Names

Good variable names communicate meaning.

Good:

```python
user_name = "Alice"
age = 25
total_price = 49.99
number_of_students = 30
```

Bad:

```python
x = "Alice"
a = 25
thing = 49.99
n = 30
```

Short names are sometimes appropriate, but meaningful names are usually easier to understand.

Compare:

```python
x = price * quantity
```

with:

```python
total_price = price * quantity
```

The second one communicates more information.

---

# 17. Naming Conventions

Python commonly uses **snake_case** for variable names.

Examples:

```python
first_name
last_name
total_price
number_of_students
is_logged_in
```

Avoid:

```python
firstName
TotalPrice
numberofstudents
```

Python also distinguishes uppercase and lowercase.

These are different:

```python
name
Name
NAME
```

---

# 18. Types

Every value in Python has a type.

For example:

```python
name = "Alice"
age = 25
price = 19.99
```

The values have different types.

You can inspect a type using:

```python
type(name)
```

or:

```python
print(type(name))
```

You might see:

```text
<class 'str'>
```

For the number:

```python
print(type(age))
```

you might see:

```text
<class 'int'>
```

---

# 19. Common Python Types

You should become familiar with these:

```text
str
int
float
bool
list
tuple
dict
set
NoneType
```

We will study them throughout Phase 1.

---

# 20. Booleans

A Boolean represents one of two values:

```python
True
False
```

For example:

```python
is_logged_in = True
```

or:

```python
is_admin = False
```

Booleans are fundamental to decision-making.

---

# 21. Comparisons

Python can compare values.

For example:

```python
age = 20

print(age > 18)
```

Output:

```text
True
```

Other comparison operators include:

```python
>
<
>=
<=
==
!=
```

Examples:

```python
10 > 5
10 < 5
10 >= 10
10 <= 10
10 == 10
10 != 5
```

Each expression produces a Boolean.

---

# 22. `=` vs `==`

This is one of the most important beginner distinctions.

Assignment:

```python
age = 20
```

Comparison:

```python
age == 20
```

The first means:

> Store 20 in `age`.

The second means:

> Is `age` equal to 20?

They are completely different operations.

---

# 23. Logical Operators

Python provides:

```python
and
or
not
```

For example:

```python
age >= 18 and age <= 65
```

This is true only if both conditions are true.

Another example:

```python
is_admin or is_owner
```

This is true if either condition is true.

And:

```python
not is_logged_in
```

reverses the Boolean value.

---

# 24. Conditional Statements

Programs often need to make decisions.

For example:

> If the user is old enough, allow access.

Python:

```python
age = 20

if age >= 18:
    print("Access granted")
```

The `if` statement allows your program to make a decision.

---

# 25. `else`

Sometimes we need an alternative.

```python
age = 16

if age >= 18:
    print("Access granted")
else:
    print("Access denied")
```

The program chooses one path.

Conceptually:

```text
             age >= 18?
              /     \
            yes      no
             ↓        ↓
          allow     deny
```

---

# 26. `elif`

You can have multiple conditions.

```python
score = 85

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
else:
    print("Needs improvement")
```

Python checks conditions from top to bottom.

Once one condition is true, the remaining branches are skipped.

---

# 27. Indentation

Python uses indentation to define blocks of code.

For example:

```python
if age >= 18:
    print("Adult")
```

The indented line belongs to the `if`.

This is not valid:

```python
if age >= 18:
print("Adult")
```

Indentation is part of Python's syntax.

Use four spaces for indentation.

Most editors will handle this automatically.

---

# 28. Nested Conditions

You can place conditions inside other conditions.

For example:

```python
age = 25
has_ticket = True

if age >= 18:
    if has_ticket:
        print("Enter")
```

However, deeply nested code can become difficult to understand.

As you become more experienced, you will learn ways to simplify complicated logic.

---

# 29. Input

Programs become much more interesting when they interact with users.

Python's `input()` function lets you receive text from the user.

```python
name = input("What is your name? ")

print("Hello", name)
```

If the user enters:

```text
Alice
```

the program prints:

```text
Hello Alice
```

---

# 30. Important: `input()` Returns a String

This surprises many beginners.

Suppose you write:

```python
age = input("How old are you? ")
```

Even if the user types:

```text
25
```

Python gives you:

```text
"25"
```

not:

```python
25
```

The result is a string.

This matters when doing arithmetic.

---

# 31. Converting Types

Suppose we want an integer.

We can use:

```python
age = int(input("How old are you? "))
```

Now `age` is an integer.

Similarly:

```python
price = float(input("Price: "))
```

converts the input to a floating-point number.

---

# 32. Type Conversion

Common conversion functions include:

```python
int()
float()
str()
bool()
```

Examples:

```python
int("42")
```

```python
float("3.14")
```

```python
str(42)
```

Be careful.

Not every string can become a number.

This works:

```python
int("42")
```

This does not:

```python
int("hello")
```

It raises an error.

---

# 33. F-Strings

Python provides a convenient way to construct strings.

Instead of:

```python
name = "Alice"
age = 25

print("My name is " + name + " and I am " + str(age))
```

you can write:

```python
print(f"My name is {name} and I am {age}")
```

This is called an **f-string**.

It is one of the most useful ways to format text in Python.

---

# 34. Your First Real Program

Let's combine what we have learned.

```python
name = input("What is your name? ")
age = int(input("How old are you? "))

if age >= 18:
    status = "an adult"
else:
    status = "not an adult"

print(f"Hello {name}. You are {status}.")
```

This program:

1. asks for a name
2. asks for an age
3. converts the age to an integer
4. makes a decision
5. creates a message
6. prints the result

This is programming.

---

# 35. Lists

So far, variables have stored individual values.

But what if we have many values?

For example:

```text
Alice
Bob
Charlie
David
```

A list lets us store multiple values.

```python
names = ["Alice", "Bob", "Charlie", "David"]
```

---

# 36. Accessing List Elements

Python uses zero-based indexing.

That means the first element is index `0`.

```python
names = ["Alice", "Bob", "Charlie"]
```

Then:

```python
names[0]
```

is:

```text
Alice
```

```python
names[1]
```

is:

```text
Bob
```

```python
names[2]
```

is:

```text
Charlie
```

---

# 37. Why Does Python Start at Zero?

This can feel strange.

Think of an index as an offset from the beginning.

The first element has an offset of zero:

```text
Index:   0       1        2
        Alice    Bob    Charlie
```

You will encounter zero-based indexing frequently in programming.

---

# 38. Negative Indexing

Python also supports negative indexes.

```python
names[-1]
```

returns the last element.

For:

```python
names = ["Alice", "Bob", "Charlie"]
```

we get:

```python
names[-1]
```

→ `"Charlie"`

and:

```python
names[-2]
```

→ `"Bob"`

---

# 39. Changing List Elements

Lists are mutable.

For example:

```python
names = ["Alice", "Bob", "Charlie"]

names[1] = "Robert"
```

Now:

```python
print(names)
```

produces:

```text
['Alice', 'Robert', 'Charlie']
```

---

# 40. Adding to Lists

Use:

```python
append()
```

Example:

```python
names = ["Alice", "Bob"]

names.append("Charlie")
```

Now:

```python
print(names)
```

gives:

```text
['Alice', 'Bob', 'Charlie']
```

---

# 41. Removing from Lists

You can use:

```python
remove()
```

For example:

```python
names.remove("Bob")
```

You can also use:

```python
pop()
```

For example:

```python
names.pop()
```

This removes and returns the last element.

---

# 42. List Length

Use:

```python
len()
```

Example:

```python
names = ["Alice", "Bob", "Charlie"]

print(len(names))
```

Output:

```text
3
```

---

# 43. Membership

You can ask whether a value exists in a list.

```python
names = ["Alice", "Bob", "Charlie"]

print("Alice" in names)
```

Output:

```text
True
```

And:

```python
print("David" in names)
```

returns:

```text
False
```

---

# 44. Loops

Now we reach one of the most important programming concepts:

**repetition.**

Suppose you want to print every name.

You could write:

```python
print(names[0])
print(names[1])
print(names[2])
```

But this does not scale.

What if there are 10,000 names?

We need a loop.

---

# 45. `for` Loops

Python's `for` loop allows us to iterate over a collection.

```python
names = ["Alice", "Bob", "Charlie"]

for name in names:
    print(name)
```

Output:

```text
Alice
Bob
Charlie
```

The loop says:

> For each item in `names`, temporarily call that item `name`, then execute the indented code.

---

# 46. How a `for` Loop Works

Conceptually:

```text
names
  ↓
Alice → print
  ↓
Bob → print
  ↓
Charlie → print
```

This is one of the most important ideas in programming:

> **Do something once for every item in a collection.**

---

# 47. `range()`

Sometimes we want to repeat something a specific number of times.

Python provides:

```python
range()
```

For example:

```python
for number in range(5):
    print(number)
```

Output:

```text
0
1
2
3
4
```

Notice that `5` itself is not included.

---

# 48. `range(start, stop)`

You can specify a starting value:

```python
for number in range(1, 6):
    print(number)
```

Output:

```text
1
2
3
4
5
```

The stop value is exclusive.

This is an important Python convention.

---

# 49. `while` Loops

A `while` loop repeats while a condition remains true.

```python
count = 0

while count < 5:
    print(count)
    count += 1
```

Output:

```text
0
1
2
3
4
```

The loop continues while:

```python
count < 5
```

is true.

---

# 50. Infinite Loops

Be careful.

This loop never ends:

```python
count = 0

while count < 5:
    print(count)
```

Why?

Because `count` never changes.

The condition remains true forever.

A `while` loop must generally have some path toward making its condition false.

---

# 51. `break`

You can stop a loop early with:

```python
break
```

Example:

```python
for number in range(10):
    if number == 5:
        break

    print(number)
```

Output:

```text
0
1
2
3
4
```

---

# 52. `continue`

`continue` skips the rest of the current iteration.

Example:

```python
for number in range(5):
    if number == 2:
        continue

    print(number)
```

Output:

```text
0
1
3
4
```

The number `2` is skipped.

---

# 53. Dictionaries

Lists are useful when we have an ordered collection of values.

But sometimes we want to associate one piece of information with another.

For example:

```text
name → Alice
age → 25
city → Delhi
```

A Python dictionary can represent this:

```python
person = {
    "name": "Alice",
    "age": 25,
    "city": "Delhi"
}
```

---

# 54. Accessing Dictionary Values

You can access a value using its key:

```python
print(person["name"])
```

Output:

```text
Alice
```

Another:

```python
print(person["age"])
```

Output:

```text
25
```

The key identifies the value.

---

# 55. Adding Dictionary Values

You can add:

```python
person["occupation"] = "Developer"
```

Now the dictionary contains the new information.

---

# 56. Updating Values

You can update:

```python
person["age"] = 26
```

The existing value is replaced.

---

# 57. Dictionary Methods

Useful methods include:

```python
person.keys()
```

```python
person.values()
```

```python
person.items()
```

For example:

```python
for key, value in person.items():
    print(key, value)
```

---

# 58. Tuples

A tuple is another collection type.

Example:

```python
coordinates = (10, 20)
```

Tuples are generally immutable.

That means you cannot change an element like this:

```python
coordinates[0] = 50
```

This will fail.

Tuples are useful when you want a collection whose values should not be modified.

---

# 59. Sets

A set stores unique values.

```python
numbers = {1, 2, 3, 3, 3}
```

The result contains:

```text
{1, 2, 3}
```

Duplicates are removed.

Sets are useful for operations involving uniqueness and membership.

---

# 60. Choosing a Data Structure

You should start thinking about **why** you are choosing a particular structure.

Use a:

### List

When you have an ordered collection of items.

```python
students = ["Alice", "Bob", "Charlie"]
```

### Dictionary

When you have key-value relationships.

```python
student = {
    "name": "Alice",
    "age": 20
}
```

### Set

When uniqueness matters.

```python
unique_tags = {"python", "ai", "web"}
```

### Tuple

When you want a fixed collection of values.

```python
point = (10, 20)
```

Choosing the right data structure is part of problem solving.

---

# 61. Functions

As programs grow, putting everything into one large file of instructions becomes difficult.

Functions let us package reusable logic.

For example:

```python
def greet():
    print("Hello!")
```

We can call it:

```python
greet()
```

---

# 62. Functions With Parameters

Functions become much more useful when they accept inputs.

```python
def greet(name):
    print(f"Hello, {name}!")
```

Then:

```python
greet("Alice")
greet("Bob")
```

Output:

```text
Hello, Alice!
Hello, Bob!
```

The parameter `name` receives a value when the function is called.

---

# 63. Return Values

Functions can produce values.

```python
def add(a, b):
    return a + b
```

Now:

```python
result = add(10, 5)
```

`result` becomes:

```text
15
```

This is different from simply printing.

---

# 64. `print()` vs `return`

Consider:

```python
def add(a, b):
    print(a + b)
```

This displays the result.

But:

```python
def add(a, b):
    return a + b
```

gives the result back to the code that called the function.

For example:

```python
result = add(10, 5)
```

Now we can use `result`:

```python
print(result)
```

or:

```python
if result > 10:
    print("Large result")
```

Returning values generally makes functions more reusable.

---

# 65. Function Design

A good function usually does one clear thing.

Good:

```python
def calculate_total(price, quantity):
    return price * quantity
```

Less clear:

```python
def do_everything():
    ...
```

As programs grow, functions help create boundaries between different responsibilities.

---

# 66. Scope

Variables have a scope.

Consider:

```python
def greet():
    message = "Hello"
    print(message)
```

The variable `message` exists inside the function.

Trying to use it outside:

```python
print(message)
```

will fail because `message` is local to the function.

Understanding scope becomes increasingly important as your programs grow.

---

# 67. Modules

A Python file can contain reusable code.

Suppose you have:

```text
calculator.py
```

containing:

```python
def add(a, b):
    return a + b
```

Another file can import it:

```python
from calculator import add

print(add(10, 5))
```

This is the beginning of organizing programs into multiple modules.

---

# 68. Why Modules Matter

Imagine a project containing:

```text
app.py
database.py
users.py
payments.py
email.py
```

Instead of putting every function into one enormous file, each module can have a focused responsibility.

This becomes extremely important in larger software projects.

---

# 69. Exceptions

Programs sometimes encounter unexpected situations.

For example:

```python
number = int(input("Enter a number: "))
```

What if the user enters:

```text
hello
```

Python cannot convert `"hello"` into an integer.

It raises an exception.

---

# 70. `try` and `except`

We can handle certain errors:

```python
try:
    number = int(input("Enter a number: "))
    print(number)
except ValueError:
    print("Please enter a valid number.")
```

Now the program can respond gracefully.

This is called **exception handling**.

---

# 71. Errors Are Information

Do not develop the mindset:

> "Errors are bad."

Instead think:

> "Errors tell me something about what happened."

Python errors often tell you:

- what went wrong
- where it happened
- what type of error occurred

Learning to read error messages is a core programming skill.

---

# 72. Reading Tracebacks

Suppose Python displays:

```text
Traceback (most recent call last):
  File "app.py", line 5, in <module>
    result = 10 / 0
ZeroDivisionError: division by zero
```

Do not panic.

Read it from the bottom.

The final line says:

```text
ZeroDivisionError: division by zero
```

The traceback also tells you:

```text
app.py
line 5
```

Start there.

---

# 73. Debugging

**Debugging** means finding and fixing problems in a program.

A useful debugging process is:

```text
Observe the problem
      ↓
Reproduce the problem
      ↓
Identify where it occurs
      ↓
Form a hypothesis
      ↓
Test the hypothesis
      ↓
Make a change
      ↓
Run the program again
```

Do not randomly change code.

Try to understand the problem first.

---

# 74. The Scientific Method for Programming

Debugging is surprisingly similar to science.

You observe:

> The program gives the wrong total.

You hypothesize:

> Maybe tax is being applied twice.

You test:

```python
print(subtotal)
print(tax)
print(total)
```

You observe the output.

Then you update your hypothesis.

This mindset is much more powerful than guessing.

---

# 75. Comments

Python allows comments using `#`.

```python
# Calculate the total price
total = price * quantity
```

Comments can explain **why** something exists.

Avoid comments that merely repeat the code.

Weak:

```python
# Add 1 to count
count += 1
```

Better:

```python
# Move to the next student
count += 1
```

The best comments often explain reasoning that is not obvious from the code itself.

---

# 76. Truthiness

Python allows many values to be interpreted as true or false.

For example:

```python
if name:
    print("Name provided")
```

An empty string:

```python
""
```

is considered false.

A non-empty string:

```python
"Alice"
```

is considered true.

Similar behavior exists for collections.

For example:

```python
items = []

if items:
    print("There are items")
else:
    print("The list is empty")
```

---

# 77. `None`

Python has a special value:

```python
None
```

It represents the absence of a value.

For example:

```python
result = None
```

You might use this when a value does not exist yet.

Check for it using:

```python
if result is None:
    print("No result")
```

Prefer `is None` rather than:

```python
result == None
```

---

# 78. String Operations

Strings have many useful methods.

For example:

```python
name = "alice"
```

Uppercase:

```python
name.upper()
```

Result:

```text
ALICE
```

Lowercase:

```python
name.lower()
```

Capitalize:

```python
name.capitalize()
```

Strip whitespace:

```python
name.strip()
```

---

# 79. Splitting Strings

Suppose:

```python
sentence = "Python is fun"
```

You can split it:

```python
words = sentence.split()
```

Now:

```python
words
```

contains:

```text
["Python", "is", "fun"]
```

This is useful when processing text.

---

# 80. Joining Strings

You can join strings:

```python
words = ["Python", "is", "fun"]

sentence = " ".join(words)
```

Result:

```text
Python is fun
```

This becomes useful when working with text data.

---

# 81. File Handling

Programs often need to work with files.

Python provides `open()`.

For example:

```python
with open("notes.txt", "r") as file:
    content = file.read()

print(content)
```

The `with` statement ensures the file is handled safely.

---

# 82. Writing Files

You can write to a file:

```python
with open("notes.txt", "w") as file:
    file.write("Hello from Python!")
```

Be careful with `"w"`.

It can overwrite an existing file.

---

# 83. Appending to Files

If you want to add content rather than replace the existing content:

```python
with open("notes.txt", "a") as file:
    file.write("\nAnother line.")
```

The `"a"` means append.

---

# 84. JSON

Many applications exchange information using JSON.

JSON looks like:

```json
{
    "name": "Alice",
    "age": 25,
    "skills": ["Python", "AI"]
}
```

Python can work with JSON using the built-in `json` module.

For example:

```python
import json

data = {
    "name": "Alice",
    "age": 25
}

with open("person.json", "w") as file:
    json.dump(data, file, indent=4)
```

You will encounter JSON frequently when working with APIs.

---

# 85. List Comprehensions

Python has a concise way to create lists.

Instead of:

```python
numbers = []

for number in range(10):
    numbers.append(number * 2)
```

you can write:

```python
numbers = [number * 2 for number in range(10)]
```

This is called a **list comprehension**.

Do not use list comprehensions simply because they are shorter.

Use them when they make the code easier to understand.

---

# 86. Basic Testing

You should not assume code works because it ran once.

Suppose we write:

```python
def add(a, b):
    return a + b
```

We should test:

```python
print(add(2, 3))
print(add(0, 0))
print(add(-1, 5))
```

Expected results:

```text
5
0
4
```

Testing means deliberately checking whether your program behaves as expected.

---

# 87. Edge Cases

A good programmer asks:

> "What unusual inputs could break this?"

For a function:

```python
def divide(a, b):
    return a / b
```

We should consider:

```text
10 / 2
0 / 5
5 / 0
```

The last case causes an error.

We might decide to handle it:

```python
def divide(a, b):
    if b == 0:
        return None

    return a / b
```

Thinking about edge cases is a major part of software development.

---

# 88. A Problem-Solving Framework

When given a programming problem, do not immediately start typing.

Use this process:

## Step 1 - Understand the problem

What are we trying to accomplish?

## Step 2 - Identify inputs

What information do we have?

## Step 3 - Identify outputs

What should the program produce?

## Step 4 - Break the problem down

What smaller operations are required?

## Step 5 - Write the algorithm

Describe the steps in plain language.

## Step 6 - Implement

Write Python code.

## Step 7 - Test

Try normal inputs and edge cases.

## Step 8 - Debug

Investigate failures.

## Step 9 - Refactor

Make the solution clearer and easier to maintain.

---

# 89. Example: Build a Temperature Converter

Suppose the problem is:

> Convert Celsius to Fahrenheit.

The formula is:

```text
F = C × 9/5 + 32
```

Before coding, define:

### Input

Temperature in Celsius.

### Output

Temperature in Fahrenheit.

### Algorithm

```text
Ask for Celsius
      ↓
Convert input to a number
      ↓
Multiply by 9/5
      ↓
Add 32
      ↓
Print Fahrenheit
```

Python:

```python
celsius = float(input("Temperature in Celsius: "))

fahrenheit = celsius * 9 / 5 + 32

print(f"{fahrenheit}°F")
```

Notice how the code follows the algorithm.

---

# 90. Example: Build a Grade Calculator

Problem:

> Given a student's score, determine their grade.

Inputs:

```text
score
```

Rules:

```text
90+ → A
80–89 → B
70–79 → C
60–69 → D
below 60 → F
```

Algorithm:

```text
Get score
   ↓
Is score >= 90?
   ↓ no
Is score >= 80?
   ↓ no
Is score >= 70?
   ↓ no
Is score >= 60?
   ↓ no
F
```

Implementation:

```python
score = int(input("Enter score: "))

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Grade: {grade}")
```

---

# 91. Example: Count Even Numbers

Suppose we have:

```python
numbers = [3, 8, 12, 5, 7, 10, 14]
```

We want to count the even numbers.

Think first.

Algorithm:

```text
Start count at 0

For each number:
    If the number is even:
        increase count

Print count
```

Python:

```python
numbers = [3, 8, 12, 5, 7, 10, 14]

count = 0

for number in numbers:
    if number % 2 == 0:
        count += 1

print(count)
```

Output:

```text
4
```

---

# 92. Combining Functions, Lists, and Conditions

Now we can create a reusable function:

```python
def count_even_numbers(numbers):
    count = 0

    for number in numbers:
        if number % 2 == 0:
            count += 1

    return count
```

Then:

```python
numbers = [3, 8, 12, 5, 7, 10, 14]

result = count_even_numbers(numbers)

print(result)
```

This is much closer to how real software is structured.

---

# 93. Abstraction

You do not need to know every internal detail of a function to use it.

For example:

```python
numbers.sort()
```

You do not need to implement the sorting algorithm every time you want to sort a list.

You use an abstraction.

Abstraction means:

> Hide unnecessary implementation details behind a simpler interface.

Functions are one of the first tools you use to create abstractions.

---

# 94. DRY: Don't Repeat Yourself

Suppose you write:

```python
total1 = price1 * quantity1
total2 = price2 * quantity2
total3 = price3 * quantity3
```

Repeated logic often suggests that you need a better structure.

For example:

```python
def calculate_total(price, quantity):
    return price * quantity
```

Then:

```python
total1 = calculate_total(price1, quantity1)
total2 = calculate_total(price2, quantity2)
total3 = calculate_total(price3, quantity3)
```

The principle is often summarized as:

> **Don't Repeat Yourself.**

Avoid unnecessary duplication.

---

# 95. But Don't Over-Abstract

There is a danger on the other side.

Beginners sometimes create functions for everything:

```python
def get_number():
    ...

def add_one():
    ...

def print_number():
    ...
```

Abstraction should make code clearer, not more complicated.

Ask:

> Does this abstraction make the program easier to understand or reuse?

If not, it may not be necessary.

---

# 96. Readability Matters

Code is written for computers to execute, but humans need to maintain it.

Compare:

```python
x = p * q
```

with:

```python
total_price = price * quantity
```

Both may work.

The second communicates intent.

A useful rule:

> Write code that your future self can understand.

---

# 97. Programming Is Communication

When you write software, you are communicating with several audiences:

```text
You today
    ↓
You six months from now
    ↓
Your teammates
    ↓
The computer
```

Good programming communicates clearly with all of them.

That means:

- meaningful names
- sensible functions
- clear structure
- useful comments
- predictable behavior
- tests
- documentation

---

# 98. A Mini Project: Number Guessing Game

Let's combine the concepts.

The program should:

1. choose a secret number
2. ask the user to guess
3. tell them whether the guess is too high or too low
4. continue until they guess correctly

Python:

```python
import random

secret_number = random.randint(1, 100)

while True:
    guess = int(input("Guess the number: "))

    if guess < secret_number:
        print("Too low!")
    elif guess > secret_number:
        print("Too high!")
    else:
        print("Correct!")
        break
```

This small program uses:

- imports
- variables
- integers
- input
- type conversion
- loops
- conditionals
- comparison
- `break`

That is already a real program.

---

# 99. Improve the Number Guessing Game

Now make it better.

Add:

- a guess counter
- invalid input handling
- a maximum number of guesses
- difficulty levels
- a replay option

Do not immediately search for the solution.

First design the algorithm yourself.

For example:

```text
Start game
    ↓
Choose secret number
    ↓
Set attempts = 0
    ↓
Ask for guess
    ↓
Increase attempts
    ↓
Compare guess
    ↓
Correct?
  /     \
yes      no
 |        |
win    continue
```

This is how you should approach increasingly complex projects.

---

# 100. Phase 1 Capstone

Build a command-line application that solves a useful problem.

Choose one:

### Option A - Expense Tracker

The user can:

- add an expense
- list expenses
- calculate total spending
- categorize expenses

### Option B - Quiz Application

The program should:

- ask multiple questions
- accept answers
- calculate a score
- display the final result

### Option C - To-Do List

The user can:

- add tasks
- list tasks
- mark tasks complete
- remove tasks

### Option D - Personal Finance Calculator

The program should:

- accept income
- accept expenses
- calculate remaining money
- categorize spending
- report totals

### Option E - Text Analyzer

The program should accept text and calculate:

- number of characters
- number of words
- number of sentences
- most common words
- average word length

---

# 101. Capstone Requirements

Your program should demonstrate the concepts from this phase.

It should contain:

- variables
- strings
- numbers
- Boolean logic
- conditionals
- loops
- lists
- dictionaries
- functions
- input/output
- error handling
- at least one imported module
- meaningful variable names
- multiple commits using Git

You should also create:

```text
README.md
```

Your README should explain:

- what the project does
- how to run it
- what you learned
- what you would improve next

---

# 102. Suggested Project Structure

For a small project:

```text
my-project/
├── app.py
├── README.md
└── .gitignore
```

As your project grows, you might eventually use:

```text
my-project/
├── README.md
├── .gitignore
├── requirements.txt
├── src/
│   ├── main.py
│   ├── utils.py
│   └── models.py
└── tests/
    └── test_main.py
```

You do not need to use the second structure for every small program.

Structure should grow with complexity.

---

# 103. What You Should Be Able to Do After Phase 1

By the end of this phase, you should be comfortable with:

## Python Fundamentals

```text
Variables
Types
Strings
Numbers
Booleans
Operators
Input/output
```

## Control Flow

```text
if
elif
else
for
while
break
continue
```

## Data Structures

```text
list
tuple
dict
set
```

## Functions

```text
parameters
return values
scope
reusability
```

## Working With Data

```text
strings
files
JSON
collections
```

## Software Development

```text
debugging
exceptions
testing
edge cases
modules
Git
GitHub
```

---

# 104. More Important Than Syntax

At the end of Phase 1, do not measure yourself by asking:

> "Can I remember every Python method?"

Instead ask:

> "Can I solve a new problem?"

If someone gives you a problem you have never seen before, you should be able to:

```text
Understand the problem
       ↓
Break it into smaller pieces
       ↓
Identify inputs and outputs
       ↓
Choose appropriate data structures
       ↓
Write an algorithm
       ↓
Implement it in Python
       ↓
Test it
       ↓
Debug it
       ↓
Improve it
```

That is the real goal.

---

# 105. The Programmer's Mental Model

As you progress through the curriculum, try to develop this habit:

When you see a problem, don't immediately think:

> "What Python syntax do I need?"

Instead think:

> "What is the underlying problem?"

Then:

```text
Problem
  ↓
Inputs
  ↓
Data
  ↓
Operations
  ↓
Decisions
  ↓
Repetition
  ↓
Output
```

Only then translate those ideas into Python.

---

# 106. Final Challenge

Before moving to the next phase, build something without following a tutorial step-by-step.

Choose a problem that matters to you.

Describe it in plain English first.

For example:

```text
I want to build a program that helps me track
how much time I spend studying.
```

Then break it down:

```text
Record subject
Record duration
Store records
Calculate total
Calculate totals by subject
Display results
```

Then decide:

```text
What data structures do I need?

What functions do I need?

What decisions do I need?

What loops do I need?

What errors could happen?
```

Then build it.

Do not worry if the first version is ugly.

Build version 1.

Then improve it.

Commit each meaningful milestone with Git.

---

# 107. The Core Lesson

Programming is not primarily about typing code.

Programming is about **turning problems into precise, executable ideas**.

Python is the language we are using to practice that skill.

The most important progression in Phase 1 is:

```text
"I don't know how to solve this."
             ↓
"I can break the problem into pieces."
             ↓
"I can describe the algorithm."
             ↓
"I can implement the algorithm."
             ↓
"I can test the implementation."
             ↓
"I can debug it when it fails."
             ↓
"I can improve the solution."
```

Once you can do that, you are no longer simply learning Python syntax.

You are learning to **program**.