import pytest
from py_evalexpr.natives.context import EvalContext
from py_evalexpr.natives import evaluate_with_context


class TestContext:
    """Test cases for the EvalContext implementation"""

    def setup_method(self):
        """Create a fresh context for each test"""
        self.context = EvalContext()

    # Variable management
    def test_variable_management(self):
        # Set variables of different types
        self.context.set_variable("int_var", 42)
        self.context.set_variable("float_var", 3.14)
        self.context.set_variable("str_var", "hello")
        self.context.set_variable("bool_var", True)
        self.context.set_variable("tuple_var", (1, 2, 3))

        # Get all variables
        variables = self.context.iter_variables()
        var_dict = {name: value for name, value in variables}

        # Verify content
        assert var_dict["int_var"] == 42
        assert var_dict["float_var"] == 3.14
        assert var_dict["str_var"] == "hello"
        assert var_dict["bool_var"] is True
        assert var_dict["tuple_var"] == (1, 2, 3)

        # Get variable names
        var_names = self.context.iter_variable_names()
        assert set(var_names) == {
            "int_var",
            "float_var",
            "str_var",
            "bool_var",
            "tuple_var",
        }

    # Function management
    def test_function_management(self):
        # Define simple functions
        # For single arguments, the function is called with just that argument
        def add_one(x):
            return x + 1

        # For multiple arguments, each argument is passed individually
        def concatenate(x, y):
            return x + y

        # Register functions
        self.context.set_function("add_one", add_one)
        self.context.set_function("concatenate", concatenate)

        # Test using evaluate_with_context
        result = evaluate_with_context.evaluate_int_with_context(
            "add_one(41)", self.context
        )
        assert result == 42

        # For multiple arguments, they're passed as separate arguments
        result = evaluate_with_context.evaluate_int_with_context(
            "concatenate(40, 2)", self.context
        )
        assert result == 42

        result = evaluate_with_context.evaluate_string_with_context(
            'concatenate("hello ", "world")', self.context
        )
        assert result == "hello world"

    # Clear context
    def test_clear(self):
        # Set up variables and functions
        self.context.set_variable("x", 42)
        self.context.set_function("double", lambda x: x * 2)

        # Verify they're set
        assert len(self.context.iter_variable_names()) == 1
        assert (
            evaluate_with_context.evaluate_int_with_context("double(21)", self.context)
            == 42
        )

        # Clear the context
        self.context.clear()

        # Verify everything is cleared
        assert len(self.context.iter_variable_names()) == 0

        # Function should be gone too
        with pytest.raises(NameError):
            evaluate_with_context.evaluate_with_context("double(21)", self.context)

    # Builtin functions management
    def test_builtin_functions(self):
        # Builtins should be enabled by default
        assert (
            evaluate_with_context.evaluate_int_with_context("max(10, 20)", self.context)
            == 20
        )

        # Disable builtin functions
        self.context.set_builtin_functions_disabled(True)

        # Now builtin functions should fail
        with pytest.raises(NameError):
            evaluate_with_context.evaluate_with_context("max(10, 20)", self.context)

        # Re-enable builtin functions
        self.context.set_builtin_functions_disabled(False)

        # Builtins should work again
        assert (
            evaluate_with_context.evaluate_int_with_context("max(10, 20)", self.context)
            == 20
        )

    # String representation
    def test_string_representation(self):
        # Add some data to make the string representation non-empty
        self.context.set_variable("x", 42)

        # Check string and repr methods
        assert str(self.context) is not None
        assert repr(self.context) is not None

        # They should contain some indication of the context contents
        assert "EvalContext" in str(self.context)

    # Error handling
    def test_error_handling(self):
        # From the error_mapping.rs file, we can see non-callable functions raise TypeError
        with pytest.raises(TypeError):
            self.context.set_function("not_callable", "this is not a function")

        # Test variable operations
        self.context.set_variable("test_var", 42)
        assert dict(self.context.iter_variables())["test_var"] == 42
