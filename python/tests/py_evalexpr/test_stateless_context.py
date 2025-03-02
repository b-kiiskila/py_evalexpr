import pytest
from py_evalexpr.stateless_context import StatelessContext
from py_evalexpr.exceptions import EvaluationError


class TestStatelessContext:
    """Test the StatelessContext implementation."""

    def setup_method(self):
        """Set up a stateless context."""
        self.context = StatelessContext()

    def test_evaluate(self):
        """Test the generic evaluate method."""
        # Basic literals
        result = self.context.evaluate("42")
        assert result.value == 42
        assert result.type is int

        result = self.context.evaluate("3.14")
        assert result.value == 3.14
        assert result.type is float

        result = self.context.evaluate('"hello"')
        assert result.value == "hello"
        assert result.type is str

        result = self.context.evaluate("true")
        assert result.value is True
        assert result.type is bool

        result = self.context.evaluate("()")
        assert result.value is None

        result = self.context.evaluate("1, 2, 3")
        assert result.value == (1, 2, 3)
        assert result.type is tuple

        # Expressions
        assert self.context.evaluate("2 + 3").value == 5
        assert self.context.evaluate("2 * 3").value == 6
        assert self.context.evaluate("true && false").value is False
        assert self.context.evaluate('"hello" + " world"').value == "hello world"

    def test_error_handling(self):
        """Test error handling in stateless context."""
        # Syntax error
        with pytest.raises(EvaluationError):
            self.context.evaluate("2 +")

        # Type error
        with pytest.raises(TypeError):
            self.context.evaluate("2 + true")

    def test_no_variables_allowed(self):
        """Test that variable access is not allowed in stateless context."""
        # Variables cannot be accessed (no state)
        with pytest.raises(KeyError):
            self.context.evaluate("x")

    def test_no_variable_persistence(self):
        """Test that variable assignments don't persist in stateless context."""
        # The assignment itself might not raise an error in the implementation,
        # but the variable should not persist regardless
        try:
            self.context.evaluate("x = 42")
        except Exception:
            pass  # It's okay if it raises an error

        # The key test: the variable should not exist after attempted assignment
        with pytest.raises(KeyError):
            self.context.evaluate("x")
