"""
Stateless context implementation for pure expression evaluation.

This module provides a context that evaluates expressions using only built-in
capabilities, without any concept of state. It cannot store variables or
functions and is ideal for simple mathematical or logical expressions that
don't require external values.

Examples of valid expressions in a stateless context:
- Mathematical: "2 + 2", "sin(pi/2)", "sqrt(16)"
- Logical: "true && false", "1 < 2", "!false"
- String: '"Hello" + " World"'
- Tuple: "(1, 2, 3)", "(true, 42, "test")"
"""

from py_evalexpr.natives.result import EvalExprResults

from py_evalexpr.base_context import BaseContext, ValidTuple
from py_evalexpr.exceptions import EvaluationError
from py_evalexpr.natives import evaluate as _evaluate


class StatelessContext(BaseContext):
    """
    A context that provides pure expression evaluation without any state.

    This context type is the simplest form of evaluation context, supporting only
    expressions that use built-in operators and functions. It cannot store
    variables or custom functions, making it ideal for pure calculations.
    """

    def evaluate(self, expression: str) -> EvalExprResults:
        """
        Evaluate an expression without any context state.

        :param expression: The expression to evaluate, must be self-contained
        :raises EvaluationError: If the evaluation fails or tries to use variables
        :return: The typed result of evaluating the expression
        """
        try:
            return _evaluate.evaluate(expression)
        except ValueError as e:
            raise EvaluationError(f"Evaluation failed: {e}")

    def evaluate_int(self, expression: str) -> int:
        """
        Evaluate an expression that should result in an integer.

        :param expression: The expression to evaluate, must be self-contained
        :raises EvaluationError: If the evaluation fails or result isn't an integer
        :return: The integer result of the evaluation
        """
        try:
            return _evaluate.evaluate_int(expression)
        except ValueError as e:
            raise EvaluationError(f"Integer evaluation failed: {e}")

    def evaluate_float(self, expression: str) -> float:
        """
        Evaluate an expression that should result in a float.

        :param expression: The expression to evaluate, must be self-contained
        :raises EvaluationError: If the evaluation fails or result isn't a float
        :return: The float result of the evaluation
        """
        try:
            return _evaluate.evaluate_float(expression)
        except ValueError as e:
            raise EvaluationError(f"Float evaluation failed: {e}")

    def evaluate_string(self, expression: str) -> str:
        """
        Evaluate an expression that should result in a string.

        :param expression: The expression to evaluate, must be self-contained
        :raises EvaluationError: If the evaluation fails or result isn't a string
        :return: The string result of the evaluation
        """
        try:
            return _evaluate.evaluate_string(expression)
        except ValueError as e:
            raise EvaluationError(f"String evaluation failed: {e}")

    def evaluate_boolean(self, expression: str) -> bool:
        """
        Evaluate an expression that should result in a boolean.

        :param expression: The expression to evaluate, must be self-contained
        :raises EvaluationError: If the evaluation fails or result isn't a boolean
        :return: The boolean result of the evaluation
        """
        try:
            return _evaluate.evaluate_boolean(expression)
        except ValueError as e:
            raise EvaluationError(f"Boolean evaluation failed: {e}")

    def evaluate_tuple(self, expression: str) -> ValidTuple:
        """
        Evaluate an expression that should result in a tuple.

        :param expression: The expression to evaluate, must be self-contained
        :raises EvaluationError: If the evaluation fails or result isn't a tuple
        :return: The tuple result of the evaluation
        """
        try:
            return _evaluate.evaluate_tuple(expression)
        except ValueError as e:
            raise EvaluationError(f"Tuple evaluation failed: {e}")

    def evaluate_empty(self, expression: str) -> None:
        """
        Evaluate an expression that shouldn't return a value.

        Note that in a stateless context, this is rarely useful as there is no
        state to modify. It's primarily included for interface compatibility.

        :param expression: The expression to evaluate, must be self-contained
        :raises EvaluationError: If the evaluation fails or produces a non-None result
        :return: None
        """
        try:
            return _evaluate.evaluate_empty(expression)
        except ValueError as e:
            raise EvaluationError(f"Empty evaluation failed: {e}")
