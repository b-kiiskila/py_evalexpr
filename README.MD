# py_evalexpr

[![PyPI version](https://img.shields.io/pypi/v/py-evalexpr.svg)](https://pypi.org/project/py-evalexpr/)
[![CI](https://github.com/b-kiiskila/py_evalexpr/actions/workflows/maturin-ci.yml/badge.svg)](https://github.com/b-kiiskila/py_evalexpr/actions/workflows/maturin-ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python extension module written in Rust that provides bindings to the [`evalexpr`](https://crates.io/crates/evalexpr) crate for expression evaluation.

## 🌟 Features

- 🧮 Evaluate mathematical and logical expressions from Python
- 🔒 Three evaluation contexts:
  - **StatelessContext**: Simple expressions without variables
  - **ImmutableContext**: Expressions with predefined variables
  - **MutableContext**: Expressions that can update variables
- 📊 Type-specific evaluation methods for:
  - Integers
  - Floats
  - Strings
  - Booleans
  - Tuples
- 🚀 Built using Rust's `evalexpr` crate (version 12.0.2)
- 🐍 Python bindings via `PyO3`

## 🔧 Prerequisites

- Python 3.11 or higher
- Rust toolchain (cargo, rustc)
- Compatible C compiler

## 📦 Installation

```bash
pip install py-evalexpr
```

## 💡 Usage Examples

### Quick Evaluation

```python
from py_evalexpr import evaluate, evaluate_int, evaluate_float

# Basic arithmetic
result = evaluate("2 + 3 * 4")         # Returns 14
result = evaluate("sqrt(16) + 2")      # Returns 6.0

# Type-specific evaluation
int_val = evaluate_int("42")           # Returns 42 as int
float_val = evaluate_float("3.14159")  # Returns 3.14159 as float
bool_val = evaluate_boolean("5 > 3")   # Returns True
```

### Context Usage

#### Stateless Context

```python
from py_evalexpr import StatelessContext

context = StatelessContext()
result = context.evaluate("42").value          # Integer: 42
result = context.evaluate("sin(0.5)").value    # Uses built-in math functions
```

#### Immutable Context

```python
from py_evalexpr import ImmutableContext

context = ImmutableContext()
context.variables["x"] = 10
context.variables["y"] = 20

result = context.evaluate("x + y").value       # Returns 30
```

#### Mutable Context

```python
from py_evalexpr import MutableContext

context = MutableContext()
context.evaluate_empty("x = 10")
context.evaluate_empty("y = 20")
context.evaluate_empty("sum = x + y")
result = context.evaluate("sum * 2").value     # Returns 60
```

## 🛡️ Error Handling

```python
from py_evalexpr import evaluate
from py_evalexpr.exceptions import EvaluationError

try:
    result = evaluate("undefined_var + 5")
except EvaluationError as e:
    print(f"Evaluation error: {e}")
```

## 🤝 Contributing

Contributions are welcome:
- Open an issue to discuss proposed changes
- Submit pull requests
- Follow existing code style

## 🙏 Acknowledgments

- [evalexpr](https://crates.io/crates/evalexpr) - Rust crate that powers this project
- [PyO3](https://pyo3.rs) - Python extensions framework
- [maturin](https://maturin.rs) - Python packaging tool
- [devbox](https://www.jetify.com/devbox) - Predictable development environments
- [uv](https://github.com/astral-sh/uv) - Python package installer

---
Made in 🇨🇦🍁 by [Benjamin Kiiskila](https://github.com/b-kiiskila)
