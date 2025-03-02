from .context import EvalContext
from .result import EvalExprResults

def evaluate_with_context_mut(expr: str, context: EvalContext) -> EvalExprResults:
    """
    Evaluates an expression with a mutable context and returns the result.
    The context can be modified during evaluation.

    :param expr: The expression to evaluate.
    :param context: The mutable context containing variables and functions for evaluation.
    :raises ValueError: If the expression could not be evaluated.
    :returns: The result of the evaluation.
    """
    ...

def evaluate_string_with_context(expr: str, context: EvalContext) -> str:
    """
    Evaluates an expression with a mutable context and returns the result as a string.
    The context can be modified during evaluation.

    :param expr: The expression to evaluate.
    :param context: The mutable context containing variables and functions for evaluation.
    :raises ValueError: If the expression could not be evaluated.
    :returns: The result of the evaluation as a string.
    """
    ...

def evaluate_int_with_context(expr: str, context: EvalContext) -> int:
    """
    Evaluates an expression with a mutable context and returns the result as an integer.
    The context can be modified during evaluation.

    :param expr: The expression to evaluate.
    :param context: The mutable context containing variables and functions for evaluation.
    :raises ValueError: If the expression could not be evaluated.
    :returns: The result of the evaluation as an integer.
    """
    ...

def evaluate_float_with_context(expr: str, context: EvalContext) -> float:
    """
    Evaluates an expression with a mutable context and returns the result as a float.
    The context can be modified during evaluation.

    :param expr: The expression to evaluate.
    :param context: The mutable context containing variables and functions for evaluation.
    :raises ValueError: If the expression could not be evaluated.
    :returns: The result of the evaluation as a float.
    """
    ...

def evaluate_number_with_context(expr: str, context: EvalContext) -> float | int:
    """
    Evaluates an expression with a mutable context and returns the result as a number.
    The context can be modified during evaluation.

    :param expr: The expression to evaluate.
    :param context: The mutable context containing variables and functions for evaluation.
    :raises ValueError: If the expression could not be evaluated.
    :returns: The result of the evaluation as a number.
    """
    ...

def evaluate_boolean_with_context(expr: str, context: EvalContext) -> bool:
    """
    Evaluates an expression with a mutable context and returns the result as a boolean.
    The context can be modified during evaluation.

    :param expr: The expression to evaluate.
    :param context: The mutable context containing variables and functions for evaluation.
    :raises ValueError: If the expression could not be evaluated.
    :returns: The result of the evaluation as a boolean.
    """
    ...

def evaluate_tuple_with_context(expr: str, context: EvalContext) -> tuple:
    """
    Evaluates an expression with a mutable context and returns the result as a tuple.
    The context can be modified during evaluation.

    :param expr: The expression to evaluate.
    :param context: The mutable context containing variables and functions for evaluation.
    :raises ValueError: If the expression could not be evaluated.
    :returns: The result of the evaluation as a tuple.
    """
    ...

def evaluate_empty_with_context_mut(expr: str, context: EvalContext) -> None:
    """
    Evaluates an expression with a mutable context and returns None if the result is empty.
    The context can be modified during evaluation.

    :param expr: The expression to evaluate.
    :param context: The mutable context containing variables and functions for evaluation.
    :raises ValueError: If the expression could not be evaluated.
    :returns: None if the result is empty.
    """
    ...
