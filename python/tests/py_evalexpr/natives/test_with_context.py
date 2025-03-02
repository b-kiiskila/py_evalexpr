import pytest
from py_evalexpr.natives import evaluate_with_context
from py_evalexpr.natives.context import EvalContext


class TestEvaluateWithContext:
    """Test cases for evaluation with a read-only context"""

    def setup_method(self):
        """Set up a context with variables and functions for testing"""
        self.context = EvalContext()

        # Set up variables of different types
        self.context.set_variable("int_var", 42)
        self.context.set_variable("float_var", 3.14)
        self.context.set_variable("str_var", "hello")
        # In the py_evalexpr implementation, booleans are handled as their actual boolean type
        self.context.set_variable("bool_var", True)
        self.context.set_variable("tuple_var", (1, 2, 3))

        # Set up functions
        # For multiple argument functions, each argument is passed individually
        def add_function(x, y):
            return x + y

        self.context.set_function("add", add_function)
        self.context.set_function("double", lambda x: x * 2)

    # Variable access
    def test_variable_access(self):
        # Get variables of different types
        result = evaluate_with_context.evaluate_with_context("int_var", self.context)
        assert result.as_int() == 42

        result = evaluate_with_context.evaluate_with_context("float_var", self.context)
        assert result.as_float() == 3.14

        result = evaluate_with_context.evaluate_with_context("str_var", self.context)
        assert result.as_string() == "hello"

        # In evalexpr, booleans are properly handled as boolean values
        result = evaluate_with_context.evaluate_with_context("bool_var", self.context)
        assert result.as_bool() is True

        result = evaluate_with_context.evaluate_with_context("tuple_var", self.context)
        assert result.as_tuple() == (1, 2, 3)

    # Type-specific evaluation functions
    def test_type_specific_functions(self):
        assert (
            evaluate_with_context.evaluate_int_with_context("int_var", self.context)
            == 42
        )
        assert (
            evaluate_with_context.evaluate_float_with_context("float_var", self.context)
            == 3.14
        )
        assert (
            evaluate_with_context.evaluate_string_with_context("str_var", self.context)
            == "hello"
        )
        # Boolean handling
        assert (
            evaluate_with_context.evaluate_boolean_with_context(
                "bool_var", self.context
            )
            is True
        )
        assert evaluate_with_context.evaluate_tuple_with_context(
            "tuple_var", self.context
        ) == (1, 2, 3)

        # Empty evaluation (should work with an expression that evaluates to empty)
        assert (
            evaluate_with_context.evaluate_empty_with_context("()", self.context)
            is None
        )

    # Function calls
    def test_function_calls(self):
        # Call function with single argument
        assert (
            evaluate_with_context.evaluate_int_with_context("double(21)", self.context)
            == 42
        )

        # Call function with multiple arguments - pass them directly
        assert (
            evaluate_with_context.evaluate_int_with_context("add(20, 22)", self.context)
            == 42
        )

        # Call function with variable arguments
        assert (
            evaluate_with_context.evaluate_int_with_context(
                "add(int_var, 0)", self.context
            )
            == 42
        )

    # Expressions with variables
    def test_expressions_with_variables(self):
        # Arithmetic with variables
        assert (
            evaluate_with_context.evaluate_int_with_context("int_var + 8", self.context)
            == 50
        )
        assert (
            evaluate_with_context.evaluate_float_with_context(
                "float_var * 2", self.context
            )
            == 6.28
        )

        # String operations with variables
        assert (
            evaluate_with_context.evaluate_string_with_context(
                'str_var + " world"', self.context
            )
            == "hello world"
        )

        # Logical operations with variables
        assert (
            evaluate_with_context.evaluate_boolean_with_context(
                "bool_var && true", self.context
            )
            is True
        )
        assert (
            evaluate_with_context.evaluate_boolean_with_context(
                "bool_var && false", self.context
            )
            is False
        )
        assert (
            evaluate_with_context.evaluate_boolean_with_context(
                "bool_var && false", self.context
            )
            is False
        )

        # Complex expressions
        assert (
            evaluate_with_context.evaluate_boolean_with_context(
                "int_var > 40 && float_var < 4", self.context
            )
            is True
        )

    # Built-in functions
    def test_builtin_functions(self):
        # Math functions
        assert (
            evaluate_with_context.evaluate_int_with_context("max(10, 20)", self.context)
            == 20
        )
        assert (
            evaluate_with_context.evaluate_int_with_context(
                "min(int_var, 50)", self.context
            )
            == 42
        )

        # String functions
        assert (
            evaluate_with_context.evaluate_int_with_context(
                "len(str_var)", self.context
            )
            == 5
        )

        # Conditional functions with boolean
        assert (
            evaluate_with_context.evaluate_int_with_context(
                "if(bool_var, 42, 0)", self.context
            )
            == 42
        )

    # Disabling built-in functions
    def test_disable_builtin_functions(self):
        # Built-in functions should work by default
        assert (
            evaluate_with_context.evaluate_int_with_context("max(10, 20)", self.context)
            == 20
        )

        # Disable built-in functions
        self.context.set_builtin_functions_disabled(True)

        # Now the built-in function should not be found - expect NameError based on error_mapping.rs
        with pytest.raises(NameError):
            evaluate_with_context.evaluate_int_with_context("max(10, 20)", self.context)

        # Re-enable for other tests
        self.context.set_builtin_functions_disabled(False)

    # Error handling
    def test_error_handling(self):
        # Variable not found - raises KeyError
        with pytest.raises(KeyError):
            evaluate_with_context.evaluate_with_context("unknown_var", self.context)

        # Function not found - raises NameError according to error_mapping.rs
        with pytest.raises(NameError):
            evaluate_with_context.evaluate_with_context(
                "unknown_func(42)", self.context
            )

        # Type error (requesting wrong type)
        with pytest.raises(TypeError):
            evaluate_with_context.evaluate_int_with_context("str_var", self.context)

        # Assignment not allowed in read-only context
        with pytest.raises(RuntimeError):
            evaluate_with_context.evaluate_with_context("new_var = 42", self.context)
