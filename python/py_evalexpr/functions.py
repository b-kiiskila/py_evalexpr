"""
Function registration support for evaluation contexts.

This module provides the FunctionsDict class which implements function registration
for evaluation contexts. It allows Python functions to be registered with names
that can then be used within expressions.
"""

from typing import Any, Callable

from py_evalexpr.exceptions import FunctionError


class FunctionsDict:
    """
    Dictionary-like interface for managing functions in evaluation contexts.

    Functions registered through this interface can be called from within
    expressions. Functions must return values of supported types (numbers,
    strings, booleans, tuples, or None).
    """

    def __init__(self, context):
        """
        Initialize the functions interface.

        :param context: The underlying evaluation context
        """
        self._context = context

    def __setitem__(self, name: str, func: Callable[..., Any]) -> None:
        """
        Register a function using dictionary syntax.

        :param name: Name to use for the function in expressions
        :param func: Python function to register
        :raises FunctionError: If name is invalid or value isn't callable
        """
        if not callable(func):
            raise FunctionError(f"Value for '{name}' must be callable")
        try:
            self._context.set_function(name, func)
        except ValueError as e:
            raise FunctionError(f"Could not register function '{name}': {e}") from e

    def register(self, name: str, func: Callable[..., Any]) -> None:
        """
        Register a function using explicit method syntax.

        :param name: Name to use for the function in expressions
        :param func: Python function to register
        :raises FunctionError: If name is invalid or value isn't callable
        """
        self[name] = func

    def clear(self) -> None:
        """
        Remove all registered functions.
        """
        self._context.clear()
