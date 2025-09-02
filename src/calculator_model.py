import json
import math

class MathCalculator:
    """
    A comprehensive mathematical calculator supporting basic arithmetic,
    power operations, square root, and trigonometric functions.
    
    Supported Operations:
    - Basic: add, subtract, multiply, divide
    - Advanced: power, sqrt, sin, cos, tan, log
    
    All trigonometric functions work with degrees (not radians).
    Logarithm uses natural log (base e).
    
    Example:
        calc = MathCalculator()
        result = calc.calculate('add', 10, 5)  # Returns 15
        result = calc.calculate('sqrt', 16)    # Returns 4.0
    """
    
    def __init__(self):
        """Initialize calculator with supported operations mapping."""
        self.operations = {
            'add': self._add,
            'subtract': self._subtract,
            'multiply': self._multiply,
            'divide': self._divide,
            'power': self._power,
            'sqrt': self._sqrt,
            'sin': self._sin,
            'cos': self._cos,
            'tan': self._tan,
            'log': self._log
        }
    
    def _add(self, a, b):
        """Add two numbers: a + b"""
        return a + b
    
    def _subtract(self, a, b):
        """Subtract two numbers: a - b"""
        return a - b
    
    def _multiply(self, a, b):
        """Multiply two numbers: a * b"""
        return a * b
    
    def _divide(self, a, b):
        """Divide two numbers: a / b
        
        Raises:
            ValueError: If b is zero (division by zero)
        """
        if b == 0:
            raise ValueError("Division by zero")
        return a / b
    
    def _power(self, a, b):
        """Raise a to the power of b: a^b"""
        return a ** b
    
    def _sqrt(self, a, b=None):
        """Calculate square root of a
        
        Args:
            a: Number to calculate square root of
            b: Unused (for consistency with other operations)
            
        Raises:
            ValueError: If a is negative
        """
        if a < 0:
            raise ValueError("Square root of negative number")
        return math.sqrt(a)
    
    def _sin(self, a, b=None):
        """Calculate sine of a (in degrees)
        
        Args:
            a: Angle in degrees
            b: Unused (for consistency with other operations)
        """
        return math.sin(math.radians(a))
    
    def _cos(self, a, b=None):
        """Calculate cosine of a (in degrees)
        
        Args:
            a: Angle in degrees
            b: Unused (for consistency with other operations)
        """
        return math.cos(math.radians(a))
    
    def _tan(self, a, b=None):
        """Calculate tangent of a (in degrees)
        
        Args:
            a: Angle in degrees
            b: Unused (for consistency with other operations)
        """
        return math.tan(math.radians(a))
    
    def _log(self, a, b=None):
        """Calculate natural logarithm of a
        
        Args:
            a: Number to calculate log of
            b: Unused (for consistency with other operations)
            
        Raises:
            ValueError: If a is zero or negative
        """
        if a <= 0:
            raise ValueError("Logarithm of non-positive number")
        return math.log(a)
    
    def calculate(self, operation, a, b=None):
        """
        Perform a mathematical calculation.
        
        Args:
            operation (str): The operation to perform. Must be one of:
                           'add', 'subtract', 'multiply', 'divide', 'power',
                           'sqrt', 'sin', 'cos', 'tan', 'log'
            a (float): First operand
            b (float, optional): Second operand (required for binary operations)
            
        Returns:
            float: Result of the calculation
            
        Raises:
            ValueError: If operation is unsupported or calculation fails
            
        Examples:
            >>> calc = MathCalculator()
            >>> calc.calculate('add', 10, 5)
            15
            >>> calc.calculate('sqrt', 16)
            4.0
            >>> calc.calculate('sin', 90)
            1.0
        """
        if operation not in self.operations:
            raise ValueError(f"Unsupported operation: {operation}. "
                           f"Supported operations: {list(self.operations.keys())}")
        
        try:
            return self.operations[operation](a, b)
        except Exception as e:
            raise ValueError(f"Calculation error in '{operation}': {str(e)}")