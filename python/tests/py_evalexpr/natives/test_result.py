import pytest
from py_evalexpr.natives import evaluate


class TestResult:
    """Test cases for the result module and EvalExprResults"""

    def test_int_result(self):
        # Get an integer result
        result = evaluate.evaluate("42")

        # Type checks - the implementation uses concrete result types, not the union type
        # Check the object's repr string instead to make sure it's the right type
        assert "ExprEvalIntResult" in repr(result)
        assert result.type is int

        # Value access
        assert result.as_int() == 42

        # Invalid conversions
        with pytest.raises(ValueError):
            result.as_float()

        with pytest.raises(ValueError):
            result.as_string()

        with pytest.raises(ValueError):
            result.as_bool()

        with pytest.raises(ValueError):
            result.as_tuple()

        with pytest.raises(ValueError):
            result.as_none()

    def test_float_result(self):
        # Get a float result
        result = evaluate.evaluate("3.14")

        # Type checks
        assert "ExprEvalFloatResult" in repr(result)
        assert result.type is float

        # Value access
        assert result.as_float() == 3.14

        # Invalid conversions
        with pytest.raises(ValueError):
            result.as_int()

        # Other invalid conversions...

    def test_string_result(self):
        # Get a string result
        result = evaluate.evaluate('"hello"')

        # Type checks
        assert "ExprEvalStringResult" in repr(result)
        assert result.type is str

        # Value access
        assert result.as_string() == "hello"

        # Invalid conversions
        with pytest.raises(ValueError):
            result.as_int()

        # Other invalid conversions...

    def test_boolean_result(self):
        # Get a boolean result
        result = evaluate.evaluate("true")

        # Type checks
        assert "ExprEvalBoolResult" in repr(result)
        assert result.type is bool

        # Value access
        assert result.as_bool() is True

        # Invalid conversions
        with pytest.raises(ValueError):
            result.as_int()

        # Other invalid conversions...

    def test_tuple_result(self):
        # Get a tuple result
        result = evaluate.evaluate("(1, 2, 3)")

        # Type checks
        assert "ExprEvalTupleResult" in repr(result)
        assert result.type is tuple

        # Value access
        assert result.as_tuple() == (1, 2, 3)

        # Invalid conversions
        with pytest.raises(ValueError):
            result.as_int()

        # Other invalid conversions...

    def test_none_result(self):
        # Get a none/empty result
        result = evaluate.evaluate("()")

        # Value access
        assert result.as_none() is None

        # Invalid conversions
        with pytest.raises(ValueError):
            result.as_int()

        # Other invalid conversions...

    def test_string_representation(self):
        # Test string and repr methods for different result types
        int_result = evaluate.evaluate("42")
        assert str(int_result) is not None
        assert repr(int_result) is not None

        float_result = evaluate.evaluate("3.14")
        assert str(float_result) is not None
        assert repr(float_result) is not None

        # Value should be visible in the string representation
        assert "42" in str(int_result)
        assert "3.14" in str(float_result)
