"""
This is an OFFICIAL Sifzz module.

File Operations Module for Sifzz
Place this file in the modules/ directory

This module adds file operations to Sifzz:
- read file "filename.txt" and store in variable
- write "text" to file "filename.txt"
- append "text" to file "filename.txt"
- delete file "filename.txt"
- file "filename.txt" exists (returns true/false)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sifzz import SifzzModule
import re

class FileOperationsModule(SifzzModule):
    """Adds file I/O operations to Sifzz"""
    
    def register_commands(self):
        """Register all file operation commands"""
        
        # Read file
        self.register(
            r'read file "([^"]+)" and store in (\w+)',
            self.read_file,
            "Read contents of a file into a variable"
        )
        
        # Write file
        self.register(
            r'write "([^"]+)" to file "([^"]+)"',
            self.write_file,
            "Write text to a file (overwrites)"
        )
        
        # Write variable to file
        self.register(
            r'write (\w+) to file "([^"]+)"',
            self.write_var_to_file,
            "Write variable contents to a file"
        )
        
        # Append to file
        self.register(
            r'append "([^"]+)" to file "([^"]+)"',
            self.append_file,
            "Append text to a file"
        )
        
        # Append variable to file
        self.register(
            r'append (\w+) to file "([^"]+)"',
            self.append_var_to_file,
            "Append variable contents to a file"
        )
        
        # Delete file
        self.register(
            r'delete file "([^"]+)"',
            self.delete_file,
            "Delete a file"
        )
        
        # Check if file exists
        self.register(
            r'set (\w+) to file "([^"]+)" exists',
            self.file_exists,
            "Check if a file exists"
        )
    
    def read_file(self, match):
        """Read file contents into a variable"""
        filename = match.group(1)
        var_name = match.group(2)
        
        try:
            with open(filename, 'r') as f:
                content = f.read()
            self.interpreter.variables[var_name] = content
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
            self.interpreter.variables[var_name] = ""
        except Exception as e:
            print(f"Error reading file: {e}")
            self.interpreter.variables[var_name] = ""
    
    def write_file(self, match):
        """Write text to a file"""
        text = match.group(1)
        filename = match.group(2)
        
        try:
            with open(filename, 'w') as f:
                f.write(text)
        except Exception as e:
            print(f"Error writing file: {e}")
    
    def write_var_to_file(self, match):
        """Write variable contents to a file"""
        var_name = match.group(1)
        filename = match.group(2)
        
        if var_name not in self.interpreter.variables:
            print(f"Error: Variable '{var_name}' not found")
            return
        
        try:
            content = str(self.interpreter.variables[var_name])
            with open(filename, 'w') as f:
                f.write(content)
        except Exception as e:
            print(f"Error writing file: {e}")
    
    def append_file(self, match):
        """Append text to a file"""
        text = match.group(1)
        filename = match.group(2)
        
        try:
            with open(filename, 'a') as f:
                f.write(text)
        except Exception as e:
            print(f"Error appending to file: {e}")
    
    def append_var_to_file(self, match):
        """Append variable contents to a file"""
        var_name = match.group(1)
        filename = match.group(2)
        
        if var_name not in self.interpreter.variables:
            print(f"Error: Variable '{var_name}' not found")
            return
        
        try:
            content = str(self.interpreter.variables[var_name])
            with open(filename, 'a') as f:
                f.write(content)
        except Exception as e:
            print(f"Error appending to file: {e}")
    
    def delete_file(self, match):
        """Delete a file"""
        filename = match.group(1)
        
        try:
            os.remove(filename)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
        except Exception as e:
            print(f"Error deleting file: {e}")
    
    def file_exists(self, match):
        """Check if file exists"""
        var_name = match.group(1)
        filename = match.group(2)
        
        self.interpreter.variables[var_name] = os.path.exists(filename)
