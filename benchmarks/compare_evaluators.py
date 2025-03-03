"""
Benchmark comparing various Python expression evaluation libraries.
"""

import time
import statistics
import os
from typing import Callable, Dict, List, Any

# Import libraries
import py_evalexpr
import sympy
import asteval
import simpleeval

# Disable debug output from py_evalexpr
os.environ["RUST_LOG"] = "error"


class BenchmarkResult:
    """Stores benchmark results for a single library."""

    def __init__(self, name: str):
        self.name = name
        self.times: Dict[str, List[float]] = {}

    def add_result(self, expr_name: str, execution_time: float):
        if expr_name not in self.times:
            self.times[expr_name] = []
        self.times[expr_name].append(execution_time)

    def get_median(self, expr_name: str) -> float:
        return statistics.median(self.times[expr_name])

    def get_overall_median(self) -> float:
        all_times = [time for times in self.times.values() for time in times]
        return statistics.median(all_times) if all_times else float("inf")


def time_execution(func: Callable, iterations: int = 1000) -> float:
    """Time the execution of a function over multiple iterations."""
    start_time = time.time()
    for _ in range(iterations):
        func()
    end_time = time.time()
    return (end_time - start_time) / iterations * 1000  # Convert to milliseconds


class PyEvalExprBenchmark:
    """Benchmark for PyEvalExpr library."""

    def __init__(self):
        self.context = py_evalexpr.ImmutableContext()
        self.context.variables["x"] = 5
        self.context.variables["y"] = 10
        self.context.variables["z"] = 15
        # sqrt is built-in to evalexpr

    def can_evaluate(self, expr_name: str, expr: str) -> bool:
        # PyEvalExpr doesn't support Python's conditional syntax
        # It can evaluate all of our test cases, including math functions with math:: prefix
        return True

    def evaluate(self, expr: str) -> Any:
        return self.context.evaluate(expr).value

    def get_expression(self, name: str) -> str:
        expressions = {
            "simple_arithmetic": "2 + 3 * 4",
            "complex_arithmetic": "(2 + 3) * 4 / (1 + 1)",
            "variables": "x + y * z",
            "math_functions": "math::sqrt(x*x + y*y)",
            "complex_expression": "(x + y) * (z - x) / (y + 2)",
            "boolean_logic": "x > y && y < z",
        }
        return expressions.get(name, "")


class SympyBenchmark:
    """Benchmark for SymPy library."""

    def __init__(self):
        self.symbols = {
            "x": sympy.Symbol("x"),
            "y": sympy.Symbol("y"),
            "z": sympy.Symbol("z"),
        }
        self.values = {"x": 5, "y": 10, "z": 15}

    def can_evaluate(self, expr_name: str, expr: str) -> bool:
        # SymPy doesn't handle boolean logic with relational operators well
        return "boolean_logic" not in expr_name and "?" not in expr

    def evaluate(self, expr: str) -> Any:
        parsed = sympy.sympify(expr, locals=self.symbols)
        return parsed.subs(self.values)

    def get_expression(self, name: str) -> str:
        expressions = {
            "simple_arithmetic": "2 + 3 * 4",
            "complex_arithmetic": "(2 + 3) * 4 / (1 + 1)",
            "variables": "x + y * z",
            "math_functions": "sqrt(x**2 + y**2)",
            "complex_expression": "(x + y) * (z - x) / (y + 2)",
            # Boolean logic doesn't work well in sympy with relational operators
        }
        return expressions.get(name, "")


class ASTEvalBenchmark:
    """Benchmark for ASTEval library."""

    def __init__(self):
        self.interpreter = asteval.Interpreter(use_numpy=False)
        self.interpreter.symtable["x"] = 5
        self.interpreter.symtable["y"] = 10
        self.interpreter.symtable["z"] = 15

    def can_evaluate(self, expr_name: str, expr: str) -> bool:
        return True  # ASTEval can handle all of our test cases with Python syntax

    def evaluate(self, expr: str) -> Any:
        return self.interpreter.eval(expr)

    def get_expression(self, name: str) -> str:
        expressions = {
            "simple_arithmetic": "2 + 3 * 4",
            "complex_arithmetic": "(2 + 3) * 4 / (1 + 1)",
            "variables": "x + y * z",
            "math_functions": "pow(x**2 + y**2, 0.5)",  # No built-in sqrt
            "complex_expression": "(x + y) * (z - x) / (y + 2)",
            "boolean_logic": "x > y and y < z",
        }
        return expressions.get(name, "")


class SimpleEvalBenchmark:
    """Benchmark for SimpleEval library."""

    def __init__(self):
        self.names = {"x": 5, "y": 10, "z": 15}
        self.functions = {"sqrt": lambda x: x**0.5}

    def can_evaluate(self, expr_name: str, expr: str) -> bool:
        return True  # SimpleEval can handle all of our test cases with Python syntax

    def evaluate(self, expr: str) -> Any:
        return simpleeval.simple_eval(expr, names=self.names, functions=self.functions)

    def get_expression(self, name: str) -> str:
        expressions = {
            "simple_arithmetic": "2 + 3 * 4",
            "complex_arithmetic": "(2 + 3) * 4 / (1 + 1)",
            "variables": "x + y * z",
            "math_functions": "sqrt(x**2 + y**2)",
            "complex_expression": "(x + y) * (z - x) / (y + 2)",
            "boolean_logic": "x > y and y < z",
        }
        return expressions.get(name, "")


def run_benchmarks(iterations: int = 50000) -> Dict[str, BenchmarkResult]:
    """Run benchmarks for all libraries."""

    # Test cases to benchmark
    benchmark_cases = [
        "simple_arithmetic",
        "complex_arithmetic",
        "variables",
        "math_functions",
        "complex_expression",
        "boolean_logic",
    ]

    # Initialize benchmarkers
    benchmarkers = {
        "py_evalexpr": PyEvalExprBenchmark(),
        "sympy": SympyBenchmark(),
        "asteval": ASTEvalBenchmark(),
        "simpleeval": SimpleEvalBenchmark(),
    }

    # Initialize results
    results = {name: BenchmarkResult(name) for name in benchmarkers}

    print(f"Running benchmarks with {iterations} iterations each...")

    # Run benchmarks for each test case
    for case in benchmark_cases:
        print(f"\nBenchmarking: {case}")

        for name, benchmarker in benchmarkers.items():
            expr = benchmarker.get_expression(case)
            if not expr:
                print(f"  {name}: Skipped - no suitable expression defined")
                continue

            if not benchmarker.can_evaluate(case, expr):
                print(f"  {name}: Skipped - not supported by this library")
                continue

            try:
                # Test that evaluation works
                benchmarker.evaluate(expr)

                # Measure performance
                time_taken = time_execution(
                    lambda: benchmarker.evaluate(expr), iterations
                )

                results[name].add_result(case, time_taken)
                print(f"  {name}: {time_taken:.4f} ms (expression: {expr})")

            except Exception as e:
                print(f"  {name}: Error - {str(e)}")

    return results


def print_summary(results: Dict[str, BenchmarkResult], benchmark_cases: List[str]):
    """Print a summary of benchmark results."""
    print("\n" + "=" * 80)
    print("BENCHMARK SUMMARY")
    print("=" * 80)

    for case in benchmark_cases:
        print(f"\nCase: {case}")
        print("-" * 60)

        # Sort libraries by median execution time
        sorted_libs = sorted(
            [lib for lib in results.keys() if case in results[lib].times],
            key=lambda lib: results[lib].get_median(case),
        )

        if sorted_libs:  # Check if any libraries succeeded for this case
            fastest_time = results[sorted_libs[0]].get_median(case)

            for lib in sorted_libs:
                median_time = results[lib].get_median(case)
                relative_speed = median_time / fastest_time
                print(f"{lib:20} {median_time:.4f} ms ({relative_speed:.2f}x)")
        else:
            print("No libraries successfully evaluated this case")

    print("\n" + "=" * 80)
    print("OVERALL PERFORMANCE (median across all cases)")
    print("=" * 80)

    # Get libraries that have results for at least one case
    libs_with_results = [lib for lib in results if results[lib].times]

    # Sort by mean of available results
    sorted_by_overall = sorted(
        libs_with_results, key=lambda lib: results[lib].get_overall_median()
    )

    if sorted_by_overall:
        fastest_overall = results[sorted_by_overall[0]].get_overall_median()

        for lib in sorted_by_overall:
            overall_median = results[lib].get_overall_median()
            relative_speed = overall_median / fastest_overall
            # Count how many cases this library completed
            case_count = len(results[lib].times)
            print(
                f"{lib:20} {overall_median:.4f} ms ({relative_speed:.2f}x) - {case_count}/{len(benchmark_cases)} cases"
            )
    else:
        print("No libraries have benchmark results.")


def generate_markdown_table(
    results: Dict[str, BenchmarkResult], benchmark_cases: List[str]
):
    """Generate a markdown table for the README."""
    print("\n\n## Benchmark Results for README")
    print("```markdown")
    print("## ⚡ Performance Benchmarks")
    print("")
    print(
        "PyEvalExpr was benchmarked against several popular Python expression evaluation libraries:"
    )
    print("")

    # Create header row
    libraries = ["py_evalexpr", "sympy", "asteval", "simpleeval"]
    header = "| Test Case | " + " | ".join(libraries) + " |"
    print(header)

    # Create separator row
    print("|------------|------------|--------|---------|------------|")

    # Add data rows
    for case in benchmark_cases:
        row = f"| {case} |"

        for lib in libraries:
            if case in results.get(lib, {}).times:
                median_time = results[lib].get_median(case)
                row += f" {median_time:.4f} ms |"
            else:
                row += " N/A |"

        print(row)

    print("")
    print(
        "*Benchmarks performed on AMD Ryzen 9 7950X with 32GB RAM running Python 3.11 using 50,000 iterations per test. Lower is better.*"
    )
    print("```")


def main():
    # Benchmark cases to test
    benchmark_cases = [
        "simple_arithmetic",
        "complex_arithmetic",
        "variables",
        "math_functions",
        "complex_expression",
        "boolean_logic",
    ]

    # Run benchmarks
    results = run_benchmarks(iterations=50000)

    # Print summary
    print_summary(results, benchmark_cases)

    # Generate markdown for README
    generate_markdown_table(results, benchmark_cases)


if __name__ == "__main__":
    main()
