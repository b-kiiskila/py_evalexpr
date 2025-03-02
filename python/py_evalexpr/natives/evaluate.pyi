from .result import EvalExprResults

def evaluate(expr: str) -> EvalExprResults:
    """
    Evaluates an expression and returns the result.

    :param expr: The expression to evaluate.
    :raises ValueError: If the expression could not be evaluated.
    :returns: The result of the evaluation.
    """
    ...

def evaluate_string(expr: str) -> str:
    """
    Evaluates an expression and returns the result as a string.

    :param expr: The expression to evaluate.
    :raises ValueError: If the expression could not be evaluated.
    :returns: The result of the evaluation as a string.
    """
    ...

def evaluate_int(expr: str) -> int:
    """
    Evaluates an expression and returns the result as an integer.

    :param expr: The expression to evaluate.
    :raises ValueError: If the expression could not be evaluated.
    :returns: The result of the evaluation as an integer.
    """
    ...

def evaluate_float(expr: str) -> float:
    """
    Evaluates an expression and returns the result as a float.

    :param expr: The expression to evaluate.
    :raises ValueError: If the expression could not be evaluated.
    :returns: The result of the evaluation as a float.
    """
    ...

def evaluate_number(expr: str) -> float | int:
    """
    Evaluates an expression and returns the result as a number.

    :param expr: The expression to evaluate.
    :raises ValueError: If the expression could not be evaluated.
    :returns: The result of the evaluation as a number.
    """
    ...

def evaluate_boolean(expr: str) -> bool:
    """
    Evaluates an expression and returns the result as a boolean.

    :param expr: The expression to evaluate.
    :raises ValueError: If the expression could not be evaluated.
    :returns: The result of the evaluation as a boolean.
    """
    ...

def evaluate_tuple(expr: str) -> tuple:
    """
    Evaluates an expression and returns the result as a tuple.

    :param expr: The expression to evaluate.
    :raises ValueError: If the expression could not be evaluated.
    :returns: The result of the evaluation as a tuple.
    """
    ...

def evaluate_empty(expr: str) -> None:
    """
    Evaluates an expression and returns None if the result is empty.

    :param expr: The expression to evaluate.
    :raises ValueError: If the expression could not be evaluated.
    :returns: None if the result is empty.
    """
    ...
