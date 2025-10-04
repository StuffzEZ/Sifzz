"""
This is an OFFICIAL Sifzz module.

Tkinter GUI Module for Sifzz
Skript-style GUI commands

Commands:
- create window "Title" width <w> height <h>
- add label "Text" at x <x> y <y>
- add button "Text" at x <x> y <y> and run "command" on click
- add entry at x <x> y <y> store in <variable>
- add text box at x <x> y <y> width <w> height <h> store in <variable>
- add checkbox "Text" at x <x> y <y> store in <variable>
- add dropdown at x <x> y <y> options <list> store in <variable>
- update label <id> to "New Text"
- get entry <variable>
- clear entry <variable>
- show message "Title" "Message"
- show error "Title" "Message"
- show warning "Title" "Message"
- ask yes/no "Title" "Question" store in <variable>
- close window
- start gui
"""

import sys
import os

# Add the parent directory to sys.path so we can import sifzz
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Now import SifzzModule
try:
    from sifzz import SifzzModule
except ImportError as e:
    print(f"[ERROR] Could not import SifzzModule: {e}")
    print(f"[ERROR] sys.path: {sys.path}")
    raise

try:
    import tkinter as tk
    from tkinter import messagebox, ttk
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    print("[WARNING] tkinter not available - GUI module will not work")

class TkinterModule(SifzzModule):
    def __init__(self, interpreter):
        super().__init__(interpreter)
        self.root = None
        self.widgets = {}
        self.widget_vars = {}  # Track tkinter variables
        
        if not TKINTER_AVAILABLE:
            print("[ERROR] Tkinter module failed to load - tkinter not installed")

    def register_commands(self):
        if not TKINTER_AVAILABLE:
            return
            
        # Window management
        self.register(
            r'create window "([^"]+)" width (\d+) height (\d+)',
            self.create_window,
            "Create a GUI window with title, width, and height"
        )
        self.register(
            r'close window',
            self.close_window,
            "Close the GUI window"
        )
        self.register(
            r'start gui',
            self.start_gui,
            "Start the GUI event loop"
        )
        
        # Basic widgets
        self.register(
            r'add label "([^"]+)" at x (\d+) y (\d+)',
            self.add_label,
            "Add a label at x,y coordinates"
        )
        self.register(
            r'add button "([^"]+)" at x (\d+) y (\d+) and run "([^"]+)" on click',
            self.add_button,
            "Add a button at x,y that executes a Sifzz command on click"
        )
        self.register(
            r'add entry at x (\d+) y (\d+) store in (\w+)',
            self.add_entry,
            "Add a text entry field and store its value in a variable"
        )
        
        # Advanced widgets
        self.register(
            r'add text box at x (\d+) y (\d+) width (\d+) height (\d+) store in (\w+)',
            self.add_text_box,
            "Add a multi-line text box"
        )
        self.register(
            r'add checkbox "([^"]+)" at x (\d+) y (\d+) store in (\w+)',
            self.add_checkbox,
            "Add a checkbox"
        )
        self.register(
            r'add dropdown at x (\d+) y (\d+) options (\w+) store in (\w+)',
            self.add_dropdown,
            "Add a dropdown menu from a list"
        )
        
        # Widget manipulation
        self.register(
            r'update label "([^"]+)" to "([^"]+)"',
            self.update_label,
            "Update label text"
        )
        self.register(
            r'get entry (\w+)',
            self.get_entry,
            "Get the current value from an entry field"
        )
        self.register(
            r'clear entry (\w+)',
            self.clear_entry,
            "Clear an entry field"
        )
        
        # Dialogs
        self.register(
            r'show message "([^"]+)" "([^"]+)"',
            self.show_message,
            "Show an info message dialog"
        )
        self.register(
            r'show error "([^"]+)" "([^"]+)"',
            self.show_error,
            "Show an error message dialog"
        )
        self.register(
            r'show warning "([^"]+)" "([^"]+)"',
            self.show_warning,
            "Show a warning message dialog"
        )
        self.register(
            r'ask yes/no "([^"]+)" "([^"]+)" store in (\w+)',
            self.ask_yesno,
            "Show a yes/no dialog and store result"
        )

    def create_window(self, match):
        title = match.group(1)
        width = int(match.group(2))
        height = int(match.group(3))
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        print(f"[INFO] Created window '{title}' ({width}x{height})")

    def close_window(self, match):
        if self.root:
            self.root.destroy()
            self.root = None
            print("[INFO] Window closed")

    def add_label(self, match):
        text = match.group(1)
        x = int(match.group(2))
        y = int(match.group(3))
        if not self.root:
            print("[ERROR] Create a window first!")
            return
        label = tk.Label(self.root, text=text)
        label.place(x=x, y=y)
        self.widgets[text] = label
        print(f"[INFO] Added label '{text}' at ({x}, {y})")

    def add_button(self, match):
        text = match.group(1)
        x = int(match.group(2))
        y = int(match.group(3))
        command_str = match.group(4)

        if not self.root:
            print("[ERROR] Create a window first!")
            return

        def on_click():
            print(f"[INFO] Button '{text}' clicked, executing: {command_str}")
            self.interpreter.run_line(command_str)

        button = tk.Button(self.root, text=text, command=on_click)
        button.place(x=x, y=y)
        self.widgets[f"button_{text}"] = button
        print(f"[INFO] Added button '{text}' at ({x}, {y})")

    def add_entry(self, match):
        x = int(match.group(1))
        y = int(match.group(2))
        var_name = match.group(3)

        if not self.root:
            print("[ERROR] Create a window first!")
            return

        entry = tk.Entry(self.root)
        entry.place(x=x, y=y)

        def save_value(event=None):
            self.interpreter.variables[var_name] = entry.get()
            print(f"[INFO] Stored '{entry.get()}' in variable '{var_name}'")

        entry.bind("<Return>", save_value)
        entry.bind("<FocusOut>", save_value)
        self.widgets[f"entry_{var_name}"] = entry
        print(f"[INFO] Added entry at ({x}, {y}) linked to variable '{var_name}'")

    def add_text_box(self, match):
        x = int(match.group(1))
        y = int(match.group(2))
        width = int(match.group(3))
        height = int(match.group(4))
        var_name = match.group(5)

        if not self.root:
            print("[ERROR] Create a window first!")
            return

        text_box = tk.Text(self.root, width=width, height=height)
        text_box.place(x=x, y=y)
        
        def save_value(event=None):
            self.interpreter.variables[var_name] = text_box.get("1.0", "end-1c")

        text_box.bind("<KeyRelease>", save_value)
        self.widgets[f"textbox_{var_name}"] = text_box
        print(f"[INFO] Added text box at ({x}, {y}) linked to variable '{var_name}'")

    def add_checkbox(self, match):
        text = match.group(1)
        x = int(match.group(2))
        y = int(match.group(3))
        var_name = match.group(4)

        if not self.root:
            print("[ERROR] Create a window first!")
            return

        var = tk.BooleanVar()
        
        def on_change():
            self.interpreter.variables[var_name] = var.get()
            print(f"[INFO] Checkbox '{text}' is now: {var.get()}")

        checkbox = tk.Checkbutton(self.root, text=text, variable=var, command=on_change)
        checkbox.place(x=x, y=y)
        
        self.widgets[f"checkbox_{var_name}"] = checkbox
        self.widget_vars[var_name] = var
        self.interpreter.variables[var_name] = False
        print(f"[INFO] Added checkbox '{text}' at ({x}, {y})")

    def add_dropdown(self, match):
        x = int(match.group(1))
        y = int(match.group(2))
        list_name = match.group(3)
        var_name = match.group(4)

        if not self.root:
            print("[ERROR] Create a window first!")
            return

        if list_name not in self.interpreter.lists:
            print(f"[ERROR] List '{list_name}' not found!")
            return

        options = self.interpreter.lists[list_name]
        if not options:
            print(f"[ERROR] List '{list_name}' is empty!")
            return

        var = tk.StringVar(value=options[0])
        
        def on_change(*args):
            self.interpreter.variables[var_name] = var.get()
            print(f"[INFO] Dropdown selection: {var.get()}")

        var.trace_add("write", on_change)
        
        dropdown = ttk.Combobox(self.root, textvariable=var, values=options, state="readonly")
        dropdown.place(x=x, y=y)
        
        self.widgets[f"dropdown_{var_name}"] = dropdown
        self.widget_vars[var_name] = var
        self.interpreter.variables[var_name] = options[0]
        print(f"[INFO] Added dropdown at ({x}, {y}) with {len(options)} options")

    def update_label(self, match):
        label_text = match.group(1)
        new_text = match.group(2)
        
        if label_text in self.widgets:
            widget = self.widgets[label_text]
            if isinstance(widget, tk.Label):
                widget.config(text=new_text)
                print(f"[INFO] Updated label '{label_text}' to '{new_text}'")
            else:
                print(f"[ERROR] Widget '{label_text}' is not a label!")
        else:
            print(f"[ERROR] Label '{label_text}' not found!")

    def get_entry(self, match):
        var_name = match.group(1)
        widget_key = f"entry_{var_name}"
        
        if widget_key in self.widgets:
            entry = self.widgets[widget_key]
            value = entry.get()
            self.interpreter.variables[var_name] = value
            print(f"[INFO] Got entry value: '{value}'")
        else:
            print(f"[ERROR] Entry field '{var_name}' not found!")

    def clear_entry(self, match):
        var_name = match.group(1)
        widget_key = f"entry_{var_name}"
        
        if widget_key in self.widgets:
            entry = self.widgets[widget_key]
            entry.delete(0, tk.END)
            self.interpreter.variables[var_name] = ""
            print(f"[INFO] Cleared entry field '{var_name}'")
        else:
            print(f"[ERROR] Entry field '{var_name}' not found!")

    def show_message(self, match):
        title = match.group(1)
        message = match.group(2)
        messagebox.showinfo(title, message)

    def show_error(self, match):
        title = match.group(1)
        message = match.group(2)
        messagebox.showerror(title, message)

    def show_warning(self, match):
        title = match.group(1)
        message = match.group(2)
        messagebox.showwarning(title, message)

    def ask_yesno(self, match):
        title = match.group(1)
        question = match.group(2)
        var_name = match.group(3)
        
        result = messagebox.askyesno(title, question)
        self.interpreter.variables[var_name] = result
        print(f"[INFO] User answered: {'Yes' if result else 'No'}")

    def start_gui(self, match):
        if not self.root:
            print("[ERROR] Create a window first!")
            return
        print("[INFO] Starting GUI event loop...")
        self.root.mainloop()