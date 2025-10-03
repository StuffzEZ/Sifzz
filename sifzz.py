#!/usr/bin/env python3
"""
Sifzz (.sfzz) Interpreter v3.0
A simple, beginner-friendly scripting language with modular architecture
"""

import re
import sys
import random
import time
import math
import importlib.util
from pathlib import Path

class SifzzModule:
    """Base class for Sifzz modules"""
    
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.commands = {}
        self.register_commands()
    
    def register_commands(self):
        """Override this method to register module commands"""
        pass
    
    def register(self, pattern, handler, description=""):
        """Register a command pattern with its handler"""
        self.commands[pattern] = {
            'handler': handler,
            'description': description
        }

class SifzzInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.lists = {}
        self.loop_break = False
        self.loop_continue = False
        self.modules = []
        self.all_lines = []
        
        # Load built-in modules
        self.load_builtin_modules()
        
        # Load external modules from modules/ directory
        self.load_external_modules()
    
    def load_builtin_modules(self):
        """Load built-in core modules"""
        # Core functionality is built into the interpreter
        pass
    
    def load_external_modules(self, directory="modules"):
        """Load external Python modules from directory"""
        module_dir = Path(directory)
        
        if not module_dir.exists():
            return
        
        # Find all .py files in modules directory
        for module_file in module_dir.glob("*.py"):
            if module_file.stem.startswith("_"):
                continue
                
            try:
                # Load the module dynamically
                spec = importlib.util.spec_from_file_location(
                    module_file.stem, 
                    module_file
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Look for SifzzModule classes
                for item_name in dir(module):
                    item = getattr(module, item_name)
                    if (isinstance(item, type) and 
                        issubclass(item, SifzzModule) and 
                        item is not SifzzModule):
                        # Instantiate and register the module
                        module_instance = item(self)
                        self.modules.append(module_instance)
                        print(f"[INFO] Loaded module: {module_file.stem}")
            
            except Exception as e:
                print(f"[WARNING] Failed to load module {module_file.stem}: {e}")
    
    def run_file(self, filename):
        """Run a .sfzz file"""
        try:
            with open(filename, 'r') as f:
                code = f.read()
            self.run(code)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
            sys.exit(1)
    
    def run(self, code):
        """Run Sifzz code"""
        self.all_lines = code.split('\n')
        self.execute_block(self.all_lines, 0, len(self.all_lines))
    
    def execute_block(self, lines, start, end):
        """Execute a block of code"""
        i = start
        while i < end:
            if self.loop_break or self.loop_continue:
                break
                
            line = lines[i].strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                i += 1
                continue
            
            # Handle function definitions
            if line.startswith('function '):
                func_name = line.split()[1].rstrip(':')
                func_start = i + 1
                func_end = self.find_block_end(lines, i, 'end function')
                self.functions[func_name] = (func_start, func_end)
                i = func_end + 1
                continue
            
            # Handle if statements
            if line.startswith('if '):
                i = self.handle_if(lines, i)
                continue
            
            # Handle loops
            if line.startswith('repeat '):
                i = self.handle_repeat(lines, i)
                continue
            
            if line.startswith('loop '):
                i = self.handle_loop(lines, i)
                continue
            
            if line.startswith('for each '):
                i = self.handle_foreach(lines, i)
                continue
            
            # Break and continue
            if line == 'break':
                self.loop_break = True
                return i
            
            if line == 'continue':
                self.loop_continue = True
                return i
            
            # Try to execute line
            if not self.execute_line(line):
                # If core didn't handle it, try modules
                self.try_module_commands(line)
            
            i += 1
        
        return i
    
    def try_module_commands(self, line):
        """Try to execute a command using loaded modules"""
        for module in self.modules:
            for pattern, command_info in module.commands.items():
                match = re.match(pattern, line)
                if match:
                    handler = command_info['handler']
                    handler(match)
                    return True
        return False
    
    def find_block_end(self, lines, start, end_marker):
        """Find the end of a block"""
        depth = 1
        i = start + 1
        
        block_starters = ['if ', 'repeat ', 'loop ', 'for each ', 'function ', 'else if ', 'else:']
        block_enders = ['end if', 'end repeat', 'end loop', 'end for', 'end function']
        
        while i < len(lines):
            line = lines[i].strip()
            
            if any(line.startswith(starter) for starter in block_starters):
                depth += 1
            
            if any(line == ender for ender in block_enders):
                depth -= 1
                if depth == 0:
                    return i
            
            if line.startswith('else if ') or line == 'else:':
                if depth == 1:
                    return i - 1
            
            i += 1
        
        return i
    
    def handle_if(self, lines, start):
        """Handle if/else if/else statements"""
        line = lines[start].strip()
        match = re.match(r'if (.+):', line)
        
        if not match:
            return start + 1
        
        condition = match.group(1)
        block_start = start + 1
        block_end = self.find_block_end(lines, start, 'end if')
        
        i = block_start
        current_start = block_start
        executed = False
        
        if self.eval_condition(condition):
            clause_end = block_end
            for j in range(block_start, block_end + 1):
                if lines[j].strip().startswith('else if ') or lines[j].strip() == 'else:':
                    clause_end = j - 1
                    break
            self.execute_block(lines, block_start, clause_end + 1)
            executed = True
        
        if not executed:
            i = block_start
            while i <= block_end:
                line = lines[i].strip()
                
                if line.startswith('else if '):
                    match = re.match(r'else if (.+):', line)
                    if match and self.eval_condition(match.group(1)):
                        clause_start = i + 1
                        clause_end = block_end
                        for j in range(i + 1, block_end + 1):
                            check_line = lines[j].strip()
                            if check_line.startswith('else if ') or check_line == 'else:':
                                clause_end = j - 1
                                break
                        self.execute_block(lines, clause_start, clause_end + 1)
                        executed = True
                        break
                
                elif line == 'else:':
                    self.execute_block(lines, i + 1, block_end)
                    break
                
                i += 1
        
        return block_end + 1
    
    def handle_repeat(self, lines, start):
        """Handle repeat X times loops"""
        line = lines[start].strip()
        match = re.match(r'repeat (\d+) times?:', line)
        
        if not match:
            return start + 1
        
        times = int(match.group(1))
        block_start = start + 1
        block_end = self.find_block_end(lines, start, 'end repeat')
        
        for _ in range(times):
            self.loop_break = False
            self.loop_continue = False
            self.execute_block(lines, block_start, block_end)
            if self.loop_break:
                self.loop_break = False
                break
        
        return block_end + 1
    
    def handle_loop(self, lines, start):
        """Handle while loops"""
        line = lines[start].strip()
        match = re.match(r'loop while (.+):', line)
        
        if not match:
            return start + 1
        
        condition = match.group(1)
        block_start = start + 1
        block_end = self.find_block_end(lines, start, 'end loop')
        
        while self.eval_condition(condition):
            self.loop_break = False
            self.loop_continue = False
            self.execute_block(lines, block_start, block_end)
            if self.loop_break:
                self.loop_break = False
                break
        
        return block_end + 1
    
    def handle_foreach(self, lines, start):
        """Handle for each loops"""
        line = lines[start].strip()
        match = re.match(r'for each (\w+) in (.+):', line)
        
        if not match:
            return start + 1
        
        var_name = match.group(1)
        list_expr = match.group(2)
        
        if list_expr in self.lists:
            items = self.lists[list_expr]
        else:
            range_match = re.match(r'range\((\d+),\s*(\d+)\)', list_expr)
            if range_match:
                items = list(range(int(range_match.group(1)), int(range_match.group(2))))
            else:
                items = []
        
        block_start = start + 1
        block_end = self.find_block_end(lines, start, 'end for')
        
        for item in items:
            self.variables[var_name] = item
            self.loop_break = False
            self.loop_continue = False
            self.execute_block(lines, block_start, block_end)
            if self.loop_break:
                self.loop_break = False
                break
        
        return block_end + 1
    
    def execute_line(self, line):
        """Execute a single line of code - returns True if handled"""
        
        # Set variable
        if line.startswith('set ') and ' to ' in line:
            match = re.match(r'set (\w+) to (.+)', line)
            if match:
                var_name = match.group(1)
                value = self.eval_expression(match.group(2))
                self.variables[var_name] = value
                return True
        
        # Create list
        if line.startswith('create list '):
            list_name = line.split()[2]
            self.lists[list_name] = []
            return True
        
        # Add to list/variable
        if line.startswith('add ') and ' to ' in line:
            match = re.match(r'add (.+) to (\w+)', line)
            if match:
                value = self.eval_expression(match.group(1))
                target = match.group(2)
                
                if target in self.lists:
                    self.lists[target].append(value)
                elif target in self.variables:
                    self.variables[target] += value
                else:
                    self.variables[target] = value
                return True
        
        # Remove from list
        if line.startswith('remove ') and ' from ' in line:
            match = re.match(r'remove (.+) from (\w+)', line)
            if match:
                value = self.eval_expression(match.group(1))
                list_name = match.group(2)
                if list_name in self.lists:
                    try:
                        self.lists[list_name].remove(value)
                    except ValueError:
                        pass
                return True
        
        # Get list size
        if 'size of' in line:
            match = re.match(r'set (\w+) to size of (\w+)', line)
            if match:
                var_name = match.group(1)
                list_name = match.group(2)
                if list_name in self.lists:
                    self.variables[var_name] = len(self.lists[list_name])
                return True
        
        # Get list item
        if 'item' in line and ' of ' in line:
            match = re.match(r'set (\w+) to item (\d+) of (\w+)', line)
            if match:
                var_name = match.group(1)
                index = int(match.group(2))
                list_name = match.group(3)
                if list_name in self.lists and index < len(self.lists[list_name]):
                    self.variables[var_name] = self.lists[list_name][index]
                return True
        
        # Clear list
        if line.startswith('clear '):
            list_name = line.split()[1]
            if list_name in self.lists:
                self.lists[list_name].clear()
            return True
        
        # Say/Print
        if line.startswith('say '):
            message = line[4:].strip()
            output = self.eval_expression(message)
            print(output)
            return True
        
        # Write without newline
        if line.startswith('write '):
            message = line[6:].strip()
            output = self.eval_expression(message)
            print(output, end='')
            return True
        
        # Newline
        if line == 'newline':
            print()
            return True
        
        # Wait
        if line.startswith('wait '):
            match = re.match(r'wait (\d+\.?\d*) seconds?', line)
            if match:
                time.sleep(float(match.group(1)))
                return True
        
        # Subtract
        if line.startswith('subtract ') and ' from ' in line:
            match = re.match(r'subtract (.+) from (\w+)', line)
            if match:
                value = self.eval_expression(match.group(1))
                var_name = match.group(2)
                if var_name in self.variables:
                    self.variables[var_name] -= value
                return True
        
        # Multiply
        if line.startswith('multiply ') and ' by ' in line:
            match = re.match(r'multiply (\w+) by (.+)', line)
            if match:
                var_name = match.group(1)
                value = self.eval_expression(match.group(2))
                if var_name in self.variables:
                    self.variables[var_name] *= value
                return True
        
        # Divide
        if line.startswith('divide ') and ' by ' in line:
            match = re.match(r'divide (\w+) by (.+)', line)
            if match:
                var_name = match.group(1)
                value = self.eval_expression(match.group(2))
                if var_name in self.variables and value != 0:
                    self.variables[var_name] /= value
                return True
        
        # Call function
        if line.startswith('call '):
            func_name = line[5:].strip()
            if func_name in self.functions:
                func_start, func_end = self.functions[func_name]
                self.execute_block(self.all_lines, func_start, func_end)
                return True
        
        # Ask for input
        if line.startswith('ask '):
            match = re.match(r'ask "([^"]+)" and store in (\w+)', line)
            if match:
                prompt = match.group(1)
                var_name = match.group(2)
                self.variables[var_name] = input(prompt + " ")
                return True
        
        # Ask for number
        if line.startswith('ask for number '):
            match = re.match(r'ask for number "([^"]+)" and store in (\w+)', line)
            if match:
                prompt = match.group(1)
                var_name = match.group(2)
                try:
                    self.variables[var_name] = float(input(prompt + " "))
                except ValueError:
                    self.variables[var_name] = 0
                return True
        
        # Random number
        if 'random number between' in line:
            match = re.match(r'set (\w+) to random number between (.+) and (.+)', line)
            if match:
                var_name = match.group(1)
                min_val = int(self.eval_expression(match.group(2)))
                max_val = int(self.eval_expression(match.group(3)))
                self.variables[var_name] = random.randint(min_val, max_val)
                return True
        
        # Random choice
        if 'random choice from' in line:
            match = re.match(r'set (\w+) to random choice from (\w+)', line)
            if match:
                var_name = match.group(1)
                list_name = match.group(2)
                if list_name in self.lists and self.lists[list_name]:
                    self.variables[var_name] = random.choice(self.lists[list_name])
                return True
        
        # Increase
        if line.startswith('increase '):
            var_name = line.split()[1]
            if var_name in self.variables:
                self.variables[var_name] += 1
            else:
                self.variables[var_name] = 1
            return True
        
        # Decrease
        if line.startswith('decrease '):
            var_name = line.split()[1]
            if var_name in self.variables:
                self.variables[var_name] -= 1
            else:
                self.variables[var_name] = -1
            return True
        
        # Exit
        if line == 'exit':
            sys.exit(0)
            return True
        
        return False
    
    def eval_expression(self, expr):
        """Evaluate an expression"""
        expr = expr.strip()
        
        # String literal
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]
        
        # Math functions
        if expr.startswith('sqrt('):
            inner = expr[5:-1]
            return math.sqrt(self.eval_expression(inner))
        
        if expr.startswith('round('):
            inner = expr[6:-1]
            return round(self.eval_expression(inner))
        
        if expr.startswith('abs('):
            inner = expr[4:-1]
            return abs(self.eval_expression(inner))
        
        # String functions
        if ' uppercase' in expr:
            var = expr.split()[0]
            if var in self.variables:
                return str(self.variables[var]).upper()
        
        if ' lowercase' in expr:
            var = expr.split()[0]
            if var in self.variables:
                return str(self.variables[var]).lower()
        
        if 'length of' in expr:
            var = expr.split()[-1]
            if var in self.variables:
                return len(str(self.variables[var]))
            if var in self.lists:
                return len(self.lists[var])
        
        # Number
        try:
            if '.' in expr:
                return float(expr)
            return int(expr)
        except ValueError:
            pass
        
        # Variable
        if expr in self.variables:
            return self.variables[expr]
        
        # Expression with variables
        original_expr = expr
        for var_name, var_value in self.variables.items():
            expr = expr.replace(var_name, str(var_value))
        
        # String concatenation
        if '+' in original_expr:
            parts = original_expr.split('+')
            result = ''
            for part in parts:
                part = part.strip()
                val = self.eval_expression(part)
                result += str(val)
            return result
        
        try:
            return eval(expr)
        except:
            return expr
    
    def eval_condition(self, condition):
        """Evaluate a condition"""
        original = condition
        
        condition = condition.replace(' is not ', ' != ')
        condition = condition.replace(' is ', ' == ')
        condition = condition.replace(' equals ', ' == ')
        condition = condition.replace(' greater than or equal to ', ' >= ')
        condition = condition.replace(' less than or equal to ', ' <= ')
        condition = condition.replace(' greater than ', ' > ')
        condition = condition.replace(' less than ', ' < ')
        
        # Handle 'contains'
        if ' contains ' in original:
            parts = original.split(' contains ')
            container = self.eval_expression(parts[0].strip())
            item = self.eval_expression(parts[1].strip())
            return item in container
        
        # Replace variables
        for var_name, var_value in self.variables.items():
            if isinstance(var_value, str):
                condition = condition.replace(var_name, f'"{var_value}"')
            else:
                condition = condition.replace(var_name, str(var_value))
        
        try:
            return eval(condition)
        except:
            return False

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("=" * 50)
        print("Sifzz Interpreter v3.0 (Modular)")
        print("=" * 50)
        print("\nUsage: python sifzz.py <filename.sfzz>")
        print("\nFeatures:")
        print("  - Natural, beginner-friendly syntax")
        print("  - Modular architecture for extensions")
        print("  - Place Python modules in modules/ directory")
        print("\nExample:")
        print('  say "Hello, World!"')
        print("=" * 50)
        sys.exit(1)
    
    interpreter = SifzzInterpreter()
    interpreter.run_file(sys.argv[1])

if __name__ == "__main__":
    main()
