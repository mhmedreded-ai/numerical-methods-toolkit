import os
import subprocess
import sys

# ضمان أن مسار المجلد الحالي مضاف للمسارات المعتمدة
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from bisection import solve_bisection
from newton_raphson import solve_newton_raphson
from secant import solve_secant
from modified_secant import solve_modified_secant
from jacobi import solve_jacobi
from gauss_seidel import solve_gauss_seidel

def launch_gui():
    print("\nجارٍ فتح الواجهة الرسومية (GUI)...")
    try:
        app_path = os.path.join(BASE_DIR, "app.py")
        subprocess.Popen([sys.executable, app_path], cwd=BASE_DIR)
    except Exception as e:
        print(f"تعذر فتح الواجهة الرسومية: {e}")

def menu():
    while True:
        print("\n" + "=" * 50)
        print("     حاسبة طرق Math 3 (التحليل العددي الشامل)")
        print("=" * 50)
        print("1. Bisection Method (طريقة تنصيف الفترات)")
        print("2. Newton-Raphson Method (طريقة نيوتن-رافسون)")
        print("3. Secant Method (طريقة القاطع)")
        print("4. Modified Secant Method (طريقة القاطع المعدلة)")
        print("5. Jacobi Method (طريقة جاكوبي للأنظمة الخطية)")
        print("6. Gauss-Seidel Method (طريقة جاوس-سيدل)")
        print("7. تشغيل الواجهة الرسومية الحديثة (Launch GUI)")
        print("0. خروج")
        print("=" * 50)

        choice = input("اختر رقم الطريقة المطلوبة: ").strip()

        try:
            if choice == '1':
                solve_bisection()
            elif choice == '2':
                solve_newton_raphson()
            elif choice == '3':
                solve_secant()
            elif choice == '4':
                solve_modified_secant()
            elif choice == '5':
                solve_jacobi()
            elif choice == '6':
                solve_gauss_seidel()
            elif choice == '7':
                launch_gui()
            elif choice == '0':
                print("\nشكراً لاستخدامك حاسبة التحليل العددي. بالتوفيق!")
                break
            else:
                print("اختيار غير صحيح، يرجى إدخال رقم من 0 إلى 7.")
        except KeyboardInterrupt:
            print("\nتم إلغاء العملية بواسطة المستخدم.")
        except Exception as e:
            print(f"\nحدث خطأ غير متوقع: {e}")

if __name__ == "__main__":
    menu()
