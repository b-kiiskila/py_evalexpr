use crate::remap::{convert_native_to_py, convert_py_to_native};
use evalexpr::{Context, ContextWithMutableFunctions, ContextWithMutableVariables, DefaultNumericTypes, EvalexprError, Function, HashMapContext, IterateVariablesContext, Value};
use pyo3::prelude::*;
use pyo3::types::PyTuple;
use std::ops::{Deref, DerefMut};
use std::sync::Arc;

fn wrap_py_fn_as_native_fn(py_fn: Py<PyAny>) -> Function<DefaultNumericTypes> {
    let py_fn = Arc::new(py_fn);
    Function::new(Box::new(move |args: &Value<DefaultNumericTypes>| {
        let py_fn = Arc::clone(&py_fn);
        Python::attach(|py| {
            // Handle tuple arguments
            let py_args = match args {
                Value::Tuple(tuple_args) => {
                    // Convert each argument separately
                    let py_args: Result<Vec<Py<PyAny>>, _> = tuple_args.iter().map(|val_ref| convert_native_to_py(py, val_ref.clone())).collect();
                    py_args.map_err(|e| EvalexprError::CustomMessage(format!("Error converting arguments: {}", e)))?
                }
                // Handle single argument case
                _ => {
                    let py_arg = convert_native_to_py(py, args.clone()).map_err(|e| EvalexprError::CustomMessage(format!("Error converting argument: {}", e)))?;
                    vec![py_arg]
                }
            };

            // Create Python tuple from the arguments
            let py_args_tuple = PyTuple::new(py, &py_args).unwrap();

            let result = py_fn.call(py, py_args_tuple, None).map_err(|e| EvalexprError::CustomMessage(e.to_string()))?;

            Ok(convert_py_to_native(py, result))
        })
    }))
}

#[pymodule]
#[pyo3(module = "py_evalexpr.natives.context")]
pub mod context {
    use super::*;

    #[pymodule_init]
    fn init(m: &Bound<'_, PyModule>) -> PyResult<()> {
        Python::attach(|py| {
            let mod_name = "py_evalexpr.natives.context";
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

    #[pyclass(module = "py_evalexpr.natives.context", name = "EvalContext")]
    pub struct EvalContext {
        context: HashMapContext<DefaultNumericTypes>,
    }

    #[pymethods]
    impl EvalContext {
        #[new]
        fn new() -> Self {
            let context = HashMapContext::new();
            EvalContext { context }
        }

        fn set_variable(&mut self, py: Python<'_>, identifier: &str, value: Py<PyAny>) -> PyResult<()> {
            let value = convert_py_to_native(py, value);
            let ident = identifier.to_string();
            self.context
                .set_value(ident, value)
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("{}", e)))?;
            Ok(())
        }

        fn set_function(&mut self, py: Python<'_>, identifier: &str, value: Py<PyAny>) -> PyResult<()> {
            let is_callable = value.bind(py).is_callable();

            if !is_callable {
                return Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>("Value is not callable"));
            }

            let value = wrap_py_fn_as_native_fn(value);
            let ident = identifier.to_string();
            self.context
                .set_function(ident, value)
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("{}", e)))?;
            Ok(())
        }

        fn iter_variables(&self, py: Python<'_>) -> PyResult<Vec<(String, Py<PyAny>)>> {
            let variables = self
                .context
                .iter_variables()
                .map(|(name, value)| {
                    let py_value = convert_native_to_py(py, value).unwrap();
                    (name.clone(), py_value)
                })
                .collect();
            Ok(variables)
        }

        fn iter_variable_names(&self) -> PyResult<Vec<String>> {
            let variable_names = self.context.iter_variable_names().collect();
            Ok(variable_names)
        }

        fn set_builtin_functions_disabled(&mut self, disabled: bool) -> PyResult<()> {
            self.context
                .set_builtin_functions_disabled(disabled)
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("{}", e)))?;
            Ok(())
        }

        fn clear(&mut self) {
            self.context.clear();
        }

        fn __str__(&self) -> String {
            format!("<EvalContext {ctx:?}>", ctx = self.context)
        }

        fn __repr__(&self) -> String {
            format!("<EvalContext {ctx:?}>", ctx = self.context)
        }
    }

    impl Deref for EvalContext {
        type Target = HashMapContext<DefaultNumericTypes>;

        fn deref(&self) -> &Self::Target {
            &self.context
        }
    }

    impl DerefMut for EvalContext {
        fn deref_mut(&mut self) -> &mut Self::Target {
            &mut self.context
        }
    }
}
