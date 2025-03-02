"""
Immutable context implementation for expression evaluation with constant state.

This module provides a context that maintains a set of variables and functions
that can be used in expressions, but cannot be modified by those expressions.
This allows for consistent evaluation of multiple expressions against the same
state while preventing unintended state changes.

The immutable context is ideal for scenarios like:
- Mathematical formulas using predefined constants
- Business rules that reference fixed values
- Template evaluation with predefined variables
"""

from py_evalexpr.natives.context import EvalContext
from py_evalexpr.natives.result import EvalExprResults

from py_evalexpr.base_context import BaseContext, ValidTuple
from py_evalexpr.exceptions import EvaluationError
from py_evalexpr.functions import FunctionsDict
from py_evalexpr.natives import evaluate_with_context as _evaluate_with_context
from py_evalexpr.variables import VariablesDict


class ImmutableContext(BaseContext):
    """
    A context that maintains constant state for expression evaluation.

    This context stores variables and functions that can be used in expressions,
    but prevents those expressions from modifying the stored state. This ensures
    consistent behavior across multiple evaluations.
    """

    def __init__(self):
        """
        Initialize the immutable context with empty state.
        """
        self._context = EvalContext()
        self.variables = VariablesDict(self._context)
        self.functions = FunctionsDict(self._context)

    def evaluate(self, expression: str) -> EvalExprResults:
        """
        Evaluate an expression using the context's current state.

        :param expression: The expression to evaluate, can use stored variables
        :raises EvaluationError: If evaluation fails or tries to modify state
        :return: The typed result of evaluating the expression
        """
        try:
            return _evaluate_with_context.evaluate_with_context(
                expression, self._context
            )
        except ValueError as e:
            raise EvaluationError(f"Evaluation failed: {e}")

    def evaluate_int(self, expression: str) -> int:
        """
        Evaluate an expression that should result in an integer.

        :param expression: The expression to evaluate, can use stored variables
        :raises EvaluationError: If evaluation fails or result isn't an integer
        :return: The integer result of the evaluation
        """
        try:
            return _evaluate_with_context.evaluate_int_with_context(
                expression, self._context
            )
        except ValueError as e:
            raise EvaluationError(f"Integer evaluation failed: {e}")

    def evaluate_float(self, expression: str) -> float:
        """
        Evaluate an expression that should result in a float.

        :param expression: The expression to evaluate, can use stored variables
        :raises EvaluationError: If evaluation fails or result isn't a float
        :return: The float result of the evaluation
        """
        try:
            return _evaluate_with_context.evaluate_float_with_context(
                expression, self._context
            )
        except ValueError as e:
            raise EvaluationError(f"Float evaluation failed: {e}")

    def evaluate_string(self, expression: str) -> str:
        """
        Evaluate an expression that should result in a string.

        :param expression: The expression to evaluate, can use stored variables
        :raises EvaluationError: If evaluation fails or result isn't a string
        :return: The string result of the evaluation
        """
        try:
            return _evaluate_with_context.evaluate_string_with_context(
                expression, self._context
            )
        except ValueError as e:
            raise EvaluationError(f"String evaluation failed: {e}")

    def evaluate_boolean(self, expression: str) -> bool:
        """
        Evaluate an expression that should result in a boolean.

        :param expression: The expression to evaluate, can use stored variables
        :raises EvaluationError: If evaluation fails or result isn't a boolean
        :return: The boolean result of the evaluation
        """
        try:
            return _evaluate_with_context.evaluate_boolean_with_context(
                expression, self._context
            )
        except ValueError as e:
            raise EvaluationError(f"Boolean evaluation failed: {e}")

    def evaluate_tuple(self, expression: str) -> ValidTuple:
        """
        Evaluate an expression that should result in a tuple.

        :param expression: The expression to evaluate, can use stored variables
        :raises EvaluationError: If evaluation fails or result isn't a tuple
        :return: The tuple result of the evaluation
        """
        try:
            return _evaluate_with_context.evaluate_tuple_with_context(
                expression, self._context
            )
        except ValueError as e:
            raise EvaluationError(f"Tuple evaluation failed: {e}")

    def evaluate_empty(self, expression: str) -> None:
        """
        Evaluate an expression that shouldn't return a value.

        Note that in an immutable context, this is rarely useful as expressions
        cannot modify state. It's primarily included for interface compatibility.

        :param expression: The expression to evaluate, can use stored variables
        :raises EvaluationError: If evaluation fails or produces a non-None result
        :return: None
        """
        try:
            return _evaluate_with_context.evaluate_empty_with_context(
                expression, self._context
            )
        except ValueError as e:
            raise EvaluationError(f"Empty evaluation failed: {e}")
