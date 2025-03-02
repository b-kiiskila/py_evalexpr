"""
Mutable context implementation for expression evaluation with modifiable state.

This module provides a context that maintains state (variables and functions)
that can be both read and modified by expressions. This is the most flexible
context type, enabling expressions to create new variables, update existing ones,
and build upon previous results.

The mutable context is ideal for scenarios like:
- Running calculations that need to store intermediate results
- Building up complex data structures through multiple expressions
- Implementing algorithms that require state tracking
- Template processing with variable updates
"""

from py_evalexpr.natives.context import EvalContext
from py_evalexpr.natives.result import EvalExprResults

from py_evalexpr.base_context import BaseContext, ValidTuple
from py_evalexpr.exceptions import EvaluationError
from py_evalexpr.functions import FunctionsDict
from py_evalexpr.natives import evaluate_with_context_mut as _evaluate_with_context_mut
from py_evalexpr.variables import VariablesDict


class MutableContext(BaseContext):
    """
    A context that allows expressions to modify its state during evaluation.

    This context type provides the most flexibility, allowing expressions to
    both read and write variables. This enables complex calculations where
    expressions need to store intermediate results or update running totals.
    """

    def __init__(self):
        """
        Initialize the mutable context with empty state.
        """
        self._context = EvalContext()
        self.variables = VariablesDict(self._context)
        self.functions = FunctionsDict(self._context)

    def evaluate(self, expression: str) -> EvalExprResults:
        """
        Evaluate an expression, allowing it to modify the context's state.

        This method allows expressions to both read and write variables. For example:
        - x = 42  (creates or updates variable 'x')
        - total += value  (modifies existing variable)
        - result = calculate(input)  (stores function result)

        :param expression: The expression to evaluate, can modify state
        :raises EvaluationError: If the evaluation fails
        :return: The typed result of evaluating the expression
        """
        try:
            return _evaluate_with_context_mut.evaluate_with_context_mut(
                expression, self._context
            )
        except ValueError as e:
            raise EvaluationError(f"Evaluation failed: {e}")

    def evaluate_int(self, expression: str) -> int:
        """
        Evaluate an expression that should result in an integer.

        The expression can modify state before producing its final integer result.

        :param expression: The expression to evaluate, can modify state
        :raises EvaluationError: If evaluation fails or result isn't an integer
        :return: The integer result of the evaluation
        """
        try:
            return _evaluate_with_context_mut.evaluate_int_with_context(
                expression, self._context
            )
        except ValueError as e:
            raise EvaluationError(f"Integer evaluation failed: {e}")

    def evaluate_float(self, expression: str) -> float:
        """
        Evaluate an expression that should result in a float.

        The expression can modify state before producing its final float result.

        :param expression: The expression to evaluate, can modify state
        :raises EvaluationError: If evaluation fails or result isn't a float
        :return: The float result of the evaluation
        """
        try:
            return _evaluate_with_context_mut.evaluate_float_with_context(
                expression, self._context
            )
        except ValueError as e:
            raise EvaluationError(f"Float evaluation failed: {e}")

    def evaluate_string(self, expression: str) -> str:
        """
        Evaluate an expression that should result in a string.

        The expression can modify state before producing its final string result.

        :param expression: The expression to evaluate, can modify state
        :raises EvaluationError: If evaluation fails or result isn't a string
        :return: The string result of the evaluation
        """
        try:
            return _evaluate_with_context_mut.evaluate_string_with_context(
                expression, self._context
            )
        except ValueError as e:
            raise EvaluationError(f"String evaluation failed: {e}")

    def evaluate_boolean(self, expression: str) -> bool:
        """
        Evaluate an expression that should result in a boolean.

        The expression can modify state before producing its final boolean result.

        :param expression: The expression to evaluate, can modify state
        :raises EvaluationError: If evaluation fails or result isn't a boolean
        :return: The boolean result of the evaluation
        """
        try:
            return _evaluate_with_context_mut.evaluate_boolean_with_context(
                expression, self._context
            )
        except ValueError as e:
            raise EvaluationError(f"Boolean evaluation failed: {e}")

    def evaluate_tuple(self, expression: str) -> ValidTuple:
        """
        Evaluate an expression that should result in a tuple.

        The expression can modify state before producing its final tuple result.

        :param expression: The expression to evaluate, can modify state
        :raises EvaluationError: If evaluation fails or result isn't a tuple
        :return: The tuple result of the evaluation
        """
        try:
            return _evaluate_with_context_mut.evaluate_tuple_with_context(
                expression, self._context
            )
        except ValueError as e:
            raise EvaluationError(f"Tuple evaluation failed: {e}")

    def evaluate_empty(self, expression: str) -> None:
        """
        Evaluate an expression that shouldn't return a value.

        This is particularly useful in a mutable context for expressions that only
        modify state, such as variable assignments or updates. For example:
        - counter = 0  (initialize a variable)
        - total += item  (update a running total)
        - cache.clear()  (perform state management)

        :param expression: The expression to evaluate, can modify state
        :raises EvaluationError: If evaluation fails or produces a non-None result
        :return: None
        """
        try:
            return _evaluate_with_context_mut.evaluate_empty_with_context_mut(
                expression, self._context
            )
        except ValueError as e:
            raise EvaluationError(f"Empty evaluation failed: {e}")
