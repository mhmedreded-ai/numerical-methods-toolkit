"""
Newton-Raphson Method (طريقة نيوتن-رافسون) for Root-Finding.

Theory & Mathematical Background:
    The Newton-Raphson method is an open root-finding technique based on the first-order
    Taylor series expansion of f(x) around the current estimate x_n:
        f(x) ≈ f(x_n) + f'(x_n) * (x - x_n)

    Setting f(x) = 0 and solving for x gives the iterative tangent projection formula:
        x_{n+1} = x_n - f(x_n) / f'(x_n)

Convergence & Characteristics:
    - Convergence Order: Quadratic O(h^2) near simple roots. The number of correct decimal
      places approximately doubles with each iteration when starting sufficiently close.
    - Requirements: f(x) must be differentiable, and f'(x_n) != 0.
    - Edge Cases & Hazards:
        1. Zero Derivative: If f'(x_n) ≈ 0, the tangent line is horizontal and division by
           zero occurs.
        2. Inflection Points: Can cause oscillation or infinite cycles.
        3. Local Extrema: Can project the next estimate far away from the intended root.
"""

from typing import Callable, Tuple, List, Dict, Any
import math
import sympy as sp
from math_utils import parse_math_expression

def newton_raphson(
    f: Callable[[float], float],
    df: Callable[[float], float],
    x0: float,
    tol: float = 1e-3,
    max_iter: int = 50
) -> Tuple[float, List[Dict[str, Any]], bool, str]:
    """Execute the Newton-Raphson root-finding algorithm.

    Args:
        f (Callable[[float], float]): The objective function f(x).
        df (Callable[[float], float]): The derivative function f'(x).
        x0 (float): Initial guess for the root.
        tol (float, optional): Error tolerance for convergence. Defaults to 1e-3.
        max_iter (int, optional): Maximum allowed iterations. Defaults to 50.

    Returns:
        Tuple[float, List[Dict[str, Any]], bool, str]:
            - root: Approximated root value.
            - iterations: List of step dictionaries with keys:
                ('iter', 'xn', 'fx', 'dfx', 'x_next', 'error').
            - converged: True if stopping criteria were met.
            - message: Explanatory status message.

    Raises:
        ZeroDivisionError: If the derivative df(x) is zero at any iteration.
    """
    iterations = []
    current_x = x0

    # Initial check if x0 is already an exact root
    f0 = f(current_x)
    if abs(f0) < 1e-12:
        return current_x, [], True, f"النقطة الابتدائية x0 = {current_x} هي جذر دقيق للمعادلة: f({current_x}) = 0"

    for i in range(1, max_iter + 1):
        fx = f(current_x)
        dfx = df(current_x)

        # Zero derivative guard
        if abs(dfx) < 1e-14:
            return current_x, iterations, False, f"توقف: المشتقة تساوي صفراً عند x = {current_x:.5f}، لا يمكن إكمال القسمة."

        x_next = current_x - (fx / dfx)
        err = abs(x_next - current_x)

        iterations.append({
            'iter': i,
            'xn': current_x,
            'fx': fx,
            'dfx': dfx,
            'x_next': x_next,
            'error': err
        })

        # Divergence guard
        if math.isnan(x_next) or math.isinf(x_next) or abs(x_next) > 1e12:
            return current_x, iterations, False, "تنبيه: الطريقة تتباعد (Diverges)! تحقق من اختيار نقطة بداية أقرب للجذر."

        # Convergence criteria: function residual or step difference below tolerance
        if abs(f(x_next)) < tol or err < tol:
            return x_next, iterations, True, f"تم الوصول للجذر: x = {x_next:.6f} بعد {i} دورة (الخطأ = {err:.6e})"

        current_x = x_next

    return current_x, iterations, False, f"تم الوصول للحد الأقصى للتكرارات ({max_iter}) دون الوصول للدقة المطلوبة."

def solve_newton_raphson() -> None:
    """Run an interactive CLI session for the Newton-Raphson method."""
    print("\n" + "=" * 55)
    print("      طريقة نيوتن-رافسون (Newton-Raphson Method)")
    print("=" * 55)

    try:
        expr_str = input("أدخل المعادلة بدلالة x (مثال: x^3 - x - 2 أو cos(x) - x): ").strip()
        if not expr_str:
            print("خطأ: لم يتم إدخال معادلة!")
            return

        expr, f, x = parse_math_expression(expr_str)
        diff_expr = sp.diff(expr, x)
        df_num = sp.lambdify(x, diff_expr, modules=['math'])

        def safe_df(val: float) -> float:
            try:
                res = float(df_num(float(val)))
                if math.isnan(res) or math.isinf(res):
                    raise ValueError("المشتقة غير معرفة")
                return res
            except Exception as e:
                raise ValueError(f"خطأ في حساب المشتقة عند {val}: {e}")

        print(f"الدالة المقبولة:   f(x)  = {expr}")
        print(f"المشتقة المحسوبة: f'(x) = {diff_expr}")

        x0 = float(input("أدخل النقطة الابتدائية (x0): "))
        tol_input = input("أدخل نسبة الخطأ المطلوبة (افتراضي 0.001): ").strip()
        tol = float(tol_input) if tol_input else 0.001

        max_iter_input = input("أقصى عدد تكرارات (افتراضي 50): ").strip()
        max_iter = int(max_iter_input) if max_iter_input else 50

        root, steps, conv, msg = newton_raphson(f, safe_df, x0, tol, max_iter)

        print("\n" + "-" * 75)
        print(f"{'Iter':<6}{'x_n':<14}{'f(x_n)':<14}{'f\'(x_n)':<14}{'x_(n+1)':<14}{'Error':<12}")
        print("-" * 75)

        for s in steps:
            print(f"{s['iter']:<6}{s['xn']:<14.5f}{s['fx']:<14.5f}{s['dfx']:<14.5f}{s['x_next']:<14.5f}{s['error']:<12.6f}")

        print("-" * 75)
        prefix = "[+]" if conv else "[!]"
        print(f"{prefix} {msg}")

    except Exception as e:
        print(f"\nحدث خطأ: {e}")

if __name__ == "__main__":
    solve_newton_raphson()
