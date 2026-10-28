import math
from math_utils import make_diagonally_dominant

def solve_jacobi():
    print("\n" + "=" * 55)
    print("         طريقة جاكوبي (Jacobi Iteration Method)")
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
        if x0_str:
            x = list(map(float, x0_str.split()))
            if len(x) != n:
                print(f"خطأ: التخمين الابتدائي يجب أن يحتوي على {n} أرقام!")
                return
        else:
            x = [0.0] * n

        tol_input = input("أدخل نسبة الخطأ المطلوبة (افتراضي 0.001): ").strip()
        tol = float(tol_input) if tol_input else 0.001

        max_iter_input = input("أقصى عدد تكرارات (افتراضي 50): ").strip()
        max_iter = int(max_iter_input) if max_iter_input else 50

        # فحص السيادة القطرية وإعادة الترتيب إن لزم
        A, b, is_dom, dom_msg = make_diagonally_dominant(A, b)
        print(f"\n[معاينة السيادة القطرية]: {dom_msg}")

        # التحقق من خلو القطر من الأصفار
        for i in range(n):
            if abs(A[i][i]) < 1e-12:
                print(f"خطأ: العنصر A[{i+1}][{i+1}] يساوي صفراً، لا يمكن القسمة عليه!")
                return

        print("\n" + "-" * 70)
        print(f"{'Iter':<6}{'المتجه x':<45}{'Max Error':<15}")
        print("-" * 70)

        for it in range(1, max_iter + 1):
            x_new = [0.0] * n
            for i in range(n):
                s = sum(A[i][j] * x[j] for j in range(n) if j != i)
                x_new[i] = (b[i] - s) / A[i][i]

            err = max(abs(x_new[i] - x[i]) for i in range(n))
            x_formatted = "[" + ", ".join(f"{val:.5f}" for val in x_new) + "]"
            print(f"{it:<6}{x_formatted:<45}{err:<15.6f}")

            if math.isnan(err) or math.isinf(err) or err > 1e12:
                print("-" * 70)
                print("[!] النظام متباعد (Divergent)! فشلت طريقة جاكوبي في التقارب.")
                print("ملاحظة: تأكد من أن مصفوفة المعاملات تحقق شرط السيادة القطرية.")
                return

            if err < tol:
                print("-" * 70)
                print(f"[+] تم الحل بنجاح بعد {it} تكرار.")
                for i in range(n):
                    print(f"    x{i+1} = {x_new[i]:.6f}")
                return

            x = x_new

        print("-" * 70)
        print(f"[!] تم الوصول للحد الأقصى للتكرارات ({max_iter}). آخر قيم: {[round(val, 5) for val in x]}")

    except Exception as e:
        print(f"\nحدث خطأ: {e}")

if __name__ == "__main__":
    solve_jacobi()
