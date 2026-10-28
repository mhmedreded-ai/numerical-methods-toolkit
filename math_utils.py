"""
Mathematical Utilities & Symbolic Expression Parsing Engine.

This module provides foundational helper functions used across the numerical
methods suite:
    1. Parsing arbitrary mathematical strings into symbolic expressions (SymPy)
       and safe callable numerical functions with domain validation.
    2. Evaluating strict and weak diagonal dominance of matrix systems.
    3. Applying heuristic and permutation-based row reordering to transform
       linear systems into diagonally dominant form for guaranteed iterative
       convergence (Jacobi and Gauss-Seidel).
"""

import math
import itertools
from typing import Tuple, Callable, Any, List
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor
)

# SymPy parsing transformation pipeline allowing natural human syntax
# e.g., implicit multiplication '2x', '3(x+1)', and caret '^' for exponentiation
TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application, convert_xor)

# Mapping standard mathematical constant aliases to SymPy equivalents
LOCAL_DICT = {
    'e': sp.E,
    'E': sp.E,
    'pi': sp.pi,
    'ln': sp.log
}

def parse_math_expression(expr_str: str) -> Tuple[sp.Expr, Callable[[float], float], sp.Symbol]:
    """Parse a user-supplied mathematical string into a SymPy expression and numerical callable.

    Supports implicit multiplication (e.g. '2x'), caret powers (e.g. 'x^3'),
    Euler's constant 'e', and transcendental functions ('sin', 'cos', 'exp', etc.).

    Args:
        expr_str (str): Raw mathematical formula string in terms of variable 'x'.

    Returns:
        Tuple[sp.Expr, Callable[[float], float], sp.Symbol]:
            - expr: The symbolic SymPy expression.
            - safe_f: A callable wrapper function f(val) returning float, with NaN/Inf guards.
            - x: The primary SymPy symbol object for 'x'.

    Raises:
        ValueError: If the expression string is empty, contains unrecognized free symbols
            other than 'x', or fails to parse syntactically.
    """
    clean_str = expr_str.strip()
    if not clean_str:
        raise ValueError("تعبير رياضي فارغ! يرجى إدخال معادلة صالحة بدلالة x.")

    x = sp.Symbol('x')
    expr = parse_expr(clean_str, transformations=TRANSFORMATIONS, local_dict=LOCAL_DICT)

    # Ensure no free symbols exist besides 'x'
    free_vars = expr.free_symbols - {x}
    if free_vars:
        symbol_list = ', '.join(str(s) for s in free_vars)
        raise ValueError(f"تم العثور على رموز غير معروفة: {symbol_list} - يرجى استخدام المتغير x فقط.")

    f_num = sp.lambdify(x, expr, modules=['math'])

    def safe_f(val: float) -> float:
        """Evaluate f(val) with floating-point safety and error interception."""
        try:
            res = float(f_num(float(val)))
            if math.isnan(res) or math.isinf(res):
                raise ValueError("قيمة غير معرفة أو غير منتهية (NaN / Infinity)")
            return res
        except (ValueError, OverflowError, ZeroDivisionError) as err:
            raise ValueError(f"خطأ رياضي عند حساب f({val}): {err}")

    return expr, safe_f, x

def check_diagonally_dominant(A: List[List[float]]) -> Tuple[bool, bool]:
    """Check whether matrix A satisfies diagonal dominance.

    A matrix A of size n x n is diagonally dominant if:
        |A[i][i]| >= sum(|A[i][j]| for j != i) for all i.
    It is strictly diagonally dominant if:
        |A[i][i]| > sum(|A[i][j]| for j != i) for all i.

    Strict diagonal dominance is a sufficient condition for the convergence of
    the Jacobi and Gauss-Seidel iterative methods.

    Args:
        A (List[List[float]]): Square coefficient matrix.

    Returns:
        Tuple[bool, bool]:
            - is_dominant: True if A is weakly or strictly diagonally dominant.
            - is_strict: True if strict inequality holds for all rows.
    """
    n = len(A)
    strict = True
    for i in range(n):
        diag = abs(A[i][i])
        row_sum = sum(abs(A[i][j]) for j in range(n) if j != i)
        if diag < row_sum:
            return False, False  # Violates diagonal dominance
        if diag == row_sum:
            strict = False

    return True, strict

def make_diagonally_dominant(A: List[List[float]], b: List[float]) -> Tuple[List[List[float]], List[float], bool, str]:
    """Reorder rows of linear system A x = b to achieve diagonal dominance if possible.

    Uses an exact permutation search for small systems (n <= 8) and a greedy
    pivot selection algorithm for larger matrices to minimize zero-diagonals.

    Args:
        A (List[List[float]]): Coefficient matrix.
        b (List[float]): Constant right-hand side vector.

    Returns:
        Tuple[List[List[float]], List[float], bool, str]:
            - new_A: Permuted coefficient matrix.
            - new_b: Permuted right-hand side vector.
            - success: True if strictly or weakly diagonally dominant.
            - message: Explanatory Arabic status message for UI/CLI feedback.
    """
    n = len(A)
    is_dom, is_strict = check_diagonally_dominant(A)
    if is_dom:
        desc = "المصفوفة مهيمنة قطرياً بشكل صارم" if is_strict else "المصفوفة مهيمنة قطرياً بشكل ضعيف"
        return A, b, True, desc

    # For small systems (n <= 8), perform exhaustive permutation search
    if n <= 8:
        for p in itertools.permutations(range(n)):
            perm_A = [A[i] for i in p]
            dom, strict = check_diagonally_dominant(perm_A)
            if dom:
                perm_b = [b[i] for i in p]
                return perm_A, perm_b, True, "تمت إعادة ترتيب المعادلات تلقائياً لتحقيق السيادة القطرية"

    # Greedy pivot matching to minimize zero-diagonals for larger systems
    perm = [-1] * n
    used_rows = set()
    for col in range(n):
        best_row = -1
        best_val = -1.0
        for row in range(n):
            if row not in used_rows:
                val = abs(A[row][col])
                if val > best_val and val > 0:
                    best_val = val
                    best_row = row
        if best_row != -1:
            perm[col] = best_row
            used_rows.add(best_row)

    if len(used_rows) == n:
        new_A = [A[perm[i]] for i in range(n)]
        new_b = [b[perm[i]] for i in range(n)]
        dom, _ = check_diagonally_dominant(new_A)
        if dom:
            return new_A, new_b, True, "تمت إعادة ترتيب المعادلات لتحقيق السيادة القطرية"
        return new_A, new_b, False, "تم ترتيب المعادلات لتقليل أصفار القطر، لكن السيادة القطرية غير محققة بالكامل"

    return A, b, False, "تنبيه: المصفوفة ليست مهيمنة قطرياً، قد تتباعد الطريقة (Diverge)"
