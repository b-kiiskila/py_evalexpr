import pytest
from py_evalexpr.natives.context import EvalContext

from py_evalexpr.natives import evaluate_with_context_mut


class TestEvaluateWithContextMut:
    def setup_method(self):
        self.context = EvalContext()

    # Variable assignment
    def test_variable_assignment(self):
        # Basic assignment returns empty/None
        result = evaluate_with_context_mut.evaluate_with_context_mut(
            "x = 42", self.context
        )
        assert result.as_none() is None  # Assignment returns empty/None

        # Verify the variable was stored
        variables = dict(self.context.iter_variables())
        assert variables["x"] == 42

        # Verify we can access the variable in a subsequent expression
        result = evaluate_with_context_mut.evaluate_with_context_mut("x", self.context)
        assert result.as_int() == 42

        # Assignment of different types
        evaluate_with_context_mut.evaluate_with_context_mut(
            "int_var = 10", self.context
        )
        evaluate_with_context_mut.evaluate_with_context_mut(
            "float_var = 3.14", self.context
        )
        evaluate_with_context_mut.evaluate_with_context_mut(
            'str_var = "hello"', self.context
        )
        evaluate_with_context_mut.evaluate_with_context_mut(
            "bool_var = true", self.context
        )
        evaluate_with_context_mut.evaluate_with_context_mut(
            "tuple_var = (1, 2, 3)", self.context
        )

        # Verify all variables were stored
        variables = dict(self.context.iter_variables())
        assert variables["int_var"] == 10
        assert variables["float_var"] == 3.14
        assert variables["str_var"] == "hello"
        assert variables["bool_var"] is True
        assert variables["tuple_var"] == (1, 2, 3)

        # Type safety: assigning a different type should fail
        with pytest.raises(TypeError):
            evaluate_with_context_mut.evaluate_with_context_mut(
                'int_var = "string"', self.context
            )

    def test_compound_assignment(self):
        # Initialize variables
        evaluate_with_context_mut.evaluate_with_context_mut("x = 10", self.context)
        evaluate_with_context_mut.evaluate_with_context_mut('s = "hello"', self.context)
        evaluate_with_context_mut.evaluate_with_context_mut("b = true", self.context)

        # Addition assignment
        evaluate_with_context_mut.evaluate_with_context_mut("x += 5", self.context)
        assert (
            evaluate_with_context_mut.evaluate_int_with_context("x", self.context) == 15
        )

        # String concatenation assignment
        evaluate_with_context_mut.evaluate_with_context_mut(
            's += " world"', self.context
        )
        assert (
            evaluate_with_context_mut.evaluate_string_with_context("s", self.context)
            == "hello world"
        )

        # Subtraction assignment
        evaluate_with_context_mut.evaluate_with_context_mut("x -= 3", self.context)
        assert (
            evaluate_with_context_mut.evaluate_int_with_context("x", self.context) == 12
        )

        # Multiplication assignment
        evaluate_with_context_mut.evaluate_with_context_mut("x *= 2", self.context)
        assert (
            evaluate_with_context_mut.evaluate_int_with_context("x", self.context) == 24
        )

        # Division assignment
        evaluate_with_context_mut.evaluate_with_context_mut("x /= 3", self.context)
        assert (
            evaluate_with_context_mut.evaluate_int_with_context("x", self.context) == 8
        )

        # Modulo assignment
        evaluate_with_context_mut.evaluate_with_context_mut("x %= 5", self.context)
        assert (
            evaluate_with_context_mut.evaluate_int_with_context("x", self.context) == 3
        )

        # Exponentiation assignment (returns float), we can't reuse our x because we already assigned it to an int
        evaluate_with_context_mut.evaluate_with_context_mut(
            "float_x = 3.0", self.context
        )
        evaluate_with_context_mut.evaluate_with_context_mut(
            "float_x ^= 2", self.context
        )
        assert (
            evaluate_with_context_mut.evaluate_float_with_context(
                "float_x", self.context
            )
            == 9.0
        )

        # Logical-AND assignment
        evaluate_with_context_mut.evaluate_with_context_mut("b &&= false", self.context)
        assert (
            evaluate_with_context_mut.evaluate_boolean_with_context("b", self.context)
            is False
        )

        # Logical-OR assignment
        evaluate_with_context_mut.evaluate_with_context_mut("b ||= true", self.context)
        assert (
            evaluate_with_context_mut.evaluate_boolean_with_context("b", self.context)
            is True
        )

    # Expression chaining
    def test_expression_chaining(self):
        # Multiple assignments - all assignments return EMPTY_VALUE
        result = evaluate_with_context_mut.evaluate_with_context_mut(
            "a = 10; b = 20; c = a + b", self.context
        )
        assert result.as_none() is None  # Assignment returns empty/None

        # Verify the variables were set correctly
        variables = dict(self.context.iter_variables())
        assert variables["a"] == 10
        assert variables["b"] == 20
        assert variables["c"] == 30

        # To get the value instead of None, we need a non-assignment expression at the end
        result = evaluate_with_context_mut.evaluate_with_context_mut(
            "a = 10; b = 20; a + b", self.context
        )
        assert result.as_int() == 30  # This returns the evaluation of a + b

        # Verify all variables
        variables = dict(self.context.iter_variables())
        assert variables["a"] == 10
        assert variables["b"] == 20
        assert variables["c"] == 30

        # Chain with trailing semicolon returns empty
        result = evaluate_with_context_mut.evaluate_with_context_mut(
            "a = 5; b = 10;", self.context
        )
        assert result.as_none() is None

        # Empty evaluation with chain
        assert (
            evaluate_with_context_mut.evaluate_empty_with_context_mut(
                "a = 5; b = 10;", self.context
            )
            is None
        )

    def test_function_update(self):
        self.context.set_function("double", lambda x: x * 2)
        assert (
            evaluate_with_context_mut.evaluate_int_with_context(
                "double(21)", self.context
            )
            == 42
        )

        # Update the function, and verify the new result
        self.context.set_function("double", lambda x: x * 3)
        assert (
            evaluate_with_context_mut.evaluate_int_with_context(
                "double(14)", self.context
            )
            == 42
        )

    def test_small_scripts(self):
        # A small script that performs multiple operations
        script = """
        // Initialize variables
        x = 5;
        y = 10;
        
        // Perform calculations
        sum = x + y;
        product = x * y;
        
        // Return final result
        sum + product
        """

        result = evaluate_with_context_mut.evaluate_int_with_context(
            script, self.context
        )
        assert result == 65  # (5 + 10) + (5 * 10) = 15 + 50 = 65

        # Verify all variables were stored
        variables = dict(self.context.iter_variables())
        assert variables["x"] == 5
        assert variables["y"] == 10
        assert variables["sum"] == 15
        assert variables["product"] == 50

    # Type-specific evaluation functions
    def test_type_specific_functions(self):
        # Set up initial variables
        evaluate_with_context_mut.evaluate_with_context_mut(
            "int_var = 42", self.context
        )
        evaluate_with_context_mut.evaluate_with_context_mut(
            "float_var = 3.14", self.context
        )
        evaluate_with_context_mut.evaluate_with_context_mut(
            'str_var = "hello"', self.context
        )
        evaluate_with_context_mut.evaluate_with_context_mut(
            "bool_var = true", self.context
        )
        evaluate_with_context_mut.evaluate_with_context_mut(
            "tuple_var = (1, 2, 3)", self.context
        )

        # Test each type-specific function
        assert (
            evaluate_with_context_mut.evaluate_int_with_context("int_var", self.context)
            == 42
        )
        assert (
            evaluate_with_context_mut.evaluate_float_with_context(
                "float_var", self.context
            )
            == 3.14
        )
        assert (
            evaluate_with_context_mut.evaluate_string_with_context(
                "str_var", self.context
            )
            == "hello"
        )
        assert (
            evaluate_with_context_mut.evaluate_boolean_with_context(
                "bool_var", self.context
            )
            is True
        )
        assert evaluate_with_context_mut.evaluate_tuple_with_context(
            "tuple_var", self.context
        ) == (1, 2, 3)
