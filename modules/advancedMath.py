"""
This is an OFFICIAL Sifzz module.

Advanced Math Operations Module

"""

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