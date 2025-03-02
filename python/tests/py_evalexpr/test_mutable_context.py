import pytest
from py_evalexpr.mutable_context import MutableContext
from py_evalexpr.exceptions import EvaluationError


class TestMutableContext:
    """Test the MutableContext implementation."""

    def setup_method(self):
        """Set up a mutable context with initial variables and functions."""
        self.context = MutableContext()

        # Set up initial variables
        self.context.variables["int_var"] = 42
        self.context.variables["float_var"] = 3.14
        self.context.variables["str_var"] = "hello"
        self.context.variables["bool_var"] = True
        self.context.variables["tuple_var"] = (1, 2, 3)

        # Set up functions
        self.context.functions["add"] = lambda x, y: x + y
        self.context.functions["double"] = lambda x: x * 2

    def test_variable_mutation(self):
        """Test modifying variables through expressions."""
        # Assign new variable in expression
        result = self.context.evaluate("new_var = 100")
        assert result.value is None  # Assignment returns None
        assert self.context.variables["new_var"] == 100

        # Modify existing variable
        self.context.evaluate("int_var = 99")
        assert self.context.variables["int_var"] == 99

    def test_evaluate_empty(self):
        """Test evaluating expressions that don't return values."""
        # Assignment expression
        result = self.context.evaluate_empty("x = 42")
        assert result is None
        assert self.context.variables["x"] == 42

        # Expression with return value causes error
        with pytest.raises((EvaluationError, TypeError)):
            self.context.evaluate_empty("5 + 5")  # Returns a value

    def test_assignment_with_variables(self):
        """Test assignments that use existing variables."""
        # Assign based on existing variable
        self.context.evaluate("derived = int_var + 8")
        assert self.context.variables["derived"] == 50

        # Update based on self
        self.context.evaluate("int_var = int_var + 1")
        assert self.context.variables["int_var"] == 43

    def test_assignment_with_functions(self):
        """Test assignments that use function results."""
        # Assign result of function call
        self.context.evaluate("doubled = double(21)")
        assert self.context.variables["doubled"] == 42

        # Update based on function result
        self.context.evaluate("int_var = add(int_var, 10)")
        assert self.context.variables["int_var"] == 52
