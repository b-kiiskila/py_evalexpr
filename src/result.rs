use pyo3::exceptions::PyValueError;
use pyo3::prelude::{PyAnyMethods, PyModule};
use pyo3::types::PyType;
use pyo3::Bound;
use pyo3::{pyclass, pymethods, pymodule, Py, PyRef, PyResult, Python};

#[pymodule]
pub mod result {
    use super::*;

    use pyo3::PyAny;

    #[pymodule_init]
    fn init(m: &Bound<'_, PyModule>) -> PyResult<()> {
        Python::attach(|py| {
            let mod_name = "py_evalexpr.natives.result";
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

    #[pyclass(subclass)]
    pub(crate) struct ExprEvalResult {
        #[pyo3(get)]
        pub(crate) value: Py<PyAny>,
        #[pyo3(get, name = "type")]
        pub(crate) _type: Py<PyType>,
    }

    #[pymethods]
    impl ExprEvalResult {
        #[new]
        fn new(value: Py<PyAny>, _type: Py<PyType>) -> Self {
            ExprEvalResult { value, _type }
        }

        fn as_int(&self, _py: Python) -> PyResult<i64> {
            Err(PyValueError::new_err("Value is not an integer"))
        }

        fn as_float(&self, _py: Python) -> PyResult<f64> {
            Err(PyValueError::new_err("Value is not a float"))
        }

        fn as_bool(&self, _py: Python) -> PyResult<bool> {
            Err(PyValueError::new_err("Value is not a boolean"))
        }

        fn as_string(&self, _py: Python) -> PyResult<String> {
            Err(PyValueError::new_err("Value is not a string"))
        }

        fn as_tuple(&self, _py: Python) -> PyResult<Vec<Py<PyAny>>> {
            Err(PyValueError::new_err("Value is not a tuple"))
        }

        fn as_none(&self, _py: Python) -> PyResult<()> {
            Err(PyValueError::new_err("Value is not None"))
        }

        fn __str__(&self, _py: Python) -> PyResult<String> {
            Ok(self.value.to_string())
        }
    }

    #[pyclass(extends = ExprEvalResult)]
    pub(crate) struct ExprEvalIntResult {}

    #[pymethods]
    impl ExprEvalIntResult {
        #[new]
        fn new(value: Py<PyAny>, _type: Py<PyType>) -> (Self, ExprEvalResult) {
            (ExprEvalIntResult {}, ExprEvalResult::new(value, _type))
        }

        fn as_int(self_: PyRef<'_, Self>) -> PyResult<i64> {
            self_.as_super().value.extract::<i64>(self_.py())
        }

        fn __repr__(self_: PyRef<'_, Self>) -> PyResult<String> {
            Ok(format!("ExprEvalIntResult(value={}, type={})", self_.as_super().value, self_.as_super()._type))
        }
    }

    #[pyclass(extends = ExprEvalResult)]
    pub(crate) struct ExprEvalFloatResult {}

    #[pymethods]
    impl ExprEvalFloatResult {
        #[new]
        fn new(value: Py<PyAny>, _type: Py<PyType>) -> (Self, ExprEvalResult) {
            (ExprEvalFloatResult {}, ExprEvalResult::new(value, _type))
        }

        fn as_float(self_: PyRef<'_, Self>) -> PyResult<f64> {
            self_.as_super().value.extract::<f64>(self_.py())
        }

        fn __repr__(self_: PyRef<'_, Self>) -> PyResult<String> {
            Ok(format!("ExprEvalFloatResult(value={}, type={})", self_.as_super().value, self_.as_super()._type))
        }
    }

    #[pyclass(extends = ExprEvalResult)]
    pub(crate) struct ExprEvalBoolResult {}

    #[pymethods]
    impl ExprEvalBoolResult {
        #[new]
        fn new(value: Py<PyAny>, _type: Py<PyType>) -> (Self, ExprEvalResult) {
            (ExprEvalBoolResult {}, ExprEvalResult::new(value, _type))
        }

        fn as_bool(self_: PyRef<'_, Self>) -> PyResult<bool> {
            self_.as_super().value.extract::<bool>(self_.py())
        }

        fn __repr__(self_: PyRef<'_, Self>) -> PyResult<String> {
            Ok(format!("ExprEvalBoolResult(value={}, type={})", self_.as_super().value, self_.as_super()._type))
        }
    }

    #[pyclass(extends = ExprEvalResult)]
    pub(crate) struct ExprEvalStringResult {}

    #[pymethods]
    impl ExprEvalStringResult {
        #[new]
        fn new(value: Py<PyAny>, _type: Py<PyType>) -> (Self, ExprEvalResult) {
            (ExprEvalStringResult {}, ExprEvalResult::new(value, _type))
        }

        fn as_string(self_: PyRef<'_, Self>) -> PyResult<String> {
            self_.as_super().value.extract::<String>(self_.py())
        }

        fn __repr__(self_: PyRef<'_, Self>) -> PyResult<String> {
            Ok(format!("ExprEvalStringResult(value={}, type={})", self_.as_super().value, self_.as_super()._type))
        }
    }

    #[pyclass(extends = ExprEvalResult)]
    pub(crate) struct ExprEvalTupleResult {}

    #[pymethods]
    impl ExprEvalTupleResult {
        #[new]
        fn new(value: Py<PyAny>, _type: Py<PyType>) -> (Self, ExprEvalResult) {
            (ExprEvalTupleResult {}, ExprEvalResult::new(value, _type))
        }

        fn as_tuple(self_: PyRef<'_, Self>) -> PyResult<Py<PyAny>> {
            Ok(self_.as_super().value.clone_ref(self_.py()))
        }

        fn __repr__(self_: PyRef<'_, Self>) -> PyResult<String> {
            Ok(format!("ExprEvalTupleResult(value={}, type={})", self_.as_super().value, self_.as_super()._type))
        }
    }

    #[pyclass(extends = ExprEvalResult)]
    pub(crate) struct ExprEvalNoneResult {}

    #[pymethods]
    impl ExprEvalNoneResult {
        #[new]
        fn new(value: Py<PyAny>, _type: Py<PyType>) -> (Self, ExprEvalResult) {
            (ExprEvalNoneResult {}, ExprEvalResult::new(value, _type))
        }

        fn as_none(_self_: PyRef<'_, Self>) -> PyResult<()> {
            Ok(())
        }

        fn __repr__(self_: PyRef<'_, Self>) -> PyResult<String> {
            Ok(format!("ExprEvalNoneResult(value={}, type={})", self_.as_super().value, self_.as_super()._type))
        }
    }

    // This is a dummy class just to simplify imports in the Python code for our type annotations.
    #[pyclass]
    struct EvalExprResults {}
}
