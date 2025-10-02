#!/usr/bin/env python3
"""
Sifzz (.sfzz) Interpreter v2.0
A simple, beginner-friendly scripting language with natural syntax
"""

import re
import sys
import random
import time
import math
from pathlib import Path

class SifzzInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.lists = {}
        self.loop_break = False
        self.loop_continue = False
        
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
        lines = code.split('\n')
        self.execute_block(lines, 0, len(lines))
    
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
            
            self.execute_line(line)
            i += 1
        
        return i
    
    def find_block_end(self, lines, start, end_marker):
        """Find the end of a block"""
        depth = 1
        i = start + 1
        
        block_starters = ['if ', 'repeat ', 'loop ', 'for each ', 'function ', 'else if ', 'else:']
        block_enders = ['end if', 'end repeat', 'end loop', 'end for', 'end function']
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Check if this line starts a new block
            if any(line.startswith(starter) for starter in block_starters):
                depth += 1
            
            # Check if this line ends a block
            if any(line == ender for ender in block_enders):
                depth -= 1
                if depth == 0:
                    return i
            
            # Special case for else/else if (doesn't increase depth)
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
        
        # Find else if and else clauses
        i = block_start
        current_start = block_start
        executed = False
        
        if self.eval_condition(condition):
            # Find where this if block ends (before else if/else)
            clause_end = block_end
            for j in range(block_start, block_end + 1):
                if lines[j].strip().startswith('else if ') or lines[j].strip() == 'else:':
                    clause_end = j - 1
                    break
            self.execute_block(lines, block_start, clause_end + 1)
            executed = True
        
        # Check else if and else
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
        
        # Get the list
        if list_expr in self.lists:
            items = self.lists[list_expr]
        else:
            # Try to evaluate as range
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
        """Execute a single line of code"""
        # Set variable: set x to 5
        if line.startswith('set ') and ' to ' in line:
            match = re.match(r'set (\w+) to (.+)', line)
            if match:
                var_name = match.group(1)
                value = self.eval_expression(match.group(2))
                self.variables[var_name] = value
                return
        
        # Create list: create list myList
        if line.startswith('create list '):
            list_name = line.split()[2]
            self.lists[list_name] = []
            return
        
        # Add to list: add "item" to myList
        if line.startswith('add ') and ' to ' in line:
            match = re.match(r'add (.+) to (\w+)', line)
            if match:
                value = self.eval_expression(match.group(1))
                target = match.group(2)
                
                # Check if target is a list
                if target in self.lists:
                    self.lists[target].append(value)
                # Otherwise treat as numeric addition to variable
                elif target in self.variables:
                    self.variables[target] += value
                else:
                    self.variables[target] = value
                return
        
        # Remove from list: remove "item" from myList
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
                return
        
        # Get list size: set x to size of myList
        if 'size of' in line:
            match = re.match(r'set (\w+) to size of (\w+)', line)
            if match:
                var_name = match.group(1)
                list_name = match.group(2)
                if list_name in self.lists:
                    self.variables[var_name] = len(self.lists[list_name])
                return
        
        # Get list item: set x to item 0 of myList
        if 'item' in line and ' of ' in line:
            match = re.match(r'set (\w+) to item (\d+) of (\w+)', line)
            if match:
                var_name = match.group(1)
                index = int(match.group(2))
                list_name = match.group(3)
                if list_name in self.lists and index < len(self.lists[list_name]):
                    self.variables[var_name] = self.lists[list_name][index]
                return
        
        # Clear list: clear myList
        if line.startswith('clear '):
            list_name = line.split()[1]
            if list_name in self.lists:
                self.lists[list_name].clear()
            return
        
        # Say/Print: say "Hello" or say x
        if line.startswith('say '):
            message = line[4:].strip()
            output = self.eval_expression(message)
            print(output)
            return
        
        # Say without newline: write "Hello"
        if line.startswith('write '):
            message = line[6:].strip()
            output = self.eval_expression(message)
            print(output, end='')
            return
        
        # Say with newline: newline
        if line == 'newline':
            print()
            return
        
        # Wait: wait 2 seconds
        if line.startswith('wait '):
            match = re.match(r'wait (\d+\.?\d*) seconds?', line)
            if match:
                time.sleep(float(match.group(1)))
                return
        
        # Subtract from variable: subtract 1 from x
        if line.startswith('subtract ') and ' from ' in line:
            match = re.match(r'subtract (.+) from (\w+)', line)
            if match:
                value = self.eval_expression(match.group(1))
                var_name = match.group(2)
                if var_name in self.variables:
                    self.variables[var_name] -= value
                return
        
        # Multiply variable: multiply x by 2
        if line.startswith('multiply ') and ' by ' in line:
            match = re.match(r'multiply (\w+) by (.+)', line)
            if match:
                var_name = match.group(1)
                value = self.eval_expression(match.group(2))
                if var_name in self.variables:
                    self.variables[var_name] *= value
                return
        
        # Divide variable: divide x by 2
        if line.startswith('divide ') and ' by ' in line:
            match = re.match(r'divide (\w+) by (.+)', line)
            if match:
                var_name = match.group(1)
                value = self.eval_expression(match.group(2))
                if var_name in self.variables and value != 0:
                    self.variables[var_name] /= value
                return
        
        # Call function: call myFunction
        if line.startswith('call '):
            func_name = line[5:].strip()
            if func_name in self.functions:
                func_start, func_end = self.functions[func_name]
                # Need access to original lines - store them
                if hasattr(self, 'all_lines'):
                    self.execute_block(self.all_lines, func_start, func_end)
                return
        
        # Ask for input: ask "What's your name?" and store in name
        if line.startswith('ask '):
            match = re.match(r'ask "([^"]+)" and store in (\w+)', line)
            if match:
                prompt = match.group(1)
                var_name = match.group(2)
                self.variables[var_name] = input(prompt + " ")
                return
        
        # Ask for number: ask for number "Enter age:" and store in age
        if line.startswith('ask for number '):
            match = re.match(r'ask for number "([^"]+)" and store in (\w+)', line)
            if match:
                prompt = match.group(1)
                var_name = match.group(2)
                try:
                    self.variables[var_name] = float(input(prompt + " "))
                except ValueError:
                    self.variables[var_name] = 0
                return
        
        # Random number: set x to random number between 1 and 10
        if 'random number between' in line:
            match = re.match(r'set (\w+) to random number between (.+) and (.+)', line)
            if match:
                var_name = match.group(1)
                min_val = int(self.eval_expression(match.group(2)))
                max_val = int(self.eval_expression(match.group(3)))
                self.variables[var_name] = random.randint(min_val, max_val)
                return
        
        # Random choice: set x to random choice from myList
        if 'random choice from' in line:
            match = re.match(r'set (\w+) to random choice from (\w+)', line)
            if match:
                var_name = match.group(1)
                list_name = match.group(2)
                if list_name in self.lists and self.lists[list_name]:
                    self.variables[var_name] = random.choice(self.lists[list_name])
                return
        
        # Increase: increase x
        if line.startswith('increase '):
            var_name = line.split()[1]
            if var_name in self.variables:
                self.variables[var_name] += 1
            else:
                self.variables[var_name] = 1
            return
        
        # Decrease: decrease x
        if line.startswith('decrease '):
            var_name = line.split()[1]
            if var_name in self.variables:
                self.variables[var_name] -= 1
            else:
                self.variables[var_name] = -1
            return
        
        # Exit program: exit
        if line == 'exit':
            sys.exit(0)
            return
    
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
        
        # Handle string concatenation
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
        # Store original for string handling
        original = condition
        
        # Replace natural language operators
        condition = condition.replace(' is not ', ' != ')
        condition = condition.replace(' is ', ' == ')
        condition = condition.replace(' equals ', ' == ')
        condition = condition.replace(' greater than or equal to ', ' >= ')
        condition = condition.replace(' less than or equal to ', ' <= ')
        condition = condition.replace(' greater than ', ' > ')
        condition = condition.replace(' less than ', ' < ')
        condition = condition.replace(' and ', ' and ')
        condition = condition.replace(' or ', ' or ')
        condition = condition.replace(' not ', ' not ')
        
        # Handle 'contains' operator for strings and lists
        if ' contains ' in original:
            parts = original.split(' contains ')
            container = self.eval_expression(parts[0].strip())
            item = self.eval_expression(parts[1].strip())
            return item in container
        
        # Replace variables with their values
        for var_name, var_value in self.variables.items():
            if isinstance(var_value, str):
                condition = condition.replace(var_name, f'"{var_value}"')
            else:
                condition = condition.replace(var_name, str(var_value))
        
        try:
            return eval(condition)
        except:
            return False
    
    def run(self, code):
        """Run Sifzz code (override to store lines)"""
        self.all_lines = code.split('\n')
        self.execute_block(self.all_lines, 0, len(self.all_lines))

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("=" * 50)
        print("Sifzz Interpreter v2.0")
        print("=" * 50)
        print("\nUsage: python sifzz.py <filename.sfzz>")
        print("\nQuick Example:")
        print('  say "Hello, World!"')
        print('  set x to 10')
        print('  say x')
        print("\nFor full documentation, visit:")
        print("  https://github.com/yourusername/sifzz")
        print("=" * 50)
        sys.exit(1)
    
    interpreter = SifzzInterpreter()
    interpreter.run_file(sys.argv[1])

if __name__ == "__main__":
    main()
