import os
import sys
import math

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import customtkinter as ctk
import sympy as sp
import tkinter as tk
from tkinter import ttk
from math_utils import parse_math_expression, make_diagonally_dominant

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class NumericalApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Math 3 - Numerical Analysis Suite (التحليل العددي)")
        self.geometry("980x780")
        self.minsize(850, 650)

        # تهيئة ستايل الجداول Treeview لتتناغم مع الوضع الداكن
        self.setup_treeview_styles()

        # العنوان الرئيسي
        self.header = ctk.CTkLabel(
            self, 
            text="حاسبة طرق التحليل العددي المتكاملة (Math 3)", 
            font=("Segoe UI", 22, "bold")
        )
        self.header.pack(pady=(12, 4))

        # التبويبات الرئيسية (Tabs)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=15, pady=8, fill="both", expand=True)

        self.tab_roots = self.tabview.add("جذور المعادلات (Root Finding)")
        self.tab_linear = self.tabview.add("الأنظمة الخطية (Linear Systems)")

        self.setup_roots_tab()
        self.setup_linear_tab()

    def setup_treeview_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#23272e",
            foreground="#dcdfe4",
            rowheight=26,
            fieldbackground="#23272e",
            font=("Segoe UI", 10)
        )
        style.configure(
            "Treeview.Heading",
            background="#1f538d",
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief="flat"
        )
        style.map(
            "Treeview",
            background=[("selected", "#2a5d9f")],
            foreground=[("selected", "#ffffff")]
        )

    # -------------------------------------------------------------
    # 1. تبويب جذور المعادلات (Bisection, Newton-Raphson, Secant)
    # -------------------------------------------------------------
    def setup_roots_tab(self):
        self.root_method_var = ctk.StringVar(value="Bisection")
        self.root_selector = ctk.CTkSegmentedButton(
            self.tab_roots, 
            values=["Bisection", "Newton-Raphson", "Secant"],
            variable=self.root_method_var,
            command=self.update_root_inputs,
            font=("Segoe UI", 13, "bold"),
            height=32
        )
        self.root_selector.pack(pady=8)

        input_frame = ctk.CTkFrame(self.tab_roots)
        input_frame.pack(pady=4, padx=12, fill="x")

        # شبكة المدخلات
        # المعادلة f(x)
        self.lbl_eq = ctk.CTkLabel(input_frame, text="المعادلة f(x):", font=("Segoe UI", 12, "bold"))
        self.lbl_eq.grid(row=0, column=3, padx=10, pady=6, sticky="e")
        self.entry_eq = ctk.CTkEntry(input_frame, placeholder_text="مثال: x^3 - x - 2 أو e^x - 3x", width=280)
        self.entry_eq.insert(0, "x^3 - x - 2")
        self.entry_eq.grid(row=0, column=2, padx=10, pady=6, sticky="w")

        # عرض المشتقة إن وجدت (لنيوتن)
        self.lbl_diff_info = ctk.CTkLabel(input_frame, text="", font=("Segoe UI", 11, "italic"), text_color="#3498db")
        self.lbl_diff_info.grid(row=0, column=0, columnspan=2, padx=10, pady=6, sticky="w")

        # المعامل الأول (a أو x0)
        self.lbl_p1 = ctk.CTkLabel(input_frame, text="بداية الفترة (a):", font=("Segoe UI", 12))
        self.lbl_p1.grid(row=1, column=3, padx=10, pady=4, sticky="e")
        self.entry_p1 = ctk.CTkEntry(input_frame, placeholder_text="1.0", width=120)
        self.entry_p1.insert(0, "1.0")
        self.entry_p1.grid(row=1, column=2, padx=10, pady=4, sticky="w")

        # المعامل الثاني (b أو x1)
        self.lbl_p2 = ctk.CTkLabel(input_frame, text="نهاية الفترة (b):", font=("Segoe UI", 12))
        self.lbl_p2.grid(row=2, column=3, padx=10, pady=4, sticky="e")
        self.entry_p2 = ctk.CTkEntry(input_frame, placeholder_text="2.0", width=120)
        self.entry_p2.insert(0, "2.0")
        self.entry_p2.grid(row=2, column=2, padx=10, pady=4, sticky="w")

        # نسبة الخطأ (Tol) وأقصى تكرارات
        self.lbl_tol = ctk.CTkLabel(input_frame, text="نسبة الخطأ (Tol):", font=("Segoe UI", 12))
        self.lbl_tol.grid(row=1, column=1, padx=10, pady=4, sticky="e")
        self.entry_tol = ctk.CTkEntry(input_frame, placeholder_text="0.001", width=100)
        self.entry_tol.insert(0, "0.001")
        self.entry_tol.grid(row=1, column=0, padx=10, pady=4, sticky="w")

        self.lbl_max_iter = ctk.CTkLabel(input_frame, text="أقصى تكرار:", font=("Segoe UI", 12))
        self.lbl_max_iter.grid(row=2, column=1, padx=10, pady=4, sticky="e")
        self.entry_max_iter = ctk.CTkEntry(input_frame, placeholder_text="50", width=100)
        self.entry_max_iter.insert(0, "50")
        self.entry_max_iter.grid(row=2, column=0, padx=10, pady=4, sticky="w")

        # زر الحساب
        self.btn_calc_roots = ctk.CTkButton(
            self.tab_roots, 
            text="احسب الحل الآن", 
            font=("Segoe UI", 13, "bold"),
            fg_color="#1f538d",
            hover_color="#14375e",
            height=34,
            command=self.calculate_roots
        )
        self.btn_calc_roots.pack(pady=6)

        # رسالة النتيجة
        self.res_roots = ctk.CTkLabel(self.tab_roots, text="", font=("Segoe UI", 13, "bold"), wraplength=850)
        self.res_roots.pack(pady=2)

        # إطار جدول التكرارات مع شريط التمرير Scrollbar
        tree_container = ctk.CTkFrame(self.tab_roots)
        tree_container.pack(fill="both", expand=True, padx=10, pady=4)

        self.roots_scroll = ttk.Scrollbar(tree_container, orient="vertical")
        self.tree_roots = ttk.Treeview(
            tree_container, 
            columns=("c1", "c2", "c3", "c4", "c5", "c6"), 
            show="headings", 
            yscrollcommand=self.roots_scroll.set
        )
        self.roots_scroll.config(command=self.tree_roots.yview)
        self.roots_scroll.pack(side="right", fill="y")
        self.tree_roots.pack(side="left", fill="both", expand=True)

        self.update_root_headings("Bisection")

    def update_root_headings(self, method):
        if method == "Bisection":
            cols = [
                ("c1", "الدورة", 70),
                ("c2", "a", 120),
                ("c3", "b", 120),
                ("c4", "c (المنتصف)", 140),
                ("c5", "f(c)", 140),
                ("c6", "الخطأ (Error)", 120)
            ]
        elif method == "Newton-Raphson":
            cols = [
                ("c1", "الدورة", 70),
                ("c2", "x_n", 130),
                ("c3", "f(x_n)", 130),
                ("c4", "f'(x_n)", 130),
                ("c5", "x_(n+1)", 140),
                ("c6", "الخطأ (Error)", 120)
            ]
        else: # Secant
            cols = [
                ("c1", "الدورة", 70),
                ("c2", "x_(n-1)", 130),
                ("c3", "x_n", 130),
                ("c4", "x_(n+1)", 140),
                ("c5", "f(x_(n+1))", 130),
                ("c6", "الخطأ (Error)", 120)
            ]

        for col_id, text, width in cols:
            self.tree_roots.heading(col_id, text=text)
            self.tree_roots.column(col_id, width=width, anchor="center")

    def update_root_inputs(self, choice):
        self.update_root_headings(choice)
        self.lbl_diff_info.configure(text="")
        if choice == "Bisection":
            self.lbl_p1.configure(text="بداية الفترة (a):")
            self.lbl_p2.configure(text="نهاية الفترة (b):")
            self.lbl_p2.grid()
            self.entry_p2.grid()
        elif choice == "Newton-Raphson":
            self.lbl_p1.configure(text="النقطة الابتدائية (x0):")
            self.lbl_p2.grid_remove()
            self.entry_p2.grid_remove()
        elif choice == "Secant":
            self.lbl_p1.configure(text="النقطة الأولى (x0):")
            self.lbl_p2.configure(text="النقطة الثانية (x1):")
            self.lbl_p2.grid()
            self.entry_p2.grid()

    def calculate_roots(self):
        for row in self.tree_roots.get_children():
            self.tree_roots.delete(row)
        self.res_roots.configure(text="")

        try:
            raw_eq = self.entry_eq.get()
            if not raw_eq.strip():
                self.res_roots.configure(text="خطأ: يرجى كتابة معادلة صحيحة!", text_color="#e74c3c")
                return

            expr, f, x_sym = parse_math_expression(raw_eq)
            tol = float(self.entry_tol.get())
            max_iter = int(self.entry_max_iter.get())
            method = self.root_method_var.get()

            # ---------------- Bisection ----------------
            if method == "Bisection":
                a = float(self.entry_p1.get())
                b = float(self.entry_p2.get())

                if a > b:
                    a, b = b, a
                    self.entry_p1.delete(0, "end")
                    self.entry_p1.insert(0, str(a))
                    self.entry_p2.delete(0, "end")
                    self.entry_p2.insert(0, str(b))
                elif a == b:
                    self.res_roots.configure(text="خطأ: بداية الفترة ونهايتها متطابقتان!", text_color="#e74c3c")
                    return

                fa = f(a)
                fb = f(b)

                if abs(fa) < 1e-12:
                    self.res_roots.configure(text=f"النقطة a = {a} هي جذر دقيق للمعادلة!", text_color="#2ecc71")
                    return
                if abs(fb) < 1e-12:
                    self.res_roots.configure(text=f"النقطة b = {b} هي جذر دقيق للمعادلة!", text_color="#2ecc71")
                    return

                if fa * fb > 0:
                    self.res_roots.configure(
                        text=f"خطأ: f({a})={fa:.4f} و f({b})={fb:.4f} لهما نفس الإشارة! شرط التغير في الإشارة غير محقق.",
                        text_color="#e74c3c"
                    )
                    return

                last_c = None
                for it in range(1, max_iter + 1):
                    c = (a + b) / 2.0
                    last_c = c
                    fc = f(c)
                    err = (b - a) / 2.0

                    self.tree_roots.insert("", "end", values=(it, f"{a:.5f}", f"{b:.5f}", f"{c:.6f}", f"{fc:.6f}", f"{err:.6f}"))

                    if abs(fc) < 1e-12 or err < tol:
                        self.res_roots.configure(text=f"تم الوصول للجذر التقريبي: {c:.6f} بعد {it} دورة (الخطأ: {err:.6f})", text_color="#2ecc71")
                        return

                    if fa * fc < 0:
                        b = c
                        fb = fc
                    else:
                        a = c
                        fa = fc

                self.res_roots.configure(text=f"وصل للحد الأقصى للتكرارات ({max_iter}) دون الوصول للدقة المطلوبة. آخر قيمة: {last_c:.6f}", text_color="#e67e22")

            # ---------------- Newton-Raphson ----------------
            elif method == "Newton-Raphson":
                diff_expr = sp.diff(expr, x_sym)
                df_num = sp.lambdify(x_sym, diff_expr, modules=['math'])
                self.lbl_diff_info.configure(text=f"المشتقة المحسوبة: f'(x) = {diff_expr}")

                def safe_df(val):
                    res = float(df_num(float(val)))
                    if math.isnan(res) or math.isinf(res):
                        raise ValueError("المشتقة غير معرفة")
                    return res

                x0 = float(self.entry_p1.get())
                if abs(f(x0)) < 1e-12:
                    self.res_roots.configure(text=f"النقطة الابتدائية x0 = {x0} هي جذر دقيق للمعادلة!", text_color="#2ecc71")
                    return

                for it in range(1, max_iter + 1):
                    fx = f(x0)
                    dfx = safe_df(x0)

                    if abs(dfx) < 1e-14:
                        self.res_roots.configure(text=f"خطأ: المشتقة تساوي صفراً عند x={x0:.5f}، لا يمكن القسمة عليها!", text_color="#e74c3c")
                        return

                    x1 = x0 - (fx / dfx)
                    err = abs(x1 - x0)

                    self.tree_roots.insert("", "end", values=(it, f"{x0:.5f}", f"{fx:.5f}", f"{dfx:.5f}", f"{x1:.6f}", f"{err:.6f}"))

                    if math.isnan(x1) or math.isinf(x1) or abs(x1) > 1e12:
                        self.res_roots.configure(text="النظام متباعد (Diverges)! قيم x تتزايد بشكل لا نهائي.", text_color="#e74c3c")
                        return

                    if err < tol or abs(f(x1)) < 1e-12:
                        self.res_roots.configure(text=f"تم الوصول للجذر التقريبي: {x1:.6f} بعد {it} دورة", text_color="#2ecc71")
                        return

                    x0 = x1

                self.res_roots.configure(text=f"وصل للحد الأقصى للتكرارات ({max_iter}) دون الوصول للدقة المطلوبة. آخر قيمة: {x0:.6f}", text_color="#e67e22")

            # ---------------- Secant ----------------
            elif method == "Secant":
                x0 = float(self.entry_p1.get())
                x1 = float(self.entry_p2.get())

                if x0 == x1:
                    self.res_roots.configure(text="خطأ: يجب إدخال نقطتين مختلفتين (x0 != x1)!", text_color="#e74c3c")
                    return

                f0 = f(x0)
                f1 = f(x1)

                if abs(f0) < 1e-12:
                    self.res_roots.configure(text=f"النقطة x0 = {x0} هي جذر دقيق للمعادلة!", text_color="#2ecc71")
                    return
                if abs(f1) < 1e-12:
                    self.res_roots.configure(text=f"النقطة x1 = {x1} هي جذر دقيق للمعادلة!", text_color="#2ecc71")
                    return

                for it in range(1, max_iter + 1):
                    denom = f1 - f0
                    if abs(denom) < 1e-14:
                        self.res_roots.configure(text="خطأ: مقام قانون القاطع (f1 - f0) يساوي صفراً!", text_color="#e74c3c")
                        return

                    x2 = x1 - f1 * (x1 - x0) / denom
                    f2 = f(x2)
                    err = abs(x2 - x1)

                    self.tree_roots.insert("", "end", values=(it, f"{x0:.5f}", f"{x1:.5f}", f"{x2:.6f}", f"{f2:.6f}", f"{err:.6f}"))

                    if math.isnan(x2) or math.isinf(x2) or abs(x2) > 1e12:
                        self.res_roots.configure(text="النظام متباعد (Diverges)! قيم x تتزايد بشكل لا نهائي.", text_color="#e74c3c")
                        return

                    if err < tol or abs(f2) < 1e-12:
                        self.res_roots.configure(text=f"تم الوصول للجذر التقريبي: {x2:.6f} بعد {it} دورة", text_color="#2ecc71")
                        return

                    x0, f0 = x1, f1
                    x1, f1 = x2, f2

                self.res_roots.configure(text=f"وصل للحد الأقصى للتكرارات ({max_iter}) دون الوصول للدقة المطلوبة. آخر قيمة: {x1:.6f}", text_color="#e67e22")

        except Exception as e:
            self.res_roots.configure(text=f"خطأ: {e}", text_color="#e74c3c")

    # -------------------------------------------------------------
    # 2. تبويب المصفوفات والأنظمة الخطية (Jacobi & Gauss-Seidel)
    # -------------------------------------------------------------
    def setup_linear_tab(self):
        self.linear_method_var = ctk.StringVar(value="Gauss-Seidel")
        self.linear_selector = ctk.CTkSegmentedButton(
            self.tab_linear,
            values=["Gauss-Seidel", "Jacobi"],
            variable=self.linear_method_var,
            font=("Segoe UI", 13, "bold"),
            height=32
        )
        self.linear_selector.pack(pady=8)

        info_frame = ctk.CTkFrame(self.tab_linear)
        info_frame.pack(pady=4, padx=12, fill="x")

        # إدخال المصفوفة A
        lbl_mat = ctk.CTkLabel(info_frame, text="مصفوفة المعاملات A (كل سطر يمثل معادلة، الأرقام مفصولة بمسافات):", font=("Segoe UI", 12, "bold"))
        lbl_mat.pack(anchor="e", padx=10, pady=(4, 0))
        self.txt_matrix = ctk.CTkTextbox(info_frame, height=75, font=("Consolas", 12))
        self.txt_matrix.insert("1.0", "4 1 -1\n2 7 1\n1 -3 12")
        self.txt_matrix.pack(fill="x", padx=10, pady=3)

        # صف المدخلات: b، التخمين الابتدائي، الدقة، والتكرار
        param_grid = ctk.CTkFrame(info_frame, fg_color="transparent")
        param_grid.pack(fill="x", padx=10, pady=4)

        lbl_b = ctk.CTkLabel(param_grid, text="الحدود المطلقة b:", font=("Segoe UI", 12))
        lbl_b.grid(row=0, column=5, padx=5, sticky="e")
        self.entry_b = ctk.CTkEntry(param_grid, placeholder_text="مثال: 3 19 31", width=140)
        self.entry_b.insert(0, "3 19 31")
        self.entry_b.grid(row=0, column=4, padx=5, sticky="w")

        lbl_x0 = ctk.CTkLabel(param_grid, text="التخمين X0 (اختياري):", font=("Segoe UI", 12))
        lbl_x0.grid(row=0, column=3, padx=5, sticky="e")
        self.entry_x0 = ctk.CTkEntry(param_grid, placeholder_text="افتراضي: 0 0 0", width=120)
        self.entry_x0.grid(row=0, column=2, padx=5, sticky="w")

        lbl_lin_tol = ctk.CTkLabel(param_grid, text="نسبة الخطأ:", font=("Segoe UI", 12))
        lbl_lin_tol.grid(row=0, column=1, padx=5, sticky="e")
        self.entry_lin_tol = ctk.CTkEntry(param_grid, width=75)
        self.entry_lin_tol.insert(0, "0.001")
        self.entry_lin_tol.grid(row=0, column=0, padx=5, sticky="w")

        # تنبيه السيادة القطرية
        self.lbl_dom_status = ctk.CTkLabel(self.tab_linear, text="", font=("Segoe UI", 11, "italic"), text_color="#3498db")
        self.lbl_dom_status.pack(pady=2)

        self.btn_calc_linear = ctk.CTkButton(
            self.tab_linear,
            text="حل النظام الخطي الآن",
            font=("Segoe UI", 13, "bold"),
            fg_color="#1f538d",
            hover_color="#14375e",
            height=34,
            command=self.calculate_linear
        )
        self.btn_calc_linear.pack(pady=4)

        self.res_linear = ctk.CTkLabel(self.tab_linear, text="", font=("Segoe UI", 13, "bold"), wraplength=850)
        self.res_linear.pack(pady=2)

        # جدول عرض نتائج المتغيرات مع Scrollbar
        linear_container = ctk.CTkFrame(self.tab_linear)
        linear_container.pack(fill="both", expand=True, padx=10, pady=4)

        self.linear_scroll = ttk.Scrollbar(linear_container, orient="vertical")
        self.tree_linear = ttk.Treeview(
            linear_container, 
            columns=("Iter", "Values", "Error"), 
            show="headings", 
            yscrollcommand=self.linear_scroll.set
        )
        self.linear_scroll.config(command=self.tree_linear.yview)
        self.linear_scroll.pack(side="right", fill="y")
        self.tree_linear.pack(side="left", fill="both", expand=True)

        self.tree_linear.heading("Iter", text="الدورة")
        self.tree_linear.heading("Values", text="قيم المجاهيل [x1, x2, x3, ...]")
        self.tree_linear.heading("Error", text="أقصى خطأ (Max Error)")
        self.tree_linear.column("Iter", width=80, anchor="center")
        self.tree_linear.column("Values", width=550, anchor="center")
        self.tree_linear.column("Error", width=160, anchor="center")

    def calculate_linear(self):
        for row in self.tree_linear.get_children():
            self.tree_linear.delete(row)
        self.res_linear.configure(text="")
        self.lbl_dom_status.configure(text="")

        try:
            # قراءة مصفوفة A
            raw_lines = self.txt_matrix.get("1.0", "end").strip().split("\n")
            A = [[float(val) for val in line.split()] for line in raw_lines if line.strip()]

            # قراءة مصفوفة b
            b = [float(val) for val in self.entry_b.get().strip().split()]
            tol = float(self.entry_lin_tol.get())
            method = self.linear_method_var.get()

            n = len(A)
            if n < 2:
                self.res_linear.configure(text="خطأ: يجب إدخال معادلتين على الأقل!", text_color="#e74c3c")
                return

            if n != len(b) or any(len(row) != n for row in A):
                self.res_linear.configure(
                    text=f"خطأ: أبعاد المصفوفة غير متطابقة! A تحتوي على {len(A)} أسطر، لكن الأسطر و متجه b يجب أن يكون لكل منها {n} عناصر.",
                    text_color="#e74c3c"
                )
                return

            # التخمين الابتدائي
            raw_x0 = self.entry_x0.get().strip()
            if raw_x0:
                x = [float(val) for val in raw_x0.split()]
                if len(x) != n:
                    self.res_linear.configure(text=f"خطأ: التخمين الابتدائي يجب أن يحتوي على {n} أرقام!", text_color="#e74c3c")
                    return
            else:
                x = [0.0] * n

            # التحقق من السيادة القطرية وإعادة الترتيب التلقائي
            A, b, is_dom, dom_msg = make_diagonally_dominant(A, b)
            self.lbl_dom_status.configure(text=f"[معاينة السيادة القطرية]: {dom_msg}")

            # التحقق من أن عناصر القطر الرئيسي لا تساوي صفراً
            for i in range(n):
                if abs(A[i][i]) < 1e-12:
                    self.res_linear.configure(text=f"خطأ: العنصر A[{i+1}][{i+1}] يساوي صفراً، لا يمكن القسمة عليه!", text_color="#e74c3c")
                    return

            for it in range(1, 101):
                x_old = list(x)
                if method == "Jacobi":
                    x_new = [0.0] * n
                    for i in range(n):
                        s = sum(A[i][j] * x_old[j] for j in range(n) if j != i)
                        x_new[i] = (b[i] - s) / A[i][i]
                    err = max(abs(x_new[i] - x_old[i]) for i in range(n))
                    x = x_new
                else:  # Gauss-Seidel
                    for i in range(n):
                        s = sum(A[i][j] * x[j] for j in range(n) if j != i)
                        x[i] = (b[i] - s) / A[i][i]
                    err = max(abs(x[i] - x_old[i]) for i in range(n))

                formatted_vals = "[" + ", ".join([f"{v:.5f}" for v in x]) + "]"
                self.tree_linear.insert("", "end", values=(it, formatted_vals, f"{err:.6f}"))

                # فحص التباعد
                if math.isnan(err) or math.isinf(err) or err > 1e12:
                    self.res_linear.configure(text="النظام متباعد (Diverges)! تأكد من تحقق شرط السيادة القطرية للمصفوفة.", text_color="#e74c3c")
                    return

                if err < tol:
                    self.res_linear.configure(text=f"تم الوصول للحل بنجاح: {formatted_vals} بعد {it} دورة", text_color="#2ecc71")
                    return

            self.res_linear.configure(text=f"وصل للحد الأقصى للتكرارات (100) دون الوصول للدقة المطلوبة. آخر قيم: {formatted_vals}", text_color="#e67e22")

        except Exception as e:
            self.res_linear.configure(text=f"خطأ في الإدخال: {e}", text_color="#e74c3c")

if __name__ == "__main__":
    app = NumericalApp()
    app.mainloop()
