"""
Regression and Curve Fitting Module (الانحدار ومواءمة المنحنيات).

Theory & Mathematical Background:
    Curve fitting seeks an empirical functional relationship y ≈ f(x) that best describes
    a discrete dataset {(x_i, y_i)}_{i=1}^n under the Least-Squares criterion:
        Minimize S_r = sum_{i=1}^n (y_i - f(x_i))^2

Supported Models:
    1. Linear Regression:
       y = a_0 + a_1 * x
       Coefficients are directly computed from the 2x2 normal equations:
           a_1 = (n * sum(x*y) - sum(x)*sum(y)) / (n * sum(x^2) - (sum(x))^2)
           a_0 = mean(y) - a_1 * mean(x)

    2. Polynomial Regression (Degree m):
       y = a_0 + a_1 * x + a_2 * x^2 + ... + a_m * x^m
       Constructs the (m+1) x (m+1) symmetric Vandermonde-normal equations:
           sum_{k=0}^m [ a_k * sum(x_i^{j+k}) ] = sum(x_i^j * y_i)   for j = 0, ..., m
       and solves for coefficients [a_0, ..., a_m] using Gaussian elimination with
       partial row pivoting.

    3. Exponential Fitting:
       y = a * e^(b * x)
       Transformed logarithmically into linear form:
           ln(y) = ln(a) + b * x
       Requires all y_i > 0.

    4. Power Function Fitting:
       y = a * x^b
       Transformed logarithmically into linear form:
           ln(y) = ln(a) + b * ln(x)
       Requires all x_i > 0 and y_i > 0.

Statistical Metrics Computed:
    - S_t: Total sum of squares around the mean: sum((y_i - mean(y))^2).
    - S_r (SSE): Residual sum of squares: sum((y_i - y_pred_i)^2).
    - R^2: Coefficient of determination: (S_t - S_r) / S_t.
    - r: Correlation coefficient: sqrt(R^2).
    - S_{y/x}: Standard error of the estimate: sqrt(S_r / (n - (m + 1))).
"""

from typing import List, Tuple, Dict, Any, Callable, Union
import math

def solve_linear_system_gaussian(A: List[List[float]], b: List[float]) -> List[float]:
    """Solve linear system A * x = b using Gaussian elimination with partial pivoting.

    Args:
        A (List[List[float]]): Square coefficient matrix n x n.
        b (List[float]): Right-hand side vector of length n.

    Returns:
        List[float]: Unique solution vector x of length n.

    Raises:
        ValueError: If matrix A is singular or numerically rank-deficient.
    """
    n = len(A)
    # Construct augmented matrix [A | b]
    M = [row[:] + [b[i]] for i, row in enumerate(A)]

    for i in range(n):
        # Search for maximal pivot element in column i
        max_row = i
        max_val = abs(M[i][i])
        for k in range(i + 1, n):
            if abs(M[k][i]) > max_val:
                max_val = abs(M[k][i])
                max_row = k

        if max_val < 1e-14:
            raise ValueError("المصفوفة شاذة (Singular Matrix) ولا يمكن حل النظام الخطي.")

        M[i], M[max_row] = M[max_row], M[i]

        # Eliminate sub-diagonal entries
        for k in range(i + 1, n):
            factor = M[k][i] / M[i][i]
            for j in range(i, n + 1):
                M[k][j] -= factor * M[i][j]

    # Back-substitution
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = sum(M[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (M[i][n] - s) / M[i][i]

    return x

def compute_dense_curve(
    x_min: float,
    x_max: float,
    eval_func: Callable[[float], float],
    num_points: int = 200
) -> Tuple[List[float], List[float]]:
    """Generate high-density smooth points for accurate curve plotting.

    Args:
        x_min (float): Minimum X bound.
        x_max (float): Maximum X bound.
        eval_func (Callable[[float], float]): Mathematical prediction function.
        num_points (int, optional): Density count. Defaults to 200.

    Returns:
        Tuple[List[float], List[float]]: (x_dense, y_dense) coordinate lists.
    """
    if x_min == x_max:
        return [x_min], [eval_func(x_min)]
    step = (x_max - x_min) / (num_points - 1)
    x_dense = [x_min + i * step for i in range(num_points)]
    y_dense = []
    for xi in x_dense:
        try:
            yi = eval_func(xi)
            y_dense.append(yi)
        except Exception:
            y_dense.append(float('nan'))
    return x_dense, y_dense

def calculate_metrics(y_actual: List[float], y_pred: List[float], num_params: int) -> Dict[str, Any]:
    """Compute standard goodness-of-fit statistical indicators.

    Args:
        y_actual (List[float]): Actual observed target values.
        y_pred (List[float]): Fitted model predicted values.
        num_params (int): Number of estimated parameters in the model.

    Returns:
        Dict[str, Any]: Dictionary containing:
            - 'st': Total sum of squares.
            - 'sr': Residual sum of squares (SSE).
            - 'r2': Coefficient of determination R^2 in [0, 1].
            - 'r': Correlation coefficient.
            - 'syx': Standard error of the estimate S_{y/x}.
            - 'residuals': Residual differences list [y_i - y_pred_i].
    """
    n = len(y_actual)
    y_mean = sum(y_actual) / n
    st = sum((y - y_mean) ** 2 for y in y_actual)
    residuals = [y - yp for y, yp in zip(y_actual, y_pred)]
    sr = sum(e ** 2 for e in residuals)

    if st > 1e-14:
        r2 = max(0.0, min(1.0, 1.0 - (sr / st)))
    else:
        r2 = 1.0 if sr < 1e-14 else 0.0

    r = math.sqrt(r2)

    df = n - num_params
    if df > 0:
        syx = math.sqrt(max(0.0, sr / df))
    else:
        syx = 0.0

    return {
        "st": st,
        "sr": sr,
        "r2": r2,
        "r": r,
        "syx": syx,
        "residuals": residuals
    }

def linear_regression(x: List[float], y: List[float]) -> Dict[str, Any]:
    """Perform simple linear regression: y = a0 + a1 * x.

    Args:
        x (List[float]): Independent variable data points.
        y (List[float]): Dependent variable observations.

    Returns:
        Dict[str, Any]: Complete regression result dictionary with coefficients,
            equation string, metrics, and dense plotting coordinates.

    Raises:
        ValueError: If fewer than 2 points are provided or if all X values are identical.
    """
    n = len(x)
    if n < 2:
        raise ValueError("يلزم نقطتان على الأقل لحساب الانحدار الخطي.")

    sum_x = sum(x)
    sum_y = sum(y)
    sum_x2 = sum(xi ** 2 for xi in x)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))

    denom = n * sum_x2 - sum_x ** 2
    if abs(denom) < 1e-14:
        raise ValueError("جميع قيم X متطابقة، لا يمكن حساب الانحدار الخطي.")

    a1 = (n * sum_xy - sum_x * sum_y) / denom
    a0 = (sum_y - a1 * sum_x) / n

    def predict(val: float) -> float:
        return a0 + a1 * val

    y_pred = [predict(xi) for xi in x]
    metrics = calculate_metrics(y, y_pred, num_params=2)

    sign = "+" if a1 >= 0 else "-"
    eq_str = f"y = {a0:.5f} {sign} {abs(a1):.5f} * x"

    x_dense, y_dense = compute_dense_curve(min(x), max(x), predict)

    return {
        "method": "Linear",
        "method_name": "الانحدار الخطي (Linear Regression)",
        "equation": eq_str,
        "coefficients": [a0, a1],
        "coeff_labels": ["a0 (الثابت / Intercept)", "a1 (الميل / Slope)"],
        "y_pred": y_pred,
        "residuals": metrics["residuals"],
        "r2": metrics["r2"],
        "r": metrics["r"] if a1 >= 0 else -metrics["r"],
        "syx": metrics["syx"],
        "sr": metrics["sr"],
        "st": metrics["st"],
        "x_curve": x_dense,
        "y_curve": y_dense
    }

def polynomial_regression(x: List[float], y: List[float], degree: int = 2) -> Dict[str, Any]:
    """Fit a polynomial of arbitrary degree m: y = a0 + a1*x + ... + am*x^m.

    Args:
        x (List[float]): Independent variable data points.
        y (List[float]): Dependent variable observations.
        degree (int, optional): Polynomial degree m >= 1. Defaults to 2.

    Returns:
        Dict[str, Any]: Complete regression result dictionary.

    Raises:
        ValueError: If degree < 1 or if number of points n <= degree.
    """
    n = len(x)
    m = int(degree)
    if m < 1:
        raise ValueError("درجة كثير الحدود يجب أن تكون 1 على الأقل.")
    if n <= m:
        raise ValueError(f"عدد النقاط ({n}) يجب أن يكون أكبر من درجة كثير الحدود ({m}).")

    # Construct the (m+1) x (m+1) normal equations matrix
    M = [[0.0] * (m + 1) for _ in range(m + 1)]
    v = [0.0] * (m + 1)

    for j in range(m + 1):
        for k in range(m + 1):
            M[j][k] = sum(xi ** (j + k) for xi in x)
        v[j] = sum((xi ** j) * yi for xi, yi in zip(x, y))

    coeffs = solve_linear_system_gaussian(M, v)

    def predict(val: float) -> float:
        return sum(c * (val ** p) for p, c in enumerate(coeffs))

    y_pred = [predict(xi) for xi in x]
    metrics = calculate_metrics(y, y_pred, num_params=m + 1)

    terms = []
    for p, c in enumerate(coeffs):
        if p == 0:
            terms.append(f"{c:.5f}")
        elif p == 1:
            sign = "+" if c >= 0 else "-"
            terms.append(f"{sign} {abs(c):.5f}*x")
        else:
            sign = "+" if c >= 0 else "-"
            terms.append(f"{sign} {abs(c):.5f}*x^{p}")
    eq_str = "y = " + " ".join(terms)

    x_dense, y_dense = compute_dense_curve(min(x), max(x), predict)

    return {
        "method": "Polynomial",
        "method_name": f"انحدار متعدد الحدود من الدرجة {m} (Polynomial Degree {m})",
        "equation": eq_str,
        "degree": m,
        "coefficients": coeffs,
        "coeff_labels": [f"a{p}" for p in range(m + 1)],
        "y_pred": y_pred,
        "residuals": metrics["residuals"],
        "r2": metrics["r2"],
        "r": metrics["r"],
        "syx": metrics["syx"],
        "sr": metrics["sr"],
        "st": metrics["st"],
        "x_curve": x_dense,
        "y_curve": y_dense
    }

def exponential_regression(x: List[float], y: List[float]) -> Dict[str, Any]:
    """Fit an exponential model: y = a * e^(b * x) via logarithmic linearization.

    Linear transformation:
        ln(y) = ln(a) + b * x

    Args:
        x (List[float]): Independent variable data points.
        y (List[float]): Dependent variable observations (must all be > 0).

    Returns:
        Dict[str, Any]: Complete regression result dictionary.

    Raises:
        ValueError: If fewer than 2 points are provided, if any y_i <= 0,
            or if all X values are identical.
    """
    n = len(x)
    if n < 2:
        raise ValueError("يلزم نقطتان على الأقل لحساب المواءمة الأسية.")

    if any(yi <= 0 for yi in y):
        raise ValueError("المواءمة الأسية تتطلب أن تكون جميع قيم Y موجبة تماماً (Y > 0) لتطبيق اللوغاريتم الطبيعي.")

    ln_y = [math.log(yi) for yi in y]

    sum_x = sum(x)
    sum_lny = sum(ln_y)
    sum_x2 = sum(xi ** 2 for xi in x)
    sum_x_lny = sum(xi * lyi for xi, lyi in zip(x, ln_y))

    denom = n * sum_x2 - sum_x ** 2
    if abs(denom) < 1e-14:
        raise ValueError("جميع قيم X متطابقة، لا يمكن حساب المواءمة الأسية.")

    b = (n * sum_x_lny - sum_x * sum_lny) / denom
    ln_a = (sum_lny - b * sum_x) / n
    a = math.exp(ln_a)

    def predict(val: float) -> float:
        return a * math.exp(b * val)

    y_pred = [predict(xi) for xi in x]
    metrics = calculate_metrics(y, y_pred, num_params=2)

    eq_str = f"y = {a:.5f} * e^({b:.5f} * x)"
    x_dense, y_dense = compute_dense_curve(min(x), max(x), predict)

    return {
        "method": "Exponential",
        "method_name": "المواءمة الأسية (Exponential Fit: y = a*e^(bx))",
        "equation": eq_str,
        "coefficients": [a, b],
        "coeff_labels": ["a (المعامل الأساسي)", "b (معامل الأس)"],
        "y_pred": y_pred,
        "residuals": metrics["residuals"],
        "r2": metrics["r2"],
        "r": metrics["r"],
        "syx": metrics["syx"],
        "sr": metrics["sr"],
        "st": metrics["st"],
        "x_curve": x_dense,
        "y_curve": y_dense
    }

def power_regression(x: List[float], y: List[float]) -> Dict[str, Any]:
    """Fit a power model: y = a * x^b via logarithmic linearization.

    Linear transformation:
        ln(y) = ln(a) + b * ln(x)

    Args:
        x (List[float]): Independent variable data points (must all be > 0).
        y (List[float]): Dependent variable observations (must all be > 0).

    Returns:
        Dict[str, Any]: Complete regression result dictionary.

    Raises:
        ValueError: If fewer than 2 points are provided, if any x_i <= 0 or y_i <= 0,
            or if all ln(X) values are identical.
    """
    n = len(x)
    if n < 2:
        raise ValueError("يلزم نقطتان على الأقل لمواءمة دالة القوى.")

    if any(xi <= 0 for xi in x):
        raise ValueError("مواءمة دالة القوى تتطلب أن تكون جميع قيم X موجبة تماماً (X > 0).")
    if any(yi <= 0 for yi in y):
        raise ValueError("مواءمة دالة القوى تتطلب أن تكون جميع قيم Y موجبة تماماً (Y > 0).")

    ln_x = [math.log(xi) for xi in x]
    ln_y = [math.log(yi) for yi in y]

    sum_lnx = sum(ln_x)
    sum_lny = sum(ln_y)
    sum_lnx2 = sum(lx ** 2 for lx in ln_x)
    sum_lnx_lny = sum(lx * ly for lx, ly in zip(ln_x, ln_y))

    denom = n * sum_lnx2 - sum_lnx ** 2
    if abs(denom) < 1e-14:
        raise ValueError("جميع قيم ln(X) متطابقة، لا يمكن حساب مواءمة القوى.")

    b = (n * sum_lnx_lny - sum_lnx * sum_lny) / denom
    ln_a = (sum_lny - b * sum_lnx) / n
    a = math.exp(ln_a)

    def predict(val: float) -> float:
        return a * (val ** b)

    y_pred = [predict(xi) for xi in x]
    metrics = calculate_metrics(y, y_pred, num_params=2)

    eq_str = f"y = {a:.5f} * x^({b:.5f})"
    x_dense, y_dense = compute_dense_curve(min(x), max(x), predict)

    return {
        "method": "Power",
        "method_name": "مواءمة دالة القوى (Power Fit: y = a*x^b)",
        "equation": eq_str,
        "coefficients": [a, b],
        "coeff_labels": ["a (المعامل الأساسي)", "b (الأس / Power)"],
        "y_pred": y_pred,
        "residuals": metrics["residuals"],
        "r2": metrics["r2"],
        "r": metrics["r"],
        "syx": metrics["syx"],
        "sr": metrics["sr"],
        "st": metrics["st"],
        "x_curve": x_dense,
        "y_curve": y_dense
    }

def fit_curve(
    x: List[float],
    y: List[float],
    method: str = "linear",
    degree: int = 2
) -> Dict[str, Any]:
    """Unified dispatcher for all supported curve fitting models.

    Args:
        x (List[float]): X values.
        y (List[float]): Y values.
        method (str, optional): One of 'linear', 'polynomial', 'exponential', 'power'. Defaults to "linear".
        degree (int, optional): Polynomial degree if method is 'polynomial'. Defaults to 2.

    Returns:
        Dict[str, Any]: Complete regression result dictionary.

    Raises:
        ValueError: If an unrecognized method identifier is provided.
    """
    m = method.lower()
    if m in ["linear", "خطي"]:
        return linear_regression(x, y)
    elif m in ["polynomial", "متعدد الحدود"]:
        return polynomial_regression(x, y, degree=degree)
    elif m in ["exponential", "أسي", "اسي"]:
        return exponential_regression(x, y)
    elif m in ["power", "قوى"]:
        return power_regression(x, y)
    else:
        raise ValueError(f"طريقة غير معروفة: {method}. الطرق المتاحة: linear, polynomial, exponential, power.")

def solve_regression() -> None:
    """Run an interactive CLI session for curve fitting and regression."""
    print("\n" + "=" * 60)
    print("      الانحدار ومواءمة المنحنيات (Curve Fitting & Regression)")
    print("=" * 60)

    try:
        x_str = input("أدخل قيم X مفصولة بمسافات (مثال: 1 2 3 4 5): ").strip()
        y_str = input("أدخل قيم Y مفصولة بمسافات (مثال: 0.5 2.5 2.0 4.0 3.5): ").strip()

        x = [float(v) for v in x_str.replace(",", " ").split()]
        y = [float(v) for v in y_str.replace(",", " ").split()]

        if len(x) != len(y):
            print(f"خطأ: عدد قيم X ({len(x)}) لا يساوي عدد قيم Y ({len(y)})!")
            return

        print("\nاختر نموذج المواءمة:")
        print("1. Linear (خطي: y = a0 + a1*x)")
        print("2. Polynomial (متعدد الحدود: y = a0 + a1*x + ... + am*x^m)")
        print("3. Exponential (أسي: y = a * e^(b*x))")
        print("4. Power (دالة قوى: y = a * x^b)")

        choice = input("اختر رقم الطريقة (1-4): ").strip()
        if choice == "1":
            res = linear_regression(x, y)
        elif choice == "2":
            deg = int(input("أدخل درجة كثير الحدود (مثال: 2): ").strip() or "2")
            res = polynomial_regression(x, y, degree=deg)
        elif choice == "3":
            res = exponential_regression(x, y)
        elif choice == "4":
            res = power_regression(x, y)
        else:
            print("اختيار غير صحيح!")
            return

        print("\n" + "-" * 60)
        print(f"النموذج: {res['method_name']}")
        print(f"معادلة المنحنى: {res['equation']}")
        print(f"معامل التحديد (R^2): {res['r2']:.6f} ({res['r2']*100:.2f}%)")
        print(f"الخطأ المعياري للتقدير (Sy/x): {res['syx']:.6f}")
        print(f"مجموع مربعات البواقي (SSE / Sr): {res['sr']:.6f}")
        print("-" * 60)

        print(f"{'i':<4}{'X':<12}{'Y (Actual)':<14}{'Y (Pred)':<14}{'Residual (e)':<14}")
        print("-" * 60)
        for i, (xi, yi, yp, e) in enumerate(zip(x, y, res['y_pred'], res['residuals']), 1):
            print(f"{i:<4}{xi:<12.4f}{yi:<14.4f}{yp:<14.4f}{e:<14.4f}")
        print("-" * 60)

    except Exception as e:
        print(f"\nحدث خطأ: {e}")

if __name__ == "__main__":
    solve_regression()
