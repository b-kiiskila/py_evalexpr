from py_evalexpr.quickeval import (
    evaluate,
)


class TestQuickEval:
    """Test the quickeval module functions."""

    def test_evaluate(self):
        """Test the generic evaluate function."""
        # Basic literals
        assert evaluate("42") == 42
        assert evaluate("3.14") == 3.14
        assert evaluate('"hello"') == "hello"
        assert evaluate("true") is True
        assert evaluate("()") is None
        assert evaluate("1, 2, 3") == (1, 2, 3)

        # Expressions
        assert evaluate("2 + 3") == 5
        assert evaluate("2 * 3") == 6
        assert evaluate("true && false") is False
        assert evaluate("(2 > 1) && (3 < 4)") is True
        assert evaluate('"hello" + " " + "world"') == "hello world"
