"""
Exception definitions for expression evaluation errors.

This module provides the exception hierarchy used by the package for reporting
errors that occur during expression evaluation, variable management, and function
handling. All exceptions inherit from EvalExprError to enable consistent error
handling.
"""


class EvalExprError(Exception):
    """
    Base exception class for all errors in the expression evaluation system.
    """

    pass


class VariableError(EvalExprError):
    """
    Indicates an error in variable operations such as assignment or access.

    This error occurs when:
    - A variable name is invalid
    - A variable value has an unsupported type
    - A nonexistent variable is accessed or deleted
    """

    pass


class FunctionError(EvalExprError):
    """
    Indicates an error in function registration or execution.

    This error occurs when:
    - A function name is invalid
    - A registered value isn't callable
    - A function fails during execution
    """

    pass


class EvaluationError(EvalExprError):
    """
    Indicates an error during expression evaluation.

    This error occurs when:
    - An expression has syntax errors
    - Types don't match the operation (e.g., adding string to number)
    - Runtime errors occur (e.g., division by zero)
    """

    pass
