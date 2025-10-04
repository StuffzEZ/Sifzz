# Tkinter GUI Module

An **official** Sifzz module that enables creation of graphical user interfaces using Tkinter.

---

## Installation

Place `tkinterGui.py` in your `modules/` directory. The module will be automatically loaded when you run Sifzz.

**Requirements:** Python with tkinter (included by default in most Python installations)

---

## Basic Commands

### create window "Title" width \<w> height \<h>

Creates a GUI window with the specified title, width, and height.

**Example:**
```
create window "My App" width 500 height 400
```

---

### start gui

Starts the GUI event loop. This must be called **after** creating the window and adding all widgets.

**Example:**
```
start gui
```

---

### close window

Closes the GUI window programmatically.

**Example:**
```
close window
```

---

## Widget Commands

### add label "Text" at x \<x> y \<y>

Adds a text label at the specified coordinates.

**Example:**
```
add label "Enter your name:" at x 20 y 20
```

---

### add button "Text" at x \<x> y \<y> and run "command" on click

Adds a clickable button that executes a Sifzz command when clicked.

**Example:**
```
add button "Greet" at x 150 y 60 and run "say 'Hello, ' + username" on click
```

**Note:** The command can access any Sifzz variables and execute any valid Sifzz code.

---

### add entry at x \<x> y \<y> store in \<variable>

Adds a single-line text input field. The value is automatically stored in the specified variable when:
- User presses Enter
- Field loses focus

**Example:**
```
add entry at x 150 y 20 store in username
```

---

### add text box at x \<x> y \<y> width \<w> height \<h> store in \<variable>

Adds a multi-line text input area. Updates the variable as the user types.

**Example:**
```
add text box at x 50 y 100 width 40 height 10 store in bio
```

**Note:** Width and height are in character units, not pixels.

---

### add checkbox "Text" at x \<x> y \<y> store in \<variable>

Adds a checkbox that stores `true` or `false` in the specified variable.

**Example:**
```
add checkbox "Subscribe to newsletter" at x 50 y 200 store in subscribe
```

---

### add dropdown at x \<x> y \<y> options \<list> store in \<variable>

Adds a dropdown menu populated from a Sifzz list. The selected value is stored in the variable.

**Example:**
```
create list colors
add "Red" to colors
add "Blue" to colors
add "Green" to colors

add dropdown at x 150 y 250 options colors store in favoriteColor
```

---

## Widget Manipulation Commands

### update label "Text" to "New Text"

Changes the text of an existing label.

**Example:**
```
update label "Enter your name:" to "Your Name:"
```

---

### get entry \<variable>

Manually retrieves the current value from an entry field and stores it in the variable.

**Example:**
```
get entry username
```

---

### clear entry \<variable>

Clears the text from an entry field and resets the variable to empty string.

**Example:**
```
clear entry username
```

---

## Dialog Commands

### show message "Title" "Message"

Displays an information dialog box.

**Example:**
```
show message "Success" "Your data has been saved!"
```

---

### show error "Title" "Message"

Displays an error dialog box.

**Example:**
```
show error "Error" "Invalid username format"
```

---

### show warning "Title" "Message"

Displays a warning dialog box.

**Example:**
```
show warning "Warning" "This action cannot be undone"
```

---

### ask yes/no "Title" "Question" store in \<variable>

Shows a yes/no dialog and stores the result (`true` for yes, `false` for no) in a variable.

**Example:**
```
ask yes/no "Confirm" "Are you sure?" store in confirmed

if confirmed is true:
    say "User confirmed"
end if
```

---

## Complete Examples

### Example 1: Simple Login Form

```
create window "Login" width 400 height 200

add label "Username:" at x 50 y 30
add entry at x 150 y 30 store in username

add label "Password:" at x 50 y 70
add entry at x 150 y 70 store in password

add button "Login" at x 150 y 120 and run "show message 'Welcome' 'Hello, ' + username" on click

start gui
```

---

### Example 2: Form with Multiple Widget Types

```
create window "User Profile" width 600 height 500

# Text inputs
add label "Name:" at x 50 y 50
add entry at x 150 y 50 store in name

add label "Bio:" at x 50 y 100
add text box at x 150 y 100 width 30 height 5 store in bio

# Checkbox
add checkbox "Subscribe to updates" at x 50 y 200 store in subscribe

# Dropdown
create list countries
add "USA" to countries
add "Canada" to countries
add "UK" to countries

add label "Country:" at x 50 y 250
add dropdown at x 150 y 250 options countries store in country

# Submit button
add button "Submit" at x 200 y 320 and run "show message 'Success' 'Profile updated!'" on click

start gui
```

---

### Example 3: Interactive Counter

```
create window "Counter" width 300 height 200

set count to 0

add label "0" at x 130 y 50

add button "Increment" at x 80 y 100 and run "increase count" on click
add button "Decrement" at x 180 y 100 and run "decrease count" on click

function updateDisplay:
    update label "0" to count
end function

start gui
```

---

### Example 4: Dialog Confirmation

```
create window "Delete File" width 400 height 200

add label "Are you sure you want to delete this file?" at x 50 y 50

add button "Delete" at x 100 y 100 and run "ask yes/no 'Confirm Delete' 'This cannot be undone!' store in confirmed" on click

add button "Check Result" at x 200 y 100 and run "say confirmed" on click

start gui
```

---

## Important Notes

### Coordinate System
- Coordinates `(x, y)` are in pixels from the **top-left corner** of the window
- X increases to the right, Y increases downward

### Widget Sizing
- Entry fields have default width (can't be customized with current commands)
- Text boxes use **character units** for width and height
- Labels auto-size to fit their text

### Variable Synchronization
- Entry fields update on Enter key or focus loss
- Text boxes update in real-time as user types
- Checkboxes update immediately on click
- Dropdowns update immediately on selection

### Limitations
- Only one window can be created per script
- Widgets must be added after creating a window
- Widget positions are absolute (no layout managers)
- Labels are referenced by their original text for updates

### Best Practices
1. Create window first, add widgets second, call `start gui` last
2. Use descriptive variable names for widget storage
3. Test button commands separately before adding to GUI
4. Use dialogs for important confirmations
5. Consider widget placement carefully (no auto-layout)

---

## Troubleshooting

**Problem:** "Create a window first!" error  
**Solution:** Call `create window` before adding any widgets

**Problem:** Variables not updating from entry fields  
**Solution:** Press Enter or click outside the field to trigger update

**Problem:** Dropdown shows no options  
**Solution:** Ensure the list exists and has items before creating the dropdown

**Problem:** Label won't update  
**Solution:** Use the exact original label text in the `update label` command

**Problem:** Button command doesn't execute  
**Solution:** Check that the command is enclosed in quotes and is valid Sifzz syntax

---

## Module Information

**Module File:** `tkinterGui.py`  
**Class Name:** `TkinterModule`  
**Dependencies:** tkinter (Python standard library)  
**Version:** 1.0  
**Status:** Official

---

**For more information on creating custom modules, see the [Module Development Guide](mdg)**