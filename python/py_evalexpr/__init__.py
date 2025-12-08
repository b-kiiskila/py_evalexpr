"""
Python bindings for the evalexpr expression evaluation engine.

This package provides a safe and efficient way to evaluate mathematical and logical
expressions in Python. It supports different evaluation contexts for various use
cases, from simple stateless evaluation to full stateful expression processing.

The package provides three types of evaluation contexts:
- StatelessContext: For pure expression evaluation without any state
- ImmutableContext: For evaluation with constant state that expressions can read
- MutableContext: For evaluation with state that expressions can modify

Author: Benjamin Kiiskila
License: MIT
Repository: https://github.com/b-kiiskila/py_evalexpr
"""

__version__ = "1.1.0"

from . import natives

# Import our public interfaces
from py_evalexpr.base_context import ValidTypes, ValidTuple
from py_evalexpr.exceptions import (
    EvalExprError,
    EvaluationError,
    VariableError,
    FunctionError,
)
from py_evalexpr.immutable_context import ImmutableContext
from py_evalexpr.mutable_context import MutableContext
from py_evalexpr.quickeval import (
    evaluate,
    evaluate_int,
    evaluate_float,
    evaluate_string,
    evaluate_boolean,
    evaluate_tuple,
)
from py_evalexpr.stateless_context import StatelessContext


__all__ = [
    # Native functions, direct bindings to our Rust code
    "natives",
    # Context types
    "StatelessContext",
    "ImmutableContext",
    "MutableContext",
    # Type definitions
    "ValidTypes",
    "ValidTuple",
    # Convenience functions
    "evaluate",
    "evaluate_int",
    "evaluate_float",
    "evaluate_string",
    "evaluate_boolean",
    "evaluate_tuple",
    # Exceptions
    "EvalExprError",
    "EvaluationError",
    "VariableError",
    "FunctionError",
]
