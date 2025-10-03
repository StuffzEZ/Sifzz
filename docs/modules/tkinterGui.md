# Tkinter GUI Module  
An **official** Sifzz module that allows creation of simple GUI applications using Tkinter.  

## Commands  

### create window "Title" width <w> height <h>  
Creates a GUI window with the given title, width, and height.  

**Example:**  
```
create window "My App" width 400 height 300
```

---

### add label "Text" at x <x> y <y>  
Adds a text label to the window at the specified coordinates `(x, y)`.  

**Example:** 
```
add label "Enter your name:" at x 20 y 20
```

---

### add entry at x <x> y <y> store in <variable>
Adds a text input field at `(x, y)` and stores the entered value in a Sifzz variable.  
Pressing **Enter** updates the variable automatically.  

**Example:**  
```
add entry at x 150 y 20 store in username
```
---

### add button "Text" at x <x> y <y> and run "<command>" on click  
Adds a button at `(x, y)` that executes a Sifzz command when clicked.  
The command can use any Sifzz variable or expression.  

**Example:**  
```
add button "Greet" at x 150 y 60 and run "say 'Hello, ' + username" on click
```
NOTE: Username is not a built in variable

---
### start gui
Starts the Tkinter GUI event loop.  
This command must be called **after creating the window and adding widgets**.  

**Example:**  
```
start gui
```

---

### Notes  

- Coordinates `(x, y)` are measured in pixels from the top-left corner of the window.  
- Entry fields automatically update their linked variable when **Enter** is pressed.  
- Buttons can execute any **function** on click.  
- Create **only one window** per script; adding widgets before creating a window will result in an error.  
