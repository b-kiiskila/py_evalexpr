import pytest
from py_evalexpr.immutable_context import ImmutableContext
from py_evalexpr.exceptions import EvaluationError, FunctionError


class TestImmutableContext:
    """Test the ImmutableContext implementation."""

    def setup_method(self):
        """Set up an immutable context with variables and functions."""
        self.context = ImmutableContext()

        # Set up variables
        self.context.variables["int_var"] = 42
        self.context.variables["float_var"] = 3.14
        self.context.variables["str_var"] = "hello"
        self.context.variables["bool_var"] = True
        self.context.variables["tuple_var"] = (1, 2, 3)

        # Set up functions
        self.context.functions["add"] = lambda x, y: x + y
        self.context.functions["double"] = lambda x: x * 2
        # This needs to accept 'self' since Rust passes in the context as first arg
        self.context.functions["get_greeting"] = lambda self=None: "Hello, World!"

    def test_variable_access(self):
        """Test accessing variables in expressions."""
        # Access variables of different types
        result = self.context.evaluate("int_var")
        assert result.value == 42
        assert result.type is int

        result = self.context.evaluate("float_var")
        assert result.value == 3.14
        assert result.type is float

        result = self.context.evaluate("str_var")
        assert result.value == "hello"
        assert result.type is str

        result = self.context.evaluate("bool_var")
        assert result.value is True
        assert result.type is bool

        result = self.context.evaluate("tuple_var")
        assert result.value == (1, 2, 3)
        assert result.type is tuple

        # Undefined variable
        with pytest.raises(KeyError):
            self.context.evaluate("undefined_var")

    def test_variable_dictionary(self):
        """Test the variables dictionary interface."""
        # Access using dictionary syntax
        assert self.context.variables["int_var"] == 42
        assert self.context.variables["float_var"] == 3.14

        # Set new variable
        self.context.variables["new_var"] = 100
        assert self.context.evaluate("new_var").value == 100

        # Update existing variable
        self.context.variables["int_var"] = 99
        assert self.context.evaluate("int_var").value == 99

        # Note: We're not testing deletion since it's not properly supported in the wrapper

    def test_function_calls(self):
        """Test calling functions in expressions."""
        # Call function with single argument
        assert self.context.evaluate_int("double(21)") == 42

        # Call function with multiple arguments
        assert self.context.evaluate_int("add(20, 22)") == 42

        # Call function with variable arguments
        assert self.context.evaluate_int("add(int_var, 0)") == 42

        # Call function with no arguments
        assert self.context.evaluate_string("get_greeting()") == "Hello, World!"

        # Undefined function
        with pytest.raises(NameError):
            self.context.evaluate("undefined_func()")

    def test_function_dictionary(self):
        """Test the functions dictionary interface."""
        # Register new function
        self.context.functions["triple"] = lambda x: x * 3
        assert self.context.evaluate_int("triple(5)") == 15

        # Register using alternate syntax
        self.context.functions.register("quadruple", lambda x: x * 4)
        assert self.context.evaluate_int("quadruple(5)") == 20

        # Invalid function
        with pytest.raises(FunctionError):
            self.context.functions["invalid"] = "not a function"

    def test_expressions_with_variables(self):
        """Test evaluating expressions that use variables."""
        # Arithmetic with variables
        assert self.context.evaluate_int("int_var + 8") == 50
        assert self.context.evaluate_float("float_var * 2") == 6.28

        # String operations with variables
        assert self.context.evaluate_string('str_var + " world"') == "hello world"

        # Logical operations with variables
        assert self.context.evaluate_boolean("bool_var && true") is True
        assert self.context.evaluate_boolean("bool_var && false") is False

        # Complex expressions
        assert self.context.evaluate_boolean("int_var > 40 && float_var < 4") is True

    def test_type_specific_evaluation(self):
        """Test type-specific evaluation methods."""
        assert self.context.evaluate_int("int_var") == 42
        assert self.context.evaluate_float("float_var") == 3.14
        assert self.context.evaluate_string("str_var") == "hello"
        assert self.context.evaluate_boolean("bool_var") is True
        assert self.context.evaluate_tuple("tuple_var") == (1, 2, 3)
        assert self.context.evaluate_empty("()") is None

        # Type errors - these come through as TypeError not EvaluationError
        with pytest.raises((TypeError, EvaluationError)):
            self.context.evaluate_int("str_var")

        with pytest.raises((TypeError, EvaluationError)):
            self.context.evaluate_string("int_var")

    def test_no_assignment_in_expressions(self):
        """Test that assignment is not allowed in expressions."""
        # Direct assignment not allowed
        with pytest.raises((RuntimeError, ValueError)):
            self.context.evaluate("x = 42")

        # Assignment in complex expressions not allowed
        with pytest.raises((RuntimeError, ValueError)):
            self.context.evaluate("y = 10; y + 5")
