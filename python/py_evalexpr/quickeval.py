from .stateless_context import StatelessContext
from .base_context import ValidTypes, ValidTuple


def evaluate(expression: str) -> ValidTypes:
    """
    Evaluate an expression without any context.

    This is a convenience function for simple expressions that don't need
    variables or functions. For more complex evaluations, use one of the
    context types.

    :param expression: Expression to evaluate
    :raises EvaluationError: If evaluation fails
    :return: Result of the evaluation
    """
    return StatelessContext().evaluate(expression).value


def evaluate_int(expression: str) -> int:
    """
    Evaluate an expression that should result in an integer.

    :param expression: Expression to evaluate
    :raises EvaluationError: If evaluation fails or result isn't an integer
    :return: Integer result of the evaluation
    """
    return StatelessContext().evaluate_int(expression)


def evaluate_float(expression: str) -> float:
    """
    Evaluate an expression that should result in a float.

    :param expression: Expression to evaluate
    :raises EvaluationError: If evaluation fails or result isn't a float
    :return: Float result of the evaluation
    """
    return StatelessContext().evaluate_float(expression)


def evaluate_string(expression: str) -> str:
    """
    Evaluate an expression that should result in a string.

    :param expression: Expression to evaluate
    :raises EvaluationError: If evaluation fails or result isn't a string
    :return: String result of the evaluation
    """
    return StatelessContext().evaluate_string(expression)


def evaluate_boolean(expression: str) -> bool:
    """
    Evaluate an expression that should result in a boolean.

    :param expression: Expression to evaluate
    :raises EvaluationError: If evaluation fails or result isn't a boolean
    :return: Boolean result of the evaluation
    """
    return StatelessContext().evaluate_boolean(expression)


def evaluate_tuple(expression: str) -> ValidTuple:
    """
    Evaluate an expression that should result in a tuple.

    :param expression: Expression to evaluate
    :raises EvaluationError: If evaluation fails or result isn't a tuple
    :return: Tuple result of the evaluation
    """
    return StatelessContext().evaluate_tuple(expression)
