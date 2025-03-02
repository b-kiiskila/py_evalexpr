import pytest
from py_evalexpr.natives import evaluate


class TestEvaluate:
    """Test cases for the stateless evaluation functions"""

    # Basic value types
    def test_basic_types(self):
        # Integer
        result = evaluate.evaluate("42")
        assert result.as_int() == 42
        assert result.type is int

        # Float
        result = evaluate.evaluate("3.14")
        assert result.as_float() == 3.14
        assert result.type is float

        # Scientific notation
        result = evaluate.evaluate("2.5e2")
        assert result.as_float() == 250.0
        assert result.type is float

        # Hexadecimal
        result = evaluate.evaluate("0xA")
        assert result.as_int() == 10
        assert result.type is int

        # Boolean
        result = evaluate.evaluate("true")
        assert result.as_bool() is True
        assert result.type is bool

        # String
        result = evaluate.evaluate('"hello"')
        assert result.as_string() == "hello"
        assert result.type is str

        # Empty
        result = evaluate.evaluate("()")
        assert result.as_none() is None

        # Tuple
        result = evaluate.evaluate("(1, 2, 3)")
        assert result.as_tuple() == (1, 2, 3)
        assert result.type is tuple

    # Type-specific evaluation functions
    def test_type_specific_functions(self):
        assert evaluate.evaluate_int("42") == 42
        assert evaluate.evaluate_float("3.14") == 3.14
        assert evaluate.evaluate_string('"hello"') == "hello"
        assert evaluate.evaluate_boolean("true") is True
        assert evaluate.evaluate_tuple("(1, 2, 3)") == (1, 2, 3)
        assert evaluate.evaluate_empty("()") is None

    # Arithmetic operators
    def test_arithmetic_operators(self):
        # Addition
        assert evaluate.evaluate_int("2 + 3") == 5
        assert evaluate.evaluate_float("2.5 + 3.5") == 6.0
        assert evaluate.evaluate_string('"Hello, " + "world!"') == "Hello, world!"

        # Subtraction
        assert evaluate.evaluate_int("5 - 3") == 2
        assert evaluate.evaluate_float("5.5 - 2.5") == 3.0

        # Multiplication
        assert evaluate.evaluate_int("3 * 4") == 12
        assert evaluate.evaluate_float("2.5 * 2") == 5.0

        # Division (integer if both args are integers)
        assert evaluate.evaluate_int("6 / 3") == 2
        # When using evaluate_float on an integer result, need to handle int->float conversion
        # or test that we receive a proper type error
        with pytest.raises(TypeError):
            evaluate.evaluate_float(
                "5 / 2"
            )  # This returns an integer value (2), not a float
        assert evaluate.evaluate_float("10.0 / 2") == 5.0

        # Modulo
        assert evaluate.evaluate_int("7 % 3") == 1
        assert evaluate.evaluate_float("7.5 % 2") == 1.5

        # Exponentiation (always returns float)
        assert evaluate.evaluate_float("2 ^ 3") == 8.0

        # Unary negation
        assert evaluate.evaluate_int("-5") == -5
        assert evaluate.evaluate_float("-3.14") == -3.14

    # Comparison operators
    def test_comparison_operators(self):
        # Equality
        assert evaluate.evaluate_boolean("5 == 5") is True
        assert evaluate.evaluate_boolean("5 == 6") is False
        assert evaluate.evaluate_boolean('"abc" == "abc"') is True

        # Inequality
        assert evaluate.evaluate_boolean("5 != 6") is True
        assert evaluate.evaluate_boolean('"abc" != "def"') is True

        # Greater than
        assert evaluate.evaluate_boolean("5 > 3") is True
        assert evaluate.evaluate_boolean("3 > 5") is False

        # Less than
        assert evaluate.evaluate_boolean("3 < 5") is True
        assert evaluate.evaluate_boolean("5 < 3") is False

        # Greater than or equal
        assert evaluate.evaluate_boolean("5 >= 5") is True
        assert evaluate.evaluate_boolean("5 >= 3") is True

        # Less than or equal
        assert evaluate.evaluate_boolean("3 <= 5") is True
        assert evaluate.evaluate_boolean("5 <= 5") is True

    # Logical operators
    def test_logical_operators(self):
        # AND
        assert evaluate.evaluate_boolean("true && true") is True
        assert evaluate.evaluate_boolean("true && false") is False
        assert evaluate.evaluate_boolean("false && false") is False

        # OR
        assert evaluate.evaluate_boolean("true || false") is True
        assert evaluate.evaluate_boolean("false || false") is False

        # NOT
        assert evaluate.evaluate_boolean("!true") is False
        assert evaluate.evaluate_boolean("!false") is True

    # Operator precedence
    def test_operator_precedence(self):
        assert (
            evaluate.evaluate_int("2 + 3 * 4") == 14
        )  # Multiplication before addition
        assert (
            evaluate.evaluate_int("(2 + 3) * 4") == 20
        )  # Parentheses override precedence
        assert (
            evaluate.evaluate_boolean("2 < 3 && 4 > 1") is True
        )  # Comparison before logical

    # Aggregation (tuple creation)
    def test_aggregation(self):
        result = evaluate.evaluate("1, 2, 3")
        assert result.as_tuple() == (1, 2, 3)

        # Nested tuples with parentheses
        result = evaluate.evaluate("1, (2, 3)")
        assert result.as_tuple() == (1, (2, 3))

        # Mixed types
        result = evaluate.evaluate('1, "a", true')
        assert result.as_tuple() == (1, "a", True)

    # String handling
    def test_string_handling(self):
        # Escape sequences
        assert evaluate.evaluate_string(r'"hello \"world\""') == 'hello "world"'
        assert evaluate.evaluate_string(r'"hello\\world"') == "hello\\world"

    # Error handling
    def test_error_handling(self):
        # Syntax error
        with pytest.raises(ValueError):
            evaluate.evaluate("2 +")

        # Type error - in py_evalexpr it raises TypeError directly
        with pytest.raises(TypeError):
            evaluate.evaluate("2 + true")

        # Division by zero - from error_mapping.rs, we can see this maps to ZeroDivisionError
        with pytest.raises(ZeroDivisionError):
            evaluate.evaluate("1 / 0")

        # Undefined variable
        with pytest.raises(KeyError):
            evaluate.evaluate("x")

    # Comments
    def test_comments(self):
        # Inline comments
        assert evaluate.evaluate_int("2 + 3 /* this is a comment */ + 4") == 9

        # End-of-line comments
        assert evaluate.evaluate_int("2 + 3 // this is a comment\n + 4") == 9
