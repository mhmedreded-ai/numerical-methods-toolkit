import math
from math_utils import parse_math_expression

def solve_secant():
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

        if x0 == x1:
            print("خطأ: يجب إدخال نقطتين مختلفتين (x0 != x1)!")
            return

        tol_input = input("أدخل نسبة الخطأ المطلوبة (افتراضي 0.001): ").strip()
        tol = float(tol_input) if tol_input else 0.001

        max_iter_input = input("أقصى عدد تكرارات (افتراضي 50): ").strip()
        max_iter = int(max_iter_input) if max_iter_input else 50

        f0 = f(x0)
        f1 = f(x1)

        if abs(f0) < 1e-12:
            print(f"\n[!] النقطة x0 = {x0} هي جذر دقيق للمعادلة: f({x0}) = 0")
            return
        if abs(f1) < 1e-12:
            print(f"\n[!] النقطة x1 = {x1} هي جذر دقيق للمعادلة: f({x1}) = 0")
            return

        print("\n" + "-" * 75)
        print(f"{'Iter':<6}{'x_(n-1)':<14}{'x_n':<14}{'x_(n+1)':<14}{'f(x_(n+1))':<14}{'Error':<12}")
        print("-" * 75)

        for i in range(1, max_iter + 1):
            denom = f1 - f0
            if abs(denom) < 1e-14:
                print("-" * 75)
                print("خطأ: فرق قيم الدالة (f1 - f0) يساوي صفراً، لا يمكن تطبيق قانون القاطع.")
                return

            x2 = x1 - f1 * (x1 - x0) / denom
            f2 = f(x2)
            err = abs(x2 - x1)

            print(f"{i:<6}{x0:<14.5f}{x1:<14.5f}{x2:<14.5f}{f2:<14.5f}{err:<12.6f}")

            if math.isnan(x2) or math.isinf(x2) or abs(x2) > 1e12:
                print("-" * 75)
                print("[!] النظام متباعد (Divergent)! قيم x تتزايد بشكل غير محدود.")
                return

            if err < tol or abs(f2) < 1e-12:
                print("-" * 75)
                print(f"[+] تم الحل بنجاح: الجذر التقريبي = {x2:.6f} بعد {i} تكرار.")
                return

            x0, f0 = x1, f1
            x1, f1 = x2, f2

        print("-" * 75)
        print(f"[!] تم الوصول لأقصى تكرارات ({max_iter}) دون الوصول للدقة المطلوبة. آخر قيمة: {x1:.6f}")

    except Exception as e:
        print(f"\nحدث خطأ: {e}")

if __name__ == "__main__":
    solve_secant()
