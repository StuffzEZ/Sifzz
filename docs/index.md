> [!TIP]
> You can add more functionality to your Sifzz projects using [modules](modules)!
# Sifzz Programming Language Documentation

A beginner-friendly scripting language with natural syntax

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Sifzz CLI](#cli)
3. [Basic Syntax](#basic-syntax)
4. [Variables](#variables)
5. [Output](#output)
6. [Input](#input)
7. [Arithmetic Operations](#arithmetic-operations)
8. [Conditional Statements](#conditional-statements)
9. [Loops](#loops)
10. [Lists](#lists)
11. [Functions](#functions)
12. [String Operations](#string-operations)
13. [Math Operations](#math-operations)
14. [Random Numbers](#random-numbers)
15. [Control Flow](#control-flow)
16. [Complete Examples](#complete-examples)

[NEXT PAGE - Modules](modules/mdg)

---

## Getting Started

### Installation

To install Sifzz, follow these steps:
1. Download the release ZIP from the latest release
2. Unzip it into your project's directory
After this, you have installed Sifzz on your project

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

## CLI
`python sifzz.py FILE.sfzz -d` <-- -d does debug. This opens a file
`python sifzz.py -i MODULE_NAME` <-- install a module from our repo using SIFZZPM (Sifzz Package Manager)

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

set picked to random choice from colors
say picked
```

---

## Control Flow

### Break Statement

Exit a loop early:

```
set counter to 0

loop while counter less than 10:
    say counter
    increase counter
    
    if counter is 5:
        break
    end if
end loop

say "Loop ended at 5"
```

### Continue Statement

Skip to the next iteration:

```
repeat 5 times:
    set num to random number between 1 and 10
    
    if num less than 5:
        continue
    end if
    
    say num
end repeat
```

### Exit Program

```
set value to -1

if value less than 0:
    say "Error: Negative value!"
    exit
end if

say "This won't run"
```

---

## Complete Examples

### Example 1: Number Guessing Game

```
# Number Guessing Game
say "=== Number Guessing Game ==="
say ""

set target to random number between 1 and 10
set guesses to 0
set won to false

loop while guesses less than 3:
    ask for number "Guess a number (1-10):" and store in guess
    increase guesses
    
    if guess is target:
        say "Correct! You won!"
        set won to true
        break
    else if guess greater than target:
        say "Too high!"
    else:
        say "Too low!"
    end if
end loop

if won is false:
    say "Game Over! The number was:"
    say target
end if
```

### Example 2: Calculator

```
# Simple Calculator
say "=== Calculator ==="
say ""

ask for number "Enter first number:" and store in num1
ask for number "Enter second number:" and store in num2

say ""
say "Choose operation:"
say "1. Add"
say "2. Subtract"
say "3. Multiply"
say "4. Divide"

ask for number "Enter choice (1-4):" and store in choice

if choice is 1:
    set result to num1 + num2
    say "Result: "
    say result
else if choice is 2:
    set result to num1 - num2
    say "Result: "
    say result
else if choice is 3:
    set result to num1 * num2
    say "Result: "
    say result
else if choice is 4:
    if num2 is not 0:
        set result to num1 / num2
        say "Result: "
        say result
    else:
        say "Error: Cannot divide by zero!"
    end if
else:
    say "Invalid choice!"
end if
```

### Example 3: To-Do List

```
# To-Do List Manager
say "=== To-Do List Manager ==="
create list tasks
set running to true

loop while running is true:
    say ""
    say "1. Add task"
    say "2. View tasks"
    say "3. Remove task"
    say "4. Exit"
    say ""
    
    ask for number "Choose option:" and store in option
    
    if option is 1:
        ask "Enter task:" and store in task
        add task to tasks
        say "Task added!"
        
    else if option is 2:
        set count to size of tasks
        
        if count is 0:
            say "No tasks!"
        else:
            say "Your tasks:"
            set index to 0
            for each task in tasks:
                say index
                say ". "
                say task
                increase index
            end for
        end if
        
    else if option is 3:
        ask for number "Enter task number:" and store in taskNum
        set taskToRemove to item taskNum of tasks
        remove taskToRemove from tasks
        say "Task removed!"
        
    else if option is 4:
        say "Goodbye!"
        set running to false
        
    else:
        say "Invalid option!"
    end if
end loop
```

### Example 4: Quiz Game

```
# Quiz Game
say "=== Quiz Time! ==="
say ""

set score to 0

# Question 1
ask "What is 5 + 3? " and store in answer1
if answer1 is "8":
    say "Correct!"
    add 1 to score
else:
    say "Wrong! The answer is 8"
end if

say ""

# Question 2
ask "What is the capital of France? " and store in answer2
set lower to answer2 lowercase
if lower is "paris":
    say "Correct!"
    add 1 to score
else:
    say "Wrong! The answer is Paris"
end if

say ""

# Question 3
ask "Is the sky blue? (yes/no) " and store in answer3
set lower to answer3 lowercase
if lower is "yes":
    say "Correct!"
    add 1 to score
else:
    say "Wrong! The answer is yes"
end if

say ""
say "Your final score: "
say score
say " out of 3"

if score is 3:
    say "Perfect score!"
else if score greater than or equal to 2:
    say "Good job!"
else:
    say "Keep practicing!"
end if
```

### Example 5: Countdown Timer

```
# Countdown Timer
say "=== Countdown Timer ==="
ask for number "Enter seconds:" and store in seconds

say "Starting countdown..."

loop while seconds greater than 0:
    say seconds
    wait 1 second
    decrease seconds
end loop

say "Time's up!"
```

### Example 6: Password Generator

```
# Simple Password Generator
say "=== Password Generator ==="

create list chars
add "a" to chars
add "b" to chars
add "c" to chars
add "d" to chars
add "e" to chars
add "f" to chars
add "g" to chars
add "h" to chars
add "1" to chars
add "2" to chars
add "3" to chars
add "4" to chars
add "5" to chars

ask for number "Password length:" and store in length

set password to ""
set count to 0

loop while count less than length:
    set char to random choice from chars
    set password to password + char
    increase count
end loop

say "Your password: "
say password
```

### Example 7: Rock Paper Scissors

```
# Rock Paper Scissors
say "=== Rock Paper Scissors ==="

create list choices
add "rock" to choices
add "paper" to choices
add "scissors" to choices

set playing to true

loop while playing is true:
    say ""
    ask "Choose rock, paper, or scissors (or 'quit'):" and store in playerChoice
    set playerChoice to playerChoice lowercase
    
    if playerChoice is "quit":
        say "Thanks for playing!"
        set playing to false
        continue
    end if
    
    set computerChoice to random choice from choices
    
    say "Computer chose: "
    say computerChoice
    
    if playerChoice is computerChoice:
        say "It's a tie!"
    else if playerChoice is "rock":
        if computerChoice is "scissors":
            say "You win! Rock beats scissors"
        else:
            say "You lose! Paper beats rock"
        end if
    else if playerChoice is "paper":
        if computerChoice is "rock":
            say "You win! Paper beats rock"
        else:
            say "You lose! Scissors beats paper"
        end if
    else if playerChoice is "scissors":
        if computerChoice is "paper":
            say "You win! Scissors beats paper"
        else:
            say "You lose! Rock beats scissors"
        end if
    else:
        say "Invalid choice!"
    end if
end loop
```

### Example 8: Storytelling Adventure

```
# Interactive Story
say "=== The Forest Adventure ==="
say ""

function intro:
    say "You wake up in a dark forest..."
    say "There are two paths ahead."
end function

function leftPath:
    say ""
    say "You take the left path."
    say "You find a treasure chest!"
    
    ask "Do you open it? (yes/no) " and store in choice
    set choice to choice lowercase
    
    if choice is "yes":
        say "You found 100 gold coins!"
    else:
        say "You walk away cautiously..."
    end if
end function

function rightPath:
    say ""
    say "You take the right path."
    say "You encounter a friendly wolf!"
    say "The wolf leads you to safety."
end function

call intro

say ""
ask "Which path do you take? (left/right) " and store in choice
set choice to choice lowercase

if choice is "left":
    call leftPath
else if choice is "right":
    call rightPath
else:
    say "You stand still, paralyzed by fear..."
end if

say ""
say "=== The End ==="
```

---

## Best Practices

### 1. Use Descriptive Variable Names

**Good:**
```
set playerHealth to 100
set enemyDamage to 25
```

**Bad:**
```
set x to 100
set y to 25
```

### 2. Add Comments

```
# Initialize game variables
set score to 0
set lives to 3

# Main game loop
loop while lives greater than 0:
    # Game logic here
end loop
```

### 3. Break Down Complex Logic into Functions

```
function checkGameOver:
    if lives less than or equal to 0:
        say "Game Over!"
        exit
    end if
end function

function updateScore:
    add 10 to score
    say "Score: "
    say score
end function
```

### 4. Use Meaningful Indentation

While Sifzz doesn't require indentation, it makes code more readable:

```
if score greater than 100:
    say "High score!"
    if score greater than 500:
        say "Amazing!"
    end if
end if
```

### 5. Validate User Input

```
ask for number "Enter age (1-100):" and store in age

if age less than 1 or age greater than 100:
    say "Invalid age!"
    exit
end if
```

---

## Error Handling Tips

### Division by Zero

```
ask for number "Enter divisor:" and store in divisor

if divisor is 0:
    say "Cannot divide by zero!"
else:
    set result to 100 / divisor
    say result
end if
```

### Empty List Access

```
set count to size of myList

if count is 0:
    say "List is empty!"
else:
    set first to item 0 of myList
    say first
end if
```

### Invalid List Index

```
set count to size of myList
ask for number "Enter index:" and store in index

if index less than 0 or index greater than or equal to count:
    say "Invalid index!"
else:
    set item to item index of myList
    say item
end if
```

---

## Language Features Summary

| Feature | Syntax Example |
|---------|---------------|
| Variables | `set x to 5` |
| Output | `say "Hello"` |
| Input | `ask "Name?" and store in name` |
| Addition | `add 5 to x` |
| Subtraction | `subtract 3 from x` |
| Multiplication | `multiply x by 2` |
| Division | `divide x by 4` |
| If Statement | `if x is 5:` ... `end if` |
| While Loop | `loop while x less than 10:` ... `end loop` |
| For Loop | `repeat 5 times:` ... `end repeat` |
| For Each | `for each item in list:` ... `end for` |
| Functions | `function name:` ... `end function` |
| Lists | `create list myList` |
| Random | `set x to random number between 1 and 10` |
| Break | `break` |
| Continue | `continue` |
| Exit | `exit` |

---

## Quick Reference Card

```
# Variables
set name to "value"
increase x
decrease x

# Output
say "text"
write "text"
newline

# Input
ask "prompt?" and store in var
ask for number "prompt?" and store in var

# Math
add X to var
subtract X from var
multiply var by X
divide var by X

# Conditionals
if condition:
    # code
else if condition:
    # code
else:
    # code
end if

# Loops
repeat X times:
    # code
end repeat

loop while condition:
    # code
end loop

for each item in list:
    # code
end for

# Lists
create list name
add "item" to list
remove "item" from list
set x to size of list
set x to item 0 of list
clear list

# Functions
function name:
    # code
end function

call name

# Control
break
continue
exit
wait X seconds

# Random
set x to random number between 1 and 10
set x to random choice from list

# String Operations
set x to text uppercase
set x to text lowercase
set x to length of text

# Math Functions
set x to sqrt(num)
set x to round(num)
set x to abs(num)

# Operators
is, equals (==)
is not (!=)
greater than (>)
less than (<)
greater than or equal to (>=)
less than or equal to (<=)
and, or, not
contains
```

---

## Contributing & Support

Sifzz is designed to be simple and beginner-friendly. If you have suggestions for new features or improvements, feel free to contribute!

### Future Features Under Consideration

- File I/O operations
- Dictionary/map support
- Try/catch error handling
- Import system for libraries
- Object-oriented features
- More built-in functions

---

## License

Sifzz is open source and free to use for educational purposes.

---

**Happy Coding! 🎉**
