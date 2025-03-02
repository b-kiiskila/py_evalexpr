import pytest
from py_evalexpr.functions import FunctionsDict
from py_evalexpr.natives.context import EvalContext
from py_evalexpr.exceptions import FunctionError


class TestFunctionsDict:
    """Test the FunctionsDict implementation."""

    def setup_method(self):
        """Set up a test context and functions dictionary."""
        self.context = EvalContext()
        self.functions = FunctionsDict(self.context)

    def test_function_registration(self):
        """Test basic function registration and error handling."""

        # A simple test function that's guaranteed to work
        def add_func(x, y):
            return x + y

        # Register the function
        self.functions["add"] = add_func

        # Test error handling for non-callables
        with pytest.raises(FunctionError):
            self.functions["not_callable"] = 42

        with pytest.raises(FunctionError):
            self.functions["also_not_callable"] = "string"

        with pytest.raises(FunctionError):
            self.functions["still_not_callable"] = {"key": "value"}

    def test_register_method(self):
        """Test registering functions with the register() method."""

        # A simple test function that's guaranteed to work
        def multiply_func(x, y):
            return x * y

        # Register using alternate syntax
        self.functions.register("multiply", multiply_func)
