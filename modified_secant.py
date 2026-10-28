"""
Modified Secant Method (طريقة القاطع المعدلة) for Root-Finding.

Theory & Mathematical Background:
    Rather than requiring two distinct estimates x_{n-1} and x_n as in the classical Secant
    method, the Modified Secant method introduces a small fractional perturbation parameter δ
    (typically δ ≈ 0.01) to estimate the derivative around a single initial value x_i:
        f'(x_i) ≈ (f(x_i + δ * x_i) - f(x_i)) / (δ * x_i)

    Substituting this approximation into the Newton-Raphson update yields:
        x_{i+1} = x_i - (δ * x_i * f(x_i)) / (f(x_i + δ * x_i) - f(x_i))

Convergence & Characteristics:
    - Convergence Order: Superlinear (approximately φ ≈ 1.618).
    - Advantage: Derivative-free and requires only a single starting point x0.
    - Zero Pivot Handling: When x_i ≈ 0, the perturbation step defaults to h = δ
      instead of δ * x_i to avoid a degenerate step size.
    - Stopping Criteria:
        1. |f(x_{i+1})| < tol (function residual threshold)
        2. |x_{i+1} - x_i| < tol (step difference threshold)
"""

from typing import Callable, Tuple, List, Dict, Any
import math
from math_utils import parse_math_expression

def modified_secant(
    f: Callable[[float], float],
    x0: float,
    delta: float = 0.01,
    tol: float = 1e-3,
    max_iter: int = 50
) -> Tuple[float, List[Dict[str, Any]], bool, str]:
    """Execute the Modified Secant root-finding algorithm with fractional perturbation.

    Args:
        f (Callable[[float], float]): Objective continuous function f(x).
        x0 (float): Initial single guess estimate for the root.
        delta (float, optional): Fractional perturbation fraction δ. Defaults to 0.01.
        tol (float, optional): Convergence tolerance. Defaults to 1e-3.
        max_iter (int, optional): Maximum iteration cutoff. Defaults to 50.

    Returns:
        Tuple[float, List[Dict[str, Any]], bool, str]:
            - root: Approximated root value.
            - iterations: List of step dictionaries with keys:
                ('iter', 'xi', 'fxi', 'f_pert', 'x_next', 'err').
            - converged: True if stopping criteria were met.
            - message: Explanatory status message.
    """
    iterations = []

    if abs(delta) < 1e-15:
        return x0, iterations, False, "قيمة delta صغيرة جداً أو تساوي صفراً."

    f0 = f(x0)
    if abs(f0) < 1e-12:
        return x0, iterations, True, f"النقطة الابتدائية x0 = {x0} هي جذر دقيق للمعادلة: f({x0}) = 0"

    current_x = x0
    current_f0 = f0

    for i in range(1, max_iter + 1):
        # Calculate step perturbation h = delta * x_i (handling x_i ≈ 0)
        h = delta * current_x if abs(current_x) > 1e-12 else delta
        f_pert = f(current_x + h)
        denom = f_pert - current_f0

        if abs(denom) < 1e-14:
            return current_x, iterations, False, "مقام قانون القاطع المعدل f(x+h) - f(x) يساوي صفراً، لا يمكن إكمال القسمة."

        x1 = current_x - (h * current_f0) / denom
        err = abs(x1 - current_x)

        iterations.append({
            "iter": i,
            "xi": current_x,
            "fxi": current_f0,
            "f_pert": f_pert,
            "x_next": x1,
            "err": err
        })

        if math.isnan(x1) or math.isinf(x1) or abs(x1) > 1e12:
            return x1, iterations, False, "النظام متباعد (Divergent)! قيم x تتزايد بشكل غير محدود."

        f1 = f(x1)
        if err < tol or abs(f1) < 1e-12:
            return x1, iterations, True, f"تم الحل بنجاح: الجذر التقريبي = {x1:.6f} بعد {i} دورة."

        current_x = x1
        current_f0 = f1

    return current_x, iterations, False, f"تم الوصول للحد الأقصى للتكرارات ({max_iter}) دون الوصول للدقة المطلوبة."

def solve_modified_secant() -> None:
    """Run an interactive CLI session for the Modified Secant method."""
    print("\n" + "=" * 60)
    print("      طريقة القاطع المعدلة (Modified Secant Method)")
    print("=" * 60)

    try:
        expr_str = input("أدخل المعادلة بدلالة x (مثال: x^3 - x - 2 أو e^x - 3x): ").strip()
        if not expr_str:
            print("خطأ: لم يتم إدخال معادلة!")
            return

        expr, f, _ = parse_math_expression(expr_str)
        print(f"المعادلة المقبولة: f(x) = {expr}")

        x0 = float(input("أدخل التخمين الابتدائي (x0): "))
        delta_str = input("أدخل نسبة الاضطراب delta (افتراضي 0.01): ").strip()
        delta = float(delta_str) if delta_str else 0.01

        tol_str = input("أدخل نسبة الخطأ المطلوبة (افتراضي 0.001): ").strip()
        tol = float(tol_str) if tol_str else 0.001

        max_iter_str = input("أقصى عدد تكرارات (افتراضي 50): ").strip()
        max_iter = int(max_iter_str) if max_iter_str else 50

        root, steps, conv, msg = modified_secant(f, x0, delta, tol, max_iter)

        print("\n" + "-" * 85)
        print(f"{'Iter':<6}{'x_i':<14}{'f(x_i)':<14}{'f(x_i + d*x_i)':<18}{'x_(i+1)':<14}{'Error':<12}")
        print("-" * 85)

        for step in steps:
            print(f"{step['iter']:<6}{step['xi']:<14.6f}{step['fxi']:<14.6e}{step['f_pert']:<18.6e}{step['x_next']:<14.6f}{step['err']:<12.6e}")

        print("-" * 85)
        prefix = "[+]" if conv else "[!]"
        print(f"{prefix} {msg}")

    except Exception as e:
        print(f"\nحدث خطأ: {e}")

if __name__ == "__main__":
    solve_modified_secant()
