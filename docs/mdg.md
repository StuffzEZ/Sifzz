# Sifzz Module Development Guide

**Version 3.0** | Extending Sifzz with Python Modules

---

## Table of Contents

1. [Introduction](#introduction)
2. [Installing Modules](#installing-modules)
3. [Module Architecture](#module-architecture)
4. [Creating Your First Module](#creating-your-first-module)
5. [Module Registration](#module-registration)
6. [Accessing Interpreter State](#accessing-interpreter-state)
7. [Example Modules](#example-modules)
8. [Best Practices](#best-practices)
9. [Built-in Modules](#built-in-modules)
10. [Contributing](#contributing)

---

## Introduction

Sifzz has a **modular architecture** that allows developers to extend the language with custom Python modules. This makes contributing to Sifzz easier and enables domain-specific extensions without modifying the core interpreter.

### Why Modules?

- 📦 **Encapsulation** - Keep related functionality together
- 🔌 **Plug-and-play** - Drop modules in the `modules/` directory
- 🛠️ **Easy Development** - Simple API for adding commands
- 🌐 **Community Extensions** - Share modules with others
- 🔒 **Core Protection** - Don't modify the main interpreter

---

## Installing Modules
To install a module, download its .py file FROM THE OFFICIAL Sifzz REPOSITORY ONLY and put it in `modules/`. Sifzz should automatically detect this. If the module that you are installing isn't from the official repository, make sure that they have been approved in the [Approved Modules List](aml.md).
---

## Module Architecture

### Directory Structure

```
sifzz-project/
├── sifzz.py                  # Main interpreter
├── modules/                  # Module directory
│   ├── mdg.md                # Module Development Guide (This file)
```

### How Modules Work

1. **Discovery** - Interpreter scans `modules/` directory
2. **Loading** - Python modules are imported dynamically
3. **Registration** - Module registers its commands
4. **Execution** - Commands are matched via regex patterns
5. **Handling** - Module handlers execute the commands

---

## Creating Your First Module

### Step 1: Create the Module File

Create `modules/hello_module.py`:

```python
"""
Hello Module for Sifzz
A simple example module
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sifzz import SifzzModule
import re

class HelloModule(SifzzModule):
    """Simple greeting module"""
    
    def register_commands(self):
        """Register commands this module provides"""
        
        # Register: greet "Name"
        self.register(
            r'greet "([^"]+)"',
            self.greet_person,
            "Greet a person by name"
        )
        
        # Register: shout "Message"
        self.register(
            r'shout "([^"]+)"',
            self.shout_message,
            "Shout a message in uppercase"
        )
    
    def greet_person(self, match):
        """Handler for 'greet' command"""
        name = match.group(1)
        print(f"Hello, {name}! Nice to meet you!")
    
    def shout_message(self, match):
        """Handler for 'shout' command"""
        message = match.group(1)
        print(f"{message.upper()}!!!")
```

### Step 2: Use in Sifzz

Create `test.sfzz`:

```
# Test the hello module
greet "Alice"
shout "this is amazing"
```

### Step 3: Run

```bash
python sifzz.py test.sfzz
```

Output:
```
[INFO] Loaded module: hello_module
Hello, Alice! Nice to meet you!
THIS IS AMAZING!!!
```

---

## Module Registration

### The SifzzModule Base Class

All modules inherit from `SifzzModule`:

```python
class MyModule(SifzzModule):
    def register_commands(self):
        # Register your commands here
        pass
```

### The register() Method

```python
self.register(pattern, handler, description)
```

**Parameters:**
- `pattern` (str) - Regex pattern to match command
- `handler` (function) - Function to call when matched
- `description` (str) - Human-readable description

### Pattern Examples

```python
# Simple command
r'hello'

# Command with quoted string
r'say "([^"]+)"'

# Command with variable name
r'set (\w+) to (.+)'

# Command with number
r'wait (\d+\.?\d*) seconds?'

# Complex command
r'download "([^"]+)" as "([^"]+)"'
```

### Handler Functions

Handlers receive a `match` object from regex:

```python
def my_handler(self, match):
    # Extract captured groups
    arg1 = match.group(1)
    arg2 = match.group(2)
    
    # Do something with the interpreter
    self.interpreter.variables['result'] = arg1 + arg2
```

---

## Accessing Interpreter State

Your module has access to the interpreter through `self.interpreter`:

### Variables

```python
# Get a variable
value = self.interpreter.variables.get('myVar', default_value)

# Set a variable
self.interpreter.variables['myVar'] = 42

# Check if variable exists
if 'myVar' in self.interpreter.variables:
    # ...
```

### Lists

```python
# Get a list
my_list = self.interpreter.lists.get('myList', [])

# Set a list
self.interpreter.lists['myList'] = [1, 2, 3]

# Modify a list
self.interpreter.lists['myList'].append(item)
```

### Functions

```python
# Check if function exists
if 'myFunction' in self.interpreter.functions:
    # Get function start and end lines
    func_start, func_end = self.interpreter.functions['myFunction']
```

### Evaluate Expressions

```python
# Evaluate a Sifzz expression
result = self.interpreter.eval_expression('"hello" + " world"')

# Evaluate a condition
is_true = self.interpreter.eval_condition('x greater than 5')
```

---

## Example Modules

### 1. Math Operations Module

```python
"""Advanced Math Operations Module"""

from sifzz import SifzzModule
import math

class MathModule(SifzzModule):
    def register_commands(self):
        self.register(
            r'set (\w+) to sin\((.+)\)',
            self.calc_sin,
            "Calculate sine"
        )
        
        self.register(
            r'set (\w+) to cos\((.+)\)',
            self.calc_cos,
            "Calculate cosine"
        )
        
        self.register(
            r'set (\w+) to power\((.+), (.+)\)',
            self.calc_power,
            "Calculate power (base, exponent)"
        )
    
    def calc_sin(self, match):
        var_name = match.group(1)
        value = self.interpreter.eval_expression(match.group(2))
        self.interpreter.variables[var_name] = math.sin(float(value))
    
    def calc_cos(self, match):
        var_name = match.group(1)
        value = self.interpreter.eval_expression(match.group(2))
        self.interpreter.variables[var_name] = math.cos(float(value))
    
    def calc_power(self, match):
        var_name = match.group(1)
        base = self.interpreter.eval_expression(match.group(2))
        exp = self.interpreter.eval_expression(match.group(3))
        self.interpreter.variables[var_name] = math.pow(float(base), float(exp))
```

**Usage:**
```
set angle to 1.57
set result to sin(angle)
say result  # ~1.0

set x to power(2, 8)
say x  # 256.0
```

### 2. JSON Module

```python
"""JSON Operations Module"""

from sifzz import SifzzModule
import json

class JsonModule(SifzzModule):
    def register_commands(self):
        self.register(
            r'parse json "([^"]+)" and store in (\w+)',
            self.parse_json,
            "Parse JSON string into variable"
        )
        
        self.register(
            r'get json key "([^"]+)" from (\w+) and store in (\w+)',
            self.get_json_key,
            "Extract value from JSON by key"
        )
    
    def parse_json(self, match):
        json_str = match.group(1)
        var_name = match.group(2)
        
        try:
            data = json.loads(json_str)
            self.interpreter.variables[var_name] = data
        except json.JSONDecodeError as e:
            print(f"JSON Error: {e}")
            self.interpreter.variables[var_name] = None
    
    def get_json_key(self, match):
        key = match.group(1)
        source_var = match.group(2)
        target_var = match.group(3)
        
        if source_var in self.interpreter.variables:
            data = self.interpreter.variables[source_var]
            if isinstance(data, dict):
                self.interpreter.variables[target_var] = data.get(key, None)
```

**Usage:**
```
parse json "{\"name\": \"Alice\", \"age\": 30}" and store in person
get json key "name" from person and store in personName
say personName  # Alice
```

### 3. Date/Time Module

```python
"""Date and Time Operations Module"""

from sifzz import SifzzModule
from datetime import datetime, timedelta

class DateTimeModule(SifzzModule):
    def register_commands(self):
        self.register(
            r'set (\w+) to current time',
            self.get_current_time,
            "Get current time"
        )
        
        self.register(
            r'set (\w+) to current date',
            self.get_current_date,
            "Get current date"
        )
        
        self.register(
            r'format (\w+) as "([^"]+)" and store in (\w+)',
            self.format_datetime,
            "Format datetime with custom format"
        )
    
    def get_current_time(self, match):
        var_name = match.group(1)
        self.interpreter.variables[var_name] = datetime.now().strftime("%H:%M:%S")
    
    def get_current_date(self, match):
        var_name = match.group(1)
        self.interpreter.variables[var_name] = datetime.now().strftime("%Y-%m-%d")
    
    def format_datetime(self, match):
        source_var = match.group(1)
        format_str = match.group(2)
        target_var = match.group(3)
        
        # This is simplified - would need proper datetime object handling
        self.interpreter.variables[target_var] = format_str
```

**Usage:**
```
set now to current time
say now  # 14:30:45

set today to current date
say today  # 2025-10-03
```

### 4. Database Module

```python
"""Simple Database/Storage Module"""

from sifzz import SifzzModule
import json
import os

class DatabaseModule(SifzzModule):
    def __init__(self, interpreter):
        super().__init__(interpreter)
        self.db_file = "sifzz_db.json"
        self.load_db()
    
    def load_db(self):
        """Load database from file"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                self.db = json.load(f)
        else:
            self.db = {}
    
    def save_db(self):
        """Save database to file"""
        with open(self.db_file, 'w') as f:
            json.dump(self.db, f, indent=2)
    
    def register_commands(self):
        self.register(
            r'save "([^"]+)" as (\w+) in database',
            self.db_save,
            "Save value to database with key"
        )
        
        self.register(
            r'load (\w+) from database and store in (\w+)',
            self.db_load,
            "Load value from database by key"
        )
        
        self.register(
            r'delete (\w+) from database',
            self.db_delete,
            "Delete key from database"
        )
    
    def db_save(self, match):
        value = match.group(1)
        key = match.group(2)
        self.db[key] = value
        self.save_db()
    
    def db_load(self, match):
        key = match.group(1)
        var_name = match.group(2)
        self.interpreter.variables[var_name] = self.db.get(key, None)
    
    def db_delete(self, match):
        key = match.group(1)
        if key in self.db:
            del self.db[key]
            self.save_db()
```

**Usage:**
```
save "John Doe" as username in database
load username from database and store in name
say name  # John Doe
```

---

## Best Practices

### 1. Clear Command Syntax

Use natural, readable command syntax:

✅ **Good:**
```python
r'download "([^"]+)" as "([^"]+)"'
# Usage: download "http://example.com" as "file.zip"
```

❌ **Bad:**
```python
r'dl ([^ ]+) ([^ ]+)'
# Usage: dl http://example.com file.zip
```

### 2. Error Handling

Always handle errors gracefully:

```python
def my_handler(self, match):
    try:
        # Your logic here
        pass
    except FileNotFoundError:
        print("Error: File not found")
    except Exception as e:
        print(f"Error: {e}")
```

### 3. Dependencies

Check for optional dependencies:

```python
def __init__(self, interpreter):
    super().__init__(interpreter)
    try:
        import requests
        self.requests = requests
        self.available = True
    except ImportError:
        print("[WARNING] Module requires 'requests'")
        print("          Install with: pip install requests")
        self.available = False
```

### 4. Documentation

Document your module well:

```python
"""
My Awesome Module

This module provides:
- command1: Does something cool
- command2: Does something else

Dependencies:
- requests (pip install requests)
"""
```

### 5. Naming Conventions

- Module files: `snake_case.py`
- Class names: `PascalCase`
- Methods: `snake_case`
- Commands: `natural language syntax`

### 6. Testing

Create test scripts for your module:

```
# test_mymodule.sfzz
say "Testing My Module"

# Test command 1
my command "test"

# Test command 2
another command with params

say "Tests complete!"
```

---

## Built-in Modules

### Core (Built-in)

These are built into the interpreter:
- Variables (`set`, `increase`, `decrease`)
- Output (`say`, `write`)
- Input (`ask`)
- Lists (`create list`, `add to`, `remove from`)
- Control flow (`if`, `loop`, `repeat`, `for each`)
- Functions (`function`, `call`)
- Math operators (`add`, `subtract`, `multiply`, `divide`)

### Community Modules

Place these in `modules/`:
- `file_operations.py` - File I/O
- `web_operations.py` - HTTP requests
- `json_module.py` - JSON parsing
- `datetime_module.py` - Date/time operations
- `database_module.py` - Simple database

---

## Contributing

### Submitting a Module

1. Create your module in `modules/`
2. Test thoroughly with example scripts
3. Document the commands clearly
4. Handle errors gracefully
5. Check for dependencies
6. Submit as a pull request

### Module Template

```python
"""
Module Name
Brief description

Commands:
- command1: Description
- command2: Description

Dependencies:
- library1 (optional)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sifzz import SifzzModule

class MyModule(SifzzModule):
    """Module description"""
    
    def register_commands(self):
        """Register all commands"""
        self.register(
            r'pattern here',
            self.handler_method,
            "Description"
        )
    
    def handler_method(self, match):
        """Handle the command"""
        # Implementation here
        pass
```

---

## Advanced Topics

### Module State

Modules can maintain their own state:

```python
class StatefulModule(SifzzModule):
    def __init__(self, interpreter):
        super().__init__(interpreter)
        self.counter = 0
        self.cache = {}
    
    def increment_counter(self, match):
        self.counter += 1
        print(f"Counter: {self.counter}")
```

### Inter-Module Communication

Access other modules through the interpreter:

```python
# In one module
self.interpreter.variables['shared_data'] = data

# In another module
data = self.interpreter.variables.get('shared_data')
```

### Custom Evaluators

Add custom expression evaluators:

```python
def register_commands(self):
    # This would require core interpreter modifications
    # But you can work with eval_expression
    pass
```

---

## FAQ

**Q: Can modules modify the core interpreter?**  
A: Yes, through `self.interpreter`, but be careful!

**Q: Can modules depend on other modules?**  
A: Not directly, but they can share data through variables.

**Q: How do I debug my module?**  
A: Use print statements and test with simple .sfzz scripts.

**Q: Can I distribute my module?**  
A: Yes! Share your .py file and documentation.

**Q: What if my regex pattern conflicts with core commands?**  
A: Core commands are checked first. Use specific patterns.

---

## Resources

- Sifzz GitHub Repository
- Python Regex Documentation
- Module Examples Gallery
- Community Forum

---

**Happy Module Development! 🚀**
