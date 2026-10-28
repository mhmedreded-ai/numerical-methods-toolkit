import math
import itertools
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor
)

TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application, convert_xor)
LOCAL_DICT = {
    'e': sp.E,
    'E': sp.E,
    'pi': sp.pi,
    'ln': sp.log
}

def parse_math_expression(expr_str: str):
    """
    يقوم بتحويل النص إلى تعبير رمزي SymPy ودالة عددية.
    يدعم الضرب الضمني مثل 2x، والأس ^، وثابت أويلر e.
    """
    clean_str = expr_str.strip()
    x = sp.Symbol('x')
    expr = parse_expr(clean_str, transformations=TRANSFORMATIONS, local_dict=LOCAL_DICT)
    
    # التأكد من أن التعبير لا يحتوي على متغيرات أخرى غير x
    free_vars = expr.free_symbols - {x}
    if free_vars:
        raise ValueError(f"تم العثور على رموز غير معروفة: {', '.join(str(s) for s in free_vars)} - يرجى استخدام المتغير x فقط.")
        
    f_num = sp.lambdify(x, expr, modules=['math'])
    
    def safe_f(val):
        try:
            res = float(f_num(float(val)))
            if math.isnan(res) or math.isinf(res):
                raise ValueError("قيمة غير معرفة أو غير منتهية")
            return res
        except (ValueError, OverflowError, ZeroDivisionError) as err:
            raise ValueError(f"خطأ رياضي عند حساب f({val}): {err}")
            
    return expr, safe_f, x

def check_diagonally_dominant(A):
    """
    يتحقق من الشرط الكافي لتقارب طرق التكرار (Jacobi & Gauss-Seidel):
    السيادة القطرية الصارمة أو الضعيفة.
    """
    n = len(A)
    strict = False
    for i in range(n):
        diag = abs(A[i][i])
        row_sum = sum(abs(A[i][j]) for j in range(n) if j != i)
        if diag < row_sum:
            return False, False  # ليست مهيمنة
        if diag > row_sum:
            strict = True
    return True, strict

def make_diagonally_dominant(A, b):
    """
    يحاول إعادة ترتيب صفوف المصفوفة A و b لتصبح مهيمنة قطرياً إن أمكن.
    """
    n = len(A)
    is_dom, is_strict = check_diagonally_dominant(A)
    if is_dom:
        desc = "المصفوفة مهيمنة قطرياً بشكل صارم" if is_strict else "المصفوفة مهيمنة قطرياً بشكل ضعيف"
        return A, b, True, desc

    # إذا كان الحجم صغيراً، نجرب التباديل
    if n <= 8:
        for p in itertools.permutations(range(n)):
            perm_A = [A[i] for i in p]
            dom, strict = check_diagonally_dominant(perm_A)
            if dom:
                perm_b = [b[i] for i in p]
                return perm_A, perm_b, True, "تمت إعادة ترتيب المعادلات تلقائياً لتحقيق السيادة القطرية"

    # طريقة جشعة لضمان عدم وجود أصفار على القطر على الأقل
    # محاولة تعيين الصف ذو المعامل الأكبر في العمود i للسطر i
    perm = [-1] * n
    used_rows = set()
    for col in range(n):
        best_row = -1
        best_val = -1.0
        for row in range(n):
            if row not in used_rows:
                val = abs(A[row][col])
                if val > best_val and val > 0:
                    best_val = val
                    best_row = row
        if best_row != -1:
            perm[col] = best_row
            used_rows.add(best_row)

    if len(used_rows) == n:
        new_A = [A[perm[i]] for i in range(n)]
        new_b = [b[perm[i]] for i in range(n)]
        dom, _ = check_diagonally_dominant(new_A)
        if dom:
            return new_A, new_b, True, "تمت إعادة ترتيب المعادلات لتحقيق السيادة القطرية"
        return new_A, new_b, False, "تم ترتيب المعادلات لتقليل أصفار القطر، لكن السيادة القطرية غير محققة بالكامل"

    return A, b, False, "تنبيه: المصفوفة ليست مهيمنة قطرياً، قد تتباعد الطريقة (Diverge)"
