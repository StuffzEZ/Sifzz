An **OFFICIAL** Sifzz module that provides advanced math operations.

---

## Installation

Place `mathModule.py` in your `modules/` directory. The module will be automatically loaded when you run Sifzz.

**Requirements:** Python with the math standard library (included by default)

---

## Basic Commands

### set <variable> to sin(<expression>)

Calculates the sine of the given expression (in radians) and stores it in the specified variable.

**Example:**
```
set x to sin(3.14 / 2)
```

---

### set <variable> to cos(<expression>)

Calculates the cosine of the given expression (in radians) and stores it in the specified variable.

**Example:**
`
set y to cos(0)
`

---

### set <variable> to power(<base>, <exponent>)

Raises the base to the power of the exponent and stores the result in the specified variable.

**Example:**
`
set result to power(2, 3)
`

---

## Notes

- All expressions are evaluated using the Sifzz interpreter, so you can use variables and other commands inside the expressions.
- The resulting values are stored as Python floats.
- Input expressions should be valid mathematical expressions. Invalid inputs may raise errors.

---

## Examples

### Example 1: Basic Sine Calculation

```
set angle to 1.5708
set sineValue to sin(angle)
say sineValue  # Output: ~1.0
```

---

### Example 2: Using Cosine and Power Together

```
set a to 0
set b to cos(a)
set c to power(b, 3)
say c  # Output: 1.0
```

---

### Example 3: Combining Variables in Expressions

```
set x to 0.5
set y to sin(x) + cos(x)
say y  # Output: ~1.357
```

---

## Module Information

**Module File:** `mathModule.py`
**Class Name:** `MathModule`
**Dependencies:** math (Python standard library)  
**Version:** 1.0  
**Status:** Official

---

**For more information on creating custom modules, see the [Module Development Guide](mdg)**
