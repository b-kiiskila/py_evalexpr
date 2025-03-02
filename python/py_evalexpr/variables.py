"""
Variable management support for evaluation contexts.

This module provides the VariablesDict class which implements storage and access
of variables for evaluation contexts. It provides a dictionary-like interface
for working with variables that can be used in expressions.
"""

from typing import Any, Iterator, Tuple

from py_evalexpr.exceptions import VariableError
from py_evalexpr.natives import evaluate_with_context


class VariablesDict:
    """
    Dictionary-like interface for managing variables in evaluation contexts.

    Variables stored through this interface can be accessed from within
    expressions. Variables must be of supported types (numbers, strings,
    booleans, tuples, or None).
    """

    def __init__(self, context):
        """
        Initialize the variables interface.

        :param context: The underlying evaluation context
        """
        self._context = context

    def __getitem__(self, key: str) -> Any:
        """
        Get a variable's value using dictionary syntax.

        :param key: Name of the variable to retrieve
        :raises KeyError: If the variable doesn't exist
        :return: The variable's current value
        """
        try:
            return evaluate_with_context.evaluate_with_context(key, self._context).value
        except ValueError as e:
            raise KeyError(key) from e

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set a variable's value using dictionary syntax.

        :param key: Name of the variable to set
        :param value: Value to assign to the variable
        :raises VariableError: If name is invalid or value has unsupported type
        """
        try:
            self._context.set_variable(key, value)
        except ValueError as e:
            raise VariableError(f"Could not set variable '{key}': {e}") from e

    def __delitem__(self, key: str) -> None:
        """
        Delete a variable using dictionary syntax.

        :param key: Name of the variable to delete
        :raises KeyError: If the variable doesn't exist
        """
        if key not in self:
            raise KeyError(key)
        try:
            self._context.set_variable(key, None)
        except ValueError as e:
            raise VariableError(f"Could not delete variable '{key}': {e}") from e

    def __contains__(self, key: str) -> bool:
        """
        Check if a variable exists using 'in' operator.

        :param key: Name of the variable to check
        :return: True if the variable exists, False otherwise
        """
        return key in self._context.iter_variable_names()

    def __iter__(self) -> Iterator[str]:
        """
        Iterate over variable names.

        :return: Iterator yielding variable names
        """
        return iter(self._context.iter_variable_names())

    def __len__(self) -> int:
        """
        Get number of variables using len().

        :return: Number of variables in the context
        """
        return len(list(self._context.iter_variable_names()))

    def clear(self) -> None:
        """
        Remove all variables from the context.
        """
        self._context.clear()

    def items(self) -> Iterator[Tuple[str, Any]]:
        """
        Iterate over variable name-value pairs.

        :return: Iterator yielding (name, value) tuples
        """
        return iter(self._context.iter_variables())

    def keys(self) -> Iterator[str]:
        """
        Iterate over variable names.

        :return: Iterator yielding variable names
        """
        return iter(self)

    def values(self) -> Iterator[Any]:
        """
        Iterate over variable values.

        :return: Iterator yielding variable values
        """
        for _, value in self.items():
            yield value
