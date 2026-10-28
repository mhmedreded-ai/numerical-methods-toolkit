"""
Secant Method (طريقة القاطع) for Root-Finding.

Theory & Mathematical Background:
    The Secant method approximates the derivative f'(x_n) in the Newton-Raphson formula
    using the finite backward difference quotient between two successive estimates x_{n-1} and x_n:
        f'(x_n) ≈ (f(x_n) - f(x_{n-1})) / (x_n - x_{n-1})

    Substituting this into the Newton-Raphson update yields the Secant formula:
        x_{n+1} = x_n - f(x_n) * (x_n - x_{n-1}) / (f(x_n) - f(x_{n-1}))

Convergence & Characteristics:
    - Convergence Order: Superlinear with the Golden Ratio exponent φ ≈ 1.618.
    - Advantage: Derivative-free (does not require analytical or symbolic differentiation).
    - Requirements: Requires two distinct initial estimates x0 and x1, but does not
      require them to bracket the root.
    - Edge Cases & Hazards:
        1. Identical Function Values: If f(x_n) ≈ f(x_{n-1}), the denominator vanishes,
           causing division by zero.
        2. Sensitivity to Initial Estimates: Bad guesses can lead to divergence or slow cycles.
"""

from typing import Callable, Tuple, List, Dict, Any
import math
from math_utils import parse_math_expression

def secant(
    f: Callable[[float], float],
    x0: float,
    x1: float,
    tol: float = 1e-3,
    max_iter: int = 50
) -> Tuple[float, List[Dict[str, Any]], bool, str]:
    """Execute the Secant root-finding algorithm.

    Args:
        f (Callable[[float], float]): The mathematical function f(x).
        x0 (float): First initial guess point x_{n-1}.
        x1 (float): Second initial guess point x_n.
        tol (float, optional): Convergence tolerance. Defaults to 1e-3.
        max_iter (int, optional): Maximum iteration count. Defaults to 50.

    Returns:
        Tuple[float, List[Dict[str, Any]], bool, str]:
            - root: Approximated root value.
            - iterations: List of step dictionaries with keys:
                ('iter', 'x_prev', 'x_curr', 'x_next', 'fx_next', 'error').
            - converged: True if stopping criteria were met.
            - message: Explanatory status message.

    Raises:
        ValueError: If x0 == x1.
    """
    if x0 == x1:
        raise ValueError("يجب إدخال نقطتين مختلفتين (x0 != x1).")

    f0 = f(x0)
    f1 = f(x1)

    # Initial check if either point is an exact root
    if abs(f0) < 1e-12:
        return x0, [], True, f"النقطة x0 = {x0} هي جذر دقيق للمعادلة: f({x0}) = 0"
    if abs(f1) < 1e-12:
        return x1, [], True, f"النقطة x1 = {x1} هي جذر دقيق للمعادلة: f({x1}) = 0"

    iterations = []
    curr_x0 = x0
    curr_x1 = x1

    for i in range(1, max_iter + 1):
        f_curr0 = f(curr_x0)
        f_curr1 = f(curr_x1)

        denom = f_curr1 - f_curr0
        if abs(denom) < 1e-14:
            return curr_x1, iterations, False, "توقف: فرق قيم الدالة (f1 - f0) قريب جداً من الصفر، لا يمكن القسمة."

        x_next = curr_x1 - f_curr1 * (curr_x1 - curr_x0) / denom
        fx_next = f(x_next)
        err = abs(x_next - curr_x1)

        iterations.append({
            'iter': i,
            'x_prev': curr_x0,
            'x_curr': curr_x1,
            'x_next': x_next,
            'fx_next': fx_next,
            'error': err
        })

        # Divergence guard
        if math.isnan(x_next) or math.isinf(x_next) or abs(x_next) > 1e12:
            return curr_x1, iterations, False, "تنبيه: الطريقة تتباعد (Diverges)! تحقق من اختيار نقاط بداية أكثر ملاءمة."

        # Stopping criteria: residual is near zero or step distance is below tolerance
        if abs(fx_next) < tol or err < tol:
            return x_next, iterations, True, f"تم الوصول للجذر: x = {x_next:.6f} بعد {i} دورة (الخطأ = {err:.6e})"

        curr_x0 = curr_x1
        curr_x1 = x_next

    return curr_x1, iterations, False, f"تم الوصول للحد الأقصى للتكرارات ({max_iter}) دون الوصول للدقة المطلوبة."

def solve_secant() -> None:
    """Run an interactive CLI session for the Secant method."""
    print("\n" + "=" * 55)
    print("             طريقة القاطع (Secant Method)")
    print("=" * 55)

    try:
        expr_str = input("أدخل المعادلة بدلالة x (مثال: x^3 - x - 2 أو e^x - 3x): ").strip()
        if not expr_str:
            print("خطأ: لم يتم إدخال معادلة!")
            return

        expr, f, _ = parse_math_expression(expr_str)
        print(f"المعادلة المقبولة: f(x) = {expr}")

        x0 = float(input("أدخل النقطة الأولى (x0): "))
        x1 = float(input("أدخل النقطة الثانية (x1): "))

        tol_input = input("أدخل نسبة الخطأ المطلوبة (افتراضي 0.001): ").strip()
        tol = float(tol_input) if tol_input else 0.001

        max_iter_input = input("أقصى عدد تكرارات (افتراضي 50): ").strip()
        max_iter = int(max_iter_input) if max_iter_input else 50

        root, steps, conv, msg = secant(f, x0, x1, tol, max_iter)

        print("\n" + "-" * 75)
        print(f"{'Iter':<6}{'x_(n-1)':<14}{'x_n':<14}{'x_(n+1)':<14}{'f(x_(n+1))':<14}{'Error':<12}")
        print("-" * 75)

        for s in steps:
            print(f"{s['iter']:<6}{s['x_prev']:<14.5f}{s['x_curr']:<14.5f}{s['x_next']:<14.5f}{s['fx_next']:<14.5f}{s['error']:<12.6f}")

        print("-" * 75)
        prefix = "[+]" if conv else "[!]"
        print(f"{prefix} {msg}")

    except Exception as e:
        print(f"\nحدث خطأ: {e}")

if __name__ == "__main__":
    solve_secant()
