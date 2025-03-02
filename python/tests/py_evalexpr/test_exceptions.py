from py_evalexpr.exceptions import (
    EvalExprError,
    VariableError,
    FunctionError,
    EvaluationError,
)


class TestExceptions:
    """Test exception hierarchy and behavior."""

    def test_exception_hierarchy(self):
        """Test that exception hierarchy is correct."""
        # Base exception
        base = EvalExprError("Base error")
        assert isinstance(base, Exception)

        # Child exceptions
        var_err = VariableError("Variable error")
        func_err = FunctionError("Function error")
        eval_err = EvaluationError("Evaluation error")

        # All should be instances of the base exception
        assert isinstance(var_err, EvalExprError)
        assert isinstance(func_err, EvalExprError)
        assert isinstance(eval_err, EvalExprError)

        # But they should be distinct from each other
        assert not isinstance(var_err, FunctionError)
        assert not isinstance(var_err, EvaluationError)
        assert not isinstance(func_err, VariableError)
        assert not isinstance(func_err, EvaluationError)
        assert not isinstance(eval_err, VariableError)
        assert not isinstance(eval_err, FunctionError)

    def test_exception_messages(self):
        """Test that exception messages are preserved."""
        message = "Test error message"
        err = EvalExprError(message)
        assert str(err) == message

        var_err = VariableError(message)
        assert str(var_err) == message

        func_err = FunctionError(message)
        assert str(func_err) == message

        eval_err = EvaluationError(message)
        assert str(eval_err) == message

    def test_exception_with_cause(self):
        """Test that exceptions can have a cause."""
        cause = ValueError("Original error")
        err = EvaluationError("Wrapped error")

        # Explicitly raise with a cause
        try:
            try:
                raise cause
            except ValueError as e:
                raise err from e
        except EvaluationError as e:
            assert e.__cause__ == cause
