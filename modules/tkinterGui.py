"""
This is an OFFICIAL Sifzz module.

Tkinter GUI Module for Sifzz
Skript-style GUI commands

Commands:
- create window "Title" width <w> height <h>
- add label "Text" at x <x> y <y>
- add button "Text" at x <x> y <y> and run <command> on click
- add entry at x <x> y <y> store in <variable>
- start gui
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sifzz import SifzzModule
import tkinter as tk

class TkinterModule(SifzzModule):
    def __init__(self, interpreter):
        super().__init__(interpreter)
        self.root = None
        self.widgets = {}

    def register_commands(self):
        self.register(
            r'create window "([^"]+)" width (\d+) height (\d+)',
            self.create_window,
            "Create a GUI window with title, width, and height"
        )
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
        self.register(
            r'start gui',
            self.start_gui,
            "Start the GUI event loop"
        )

    def create_window(self, match):
        title = match.group(1)
        width = int(match.group(2))
        height = int(match.group(3))
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        print(f"[INFO] Created window '{title}' ({width}x{height})")

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
        self.widgets[text] = button

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
        self.widgets[var_name] = entry

    def start_gui(self, match):
        if not self.root:
            print("[ERROR] Create a window first!")
            return
        print("[INFO] Starting GUI event loop...")
        self.root.mainloop()
