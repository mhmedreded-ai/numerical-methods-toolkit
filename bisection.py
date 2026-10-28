import math
from math_utils import parse_math_expression

def solve_bisection():
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

        # ضمان أن a < b
        if a > b:
            print(f"ملاحظة: تم تبديل الفترة لتصبح [{b}, {a}].")
            a, b = b, a
        elif a == b:
            print("خطأ: بداية الفترة ونهايتها متطابقتان!")
            return

        fa = f(a)
        fb = f(b)

        # التحقق من أن أحد الطرفين هو الجذر مباشرة
        if abs(fa) < 1e-12:
            print(f"\n[!] النقطة a = {a} هي جذر دقيق للمعادلة: f({a}) = {fa}")
            return
        if abs(fb) < 1e-12:
            print(f"\n[!] النقطة b = {b} هي جذر دقيق للمعادلة: f({b}) = {fb}")
            return

        # شرط بولزانو (تغير الإشارة)
        if fa * fb > 0:
            print(f"\nخطأ: f({a}) = {fa:.4f} و f({b}) = {fb:.4f} لهما نفس الإشارة!")
            print("شرط طريقة Bisection يتطلب وجود تغير في الإشارة f(a) * f(b) < 0.")
            return

        print("\n" + "-" * 75)
        print(f"{'Iter':<6}{'a':<12}{'b':<12}{'c (التقريب)':<16}{'f(c)':<16}{'Error':<12}")
        print("-" * 75)

        c_last = None
        for i in range(1, max_iter + 1):
            c = (a + b) / 2.0
            c_last = c
            fc = f(c)
            err = (b - a) / 2.0

            print(f"{i:<6}{a:<12.5f}{b:<12.5f}{c:<16.6f}{fc:<16.6f}{err:<12.6f}")

            if abs(fc) < 1e-12 or err < tol:
                print("-" * 75)
                print(f"[+] تم الوصول للحل: الجذر التقريبي = {c:.6f} بعد {i} تكرار (الخطأ = {err:.6f}).")
                return

            if fa * fc < 0:
                b = c
                fb = fc
            else:
                a = c
                fa = fc

        print("-" * 75)
        print(f"[!] تم الوصول لأقصى عدد تكرارات ({max_iter}). آخر تقريب للجذر: {c_last:.6f}")

    except Exception as e:
        print(f"\nحدث خطأ: {e}")

if __name__ == "__main__":
    solve_bisection()
