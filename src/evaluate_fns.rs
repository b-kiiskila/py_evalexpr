use crate::error_mapping::convert_evalexpr_error;
use crate::remap::convert_to_eval_result;
use evalexpr::{eval, eval_boolean, eval_empty, eval_float, eval_int, eval_number, eval_string, eval_tuple, EvalexprResult, TupleType, Value};
use pyo3::prelude::{PyAnyMethods, PyModule};
use pyo3::Bound;
use pyo3::{pyfunction, pymodule, Py, PyAny, PyResult, Python};

#[pymodule]
pub mod evaluate {
    use super::*;
    use crate::remap::convert_to_py_tuple;

    #[pymodule_init]
    fn init(m: &Bound<'_, PyModule>) -> PyResult<()> {
        Python::attach(|py| {
            let mod_name = "py_evalexpr.natives.evaluate";
            py.import("sys")?.getattr("modules")?.set_item(mod_name, m)?;
            // There's a bug with pyo3 that makes the __module__ attribute of functions on submodules incorrect, so we have to iterate over the functions and set the __module__ attribute manually.
            let all = m.getattr("__all__")?.extract::<Vec<String>>()?;
            for name in all {
                let func = m.getattr(&name)?;
                func.setattr("__module__", mod_name)?;
            }
            Ok(())
        })
    }

    #[pyfunction]
    pub fn evaluate(expression: &str) -> PyResult<Py<PyAny>> {
        let result: EvalexprResult<Value> = eval(expression);

        Python::attach(|py| match result {
            Ok(value) => {
                // Determine the value type and create the appropriate subclass.
                Ok(convert_to_eval_result(py, value)?)
            }
            Err(e) => Err(convert_evalexpr_error(&e)),
        })
    }

    #[pyfunction]
    pub fn evaluate_string(expression: &str) -> PyResult<String> {
        let result: EvalexprResult<String> = eval_string(expression);

        match result {
            Ok(value) => Ok(value),
            Err(e) => Err(convert_evalexpr_error(&e)),
        }
    }

    #[pyfunction]
    pub fn evaluate_int(expression: &str) -> PyResult<i64> {
        let result: EvalexprResult<i64> = eval_int(expression);

        match result {
            Ok(value) => Ok(value),
            Err(e) => Err(convert_evalexpr_error(&e)),
        }
    }

    #[pyfunction]
    pub fn evaluate_float(expression: &str) -> PyResult<f64> {
        let result: EvalexprResult<f64> = eval_float(expression);

        match result {
            Ok(value) => Ok(value),
            Err(e) => Err(convert_evalexpr_error(&e)),
        }
    }

    #[pyfunction]
    pub fn evaluate_number(expression: &str) -> PyResult<f64> {
        let result: EvalexprResult<f64> = eval_number(expression);

        match result {
            Ok(value) => Ok(value),
            Err(e) => Err(convert_evalexpr_error(&e)),
        }
    }

    #[pyfunction]
    pub fn evaluate_boolean(expression: &str) -> PyResult<bool> {
        let result: EvalexprResult<bool> = eval_boolean(expression);

        match result {
            Ok(value) => Ok(value),
            Err(e) => Err(convert_evalexpr_error(&e)),
        }
    }

    #[pyfunction]
    pub fn evaluate_tuple(expression: &str) -> PyResult<Py<PyAny>> {
        let result: EvalexprResult<TupleType> = eval_tuple(expression);

        Python::attach(|py| match result {
            Ok(value) => Ok(convert_to_py_tuple(py, value)),
            Err(e) => Err(convert_evalexpr_error(&e)),
        })?
    }

    #[pyfunction]
    pub fn evaluate_empty(expression: &str) -> PyResult<()> {
        let result: EvalexprResult<()> = eval_empty(expression);

        match result {
            Ok(_) => Ok(()),
            Err(e) => Err(convert_evalexpr_error(&e)),
        }
    }
}
