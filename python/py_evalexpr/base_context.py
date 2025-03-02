"""
Abstract base class defining the interface for expression evaluation contexts.

This module defines the interface that all context implementations must follow.
It specifies the methods that contexts must implement but provides no
implementation details, serving as a pure contract for context behavior.

The module also defines ValidTypes and ValidTuple types which specify what
types of values can be stored in and returned from the evaluation engine.
"""

from abc import ABC, abstractmethod
from typing import Tuple

from py_evalexpr.natives.result import EvalExprResults

# Recursive type definition for valid values in expressions
ValidTypes = int | float | str | bool | tuple | Tuple["ValidTypes", ...] | None

# Type alias for tuples containing valid types
ValidTuple = Tuple["ValidTypes", ...]


class BaseContext(ABC):
    """
    Abstract base class defining the context interface.

    This class defines the methods that every evaluation context must implement.
    It provides no implementation, serving only to establish the contract that
    context implementations must fulfill.
    """

    @abstractmethod
    def evaluate(self, expression: str) -> EvalExprResults:
        """
        Evaluate an expression, returning a typed result object.

        :param expression: The expression to evaluate
        :raises EvaluationError: If the evaluation fails
        :return: A typed result object containing the evaluation result
        """
        pass

    @abstractmethod
    def evaluate_int(self, expression: str) -> int:
        """E
        Evaluate an expression, ensuring an integer result.

        :param expression: The expression to evaluate
        :raises EvaluationError: If the evaluation fails or result isn't an integer
        :return: The integer result of the evaluation
        """
        pass

    @abstractmethod
    def evaluate_float(self, expression: str) -> float:
        """E
        Evaluate an expression, ensuring a float result.

        :param expression: The expression to evaluate
        :raises EvaluationError: If the evaluation fails or result isn't a float
        :return: The float result of the evaluation
        """
        pass

    @abstractmethod
    def evaluate_string(self, expression: str) -> str:
        """
        Evaluate an expression, ensuring a string result.

        :param expression: The expression to evaluate
        :raises EvaluationError: If the evaluation fails or result isn't a string
        :return: The string result of the evaluation
        """
        pass

    @abstractmethod
    def evaluate_boolean(self, expression: str) -> bool:
        """
        Evaluate an expression, ensuring a boolean result.

        :param expression: The expression to evaluate
        :raises EvaluationError: If the evaluation fails or result isn't a boolean
        :return: The boolean result of the evaluation
        """
        pass

    @abstractmethod
    def evaluate_tuple(self, expression: str) -> ValidTuple:
        """
        Evaluate an expression, ensuring a tuple result.

        :param expression: The expression to evaluate
        :raises EvaluationError: If the evaluation fails or result isn't a tuple
        :return: The tuple result of the evaluation, containing only valid types
        """
        pass

    @abstractmethod
    def evaluate_empty(self, expression: str) -> None:
        """
        Evaluate an expression that shouldn't return a value, you likely only want to use this on context
        with a mutable state.

        :param expression: The expression to evaluate
        :raises EvaluationError: If the evaluation fails or produces a non-None result
        :return: None
        """
        pass
