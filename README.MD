# py_evalexpr

A Python extension module written in Rust that provides bindings to the [`evalexpr`](https://crates.io/crates/evalexpr)
crate, enabling quick and safe expression evaluation in Python.

## Features

- Evaluate mathematical and logical expressions from Python code
- Three types of evaluation contexts:
  - **StatelessContext**: For simple expressions without variables
  - **ImmutableContext**: For expressions using predefined variables
  - **MutableContext**: For expressions that can update variables
- Type-specific evaluation methods for integers, floats, strings, booleans, and tuples
- Convenience functions for quick expression evaluation
- Powered by Rust's `evalexpr` crate (version 12.0.2)
- Python bindings via `PyO3`

## Installation

### Prerequisites

- Python 3.11 or higher
- Rust toolchain (cargo, rustc)
- A C compiler compatible with your Python installation

### Installing from PyPI

```bash
pip install py_evalexpr
```

## Usage

### Quick Evaluation

For simple expressions, use the convenience functions:

```python
from py_evalexpr import evaluate, evaluate_int, evaluate_float

# Basic arithmetic
result = evaluate("2 + 3 * 4")         # Returns 14
result = evaluate("sqrt(16) + 2")      # Returns 6.0

# Type-specific evaluation
int_val = evaluate_int("42")           # Returns 42 as int
float_val = evaluate_float("3.14159")  # Returns 3.14159 as float
bool_val = evaluate_boolean("5 > 3")   # Returns True
str_val = evaluate_string('"hello" + " world"')  # Returns "hello world"
tuple_val = evaluate_tuple("1, 2, 3")  # Returns (1, 2, 3)
```

### Stateless Context

For expressions without variables or state:

```python
from py_evalexpr import StatelessContext

context = StatelessContext()

# Simple evaluation
result = context.evaluate("42").value          # Integer: 42
result = context.evaluate("3.14").value        # Float: 3.14
result = context.evaluate('"hello"').value     # String: "hello"
result = context.evaluate("true").value        # Boolean: True
result = context.evaluate("(1, 2, 3)").value   # Tuple: (1, 2, 3)

# Expressions with built-in functions
result = context.evaluate("sin(0.5) + cos(0.5)").value  # Uses built-in math functions
result = context.evaluate("sqrt(16) * 2").value         # Uses sqrt function
```

### Immutable Context

For expressions that use predefined variables:

```python
from py_evalexpr import ImmutableContext

context = ImmutableContext()

# Add variables
context.variables["x"] = 10
context.variables["y"] = 20
context.variables["name"] = "Alice"
context.variables["pi"] = 3.14159

# Add functions
context.functions["add"] = lambda x, y: x + y
context.functions["double"] = lambda x: x * 2

# Evaluate expressions using variables
result = context.evaluate("x + y").value             # Returns 30
result = context.evaluate_int("double(x)")           # Returns 20
result = context.evaluate_float("pi * 2")            # Returns 6.28318
result = context.evaluate_string('name + " Smith"')  # Returns "Alice Smith"
result = context.evaluate_boolean("x < y")           # Returns True

# Variables cannot be changed in expressions
# This would raise an error:
# context.evaluate("x = 20")  # Error: Cannot assign to variables in immutable context
```

### Mutable Context

For expressions that can create and modify variables:

```python
from py_evalexpr import MutableContext

context = MutableContext()

# Initialize some variables
context.variables["counter"] = 0
context.variables["total"] = 100

# Create new variables in expressions
context.evaluate_empty("new_var = 42")
assert context.variables["new_var"] == 42

# Update existing variables
context.evaluate_empty("counter += 1")
assert context.variables["counter"] == 1

# Multi-step calculations
context.evaluate_empty("x = 10")
context.evaluate_empty("y = 20")
context.evaluate_empty("sum = x + y")
result = context.evaluate("sum * 2").value  # Returns 60

# Add and use functions
context.functions["square"] = lambda x: x * x
context.evaluate_empty("squared_sum = square(sum)")
assert context.variables["squared_sum"] == 900  # (30 * 30)
```

## Error Handling

The library provides custom exception types for different error cases:

```python
from py_evalexpr import evaluate
from py_evalexpr.exceptions import EvaluationError, VariableError, FunctionError

try:
    result = evaluate("undefined_var + 5")
except EvaluationError as e:
    print(f"Evaluation error: {e}")

try:
    result = evaluate("invalid syntax +*-")
except EvaluationError as e:
    print(f"Syntax error: {e}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. It's advisable to open an issue first to discuss the changes you'd like to make.

## Acknowledgments

- [evalexpr](https://crates.io/crates/evalexpr) - The Rust crate that powers this project
- [PyO3](https://pyo3.rs) - The framework for building Python extensions in Rust
- [maturin](https://maturin.rs) - The Python packaging tool used to build this project

---
Made in 🇨🇦🍁 by [Benjamin Kiiskila](https://github.com/b-kiiskila)