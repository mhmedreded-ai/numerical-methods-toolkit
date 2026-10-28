"""
Bisection Method (طريقة تنصيف الفترات) for Root-Finding.

Theory & Mathematical Background:
    The Bisection method is a bracketing method rooted in Bolzano's Intermediate
    Value Theorem. If a continuous function f(x) satisfies f(a) * f(b) < 0 across
    the interval [a, b], at least one real root exists in (a, b).

    The method iteratively bisects the interval:
        c = (a + b) / 2
    and replaces either 'a' or 'b' based on the sign of f(c):
        - If f(a) * f(c) < 0, the root lies in [a, c] -> b = c.
        - Otherwise, the root lies in [c, b] -> a = c.

Convergence & Characteristics:
    - Convergence Order: Linear with rate O(2^(-n)).
    - Error Bound at step n: Error = (b - a) / (2^n).
    - Advantage: Absolutely guaranteed to converge if f(a) * f(b) < 0 and f is continuous.
    - Limitation: Slower than open methods (Newton-Raphson, Secant) and requires bracketing.
"""

from typing import Callable, Tuple, List, Dict, Any
from math_utils import parse_math_expression

def bisection(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-3,
    max_iter: int = 50
) -> Tuple[float, List[Dict[str, Any]], bool, str]:
    """Execute the Bisection algorithm on a callable numerical function f.

    Args:
        f (Callable[[float], float]): Continuous mathematical function f(x).
        a (float): Left boundary of the initial bracket interval.
        b (float): Right boundary of the initial bracket interval.
        tol (float, optional): Absolute error tolerance for convergence. Defaults to 1e-3.
        max_iter (int, optional): Maximum allowed iterations. Defaults to 50.

    Returns:
        Tuple[float, List[Dict[str, Any]], bool, str]:
            - root: Approximated root value.
            - iterations: List of iteration step dictionaries with keys:
                ('iter', 'a', 'b', 'c', 'fc', 'error').
            - converged: True if the stopping criteria were met.
            - message: Explanatory status message.

    Raises:
        ValueError: If a == b or if Bolzano's sign-change condition is violated (f(a)*f(b) > 0).
    """
    if a > b:
        a, b = b, a
    elif a == b:
        raise ValueError("بداية الفترة ونهايتها متطابقتان (a == b).")

    fa = f(a)
    fb = f(b)

    # Check if either boundary is already an exact root
    if abs(fa) < 1e-12:
        return a, [], True, f"النقطة a = {a} هي جذر دقيق للمعادلة: f({a}) = 0"
    if abs(fb) < 1e-12:
        return b, [], True, f"النقطة b = {b} هي جذر دقيق للمعادلة: f({b}) = 0"

    # Bolzano's condition: f(a) and f(b) must have opposite signs
    if fa * fb > 0:
        raise ValueError(f"f({a}) = {fa:.4f} و f({b}) = {fb:.4f} لهما نفس الإشارة! شرط الطريقة f(a)*f(b) < 0 غير محقق.")

    iterations = []
    c = (a + b) / 2.0

    for i in range(1, max_iter + 1):
        c = (a + b) / 2.0
        fc = f(c)
        err = (b - a) / 2.0

        iterations.append({
            'iter': i,
            'a': a,
            'b': b,
            'c': c,
            'fc': fc,
            'error': err
        })

        # Stopping criteria: residual is near zero or interval is smaller than tolerance
        if abs(fc) < 1e-12 or err < tol:
            return c, iterations, True, f"تم الوصول للجذر: c = {c:.6f} بعد {i} دورة (الخطأ = {err:.6e})"

        # Sub-interval selection
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    return c, iterations, False, f"تم الوصول للحد الأقصى للتكرارات ({max_iter}) دون الوصول للدقة المطلوبة."

def solve_bisection() -> None:
    """Run an interactive CLI session for the Bisection method."""
    print("\n" + "=" * 50)
    print("        طريقة تنصيف الفترات (Bisection Method)")
    print("=" * 50)

    try:
        expr_str = input("أدخل المعادلة بدلالة x (مثال: x^3 - x - 2 أو e^x - 3x): ").strip()
        if not expr_str:
            print("خطأ: لم يتم إدخال معادلة!")
            return

        expr, f, _ = parse_math_expression(expr_str)
        print(f"المعادلة المقبولة: f(x) = {expr}")

        a = float(input("أدخل بداية الفترة (a): "))
        b = float(input("أدخل نهاية الفترة (b): "))
        tol_input = input("أدخل نسبة الخطأ المطلوبة (افتراضي 0.001): ").strip()
        tol = float(tol_input) if tol_input else 0.001

        max_iter_input = input("أقصى عدد تكرارات (افتراضي 50): ").strip()
        max_iter = int(max_iter_input) if max_iter_input else 50

        root, steps, conv, msg = bisection(f, a, b, tol, max_iter)

        print("\n" + "-" * 75)
        print(f"{'Iter':<6}{'a':<12}{'b':<12}{'c (التقريب)':<16}{'f(c)':<16}{'Error':<12}")
        print("-" * 75)

        for step in steps:
            print(f"{step['iter']:<6}{step['a']:<12.5f}{step['b']:<12.5f}{step['c']:<16.6f}{step['fc']:<16.6f}{step['error']:<12.6f}")

        print("-" * 75)
        prefix = "[+]" if conv else "[!]"
        print(f"{prefix} {msg}")

    except Exception as e:
        print(f"\nحدث خطأ: {e}")

if __name__ == "__main__":
    solve_bisection()
