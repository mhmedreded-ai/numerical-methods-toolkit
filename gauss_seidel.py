"""
Gauss-Seidel Method (طريقة جاوس-سيدل) for Solving Linear Systems.

Theory & Mathematical Background:
    The Gauss-Seidel method is an iterative relaxation technique for solving A x = b.
    Unlike the Jacobi method (which updates all variables simultaneously from previous-step values),
    Gauss-Seidel incorporates the newly computed values x_j^{(k+1)} for j < i immediately
    into the ongoing evaluation of the remaining components:
        x_i^{(k+1)} = (1 / a_{ii}) * (b_i - sum_{j < i} (a_{ij} * x_j^{(k+1)}) - sum_{j > i} (a_{ij} * x_j^{(k)}))

Convergence & Characteristics:
    - Convergence Order: Linear, typically twice as fast as Jacobi for diagonally dominant
      or symmetric positive-definite (SPD) matrices.
    - Memory Efficiency: In-place state updates (only one vector of size n is required
      instead of two distinct previous/current vectors).
    - Convergence Conditions: Guaranteed to converge if:
        1. Matrix A is strictly diagonally dominant (|a_{ii}| > sum_{j != i} |a_{ij}|).
        2. Matrix A is symmetric and positive-definite (SPD).
    - Stopping Criteria:
        ||x^{(k+1)} - x^{(k)}||_∞ = max_i |x_i^{(k+1)} - x_i^{(k)}| < tol.
"""

from typing import List, Tuple, Dict, Any, Optional
import math
from math_utils import make_diagonally_dominant

def gauss_seidel(
    A: List[List[float]],
    b: List[float],
    x0: Optional[List[float]] = None,
    tol: float = 1e-3,
    max_iter: int = 50
) -> Tuple[List[float], List[Dict[str, Any]], bool, str]:
    """Solve the linear system A x = b using Gauss-Seidel successive displacements.

    Args:
        A (List[List[float]]): Square coefficient matrix of dimensions n x n.
        b (List[float]): Right-hand side constants vector of length n.
        x0 (Optional[List[float]], optional): Initial guess vector. Defaults to zeros [0.0]*n.
        tol (float, optional): Maximum norm error tolerance. Defaults to 1e-3.
        max_iter (int, optional): Maximum iteration cutoff. Defaults to 50.

    Returns:
        Tuple[List[float], List[Dict[str, Any]], bool, str]:
            - solution: Final estimated solution vector.
            - iterations: List of iteration step records containing:
                ('iter', 'x', 'error').
            - converged: True if error fell below tolerance.
            - message: Explanatory status message.

    Raises:
        ValueError: If matrix dimensions mismatch or if any diagonal element is zero.
    """
    n = len(A)
    if n < 2:
        raise ValueError("يجب أن يحتوي النظام على معادلتين على الأقل.")
    if n != len(b) or any(len(row) != n for row in A):
        raise ValueError("أبعاد المصفوفة A ومتجه الثوابت b غير متطابقة.")

    # Apply diagonal dominance permutation conditioning
    A_cond, b_cond, is_dom, dom_msg = make_diagonally_dominant(A, b)

    for i in range(n):
        if abs(A_cond[i][i]) < 1e-12:
            raise ValueError(f"العنصر القطري A[{i+1}][{i+1}] يساوي صفراً، لا يمكن القسمة عليه.")

    x = list(x0) if x0 is not None else [0.0] * n
    iterations = []

    for it in range(1, max_iter + 1):
        x_old = list(x)
        for i in range(n):
            s = sum(A_cond[i][j] * x[j] for j in range(n) if j != i)
            x[i] = (b_cond[i] - s) / A_cond[i][i]

        err = max(abs(x[i] - x_old[i]) for i in range(n))

        iterations.append({
            "iter": it,
            "x": list(x),
            "error": err
        })

        # Divergence guard
        if math.isnan(err) or math.isinf(err) or err > 1e12:
            return x, iterations, False, "النظام متباعد (Divergent)! تأكد من تحقق شرط السيادة القطرية."

        if err < tol:
            return x, iterations, True, f"تم الوصول للحل بنجاح بعد {it} دورة (الخطأ = {err:.6e})."

    return x, iterations, False, f"تم الوصول للحد الأقصى للتكرارات ({max_iter}) دون الوصول للدقة المطلوبة."

def solve_gauss_seidel() -> None:
    """Run an interactive CLI session for the Gauss-Seidel method."""
    print("\n" + "=" * 55)
    print("      طريقة جاوس-سيدل (Gauss-Seidel Method)")
    print("=" * 55)

    try:
        n = int(input("أدخل عدد المعادلات/المتغيرات (n): "))
        if n < 2:
            print("خطأ: يجب أن يكون عدد المعادلات 2 على الأقل!")
            return

        print(f"\nأدخل عناصر مصفوفة المعاملات A (صفاً بصف، كل صف به {n} أرقام مفصولة بمسافات):")
        A = []
        for i in range(n):
            row_vals = list(map(float, input(f"معاملات المعادلة {i+1}: ").split()))
            if len(row_vals) != n:
                print(f"خطأ: الصف يجب أن يحتوي على {n} أرقام بالضبط! أدخلت {len(row_vals)}.")
                return
            A.append(row_vals)

        print(f"\nأدخل متجه الحدود المطلقة b ({n} أرقام مفصولة بمسافات):")
        b = list(map(float, input("القيم: ").split()))
        if len(b) != n:
            print(f"خطأ: المتجه b يجب أن يحتوي على {n} أرقام بالضبط!")
            return

        x0_str = input(f"أدخل التخمين الابتدائي (اختياري، اضغط Enter للافتراضي أصفار [0]*{n}): ").strip()
        x0 = list(map(float, x0_str.split())) if x0_str else None

        tol_input = input("أدخل نسبة الخطأ المطلوبة (افتراضي 0.001): ").strip()
        tol = float(tol_input) if tol_input else 0.001

        max_iter_input = input("أقصى عدد تكرارات (افتراضي 50): ").strip()
        max_iter = int(max_iter_input) if max_iter_input else 50

        sol, steps, conv, msg = gauss_seidel(A, b, x0, tol, max_iter)

        print("\n" + "-" * 70)
        print(f"{'Iter':<6}{'المتجه x':<45}{'Max Error':<15}")
        print("-" * 70)

        for s in steps:
            formatted_vals = "[" + ", ".join([f"{v:.5f}" for v in s['x']]) + "]"
            print(f"{s['iter']:<6}{formatted_vals:<45}{s['error']:<15.6f}")

        print("-" * 70)
        prefix = "[+]" if conv else "[!]"
        print(f"{prefix} {msg}")

        if conv:
            print("\nقيم المجاهيل النهائية:")
            for idx, val in enumerate(sol, 1):
                print(f"x{idx} = {val:.6f}")

    except Exception as e:
        print(f"\nحدث خطأ: {e}")

if __name__ == "__main__":
    solve_gauss_seidel()
