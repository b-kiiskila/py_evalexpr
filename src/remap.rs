use crate::result::result::{ExprEvalBoolResult, ExprEvalFloatResult, ExprEvalIntResult, ExprEvalNoneResult, ExprEvalResult, ExprEvalStringResult, ExprEvalTupleResult};
use evalexpr::{DefaultNumericTypes, TupleType, Value};
use pyo3::prelude::*;
use pyo3::types::{PyBool, PyFloat, PyInt, PyNone, PyString, PyTuple, PyType};

#[inline]
pub(crate) fn convert_to_py_int(py: Python, value: i64) -> PyResult<PyObject> {
    Ok(value.into_pyobject(py)?.to_owned().into())
}

#[inline]
pub(crate) fn convert_to_py_float(py: Python, value: f64) -> PyResult<PyObject> {
    Ok(value.into_pyobject(py)?.to_owned().into())
}

#[inline]
pub(crate) fn convert_to_py_bool(py: Python, value: bool) -> PyResult<PyObject> {
    Ok(value.into_pyobject(py)?.to_owned().into())
}

#[inline]
pub(crate) fn convert_to_py_string(py: Python, value: String) -> PyResult<PyObject> {
    Ok(value.into_pyobject(py)?.to_owned().into())
}

#[inline]
pub(crate) fn convert_to_py_tuple(py: Python, value: TupleType) -> PyResult<PyObject> {
    let py_list: Vec<PyObject> = value.into_iter().map(|v| convert_native_to_py(py, v).unwrap_or_else(|_| py.None())).collect();
    Ok(PyTuple::new(py, py_list)?.to_owned().into())
}

#[inline]
pub(crate) fn convert_to_py_none(py: Python) -> PyResult<PyObject> {
    Ok(py.None())
}

#[inline]
pub(crate) fn convert_native_to_py(py: Python, value: Value) -> PyResult<PyObject> {
    match value {
        Value::Int(val) => convert_to_py_int(py, val),
        Value::Float(val) => convert_to_py_float(py, val),
        Value::Boolean(val) => convert_to_py_bool(py, val),
        Value::String(val) => convert_to_py_string(py, val),
        Value::Tuple(val) => convert_to_py_tuple(py, val),
        Value::Empty => convert_to_py_none(py),
    }
}

// Now refactor the existing functions to use the new conversion functions
#[inline]
pub(crate) fn convert_to_eval_int_result(py: Python, value: i64) -> PyResult<Py<ExprEvalIntResult>> {
    let py_value = convert_to_py_int(py, value)?;
    Py::new(
        py,
        (
            ExprEvalIntResult {},
            ExprEvalResult {
                value: py_value,
                _type: PyType::new::<PyInt>(py).into(),
            },
        ),
    )
}

#[inline]
pub(crate) fn convert_to_eval_float_result(py: Python, value: f64) -> PyResult<Py<ExprEvalFloatResult>> {
    let py_value = convert_to_py_float(py, value)?;
    Py::new(
        py,
        (
            ExprEvalFloatResult {},
            ExprEvalResult {
                value: py_value,
                _type: PyType::new::<PyFloat>(py).into(),
            },
        ),
    )
}

#[inline]
pub(crate) fn convert_to_eval_bool_result(py: Python, value: bool) -> PyResult<Py<ExprEvalBoolResult>> {
    let py_value = convert_to_py_bool(py, value)?;
    Py::new(
        py,
        (
            ExprEvalBoolResult {},
            ExprEvalResult {
                value: py_value,
                _type: PyType::new::<PyBool>(py).into(),
            },
        ),
    )
}

#[inline]
pub(crate) fn convert_to_eval_string_result(py: Python, value: String) -> PyResult<Py<ExprEvalStringResult>> {
    let py_value = convert_to_py_string(py, value)?;
    Py::new(
        py,
        (
            ExprEvalStringResult {},
            ExprEvalResult {
                value: py_value,
                _type: PyType::new::<PyString>(py).into(),
            },
        ),
    )
}

#[inline]
pub(crate) fn convert_to_eval_tuple_result(py: Python, value: TupleType) -> PyResult<Py<ExprEvalTupleResult>> {
    let py_value = convert_to_py_tuple(py, value)?;
    Py::new(
        py,
        (
            ExprEvalTupleResult {},
            ExprEvalResult {
                value: py_value,
                _type: PyType::new::<PyTuple>(py).into(),
            },
        ),
    )
}

#[inline]
pub(crate) fn convert_to_eval_none_result(py: Python) -> PyResult<Py<ExprEvalNoneResult>> {
    let py_value = convert_to_py_none(py)?;
    Py::new(
        py,
        (
            ExprEvalNoneResult {},
            ExprEvalResult {
                value: py_value,
                _type: PyType::new::<PyNone>(py).into(),
            },
        ),
    )
}

#[inline]
pub(crate) fn convert_to_eval_result(py: Python, value: Value) -> PyResult<PyObject> {
    match value {
        Value::Int(val) => Ok(convert_to_eval_int_result(py, val)?.into_any()),
        Value::Float(val) => Ok(convert_to_eval_float_result(py, val)?.into_any()),
        Value::Boolean(val) => Ok(convert_to_eval_bool_result(py, val)?.into_any()),
        Value::String(val) => Ok(convert_to_eval_string_result(py, val)?.into_any()),
        Value::Tuple(val) => Ok(convert_to_eval_tuple_result(py, val)?.into_any()),
        Value::Empty => Ok(convert_to_eval_none_result(py)?.into_any()),
    }
}

#[inline]
pub(crate) fn convert_py_to_native(py: Python, value: Py<PyAny>) -> Value<DefaultNumericTypes> {
    let py_any = value.bind(py);

    if py_any.is_none() {
        return Value::Empty;
    }

    if py_any.is_instance_of::<PyBool>() {
        return Value::Boolean(py_any.extract::<bool>().unwrap());
    }

    if py_any.is_instance_of::<PyFloat>() {
        return Value::Float(py_any.extract::<f64>().unwrap());
    }

    if py_any.is_instance_of::<PyInt>() {
        return Value::Int(py_any.extract::<i64>().unwrap());
    }

    if py_any.is_instance_of::<PyString>() {
        return Value::String(py_any.extract::<String>().unwrap());
    }

    if py_any.is_instance_of::<PyTuple>() {
        let tuple = py_any.downcast::<PyTuple>().unwrap();
        let elements: Vec<Value<DefaultNumericTypes>> = tuple
            .iter()
            .map(|item| {
                let py_obj = Py::from(item);
                convert_py_to_native(py, py_obj)
            })
            .collect();
        return Value::Tuple(elements);
    }

    // If all conversions fail, return Empty
    Value::Empty
}
