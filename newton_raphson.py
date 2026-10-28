import math
import sympy as sp
from math_utils import parse_math_expression

def solve_newton_raphson():
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

        def safe_df(val):
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

        # فحص إن كانت النقطة الابتدائية هي الحل بالفعل
        if abs(f(x0)) < 1e-12:
            print(f"\n[!] النقطة الابتدائية x0 = {x0} هي جذر دقيق للمعادلة: f({x0}) = 0")
            return

        print("\n" + "-" * 75)
        print(f"{'Iter':<6}{'x_n':<14}{'f(x_n)':<14}{'f\'(x_n)':<14}{'x_(n+1)':<14}{'Error':<12}")
        print("-" * 75)

        for i in range(1, max_iter + 1):
            fx = f(x0)
            dfx = safe_df(x0)

            if abs(dfx) < 1e-14:
                print("-" * 75)
                print(f"[!] خطأ: المشتقة تساوي صفراً عند x = {x0:.5f}. لا يمكن القسمة على الصفر!")
                return

            x1 = x0 - (fx / dfx)
            err = abs(x1 - x0)

            print(f"{i:<6}{x0:<14.5f}{fx:<14.5f}{dfx:<14.5f}{x1:<14.5f}{err:<12.6f}")

            # فحص التباعد الشديد
            if math.isnan(x1) or math.isinf(x1) or abs(x1) > 1e12:
                print("-" * 75)
                print("[!] النظام متباعد (Divergent)! قيم x تتزايد بشكل غير محدود.")
                return

            if err < tol or abs(f(x1)) < 1e-12:
                print("-" * 75)
                print(f"[+] تم الحل بنجاح: الجذر التقريبي = {x1:.6f} بعد {i} تكرار.")
                return

            x0 = x1

        print("-" * 75)
        print(f"[!] تم الوصول لأقصى تكرارات ({max_iter}) دون الوصول للدقة المطلوبة. آخر قيمة: {x0:.6f}")

    except Exception as e:
        print(f"\nحدث خطأ: {e}")

if __name__ == "__main__":
    solve_newton_raphson()
