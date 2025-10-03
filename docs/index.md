# Sifzz Programming Language Documentation

A beginner-friendly scripting language with natural syntax

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Syntax](#basic-syntax)
3. [Variables](#variables)
4. [Output](#output)
5. [Input](#input)
6. [Arithmetic Operations](#arithmetic-operations)
7. [Conditional Statements](#conditional-statements)
8. [Loops](#loops)
9. [Lists](#lists)
10. [Functions](#functions)
11. [String Operations](#string-operations)
12. [Math Operations](#math-operations)
13. [Random Numbers](#random-numbers)
14. [Control Flow](#control-flow)
15. [Complete Examples](#complete-examples)

[NEXT PAGE | Module Development Guide](mdg.md)

---

## Getting Started

### Installation

Save the interpreter as `sifzz.py` on your computer.

### Running Programs

```bash
python sifzz.py yourprogram.sfzz
```

### Your First Program

Create a file called `hello.sfzz`:

```
say "Hello, World!"
```

Run it:
```bash
python sifzz.py hello.sfzz
```

---

## Basic Syntax

### Comments

Comments start with `#` and are ignored by the interpreter:

```
# This is a comment
say "This will run"  # This is also a comment
```

### Line Structure

Each statement is on its own line. Sifzz reads like natural English!

```
set x to 5
say x
add 1 to x
say x
```

---

## Variables

### Creating Variables

Use `set` to create or update variables:

```
set name to "Alice"
set age to 25
set score to 100.5
set isActive to true
```

### Variable Types

Sifzz automatically handles:
- **Numbers**: `5`, `3.14`, `-10`
- **Strings**: `"Hello"`, `"123"`
- **Booleans**: `true`, `false`

### Using Variables

Simply write the variable name:

```
set greeting to "Hello"
say greeting
```

---

## Output

### Printing Text

Use `say` to print with a newline:

```
say "Hello!"
say "World!"
```

Output:
```
Hello!
World!
```

### Printing Variables

```
set name to "Bob"
say name
```

### Print Without Newline

Use `write` to print without adding a newline:

```
write "Loading"
write "..."
newline
```

Output:
```
Loading...
```

### Manual Newlines

```
newline
```

---

## Input

### Text Input

Ask the user for text input:

```
ask "What is your name?" and store in name
say "Hello, "
say name
```

### Number Input

Ask for numeric input:

```
ask for number "Enter your age:" and store in age
say "You are "
say age
say " years old"
```

---

## Arithmetic Operations

### Setting Values

```
set x to 10
set y to 5
set result to x + y
say result  # 15
```

### Addition

```
set score to 100
add 50 to score
say score  # 150
```

### Subtraction

```
set health to 100
subtract 25 from health
say health  # 75
```

### Multiplication

```
set value to 10
multiply value by 3
say value  # 30
```

### Division

```
set value to 100
divide value by 4
say value  # 25.0
```

### Increment/Decrement

```
set counter to 0
increase counter
say counter  # 1

decrease counter
say counter  # 0
```

### Complex Expressions

```
set a to 10
set b to 5
set result to a * 2 + b - 3
say result  # 22
```

---

## Conditional Statements

### Basic If Statement

```
set age to 18

if age is 18:
    say "You are exactly 18!"
end if
```

### If-Else

```
set temperature to 75

if temperature greater than 80:
    say "It's hot!"
else:
    say "It's nice!"
end if
```

### If-Else If-Else

```
set score to 85

if score greater than or equal to 90:
    say "Grade: A"
else if score greater than or equal to 80:
    say "Grade: B"
else if score greater than or equal to 70:
    say "Grade: C"
else:
    say "Grade: F"
end if
```

### Comparison Operators

- `is` or `equals` → equal to
- `is not` → not equal to
- `greater than` → greater than
- `less than` → less than
- `greater than or equal to` → ≥
- `less than or equal to` → ≤

### Logical Operators

```
set age to 25
set hasLicense to true

if age greater than 18 and hasLicense is true:
    say "You can drive!"
end if

if age less than 13 or age greater than 65:
    say "Special ticket price!"
end if
```

### Contains Operator

```
set name to "Alexander"

if name contains "alex":
    say "Name contains 'alex'"
end if
```

---

## Loops

### Repeat X Times

```
repeat 5 times:
    say "Hello!"
end repeat
```

### While Loop

```
set counter to 0

loop while counter less than 5:
    say counter
    increase counter
end loop
```

Output:
```
0
1
2
3
4
```

### For Each Loop

```
create list fruits
add "apple" to fruits
add "banana" to fruits
add "orange" to fruits

for each fruit in fruits:
    say fruit
end for
```

### Range Loop

```
for each i in range(0, 5):
    say i
end for
```

Output:
```
0
1
2
3
4
```

### Nested Loops

```
repeat 3 times:
    repeat 2 times:
        say "Inner loop"
    end repeat
    say "Outer loop"
end repeat
```

---

## Lists

### Creating Lists

```
create list myList
```

### Adding Items

```
create list colors
add "red" to colors
add "blue" to colors
add "green" to colors
```

### Removing Items

```
remove "blue" from colors
```

### Getting List Size

```
set count to size of colors
say count
```

### Accessing Items

```
set firstColor to item 0 of colors
say firstColor
```

### Clearing Lists

```
clear colors
```

### Loop Through List

```
create list numbers
add 10 to numbers
add 20 to numbers
add 30 to numbers

for each num in numbers:
    say num
end for
```

### Check if List Contains Item

```
create list inventory
add "sword" to inventory
add "shield" to inventory

if inventory contains "sword":
    say "You have a sword!"
end if
```

---

## Functions

### Defining Functions

```
function greet:
    say "Hello!"
    say "Welcome to Sifzz"
end function
```

### Calling Functions

```
call greet
```

### Functions with Variables

Functions can use and modify variables:

```
set score to 0

function addPoints:
    add 10 to score
    say "Points added!"
end function

call addPoints
say score  # 10
```

### Multiple Functions

```
function intro:
    say "=== Game Start ==="
end function

function outro:
    say "=== Game Over ==="
end function

call intro
say "Playing game..."
call outro
```

---

## String Operations

### Concatenation

```
set firstName to "John"
set lastName to "Doe"
set fullName to firstName + " " + lastName
say fullName  # John Doe
```

### Uppercase

```
set text to "hello"
set upper to text uppercase
say upper  # HELLO
```

### Lowercase

```
set text to "WORLD"
set lower to text lowercase
say lower  # world
```

### String Length

```
set message to "Hello"
set len to length of message
say len  # 5
```

### Check if String Contains

```
set email to "user@example.com"

if email contains "@":
    say "Valid email format"
end if
```

---

## Math Operations

### Square Root

```
set num to 16
set root to sqrt(num)
say root  # 4.0
```

### Rounding

```
set value to 3.7
set rounded to round(value)
say rounded  # 4
```

### Absolute Value

```
set num to -15
set positive to abs(num)
say positive  # 15
```

### Complex Math

```
set a to 5
set b to 3
set result to sqrt(a * a + b * b)
say result  # 5.830951894845301
```

---

## Random Numbers

### Random Integer

```
set dice to random number between 1 and 6
say dice
```

### Random with Variables

```
set min to 1
set max to 100
set random to random number between min and max
say random
```

### Random Choice from List

```
create list colors
add "red" to colors
add "blue" to colors
add "green" to colors
