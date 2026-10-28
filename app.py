"""
Math 3 - Numerical Analysis Desktop Application (CustomTkinter GUI).

This module implements the primary Graphical User Interface for the Math 3 numerical
analysis suite. Built using CustomTkinter, standard Tkinter Treeview widgets, and
embedded Matplotlib visualization canvases.

Application Architecture & Tab Organization:
    1. Root Finding Tab (جذور المعادلات):
       - Bisection Method
       - Newton-Raphson Method (with automatic symbolic derivative preview)
       - Secant Method
       - Modified Secant Method (with fractional perturbation δ)
       - Dynamic input fields, error handling, and scrollable Treeview iteration table.

    2. Linear Systems Tab (الأنظمة الخطية):
       - Jacobi Iteration Method
       - Gauss-Seidel Iteration Method
       - Automated diagonal dominance pre-conditioning detection and permutation.
       - Vector iteration grid and convergence status reporting.

    3. Curve Fitting & Regression Tab (الانحدار ومواءمة المنحنيات):
       - Linear, Polynomial (degree m), Exponential, and Power models.
       - Residual analysis table comparing observed Y vs predicted Y and error e_i.
       - Embedded local Matplotlib dark-themed plot comparing scatter points vs fitted curve.

Cross-Platform Compatibility:
    - Bidirectional Arabic text shaping via arabic-reshaper + python-bidi (ar() helper).
    - Dynamic font cascade (Segoe UI on Windows, Geeza Pro on macOS, Noto Sans / DejaVu on Linux).
    - Wayland / High-DPI screen scaling customization via CTK_SCALING environment variable.
"""

import os
import sys
import math

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# تهيئة الترميز للطرفية لدعم اللغة العربية بشكل سليم على أنظمة Windows و macOS و Linux
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# تهيئة مسار مكتبات Tk/Tcl الاحتياطية في حال تشغيل بيئة لينكس بدون تثبيت tk على مستوى النظام
if sys.platform.startswith("linux"):
    venv_lib = os.path.join(BASE_DIR, ".venv", "lib")
    if os.path.exists(os.path.join(venv_lib, "libtk8.6.so")):
        current_ld = os.environ.get("LD_LIBRARY_PATH", "")
        if venv_lib not in current_ld.split(":"):
            os.environ["LD_LIBRARY_PATH"] = f"{venv_lib}:{current_ld}" if current_ld else venv_lib
            os.environ["TCL_LIBRARY"] = os.path.join(venv_lib, "tcl8.6")
            os.environ["TK_LIBRARY"] = os.path.join(venv_lib, "tk8.6")
            if len(sys.argv) > 0 and sys.argv[0] != "-c":
                os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            os.environ.setdefault("TCL_LIBRARY", os.path.join(venv_lib, "tcl8.6"))
            os.environ.setdefault("TK_LIBRARY", os.path.join(venv_lib, "tk8.6"))

import customtkinter as ctk
import sympy as sp
import tkinter as tk
from tkinter import ttk
from math_utils import parse_math_expression, make_diagonally_dominant
import arabic_reshaper
from bidi.algorithm import get_display

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from regression import (
    linear_regression,
    polynomial_regression,
    exponential_regression,
    power_regression,
    fit_curve
)

def ar(text: str) -> str:
    """Reshape and reorder Arabic text for correct bidirectional rendering in Tkinter.

    Uses arabic-reshaper to connect glyphs according to Arabic orthography and
    python-bidi to order characters from right to left, preventing disjointed or
    reversed text on Linux/Wayland and across Tkinter platforms.

    Args:
        text (str): Input string containing Arabic, English, or mixed characters.

    Returns:
        str: Reshaped, correctly ordered string ready for Tkinter widgets.
    """
    if not text:
        return ""
    try:
        return get_display(arabic_reshaper.reshape(str(text)))
    except Exception:
        return str(text)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# إتاحة تجاوز مقياس الرسوميات لشاشات Wayland/Hyprland العالية الدقة
if "CTK_SCALING" in os.environ:
    try:
        scale_val = float(os.environ["CTK_SCALING"])
        ctk.set_widget_scaling(scale_val)
        ctk.set_window_scaling(scale_val)
    except ValueError:
        pass

class NumericalApp(ctk.CTk):
    """Main desktop application window for the Math 3 Numerical Analysis Suite.

    Inherits from CustomTkinter's ctk.CTk and orchestrates the user interface,
    styling, algorithm dispatch, and dynamic result rendering across the three
    main numerical domains:
        - Root Finding (Bisection, Newton-Raphson, Secant, Modified Secant).
        - Linear Systems (Jacobi, Gauss-Seidel).
        - Curve Fitting & Regression (Linear, Polynomial, Exponential, Power).
    """

    def __init__(self):
        """Initialize UI geometry, font cascade, theme, and tab components."""
        super().__init__()

        self.title("Math 3 - Numerical Analysis Suite (التحليل العددي)")
        self.geometry("1020x820")
        self.minsize(900, 700)

        # تحديد الخطوط المتوافقة تلقائياً (Segoe UI لويندوز، Geeza Pro لماك، Noto Sans/DejaVu للينكس)
        self.font_family = "Segoe UI"
        self.font_mono = "Consolas"
        try:
            import tkinter.font as tkfont
            available = set(tkfont.families(self))
            for cand in [
                "Segoe UI",
                "Noto Sans Arabic",
                "Geeza Pro",
                "Noto Sans",
                "DejaVu Sans",
                "Liberation Sans",
                "Arial"
            ]:
                if cand in available:
                    self.font_family = cand
                    break
            for mono_cand in [
                "Consolas",
                "Menlo",
                "DejaVu Sans Mono",
                "Liberation Mono",
                "Courier New",
                "monospace"
            ]:
                if mono_cand in available:
                    self.font_mono = mono_cand
                    break
        except Exception:
            pass

        # تهيئة ستايل الجداول Treeview لتتناغم مع الوضع الداكن
        self.setup_treeview_styles()

        # العنوان الرئيسي
        self.header = ctk.CTkLabel(
            self, 
            text=ar("حاسبة طرق التحليل العددي المتكاملة (Math 3)"), 
            font=(self.font_family, 22, "bold")
        )
        self.header.pack(pady=(12, 4))

        # التبويبات الرئيسية (Tabs)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=15, pady=8, fill="both", expand=True)

        self.tab_roots = self.tabview.add(ar("جذور المعادلات (Root Finding)"))
        self.tab_linear = self.tabview.add(ar("الأنظمة الخطية (Linear Systems)"))
        self.tab_regression = self.tabview.add(ar("الانحدار ومواءمة المنحنيات (Regression)"))

        self.setup_roots_tab()
        self.setup_linear_tab()
        self.setup_regression_tab()

    def setup_treeview_styles(self):
        """Configure dark-mode palette styling for ttk.Treeview data tables."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#23272e",
            foreground="#dcdfe4",
            rowheight=26,
            fieldbackground="#23272e",
            font=(self.font_family, 10)
        )
        style.configure(
            "Treeview.Heading",
            background="#1f538d",
            foreground="#ffffff",
            font=(self.font_family, 10, "bold"),
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
        """Construct the Root Finding GUI tab layout, inputs, and iteration table."""
        self.root_method_var = ctk.StringVar(value="Bisection")
        self.root_selector = ctk.CTkSegmentedButton(
            self.tab_roots, 
            values=["Bisection", "Newton-Raphson", "Secant", "Modified Secant"],
            variable=self.root_method_var,
            command=self.update_root_inputs,
            font=(self.font_family, 13, "bold"),
            height=32
        )
        self.root_selector.pack(pady=8)

        input_frame = ctk.CTkFrame(self.tab_roots)
        input_frame.pack(pady=4, padx=12, fill="x")

        # شبكة المدخلات
        # المعادلة f(x)
        self.lbl_eq = ctk.CTkLabel(input_frame, text=ar("المعادلة f(x):"), font=(self.font_family, 12, "bold"))
        self.lbl_eq.grid(row=0, column=3, padx=10, pady=6, sticky="e")
        self.entry_eq = ctk.CTkEntry(input_frame, placeholder_text=ar("مثال: x^3 - x - 2 أو e^x - 3x"), width=280)
        self.entry_eq.insert(0, "x^3 - x - 2")
        self.entry_eq.grid(row=0, column=2, padx=10, pady=6, sticky="w")

        # عرض المشتقة إن وجدت (لنيوتن)
        self.lbl_diff_info = ctk.CTkLabel(input_frame, text="", font=(self.font_family, 11, "italic"), text_color="#3498db")
        self.lbl_diff_info.grid(row=0, column=0, columnspan=2, padx=10, pady=6, sticky="w")

        # المعامل الأول (a أو x0)
        self.lbl_p1 = ctk.CTkLabel(input_frame, text=ar("بداية الفترة (a):"), font=(self.font_family, 12))
        self.lbl_p1.grid(row=1, column=3, padx=10, pady=4, sticky="e")
        self.entry_p1 = ctk.CTkEntry(input_frame, placeholder_text="1.0", width=120)
        self.entry_p1.insert(0, "1.0")
        self.entry_p1.grid(row=1, column=2, padx=10, pady=4, sticky="w")

        # المعامل الثاني (b أو x1 أو Delta)
        self.lbl_p2 = ctk.CTkLabel(input_frame, text=ar("نهاية الفترة (b):"), font=(self.font_family, 12))
        self.lbl_p2.grid(row=2, column=3, padx=10, pady=4, sticky="e")
        self.entry_p2 = ctk.CTkEntry(input_frame, placeholder_text="2.0", width=120)
        self.entry_p2.insert(0, "2.0")
        self.entry_p2.grid(row=2, column=2, padx=10, pady=4, sticky="w")

        # نسبة الخطأ (Tol) وأقصى تكرارات
        self.lbl_tol = ctk.CTkLabel(input_frame, text=ar("نسبة الخطأ (Tol):"), font=(self.font_family, 12))
        self.lbl_tol.grid(row=1, column=1, padx=10, pady=4, sticky="e")
        self.entry_tol = ctk.CTkEntry(input_frame, placeholder_text="0.001", width=100)
        self.entry_tol.insert(0, "0.001")
        self.entry_tol.grid(row=1, column=0, padx=10, pady=4, sticky="w")

        self.lbl_max_iter = ctk.CTkLabel(input_frame, text=ar("أقصى تكرار:"), font=(self.font_family, 12))
        self.lbl_max_iter.grid(row=2, column=1, padx=10, pady=4, sticky="e")
        self.entry_max_iter = ctk.CTkEntry(input_frame, placeholder_text="50", width=100)
        self.entry_max_iter.insert(0, "50")
        self.entry_max_iter.grid(row=2, column=0, padx=10, pady=4, sticky="w")

        # زر الحساب
        self.btn_calc_roots = ctk.CTkButton(
            self.tab_roots, 
            text=ar("احسب الحل الآن"), 
            font=(self.font_family, 13, "bold"),
            fg_color="#1f538d",
            hover_color="#14375e",
            height=34,
            command=self.calculate_roots
        )
        self.btn_calc_roots.pack(pady=6)

        # رسالة النتيجة
        self.res_roots = ctk.CTkLabel(self.tab_roots, text="", font=(self.font_family, 13, "bold"), wraplength=850)
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
        """Update Treeview column headers to match the active root-finding algorithm."""
        if method == "Bisection":
            cols = [
                ("c1", ar("الدورة"), 70),
                ("c2", "a", 120),
                ("c3", "b", 120),
                ("c4", ar("c (المنتصف)"), 140),
                ("c5", "f(c)", 140),
                ("c6", ar("الخطأ (Error)"), 120)
            ]
        elif method == "Newton-Raphson":
            cols = [
                ("c1", ar("الدورة"), 70),
                ("c2", "x_n", 130),
                ("c3", "f(x_n)", 130),
                ("c4", "f'(x_n)", 130),
                ("c5", "x_(n+1)", 140),
                ("c6", ar("الخطأ (Error)"), 120)
            ]
        elif method == "Modified Secant":
            cols = [
                ("c1", ar("الدورة"), 70),
                ("c2", "x_i", 120),
                ("c3", "f(x_i)", 130),
                ("c4", "f(x_i + \u03b4*x_i)", 150),
                ("c5", "x_(i+1)", 130),
                ("c6", ar("الخطأ (Error)"), 120)
            ]
        else: # Secant
            cols = [
                ("c1", ar("الدورة"), 70),
                ("c2", "x_(n-1)", 130),
                ("c3", "x_n", 130),
                ("c4", "x_(n+1)", 140),
                ("c5", "f(x_(n+1))", 130),
                ("c6", ar("الخطأ (Error)"), 120)
            ]

        for col_id, text, width in cols:
            self.tree_roots.heading(col_id, text=text)
            self.tree_roots.column(col_id, width=width, anchor="center")

    def update_root_inputs(self, choice):
        """Dynamically configure input field labels and defaults when switching root methods."""
        self.update_root_headings(choice)
        self.lbl_diff_info.configure(text="")
        if choice == "Bisection":
            self.lbl_p1.configure(text=ar("بداية الفترة (a):"))
            self.lbl_p2.configure(text=ar("نهاية الفترة (b):"))
            self.entry_p2.configure(placeholder_text="2.0")
            self.lbl_p2.grid()
            self.entry_p2.grid()
        elif choice == "Newton-Raphson":
            self.lbl_p1.configure(text=ar("النقطة الابتدائية (x0):"))
            self.lbl_p2.grid_remove()
            self.entry_p2.grid_remove()
        elif choice == "Secant":
            self.lbl_p1.configure(text=ar("النقطة الأولى (x0):"))
            self.lbl_p2.configure(text=ar("النقطة الثانية (x1):"))
            self.entry_p2.configure(placeholder_text="2.0")
            self.lbl_p2.grid()
            self.entry_p2.grid()
        elif choice == "Modified Secant":
            self.lbl_p1.configure(text=ar("النقطة الابتدائية (x0):"))
            self.lbl_p2.configure(text=ar("نسبة التغيير (Delta / \u03b4):"))
            self.entry_p2.delete(0, "end")
            self.entry_p2.insert(0, "0.01")
            self.entry_p2.configure(placeholder_text="0.01")
            self.lbl_p2.grid()
            self.entry_p2.grid()

    def calculate_roots(self):
        """Validate input parameters, execute the selected root solver, and display results."""
        for row in self.tree_roots.get_children():
            self.tree_roots.delete(row)
        self.res_roots.configure(text="")

        try:
            raw_eq = self.entry_eq.get()
            if not raw_eq.strip():
                self.res_roots.configure(text=ar("خطأ: يرجى كتابة معادلة صحيحة!"), text_color="#e74c3c")
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
                    self.res_roots.configure(text=ar("خطأ: بداية الفترة ونهايتها متطابقتان!"), text_color="#e74c3c")
                    return

                fa = f(a)
                fb = f(b)

                if abs(fa) < 1e-12:
                    self.res_roots.configure(text=ar(f"النقطة a = {a} هي جذر دقيق للمعادلة!"), text_color="#2ecc71")
                    return
                if abs(fb) < 1e-12:
                    self.res_roots.configure(text=ar(f"النقطة b = {b} هي جذر دقيق للمعادلة!"), text_color="#2ecc71")
                    return

                if fa * fb > 0:
                    self.res_roots.configure(
                        text=ar(f"خطأ: f({a})={fa:.4f} و f({b})={fb:.4f} لهما نفس الإشارة! شرط التغير في الإشارة غير محقق."),
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
                        self.res_roots.configure(text=ar(f"تم الوصول للجذر التقريبي: {c:.6f} بعد {it} دورة (الخطأ: {err:.6f})"), text_color="#2ecc71")
                        return

                    if fa * fc < 0:
                        b = c
                        fb = fc
                    else:
                        a = c
                        fa = fc

                self.res_roots.configure(text=ar(f"وصل للحد الأقصى للتكرارات ({max_iter}) دون الوصول للدقة المطلوبة. آخر قيمة: {last_c:.6f}"), text_color="#e67e22")

            # ---------------- Newton-Raphson ----------------
            elif method == "Newton-Raphson":
                diff_expr = sp.diff(expr, x_sym)
                df_num = sp.lambdify(x_sym, diff_expr, modules=['math'])
                self.lbl_diff_info.configure(text=ar(f"المشتقة المحسوبة: f'(x) = {diff_expr}"))

                def safe_df(val):
                    res = float(df_num(float(val)))
                    if math.isnan(res) or math.isinf(res):
                        raise ValueError(ar("المشتقة غير معرفة"))
                    return res

                x0 = float(self.entry_p1.get())
                if abs(f(x0)) < 1e-12:
                    self.res_roots.configure(text=ar(f"النقطة الابتدائية x0 = {x0} هي جذر دقيق للمعادلة!"), text_color="#2ecc71")
                    return

                for it in range(1, max_iter + 1):
                    fx = f(x0)
                    dfx = safe_df(x0)

                    if abs(dfx) < 1e-14:
                        self.res_roots.configure(text=ar(f"خطأ: المشتقة تساوي صفراً عند x={x0:.5f}، لا يمكن القسمة عليها!"), text_color="#e74c3c")
                        return

                    x1 = x0 - (fx / dfx)
                    err = abs(x1 - x0)

                    self.tree_roots.insert("", "end", values=(it, f"{x0:.5f}", f"{fx:.5f}", f"{dfx:.5f}", f"{x1:.6f}", f"{err:.6f}"))

                    if math.isnan(x1) or math.isinf(x1) or abs(x1) > 1e12:
                        self.res_roots.configure(text=ar("النظام متباعد (Diverges)! قيم x تتزايد بشكل لا نهائي."), text_color="#e74c3c")
                        return

                    if err < tol or abs(f(x1)) < 1e-12:
                        self.res_roots.configure(text=ar(f"تم الوصول للجذر التقريبي: {x1:.6f} بعد {it} دورة"), text_color="#2ecc71")
                        return

                    x0 = x1

                self.res_roots.configure(text=ar(f"وصل للحد الأقصى للتكرارات ({max_iter}) دون الوصول للدقة المطلوبة. آخر قيمة: {x0:.6f}"), text_color="#e67e22")

            # ---------------- Secant ----------------
            elif method == "Secant":
                x0 = float(self.entry_p1.get())
                x1 = float(self.entry_p2.get())

                if x0 == x1:
                    self.res_roots.configure(text=ar("خطأ: يجب إدخال نقطتين مختلفتين (x0 != x1)!"), text_color="#e74c3c")
                    return

                f0 = f(x0)
                f1 = f(x1)

                if abs(f0) < 1e-12:
                    self.res_roots.configure(text=ar(f"النقطة x0 = {x0} هي جذر دقيق للمعادلة!"), text_color="#2ecc71")
                    return
                if abs(f1) < 1e-12:
                    self.res_roots.configure(text=ar(f"النقطة x1 = {x1} هي جذر دقيق للمعادلة!"), text_color="#2ecc71")
                    return

                for it in range(1, max_iter + 1):
                    denom = f1 - f0
                    if abs(denom) < 1e-14:
                        self.res_roots.configure(text=ar("خطأ: مقام قانون القاطع (f1 - f0) يساوي صفراً!"), text_color="#e74c3c")
                        return

                    x2 = x1 - f1 * (x1 - x0) / denom
                    f2 = f(x2)
                    err = abs(x2 - x1)

                    self.tree_roots.insert("", "end", values=(it, f"{x0:.5f}", f"{x1:.5f}", f"{x2:.6f}", f"{f2:.6f}", f"{err:.6f}"))

                    if math.isnan(x2) or math.isinf(x2) or abs(x2) > 1e12:
                        self.res_roots.configure(text=ar("النظام متباعد (Diverges)! قيم x تتزايد بشكل لا نهائي."), text_color="#e74c3c")
                        return

                    if err < tol or abs(f2) < 1e-12:
                        self.res_roots.configure(text=ar(f"تم الوصول للجذر التقريبي: {x2:.6f} بعد {it} دورة"), text_color="#2ecc71")
                        return

                    x0, f0 = x1, f1
                    x1, f1 = x2, f2

                self.res_roots.configure(text=ar(f"وصل للحد الأقصى للتكرارات ({max_iter}) دون الوصول للدقة المطلوبة. آخر قيمة: {x1:.6f}"), text_color="#e67e22")

            # ---------------- Modified Secant ----------------
            elif method == "Modified Secant":
                x0 = float(self.entry_p1.get())
                delta_str = self.entry_p2.get().strip()
                delta = float(delta_str) if delta_str else 0.01

                if abs(delta) < 1e-15:
                    self.res_roots.configure(text=ar("خطأ: قيمة نسبة التغيير (Delta) صغيرة جداً أو تساوي صفراً!"), text_color="#e74c3c")
                    return

                f0 = f(x0)
                if abs(f0) < 1e-12:
                    self.res_roots.configure(text=ar(f"النقطة الابتدائية x0 = {x0} هي جذر دقيق للمعادلة!"), text_color="#2ecc71")
                    return

                for it in range(1, max_iter + 1):
                    h = delta * x0 if abs(x0) > 1e-12 else delta
                    f_pert = f(x0 + h)
                    denom = f_pert - f0

                    if abs(denom) < 1e-14:
                        self.res_roots.configure(text=ar("خطأ: مقام قانون القاطع المعدل f(x+h) - f(x) يساوي صفراً!"), text_color="#e74c3c")
                        return

                    x1 = x0 - (h * f0) / denom
                    err = abs(x1 - x0)

                    self.tree_roots.insert("", "end", values=(it, f"{x0:.5f}", f"{f0:.5f}", f"{f_pert:.5f}", f"{x1:.6f}", f"{err:.6f}"))

                    if math.isnan(x1) or math.isinf(x1) or abs(x1) > 1e12:
                        self.res_roots.configure(text=ar("النظام متباعد (Diverges)! قيم x تتزايد بشكل لا نهائي."), text_color="#e74c3c")
                        return

                    f_next = f(x1)
                    if err < tol or abs(f_next) < 1e-12:
                        self.res_roots.configure(text=ar(f"تم الوصول للجذر التقريبي: {x1:.6f} بعد {it} دورة (الخطأ: {err:.6f})"), text_color="#2ecc71")
                        return

                    x0 = x1
                    f0 = f_next

                self.res_roots.configure(text=ar(f"وصل للحد الأقصى للتكرارات ({max_iter}) دون الوصول للدقة المطلوبة. آخر قيمة: {x0:.6f}"), text_color="#e67e22")

        except Exception as e:
            self.res_roots.configure(text=ar(f"خطأ: {e}"), text_color="#e74c3c")

    # -------------------------------------------------------------
    # 2. تبويب المصفوفات والأنظمة الخطية (Jacobi & Gauss-Seidel)
    # -------------------------------------------------------------
    def setup_linear_tab(self):
        """Construct the Linear Systems GUI tab layout and matrix input controls."""
        self.linear_method_var = ctk.StringVar(value="Gauss-Seidel")
        self.linear_selector = ctk.CTkSegmentedButton(
            self.tab_linear,
            values=["Gauss-Seidel", "Jacobi"],
            variable=self.linear_method_var,
            font=(self.font_family, 13, "bold"),
            height=32
        )
        self.linear_selector.pack(pady=8)

        info_frame = ctk.CTkFrame(self.tab_linear)
        info_frame.pack(pady=4, padx=12, fill="x")

        # إدخال المصفوفة A
        lbl_mat = ctk.CTkLabel(info_frame, text=ar("مصفوفة المعاملات A (كل سطر يمثل معادلة، الأرقام مفصولة بمسافات):"), font=(self.font_family, 12, "bold"))
        lbl_mat.pack(anchor="e", padx=10, pady=(4, 0))
        self.txt_matrix = ctk.CTkTextbox(info_frame, height=75, font=(self.font_mono, 12))
        self.txt_matrix.insert("1.0", "4 1 -1\n2 7 1\n1 -3 12")
        self.txt_matrix.pack(fill="x", padx=10, pady=3)

        # صف المدخلات: b، التخمين الابتدائي، الدقة، والتكرار
        param_grid = ctk.CTkFrame(info_frame, fg_color="transparent")
        param_grid.pack(fill="x", padx=10, pady=4)

        lbl_b = ctk.CTkLabel(param_grid, text=ar("الحدود المطلقة b:"), font=(self.font_family, 12))
        lbl_b.grid(row=0, column=5, padx=5, sticky="e")
        self.entry_b = ctk.CTkEntry(param_grid, placeholder_text=ar("مثال: 3 19 31"), width=140)
        self.entry_b.insert(0, "3 19 31")
        self.entry_b.grid(row=0, column=4, padx=5, sticky="w")

        lbl_x0 = ctk.CTkLabel(param_grid, text=ar("التخمين X0 (اختياري):"), font=(self.font_family, 12))
        lbl_x0.grid(row=0, column=3, padx=5, sticky="e")
        self.entry_x0 = ctk.CTkEntry(param_grid, placeholder_text=ar("افتراضي: 0 0 0"), width=120)
        self.entry_x0.grid(row=0, column=2, padx=5, sticky="w")

        lbl_lin_tol = ctk.CTkLabel(param_grid, text=ar("نسبة الخطأ:"), font=(self.font_family, 12))
        lbl_lin_tol.grid(row=0, column=1, padx=5, sticky="e")
        self.entry_lin_tol = ctk.CTkEntry(param_grid, width=75)
        self.entry_lin_tol.insert(0, "0.001")
        self.entry_lin_tol.grid(row=0, column=0, padx=5, sticky="w")

        # تنبيه السيادة القطرية
        self.lbl_dom_status = ctk.CTkLabel(self.tab_linear, text="", font=(self.font_family, 11, "italic"), text_color="#3498db")
        self.lbl_dom_status.pack(pady=2)

        self.btn_calc_linear = ctk.CTkButton(
            self.tab_linear,
            text=ar("حل النظام الخطي الآن"),
            font=(self.font_family, 13, "bold"),
            fg_color="#1f538d",
            hover_color="#14375e",
            height=34,
            command=self.calculate_linear
        )
        self.btn_calc_linear.pack(pady=4)

        self.res_linear = ctk.CTkLabel(self.tab_linear, text="", font=(self.font_family, 13, "bold"), wraplength=850)
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

        self.tree_linear.heading("Iter", text=ar("الدورة"))
        self.tree_linear.heading("Values", text=ar("قيم المجاهيل [x1, x2, x3, ...]"))
        self.tree_linear.heading("Error", text=ar("أقصى خطأ (Max Error)"))
        self.tree_linear.column("Iter", width=80, anchor="center")
        self.tree_linear.column("Values", width=550, anchor="center")
        self.tree_linear.column("Error", width=160, anchor="center")

    def calculate_linear(self):
        """Parse matrix inputs, apply diagonal dominance check, and execute iterative linear solvers."""
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
                self.res_linear.configure(text=ar("خطأ: يجب إدخال معادلتين على الأقل!"), text_color="#e74c3c")
                return

            if n != len(b) or any(len(row) != n for row in A):
                self.res_linear.configure(
                    text=ar(f"خطأ: أبعاد المصفوفة غير متطابقة! A تحتوي على {len(A)} أسطر، لكن الأسطر و متجه b يجب أن يكون لكل منها {n} عناصر."),
                    text_color="#e74c3c"
                )
                return

            # التخمين الابتدائي
            raw_x0 = self.entry_x0.get().strip()
            if raw_x0:
                x = [float(val) for val in raw_x0.split()]
                if len(x) != n:
                    self.res_linear.configure(text=ar(f"خطأ: التخمين الابتدائي يجب أن يحتوي على {n} أرقام!"), text_color="#e74c3c")
                    return
            else:
                x = [0.0] * n

            # التحقق من السيادة القطرية وإعادة الترتيب التلقائي
            A, b, is_dom, dom_msg = make_diagonally_dominant(A, b)
            self.lbl_dom_status.configure(text=ar(f"[معاينة السيادة القطرية]: {dom_msg}"))

            # التحقق من أن عناصر القطر الرئيسي لا تساوي صفراً
            for i in range(n):
                if abs(A[i][i]) < 1e-12:
                    self.res_linear.configure(text=ar(f"خطأ: العنصر A[{i+1}][{i+1}] يساوي صفراً، لا يمكن القسمة عليه!"), text_color="#e74c3c")
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
                    self.res_linear.configure(text=ar("النظام متباعد (Diverges)! تأكد من تحقق شرط السيادة القطرية للمصفوفة."), text_color="#e74c3c")
                    return

                if err < tol:
                    self.res_linear.configure(text=ar(f"تم الوصول للحل بنجاح: {formatted_vals} بعد {it} دورة"), text_color="#2ecc71")
                    return

            self.res_linear.configure(text=ar(f"وصل للحد الأقصى للتكرارات (100) دون الوصول للدقة المطلوبة. آخر قيم: {formatted_vals}"), text_color="#e67e22")

        except Exception as e:
            self.res_linear.configure(text=ar(f"خطأ في الإدخال: {e}"), text_color="#e74c3c")

    # -------------------------------------------------------------
    # 3. تبويب الانحدار ومواءمة المنحنيات (Regression & Curve Fitting)
    # -------------------------------------------------------------
    def setup_regression_tab(self):
        """Construct the Curve Fitting & Regression GUI tab layout, table, and plot canvas."""
        # 1. محدد الطريقة (Linear, Polynomial, Exponential, Power)
        self.reg_method_var = ctk.StringVar(value="Linear")
        self.reg_selector = ctk.CTkSegmentedButton(
            self.tab_regression,
            values=["Linear", "Polynomial", "Exponential", "Power"],
            variable=self.reg_method_var,
            command=self.update_regression_inputs,
            font=(self.font_family, 13, "bold"),
            height=32
        )
        self.reg_selector.pack(pady=(6, 4))

        # 2. إطار المدخلات
        reg_input_frame = ctk.CTkFrame(self.tab_regression)
        reg_input_frame.pack(fill="x", padx=12, pady=4)

        # صف قيم X
        lbl_x = ctk.CTkLabel(reg_input_frame, text=ar("قيم X (مفصولة بمسافات أو فواصل):"), font=(self.font_family, 12, "bold"))
        lbl_x.grid(row=0, column=2, padx=10, pady=4, sticky="e")
        self.entry_reg_x = ctk.CTkEntry(reg_input_frame, placeholder_text=ar("مثال: 1, 2, 3, 4, 5, 6, 7"), width=380)
        self.entry_reg_x.insert(0, "1, 2, 3, 4, 5, 6, 7")
        self.entry_reg_x.grid(row=0, column=1, padx=10, pady=4, sticky="w")

        # صف قيم Y
        lbl_y = ctk.CTkLabel(reg_input_frame, text=ar("قيم Y (مفصولة بمسافات أو فواصل):"), font=(self.font_family, 12, "bold"))
        lbl_y.grid(row=1, column=2, padx=10, pady=4, sticky="e")
        self.entry_reg_y = ctk.CTkEntry(reg_input_frame, placeholder_text=ar("مثال: 0.5, 2.5, 2.0, 4.0, 3.5, 6.0, 5.5"), width=380)
        self.entry_reg_y.insert(0, "0.5, 2.5, 2.0, 4.0, 3.5, 6.0, 5.5")
        self.entry_reg_y.grid(row=1, column=1, padx=10, pady=4, sticky="w")

        # إطار الخيارات الإضافية (درجة كثير الحدود، بيانات تجريبية، مسح)
        opts_frame = ctk.CTkFrame(reg_input_frame, fg_color="transparent")
        opts_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=(2, 6), sticky="ew")

        # درجة كثير الحدود (يظهر عند اختيار Polynomial)
        self.deg_container = ctk.CTkFrame(opts_frame, fg_color="transparent")
        self.deg_container.pack(side="right", padx=10)
        
        self.lbl_reg_deg = ctk.CTkLabel(self.deg_container, text=ar("درجة كثير الحدود (Degree m):"), font=(self.font_family, 12))
        self.lbl_reg_deg.pack(side="right", padx=(5, 0))
        self.entry_reg_deg = ctk.CTkEntry(self.deg_container, width=65)
        self.entry_reg_deg.insert(0, "2")
        self.entry_reg_deg.pack(side="right", padx=(0, 5))
        self.deg_container.pack_forget()

        # أزرار مساعدة
        self.btn_sample_reg = ctk.CTkButton(
            opts_frame,
            text=ar("بيانات تجريبية (Sample)"),
            font=(self.font_family, 11),
            width=130,
            height=28,
            fg_color="#2b5278",
            hover_color="#1e3b57",
            command=self.load_sample_regression_data
        )
        self.btn_sample_reg.pack(side="left", padx=6)

        self.btn_clear_reg = ctk.CTkButton(
            opts_frame,
            text=ar("مسح الحقول (Clear)"),
            font=(self.font_family, 11),
            width=110,
            height=28,
            fg_color="#5c6370",
            hover_color="#4b5263",
            command=self.clear_regression_inputs
        )
        self.btn_clear_reg.pack(side="left", padx=6)

        # زر الحساب الرئيسي
        self.btn_calc_reg = ctk.CTkButton(
            self.tab_regression,
            text=ar("احسب وطابق المنحنى الآن (Fit Curve)"),
            font=(self.font_family, 13, "bold"),
            fg_color="#1f538d",
            hover_color="#14375e",
            height=34,
            command=self.calculate_regression
        )
        self.btn_calc_reg.pack(pady=4)

        # إطار عرض المعادلة والمقاييس الإحصائية
        self.metrics_container = ctk.CTkFrame(self.tab_regression, fg_color="#1e2227")
        self.metrics_container.pack(fill="x", padx=12, pady=2)

        self.lbl_reg_eq = ctk.CTkLabel(
            self.metrics_container, 
            text=ar("معادلة المنحنى: اضغط على زر الحساب لعرض المعادلة والمخطط"), 
            font=(self.font_family, 13, "bold"),
            text_color="#61afef"
        )
        self.lbl_reg_eq.pack(pady=(4, 2))

        self.lbl_reg_metrics = ctk.CTkLabel(
            self.metrics_container, 
            text=ar("مقاييس الجودة: R² = -- | Sy/x = -- | SSE (Sr) = --"), 
            font=(self.font_family, 11),
            text_color="#abb2bf"
        )
        self.lbl_reg_metrics.pack(pady=(0, 4))

        self.lbl_reg_error = ctk.CTkLabel(
            self.tab_regression,
            text="",
            font=(self.font_family, 12, "bold"),
            text_color="#e74c3c"
        )
        self.lbl_reg_error.pack(pady=(0, 2))

        # إطار العرض المنقسم (Split Content: جدول على اليسار ومخطط بياني على اليمين)
        split_frame = ctk.CTkFrame(self.tab_regression)
        split_frame.pack(fill="both", expand=True, padx=10, pady=(2, 6))
        split_frame.columnconfigure(0, weight=4)
        split_frame.columnconfigure(1, weight=5)
        split_frame.rowconfigure(0, weight=1)

        # 1. إطار جدول البواقي والتقييم
        table_frame = ctk.CTkFrame(split_frame)
        table_frame.grid(row=0, column=0, sticky="nsew", padx=(4, 4), pady=4)

        lbl_tbl_title = ctk.CTkLabel(
            table_frame, 
            text=ar("جدول مقارنة القيم والبواقي (Evaluation Table)"), 
            font=(self.font_family, 11, "bold")
        )
        lbl_tbl_title.pack(pady=3)

        tree_scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
        self.tree_reg = ttk.Treeview(
            table_frame,
            columns=("pt", "x", "y_act", "y_pred", "res"),
            show="headings",
            yscrollcommand=tree_scroll_y.set
        )
        tree_scroll_y.config(command=self.tree_reg.yview)
        tree_scroll_y.pack(side="right", fill="y")
        self.tree_reg.pack(side="left", fill="both", expand=True)

        cols = [
            ("pt", ar("ن"), 35),
            ("x", "X", 65),
            ("y_act", ar("Y الفعلي"), 75),
            ("y_pred", ar("Y النموذج"), 75),
            ("res", ar("الباقي (e)"), 75)
        ]
        for col_id, title, width in cols:
            self.tree_reg.heading(col_id, text=title)
            self.tree_reg.column(col_id, width=width, anchor="center")

        # 2. إطار الرسم البياني Matplotlib Canvas
        plot_frame = ctk.CTkFrame(split_frame)
        plot_frame.grid(row=0, column=1, sticky="nsew", padx=(4, 4), pady=4)

        self.fig_reg = Figure(figsize=(4.6, 3.2), dpi=95)
        self.fig_reg.patch.set_facecolor('#23272e')
        self.ax_reg = self.fig_reg.add_subplot(111)
        self.apply_dark_plot_style(self.ax_reg)

        self.canvas_reg = FigureCanvasTkAgg(self.fig_reg, master=plot_frame)
        self.canvas_reg.get_tk_widget().pack(fill="both", expand=True, padx=2, pady=2)
        self.canvas_reg.draw()

    def apply_dark_plot_style(self, ax):
        """Apply dark theme colors to Matplotlib axes, grid, spines, and labels."""
        ax.set_facecolor('#1e2227')
        ax.tick_params(colors='#abb2bf', labelsize=8)
        for spine in ax.spines.values():
            spine.set_color('#5c6370')
        ax.grid(True, color='#5c6370', linestyle='--', alpha=0.35)
        ax.set_xlabel("X", color='#abb2bf', fontsize=9)
        ax.set_ylabel("Y", color='#abb2bf', fontsize=9)

    def update_regression_inputs(self, choice=None):
        """Show or hide polynomial degree inputs based on model selection."""
        if choice is None:
            choice = self.reg_method_var.get()
        if choice == "Polynomial":
            self.deg_container.pack(side="right", padx=10)
        else:
            self.deg_container.pack_forget()

    def load_sample_regression_data(self):
        """Populate sample dataset suited for the currently active regression model."""
        method = self.reg_method_var.get()
        self.entry_reg_x.delete(0, "end")
        self.entry_reg_y.delete(0, "end")

        if method == "Linear":
            self.entry_reg_x.insert(0, "1, 2, 3, 4, 5, 6, 7")
            self.entry_reg_y.insert(0, "0.5, 2.5, 2.0, 4.0, 3.5, 6.0, 5.5")
        elif method == "Polynomial":
            self.entry_reg_x.insert(0, "0, 1, 2, 3, 4, 5")
            self.entry_reg_y.insert(0, "2.1, 7.7, 13.6, 27.2, 40.9, 61.1")
            self.entry_reg_deg.delete(0, "end")
            self.entry_reg_deg.insert(0, "2")
        elif method == "Exponential":
            self.entry_reg_x.insert(0, "1, 2, 3, 4, 5")
            self.entry_reg_y.insert(0, "0.5, 1.7, 5.0, 14.8, 44.0")
        elif method == "Power":
            self.entry_reg_x.insert(0, "1, 2, 3, 4, 5")
            self.entry_reg_y.insert(0, "0.5, 2.0, 4.5, 8.0, 12.5")

    def clear_regression_inputs(self):
        """Clear all regression input fields, metrics, table rows, and plot axes."""
        self.entry_reg_x.delete(0, "end")
        self.entry_reg_y.delete(0, "end")
        self.lbl_reg_eq.configure(text=ar("معادلة المنحنى: في انتظار الحساب..."))
        self.lbl_reg_metrics.configure(text=ar("مقاييس الجودة: R² = -- | Sy/x = -- | SSE (Sr) = --"))
        self.lbl_reg_error.configure(text="")
        for item in self.tree_reg.get_children():
            self.tree_reg.delete(item)
        self.ax_reg.clear()
        self.apply_dark_plot_style(self.ax_reg)
        self.canvas_reg.draw()

    def calculate_regression(self):
        """Execute curve fitting calculation, update metrics, table, and plot canvas."""
        self.lbl_reg_error.configure(text="")
        method = self.reg_method_var.get()

        raw_x = self.entry_reg_x.get().strip()
        raw_y = self.entry_reg_y.get().strip()

        if not raw_x or not raw_y:
            self.lbl_reg_error.configure(text=ar("خطأ: يرجى إدخال قيم X وقيم Y!"))
            return

        try:
            x_vals = [float(v) for v in raw_x.replace(",", " ").split()]
            y_vals = [float(v) for v in raw_y.replace(",", " ").split()]
        except ValueError:
            self.lbl_reg_error.configure(text=ar("خطأ: يرجى التأكد من أن جميع مدخلات X و Y أرقام صحيحة أو عشرية!"))
            return

        n = len(x_vals)
        if n != len(y_vals):
            self.lbl_reg_error.configure(text=ar(f"خطأ: عدد قيم X ({n}) لا يتطابق مع عدد قيم Y ({len(y_vals)})!"))
            return

        if n < 2:
            self.lbl_reg_error.configure(text=ar("خطأ: يجب إدخال نقطتين على الأقل (N >= 2) لإجراء مواءمة المنحنيات!"))
            return

        degree = 2
        if method == "Polynomial":
            deg_str = self.entry_reg_deg.get().strip()
            try:
                degree = int(deg_str)
                if degree < 1:
                    self.lbl_reg_error.configure(text=ar("خطأ: درجة كثير الحدود يجب أن تكون 1 على الأقل!"))
                    return
                if n < degree + 1:
                    self.lbl_reg_error.configure(text=ar(f"خطأ: عدد النقاط ({n}) غير كافٍ لدرجة كثير الحدود ({degree}). يلزم على الأقل {degree + 1} نقاط!"))
                    return
            except ValueError:
                self.lbl_reg_error.configure(text=ar("خطأ: يرجى إدخال رقم صحيح لدرجة كثير الحدود!"))
                return

        # تنفيذ الحساب
        try:
            if method == "Linear":
                res = linear_regression(x_vals, y_vals)
            elif method == "Polynomial":
                res = polynomial_regression(x_vals, y_vals, degree=degree)
            elif method == "Exponential":
                res = exponential_regression(x_vals, y_vals)
            elif method == "Power":
                res = power_regression(x_vals, y_vals)
            else:
                self.lbl_reg_error.configure(text=ar(f"طريقة غير معروفة: {method}"))
                return

            # تحديث المعادلة والمقاييس
            self.lbl_reg_eq.configure(text=ar(f"معادلة المنحنى:  {res['equation']}"))
            metrics_str = f"R² = {res['r2']:.5f} ({res['r2']*100:.2f}%)   |   Sy/x = {res['syx']:.5f}   |   SSE (Sr) = {res['sr']:.5f}   |   St = {res['st']:.5f}"
            self.lbl_reg_metrics.configure(text=ar(metrics_str))

            # تحديث جدول التقييم
            for item in self.tree_reg.get_children():
                self.tree_reg.delete(item)

            for i, (xi, yi, yp, e) in enumerate(zip(x_vals, y_vals, res['y_pred'], res['residuals']), 1):
                self.tree_reg.insert("", "end", values=(i, f"{xi:.4g}", f"{yi:.4g}", f"{yp:.4g}", f"{e:+.4g}"))

            # تحديث المخطط البياني في Matplotlib Canvas
            self.ax_reg.clear()
            self.apply_dark_plot_style(self.ax_reg)

            # رسم نقاط البيانات
            self.ax_reg.scatter(
                x_vals, y_vals,
                color='#e06c75',
                s=50,
                zorder=5,
                label=ar("نقاط البيانات (Data)"),
                edgecolors='#ffffff',
                linewidths=0.8
            )

            # رسم المنحنى المتصل الموفق
            self.ax_reg.plot(
                res['x_curve'], res['y_curve'],
                color='#61afef',
                linewidth=2.2,
                zorder=4,
                label=ar(f"منحنى المواءمة ({method})")
            )

            title_text = f"Curve Fit: {res['method_name']} (R² = {res['r2']:.4f})"
            self.ax_reg.set_title(title_text, color='#dcdfe4', fontsize=10, fontweight='bold', pad=8)
            self.ax_reg.legend(facecolor='#282c34', edgecolor='#5c6370', labelcolor='#dcdfe4', fontsize=8, loc='best')

            self.fig_reg.tight_layout()
            self.canvas_reg.draw()

        except Exception as err:
            self.lbl_reg_error.configure(text=ar(f"خطأ أثناء الحساب: {err}"))

if __name__ == "__main__":
    app = NumericalApp()
    app.mainloop()
