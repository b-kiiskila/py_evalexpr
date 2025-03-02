from typing import Union, Tuple, List, Callable
from typing_extensions import TypeAlias

# Define the recursive type for values that can be stored in the context
Value: TypeAlias = Union[
    str, float, int, bool, None, Tuple["Value", ...]  # Recursive type for nested tuples
]

class EvalContext:
    """A context for expression evaluation that stores variables and functions.

    The EvalContext class provides a way to manage variables and functions that can be used
    in expression evaluation. It supports setting and retrieving variables, registering custom
    functions, and controlling built-in function availability.

    Variables can be of the following types:
    - str (strings)
    - float (floating point numbers)
    - int (integers)
    - bool (boolean values)
    - tuple (tuples containing any of the above types)
    - None (empty/null values)
    """

    def __init__(self) -> None:
        """Initialize a new empty evaluation context."""
        ...

    def set_variable(self, identifier: str, value: Value) -> None:
        """Set a variable in the context.

        Args:
            identifier: The name of the variable to set
            value: The value to associate with the variable. Must be one of:
                  str, float, int, bool, tuple, or None

        Raises:
            ValueError: If the identifier is invalid or if the value cannot be converted
                      to a supported type
        """
        ...

    def set_function(self, identifier: str, value: Callable[..., Value]) -> None:
        """Register a custom function in the context.

        Args:
            identifier: The name of the function to register
            value: A callable that will be invoked when the function is used in expressions

        Raises:
            ValueError: If the identifier is invalid or if the value is not callable
        """
        ...

    def iter_variables(self) -> List[Tuple[str, Value]]:
        """Get all variables currently stored in the context.

        Returns:
            A list of tuples, where each tuple contains:
            - The variable name (str)
            - The variable value (Any)
        """
        ...

    def iter_variable_names(self) -> List[str]:
        """Get the names of all variables currently stored in the context.

        Returns:
            A list of variable names as strings
        """
        ...

    def set_builtin_functions_disabled(self, disabled: bool) -> None:
        """Enable or disable built-in functions in the context.

        Args:
            disabled: If True, built-in functions will be disabled.
                     If False, built-in functions will be enabled.

        Raises:
            ValueError: If the operation fails
        """
        ...

    def clear(self) -> None:
        """Remove all variables and custom functions from the context."""
        ...

    def __str__(self) -> str:
        """Get a string representation of the context.

        Returns:
            A human-readable string showing the context's current state
        """
        ...

    def __repr__(self) -> str:
        """Get a detailed string representation of the context.

        Returns:
            A detailed string representation showing the context's internal state
        """
        ...
