# result.pyi
from typing import TypeAlias, Generic, Union, Tuple

Value: TypeAlias = Union[
    str, float, int, bool, None, Tuple["Value", ...]  # Recursive type for nested tuples
]

class EvalExprResult(Generic[Value]):
    """
    Represents the result of evaluating an expression.
    """

    type: type[Value]
    value: Value

    def as_int(self) -> int:
        """
        Gets the underlying value as an integer.

        :raises ValueError: If the value is not an integer.
        :returns: The integer value.
        """
        ...

    def as_float(self) -> float:
        """
        Gets the underlying value as a float.

        :raises ValueError: If the value is not a float.
        :returns: The float value.
        """
        ...

    def as_string(self) -> str:
        """
        Gets the underlying value as a string.

        :raises ValueError: If the value is not a string.
        :returns: The string value.
        """
        ...

    def as_bool(self) -> bool:
        """
        Gets the underlying value as a boolean.

        :raises ValueError: If the value is not a boolean.
        :returns: The boolean value.
        """
        ...

    def as_tuple(self) -> tuple:
        """
        Gets the underlying value as a tuple.

        :raises ValueError: If the value is not a tuple.
        :returns: The tuple value.
        """
        ...

    def as_none(self) -> None:
        """
        Gets the underlying value as None.

        :raises ValueError: If the value is not None.
        :returns: None.
        """
        ...

EvalExprIntResult: TypeAlias = EvalExprResult[int]
EvalExprFloatResult: TypeAlias = EvalExprResult[float]
EvalExprStrResult: TypeAlias = EvalExprResult[str]
EvalExprBoolResult: TypeAlias = EvalExprResult[bool]
EvalExprTupleResult: TypeAlias = EvalExprResult[tuple]
EvalExprNoneResult: TypeAlias = EvalExprResult[None]

EvalExprResults = (
    EvalExprIntResult
    | EvalExprFloatResult
    | EvalExprStrResult
    | EvalExprBoolResult
    | EvalExprTupleResult
    | EvalExprNoneResult
)
