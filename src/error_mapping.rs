use evalexpr::EvalexprError;
use pyo3::exceptions::{PyArithmeticError, PyIndexError, PyKeyError, PyNameError, PyRuntimeError, PySyntaxError, PyTypeError, PyValueError, PyZeroDivisionError};
use pyo3::PyErr;

/// Converts `evalexpr` errors into appropriate Python exceptions.
///
/// This function maps errors from the `evalexpr` crate to the most semantically
/// appropriate Python exception type, following Python's exception hierarchy
/// conventions where possible.
///
/// # Arguments
///
/// * `error` - A reference to the evalexpr error to convert
///
/// # Returns
///
/// A `PyErr` that can be returned from a PyO3 function
///
/// # Examples
///
/// ```
/// use crate::error_mapping::convert_evalexpr_error;
///
/// fn my_eval_function(expr: &str) -> PyResult<PyObject> {
///     match eval_some_expression(expr) {
///         Ok(value) => Ok(convert_to_py_object(value)),
///         Err(e) => Err(convert_evalexpr_error(&e))
///     }
/// }
/// ```
pub(crate) fn convert_evalexpr_error(error: &EvalexprError) -> PyErr {
    match error {
        // Variable access errors -> KeyError
        EvalexprError::VariableIdentifierNotFound(var_name) => PyKeyError::new_err(var_name.clone()),

        // Function not found -> NameError (similar to Python's behavior)
        EvalexprError::FunctionIdentifierNotFound(func_name) => PyNameError::new_err(format!("Function identifier is not bound to anything by context: \"{}\".", func_name)),

        // Type errors -> TypeError
        EvalexprError::ExpectedString { actual } => PyTypeError::new_err(format!("Expected string, got {:?}", actual)),
        EvalexprError::ExpectedInt { actual } => PyTypeError::new_err(format!("Expected integer, got {:?}", actual)),
        EvalexprError::ExpectedFloat { actual } => PyTypeError::new_err(format!("Expected float, got {:?}", actual)),
        EvalexprError::ExpectedNumber { actual } => PyTypeError::new_err(format!("Expected number, got {:?}", actual)),
        EvalexprError::ExpectedNumberOrString { actual } => PyTypeError::new_err(format!("Expected number or string, got {:?}", actual)),
        EvalexprError::ExpectedBoolean { actual } => PyTypeError::new_err(format!("Expected boolean, got {:?}", actual)),
        EvalexprError::ExpectedTuple { actual } => PyTypeError::new_err(format!("Expected tuple, got {:?}", actual)),
        EvalexprError::ExpectedFixedLengthTuple { expected_length, actual } => PyTypeError::new_err(format!("Expected tuple of length {}, got {:?}", expected_length, actual)),
        EvalexprError::ExpectedRangedLengthTuple { expected_length, actual } => PyTypeError::new_err(format!(
            "Expected tuple of length between {} and {}, got {:?}",
            expected_length.start(),
            expected_length.end(),
            actual
        )),
        EvalexprError::TypeError { expected, actual } => PyTypeError::new_err(format!("Expected one of {:?}, got {:?}", expected, actual)),
        EvalexprError::WrongTypeCombination { operator, actual } => PyTypeError::new_err(format!("Invalid type combination for operator {:?}: {:?}", operator, actual)),

        // Argument count errors -> ValueError
        EvalexprError::WrongOperatorArgumentAmount { expected, actual } => PyValueError::new_err(format!("An operator expected {} arguments, but got {}.", expected, actual)),
        EvalexprError::WrongFunctionArgumentAmount { expected, actual } => PyValueError::new_err(format!(
            "Function expected between {} and {} arguments, but got {}.",
            expected.start(),
            expected.end(),
            actual
        )),

        // Parsing and syntax errors -> SyntaxError
        EvalexprError::UnmatchedLBrace => PySyntaxError::new_err("Unmatched opening brace"),
        EvalexprError::UnmatchedRBrace => PySyntaxError::new_err("Unmatched closing brace"),
        EvalexprError::UnmatchedDoubleQuote => PySyntaxError::new_err("Unmatched double quote"),
        EvalexprError::MissingOperatorOutsideOfBrace => PySyntaxError::new_err("Missing operator outside of brace"),
        EvalexprError::UnmatchedPartialToken { first, second } => PySyntaxError::new_err(format!("Unmatched token: {:?} followed by {:?}", first, second)),
        EvalexprError::IllegalEscapeSequence(seq) => PySyntaxError::new_err(format!("Illegal escape sequence: {}", seq)),

        // Math errors -> Arithmetic errors
        EvalexprError::AdditionError { augend, addend } => PyArithmeticError::new_err(format!("Addition error: {:?} + {:?}", augend, addend)),
        EvalexprError::SubtractionError { minuend, subtrahend } => PyArithmeticError::new_err(format!("Subtraction error: {:?} - {:?}", minuend, subtrahend)),
        EvalexprError::NegationError { argument } => PyArithmeticError::new_err(format!("Negation error: -{:?}", argument)),
        EvalexprError::MultiplicationError { multiplicand, multiplier } => PyArithmeticError::new_err(format!("Multiplication error: {:?} * {:?}", multiplicand, multiplier)),
        EvalexprError::DivisionError { dividend, divisor } => {
            // Special case for division by zero
            if let Ok(is_zero) = divisor.as_number().map(|n| n == 0.0) {
                if is_zero {
                    return PyZeroDivisionError::new_err("Division by zero");
                }
            }
            PyArithmeticError::new_err(format!("Division error: {:?} / {:?}", dividend, divisor))
        }
        EvalexprError::ModulationError { dividend, divisor } => {
            // Special case for modulo by zero
            if let Ok(is_zero) = divisor.as_number().map(|n| n == 0.0) {
                if is_zero {
                    return PyZeroDivisionError::new_err("Modulo by zero");
                }
            }
            PyArithmeticError::new_err(format!("Modulo error: {:?} % {:?}", dividend, divisor))
        }

        // Index errors -> IndexError
        EvalexprError::OutOfBoundsAccess => PyIndexError::new_err("Index out of bounds"),

        // Custom message -> ValueError (general purpose)
        EvalexprError::CustomMessage(msg) => PyValueError::new_err(msg.clone()),

        // Context mutation errors -> RuntimeError
        EvalexprError::ContextNotMutable => PyRuntimeError::new_err("Context is not mutable"),
        EvalexprError::BuiltinFunctionsCannotBeEnabled => PyRuntimeError::new_err("Built-in functions cannot be enabled in this context"),
        EvalexprError::BuiltinFunctionsCannotBeDisabled => PyRuntimeError::new_err("Built-in functions cannot be disabled in this context"),

        // Handle any other errors as generic ValueError
        _ => PyValueError::new_err(format!("Evaluation error: {}", error)),
    }
}
