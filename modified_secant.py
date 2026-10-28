import math
from math_utils import parse_math_expression

def modified_secant(f, x0, delta=0.01, tol=1e-3, max_iter=50):
    """
    حل المعادلات غير الخطية باستخدام طريقة القاطع المعدلة (Modified Secant Method).
    Formula: x_{i+1} = x_i - (delta * x_i * f(x_i)) / (f(x_i + delta * x_i) - f(x_i))
    
    Args:
        f (callable): الدالة الرياضية المراد إيجاد جذرها.
        x0 (float): التخمين الابتدائي للجذر.
        delta (float): نسبة التغيير الجزئي (Perturbation Fraction).
        tol (float): نسبة الخطأ المقبولة للتوقف.
        max_iter (int): أقصى عدد من التكرارات المسموح به.
        
    Returns:
        tuple: (root, iterations_list, converged, message)
    """
    iterations = []
    
    if abs(delta) < 1e-15:
        return x0, iterations, False, "قيمة delta صغيرة جداً أو تساوي صفراً"
        
    f0 = f(x0)
    if abs(f0) < 1e-12:
        return x0, iterations, True, f"النقطة الابتدائية x0 = {x0} هي جذر دقيق للمعادلة: f({x0}) = 0"
        
    for i in range(1, max_iter + 1):
        # حساب التغير الجزئي h = delta * x_i (مع تجنب الصفر إذا كانت x_i = 0)
        h = delta * x0 if abs(x0) > 1e-12 else delta
        f_pert = f(x0 + h)
        denom = f_pert - f0
        
        if abs(denom) < 1e-14:
            return x0, iterations, False, "مقام قانون القاطع المعدل f(x+h) - f(x) يساوي صفراً، لا يمكن إكمال القسمة."
            
        x1 = x0 - (h * f0) / denom
        err = abs(x1 - x0)
        
        iterations.append({
            "iter": i,
            "xi": x0,
            "fxi": f0,
            "f_pert": f_pert,
            "x_next": x1,
            "err": err
        })
        
        if math.isnan(x1) or math.isinf(x1) or abs(x1) > 1e12:
            return x1, iterations, False, "النظام متباعد (Divergent)! قيم x تتزايد بشكل غير محدود."
            
        f1 = f(x1)
        if err < tol or abs(f1) < 1e-12:
            return x1, iterations, True, f"تم الحل بنجاح: الجذر التقريبي = {x1:.6f} بعد {i} دورة."
            
        x0 = x1
        f0 = f1
        
    return x0, iterations, False, f"تم الوصول للحد الأقصى للتكرارات ({max_iter}) دون الوصول للدقة المطلوبة. آخر قيمة: {x0:.6f}"

def solve_modified_secant():
    print("\n" + "=" * 55)
    print("      طريقة القاطع المعدلة (Modified Secant Method)")
    print("=" * 55)

    try:
        expr_str = input("أدخل المعادلة بدلالة x (مثال: x^3 - x - 2 أو e^x - 3x): ").strip()
        if not expr_str:
            print("خطأ: لم يتم إدخال معادلة!")
            return

        expr, f, _ = parse_math_expression(expr_str)
        print(f"المعادلة المقبولة: f(x) = {expr}")

        x0 = float(input("أدخل النقطة الابتدائية (x0): "))
        
        delta_input = input("أدخل نسبة التغيير delta (افتراضي 0.01): ").strip()
        delta = float(delta_input) if delta_input else 0.01

        tol_input = input("أدخل نسبة الخطأ المطلوبة (افتراضي 0.001): ").strip()
        tol = float(tol_input) if tol_input else 0.001

        max_iter_input = input("أقصى عدد تكرارات (افتراضي 50): ").strip()
        max_iter = int(max_iter_input) if max_iter_input else 50

        print("\n" + "-" * 85)
        print(f"{'Iter':<6}{'x_i':<14}{'f(x_i)':<14}{'f(x_i+dx_i)':<16}{'x_(i+1)':<14}{'Error':<12}")
        print("-" * 85)

        root, steps, converged, msg = modified_secant(f, x0, delta, tol, max_iter)
        for s in steps:
            print(f"{s['iter']:<6}{s['xi']:<14.5f}{s['fxi']:<14.5f}{s['f_pert']:<16.5f}{s['x_next']:<14.5f}{s['err']:<12.6f}")

        print("-" * 85)
        if converged:
            print(f"[+] {msg}")
        else:
            print(f"[!] {msg}")

    except Exception as e:
        print(f"\nحدث خطأ: {e}")

if __name__ == "__main__":
    solve_modified_secant()
