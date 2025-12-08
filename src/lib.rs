mod context;
mod error_mapping;
mod evaluate_fns;
mod evaluate_with_context_fns;
mod evaluate_with_context_mut_fns;
mod remap;
mod result;

use pyo3::prelude::*;

#[pymodule(name = "natives")]
mod evalexpr_natives {
    use super::*;
    #[pymodule_init]

    fn init(m: &Bound<'_, PyModule>) -> PyResult<()> {
        let mod_name = "py_evalexpr.natives";
        m.setattr("__name__", mod_name)?;
        let all = m.getattr("__all__")?;
        // Bit of a hack to set the __name__ attribute of submodules, since pyo3 doesn't seem to do it correctly.
        // Re-evaluate this if we upgrade pyo3 as they may fix this in the future.
        for name in all.extract::<Vec<String>>()? {
            let sub_module = m.getattr(&name)?;
            sub_module.setattr("__name__", format!("{}.{}", mod_name, name))?;
        }
        Ok(())
    }

    #[pymodule_export]
    use evaluate_fns::evaluate;

    #[pymodule_export]
    use evaluate_with_context_fns::evaluate_with_context;

    #[pymodule_export]
    use evaluate_with_context_mut_fns::evaluate_with_context_mut;

    #[pymodule_export]
    use result::result;

    #[pymodule_export]
    use context::context;
}
