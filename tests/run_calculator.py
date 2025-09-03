"""
A simple script to demonstrate the usage of the MathCalculator class.

This file imports the MathCalculator, creates an instance, and runs
a series of predefined calculations to show how it works and how it
handles both valid operations and errors.

To run this script, you can either be in the project root directory
(`SageMakerCalculator`) and run `python tests/run_calculator.py`, or
be inside the `tests` directory and run:
    python run_calculator.py
"""

# --- Path Correction to find the 'src' directory ---
import sys
from pathlib import Path

# Add the project's 'src' directory (parent's sibling) to the Python path
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC_DIR))

# Import the MathCalculator class from the calculator_model module
from calculator_model import MathCalculator

def main():
    """
    Main function to create a calculator and run demonstrations.
    """
    print("--- Demonstrating the MathCalculator Class ---")

    # 1. Create an instance of the calculator
    calc = MathCalculator()
    print("Calculator instance created.\n")

    # 2. Define a list of test calculations to perform
    calculations = [
        {'operation': 'add', 'a': 20, 'b': 22},
        {'operation': 'multiply', 'a': 6, 'b': 7},
        {'operation': 'power', 'a': 2, 'b': 10},
        {'operation': 'sqrt', 'a': 81},
        {'operation': 'sin', 'a': 90},      # Input is in degrees
        {'operation': 'log', 'a': 1},       # Natural log
        {'operation': 'divide', 'a': 10, 'b': 0}, # Example of a calculation error
        {'operation': 'invent', 'a': 1, 'b': 1}  # Example of an unsupported operation
    ]

    # 3. Loop through the calculations and print the results
    for calc_input in calculations:
        op, a, b = calc_input['operation'], calc_input['a'], calc_input.get('b')

        print("-" * 30)
        print(f"Attempting: {calc_input}")
        try:
            # Call the core 'calculate' method
            result = calc.calculate(operation=op, a=a, b=b)
            print(f"  -> Success! Result: {result}")
        except ValueError as e:
            # Catch and print any expected errors from the calculator
            print(f"  -> Caught an error: {e}")

if __name__ == "__main__":
    main()