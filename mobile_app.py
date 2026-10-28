"""
Math 3 Numerical Methods Suite - Mobile Application (Kivy / Android).

This module provides a modern, touch-friendly, mobile-first graphical user
interface designed specifically for Android devices (via Kivy & Buildozer)
and cross-platform mobile preview on desktop.

Features:
    1. Root Finding (تنصيف الفترات, نيوتن-رافسون, القاطع, القاطع المعدلة).
    2. Linear Systems (طريقة جاكوبي, طريقة جاوس-سيدل).
    3. Regression & Curve Fitting (خطي, متعدد حدود, أسي, قوى).
    4. Full bidirectional Arabic text shaping & bundled Arabic font.
    5. Modern Material Dark aesthetic (Deep Slate & Cyan/Blue accents).
"""

import os
import sys
from typing import List, Dict, Any, Optional

# Kivy configuration before other Kivy imports
os.environ.setdefault("KIVY_NO_ARGS", "1")

import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, RoundedRectangle, Rectangle

try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_ARABIC_RESHAPER = True
except ImportError:
    HAS_ARABIC_RESHAPER = False

# Import pure mathematical numerical algorithms
from math_utils import parse_math_expression, check_strictly_diagonally_dominant, make_diagonally_dominant
from bisection import bisection
from newton_raphson import newton_raphson
from secant import secant
from modified_secant import modified_secant
from jacobi import jacobi
from gauss_seidel import gauss_seidel
from regression import (
    linear_regression,
    polynomial_regression,
    exponential_regression,
    power_regression
)

# ---------------------------------------------------------
# Arabic Text & Font Setup
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(BASE_DIR, "assets", "fonts", "NotoSansArabic-Regular.ttf")

ARABIC_FONT = "Roboto"
if os.path.exists(FONT_PATH):
    try:
        LabelBase.register(name="ArabicFont", fn_regular=FONT_PATH)
        ARABIC_FONT = "ArabicFont"
    except Exception as e:
        print(f"Warning: Could not register Arabic font: {e}")

def ar(text: Any) -> str:
    """Reshape and reorder Arabic text for bidirectional rendering."""
    if not text:
        return ""
    if not HAS_ARABIC_RESHAPER:
        return str(text)
    try:
        s = str(text)
        reshaped = arabic_reshaper.reshape(s)
        return get_display(reshaped)
    except Exception:
        return str(text)

# ---------------------------------------------------------
# Custom Styled Kivy Widgets
# ---------------------------------------------------------
class StyledCard(BoxLayout):
    """Container with dark slate background and rounded corners."""
    def __init__(self, bg_color=(0.12, 0.16, 0.23, 1), radius=12, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = bg_color
        self.radius = radius
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class ArabicLabel(Label):
    """Standard Label with Arabic font and reshaped text."""
    def __init__(self, text="", **kwargs):
        kwargs.setdefault("font_name", ARABIC_FONT)
        kwargs.setdefault("color", (0.95, 0.96, 0.98, 1))
        super().__init__(text=ar(text), **kwargs)

    def set_arabic_text(self, text):
        self.text = ar(text)

class ActionButton(Button):
    """Material-styled touch button with smooth rounded background."""
    def __init__(self, text="", bg_color=(0.02, 0.71, 0.83, 1), **kwargs):
        kwargs.setdefault("font_name", ARABIC_FONT)
        kwargs.setdefault("background_color", (0, 0, 0, 0))
        kwargs.setdefault("color", (1, 1, 1, 1))
        kwargs.setdefault("bold", True)
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", 48)
        super().__init__(text=ar(text), **kwargs)
        self.btn_bg = bg_color
        with self.canvas.before:
            self.color_instruction = Color(*self.btn_bg)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

# ---------------------------------------------------------
# Main Mobile Interface Layout
# ---------------------------------------------------------
class MobileToolkitRoot(BoxLayout):
    """Root UI layout supporting navigation tabs, dynamic forms, and results."""

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        # Background canvas
        with self.canvas.before:
            Color(0.06, 0.09, 0.16, 1)  # Deep Slate #0F172A
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        self.current_section = "roots"
        self.current_submethod = "Bisection"

        # 1. Top Header Bar
        self.header = StyledCard(
            bg_color=(0.08, 0.11, 0.19, 1),
            orientation="vertical",
            size_hint_y=None,
            height=70,
            padding=[10, 8, 10, 8]
        )
        title_lbl = ArabicLabel(
            text="Math 3 Numerical Methods | التحليل العددي",
            font_size="17sp",
            bold=True,
            halign="center"
        )
        sub_lbl = ArabicLabel(
            text="حقيبة الطرق العددية المتكاملة للهواتف الذكية",
            font_size="11sp",
            color=(0.58, 0.64, 0.72, 1),
            halign="center"
        )
        self.header.add_widget(title_lbl)
        self.header.add_widget(sub_lbl)
        self.add_widget(self.header)

        # 2. Main Navigation Tabs (Roots, Linear Systems, Regression)
        self.nav_tabs = BoxLayout(size_hint_y=None, height=44, spacing=4, padding=[6, 4, 6, 4])
        self.tab_roots = ActionButton(text="إيجاد الجذور", bg_color=(0.02, 0.71, 0.83, 1), height=36)
        self.tab_roots.bind(on_release=lambda btn: self.switch_section("roots"))

        self.tab_linear = ActionButton(text="الأنظمة الخطية", bg_color=(0.18, 0.24, 0.35, 1), height=36)
        self.tab_linear.bind(on_release=lambda btn: self.switch_section("linear"))

        self.tab_reg = ActionButton(text="الانحدار", bg_color=(0.18, 0.24, 0.35, 1), height=36)
        self.tab_reg.bind(on_release=lambda btn: self.switch_section("regression"))

        self.nav_tabs.add_widget(self.tab_roots)
        self.nav_tabs.add_widget(self.tab_linear)
        self.nav_tabs.add_widget(self.tab_reg)
        self.add_widget(self.nav_tabs)

        # 3. Scrollable Content Area
        self.scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.content_box = BoxLayout(orientation="vertical", spacing=12, padding=[12, 8, 12, 16], size_hint_y=None)
        self.content_box.bind(minimum_height=self.content_box.setter("height"))
        self.scroll.add_widget(self.content_box)
        self.add_widget(self.scroll)

        # Build initial section
        self.build_roots_section()

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def update_tab_colors(self):
        active_color = (0.02, 0.71, 0.83, 1)  # Cyan
        inactive_color = (0.18, 0.24, 0.35, 1)

        self.tab_roots.color_instruction.rgb = active_color if self.current_section == "roots" else inactive_color
        self.tab_linear.color_instruction.rgb = active_color if self.current_section == "linear" else inactive_color
        self.tab_reg.color_instruction.rgb = active_color if self.current_section == "regression" else inactive_color

    def switch_section(self, section: str):
        self.current_section = section
        self.update_tab_colors()
        self.content_box.clear_widgets()

        if section == "roots":
            self.build_roots_section()
        elif section == "linear":
            self.build_linear_section()
        elif section == "regression":
            self.build_regression_section()

    # =========================================================================
    # SECTION 1: ROOT FINDING
    # =========================================================================
    def build_roots_section(self):
        # Submethod Selector
        selector_card = StyledCard(orientation="vertical", size_hint_y=None, height=84, padding=8, spacing=6)
        sel_lbl = ArabicLabel(text="اختر طريقة إيجاد الجذر:", size_hint_y=None, height=20, font_size="13sp")
        selector_card.add_widget(sel_lbl)

        methods_map = {
            "Bisection (تنصيف الفترات)": "Bisection",
            "Newton-Raphson (نيوتن-رافسون)": "Newton-Raphson",
            "Secant (طريقة القاطع)": "Secant",
            "Modified Secant (القاطع المعدلة)": "Modified Secant"
        }
        self.root_spinner = Spinner(
            text=ar("Bisection (تنصيف الفترات)"),
            values=[ar(k) for k in methods_map.keys()],
            size_hint_y=None,
            height=44,
            font_name=ARABIC_FONT,
            background_color=(0.18, 0.24, 0.35, 1),
            color=(1, 1, 1, 1)
        )
        self.methods_map = methods_map
        self.root_spinner.bind(text=self.on_root_method_change)
        selector_card.add_widget(self.root_spinner)
        self.content_box.add_widget(selector_card)

        # Dynamic Inputs Card
        self.inputs_card = StyledCard(orientation="vertical", size_hint_y=None, padding=12, spacing=8)
        self.content_box.add_widget(self.inputs_card)
        self.rebuild_root_inputs("Bisection")

        # Action Button
        self.btn_solve_root = ActionButton(text="احسب الجذر (Calculate Root)", bg_color=(0.06, 0.72, 0.51, 1), height=48)
        self.btn_solve_root.bind(on_release=self.calculate_root)
        self.content_box.add_widget(self.btn_solve_root)

        # Results Card
        self.results_card = StyledCard(orientation="vertical", size_hint_y=None, padding=12, spacing=8)
        self.results_title = ArabicLabel(text="النتائج (Results):", bold=True, size_hint_y=None, height=24)
        self.results_content = ArabicLabel(
            text="أدخل البيانات واضغط على زر الحساب لعرض النتائج.",
            color=(0.7, 0.75, 0.82, 1),
            size_hint_y=None,
            height=60
        )
        self.results_card.add_widget(self.results_title)
        self.results_card.add_widget(self.results_content)
        self.results_card.height = 110
        self.content_box.add_widget(self.results_card)

    def on_root_method_change(self, spinner, text):
        selected = "Bisection"
        for k, v in self.methods_map.items():
            if ar(k) == text or k == text:
                selected = v
                break
        self.current_submethod = selected
        self.rebuild_root_inputs(selected)

    def rebuild_root_inputs(self, method: str):
        self.inputs_card.clear_widgets()

        # Equation input
        self.inputs_card.add_widget(ArabicLabel(text="المعادلة f(x) = 0:", size_hint_y=None, height=20, font_size="13sp"))
        self.txt_func = TextInput(
            text="x^3 - x - 2",
            multiline=False,
            size_hint_y=None,
            height=40,
            background_color=(0.09, 0.12, 0.18, 1),
            foreground_color=(1, 1, 1, 1)
        )
        self.inputs_card.add_widget(self.txt_func)

        # Dynamic parameter grid
        grid = GridLayout(cols=2, spacing=8, size_hint_y=None, height=90)

        if method == "Bisection":
            grid.add_widget(ArabicLabel(text="بداية الفترة (a / xl):", font_size="12sp"))
            self.txt_p1 = TextInput(text="1", multiline=False, size_hint_y=None, height=36, background_color=(0.09, 0.12, 0.18, 1), foreground_color=(1, 1, 1, 1))
            grid.add_widget(self.txt_p1)

            grid.add_widget(ArabicLabel(text="نهاية الفترة (b / xu):", font_size="12sp"))
            self.txt_p2 = TextInput(text="2", multiline=False, size_hint_y=None, height=36, background_color=(0.09, 0.12, 0.18, 1), foreground_color=(1, 1, 1, 1))
            grid.add_widget(self.txt_p2)

        elif method == "Newton-Raphson":
            grid.add_widget(ArabicLabel(text="التخمين الأولي (x0):", font_size="12sp"))
            self.txt_p1 = TextInput(text="1.5", multiline=False, size_hint_y=None, height=36, background_color=(0.09, 0.12, 0.18, 1), foreground_color=(1, 1, 1, 1))
            grid.add_widget(self.txt_p1)
            self.txt_p2 = None

        elif method == "Secant":
            grid.add_widget(ArabicLabel(text="النقطة الأولى (x0):", font_size="12sp"))
            self.txt_p1 = TextInput(text="1", multiline=False, size_hint_y=None, height=36, background_color=(0.09, 0.12, 0.18, 1), foreground_color=(1, 1, 1, 1))
            grid.add_widget(self.txt_p1)

            grid.add_widget(ArabicLabel(text="النقطة الثانية (x1):", font_size="12sp"))
            self.txt_p2 = TextInput(text="2", multiline=False, size_hint_y=None, height=36, background_color=(0.09, 0.12, 0.18, 1), foreground_color=(1, 1, 1, 1))
            grid.add_widget(self.txt_p2)

        elif method == "Modified Secant":
            grid.add_widget(ArabicLabel(text="التخمين الأولي (x0):", font_size="12sp"))
            self.txt_p1 = TextInput(text="1.5", multiline=False, size_hint_y=None, height=36, background_color=(0.09, 0.12, 0.18, 1), foreground_color=(1, 1, 1, 1))
            grid.add_widget(self.txt_p1)

            grid.add_widget(ArabicLabel(text="معامل الاضطراب (Delta δ):", font_size="12sp"))
            self.txt_p2 = TextInput(text="0.01", multiline=False, size_hint_y=None, height=36, background_color=(0.09, 0.12, 0.18, 1), foreground_color=(1, 1, 1, 1))
            grid.add_widget(self.txt_p2)

        self.inputs_card.add_widget(grid)

        # Tolerance and Max Iterations
        grid_tol = GridLayout(cols=4, spacing=6, size_hint_y=None, height=40)
        grid_tol.add_widget(ArabicLabel(text="الخطأ (Tol):", font_size="11sp"))
        self.txt_tol = TextInput(text="0.001", multiline=False, size_hint_y=None, height=34, background_color=(0.09, 0.12, 0.18, 1), foreground_color=(1, 1, 1, 1))
        grid_tol.add_widget(self.txt_tol)

        grid_tol.add_widget(ArabicLabel(text="أقصى تكرار:", font_size="11sp"))
        self.txt_max_iter = TextInput(text="50", multiline=False, size_hint_y=None, height=34, background_color=(0.09, 0.12, 0.18, 1), foreground_color=(1, 1, 1, 1))
        grid_tol.add_widget(self.txt_max_iter)
        self.inputs_card.add_widget(grid_tol)

        self.inputs_card.height = 230

    def calculate_root(self, *args):
        try:
            expr_str = self.txt_func.text.strip()
            tol = float(self.txt_tol.text.strip() or 0.001)
            max_iter = int(self.txt_max_iter.text.strip() or 50)

            expr, f_func, x_sym = parse_math_expression(expr_str)
            method = self.current_submethod

            if method == "Bisection":
                a = float(self.txt_p1.text.strip())
                b = float(self.txt_p2.text.strip())
                root, steps, conv, msg = bisection(f_func, a, b, tol, max_iter)

            elif method == "Newton-Raphson":
                import sympy as sp
                df_expr = sp.diff(expr, x_sym)
                df_func = sp.lambdify(x_sym, df_expr, modules=['math'])
                x0 = float(self.txt_p1.text.strip())
                root, steps, conv, msg = newton_raphson(f_func, df_func, x0, tol, max_iter)

            elif method == "Secant":
                x0 = float(self.txt_p1.text.strip())
                x1 = float(self.txt_p2.text.strip())
                root, steps, conv, msg = secant(f_func, x0, x1, tol, max_iter)

            elif method == "Modified Secant":
                x0 = float(self.txt_p1.text.strip())
                delta = float(self.txt_p2.text.strip() or 0.01)
                root, steps, conv, msg = modified_secant(f_func, x0, delta, tol, max_iter)
            else:
                return

            # Display formatted output
            status_text = "تقارب بنجاح" if conv else "لم يتقارب"
            res_str = (
                f"الحالة: {status_text} | التكرارات: {len(steps)}\n"
                f"الجذر التقريبي: x ≈ {root:.6f}\n"
                f"قيمة الدالة: f(x) ≈ {f_func(root):.4e}\n"
                f"{msg}"
            )
            self.results_content.set_arabic_text(res_str)
            self.results_card.height = 160

        except Exception as e:
            self.results_content.set_arabic_text(f"خطأ في الحساب:\n{e}")
            self.results_card.height = 120

    # =========================================================================
    # SECTION 2: LINEAR SYSTEMS
    # =========================================================================
    def build_linear_section(self):
        selector_card = StyledCard(orientation="vertical", size_hint_y=None, height=84, padding=8, spacing=6)
        selector_card.add_widget(ArabicLabel(text="اختر طريقة حل النظام الخطي:", size_hint_y=None, height=20, font_size="13sp"))

        lin_map = {
            "Jacobi Method (طريقة جاكوبي)": "Jacobi",
            "Gauss-Seidel (طريقة جاوس-سيدل)": "Gauss-Seidel"
        }
        self.lin_spinner = Spinner(
            text=ar("Jacobi Method (طريقة جاكوبي)"),
            values=[ar(k) for k in lin_map.keys()],
            size_hint_y=None,
            height=44,
            font_name=ARABIC_FONT,
            background_color=(0.18, 0.24, 0.35, 1)
        )
        self.lin_map = lin_map
        self.lin_spinner.bind(text=self.on_lin_method_change)
        selector_card.add_widget(self.lin_spinner)
        self.content_box.add_widget(selector_card)

        # System inputs
        self.lin_inputs_card = StyledCard(orientation="vertical", size_hint_y=None, height=260, padding=12, spacing=8)
        self.lin_inputs_card.add_widget(ArabicLabel(
            text="أدخل معادلات النظام الخطي (صف لكل معادلة):\nمثال (A | b): 4, 1, 1, 9",
            size_hint_y=None,
            height=38,
            font_size="12sp"
        ))

        default_system = "4, 1, 1, 9\n1, 5, 2, 15\n1, 2, 5, 18"
        self.txt_linear_eqs = TextInput(
            text=default_system,
            multiline=True,
            size_hint_y=None,
            height=90,
            background_color=(0.09, 0.12, 0.18, 1),
            foreground_color=(1, 1, 1, 1)
        )
        self.lin_inputs_card.add_widget(self.txt_linear_eqs)

        grid_tol = GridLayout(cols=4, spacing=6, size_hint_y=None, height=40)
        grid_tol.add_widget(ArabicLabel(text="الخطأ (Tol):", font_size="11sp"))
        self.txt_lin_tol = TextInput(text="0.001", multiline=False, size_hint_y=None, height=34, background_color=(0.09, 0.12, 0.18, 1), foreground_color=(1, 1, 1, 1))
        grid_tol.add_widget(self.txt_lin_tol)

        grid_tol.add_widget(ArabicLabel(text="أقصى تكرار:", font_size="11sp"))
        self.txt_lin_max_iter = TextInput(text="50", multiline=False, size_hint_y=None, height=34, background_color=(0.09, 0.12, 0.18, 1), foreground_color=(1, 1, 1, 1))
        grid_tol.add_widget(self.txt_lin_max_iter)
        self.lin_inputs_card.add_widget(grid_tol)
        self.content_box.add_widget(self.lin_inputs_card)

        # Solve button
        self.btn_solve_linear = ActionButton(text="حل النظام الخطي (Solve System)", bg_color=(0.06, 0.72, 0.51, 1), height=48)
        self.btn_solve_linear.bind(on_release=self.calculate_linear)
        self.content_box.add_widget(self.btn_solve_linear)

        # Results
        self.lin_results_card = StyledCard(orientation="vertical", size_hint_y=None, height=130, padding=12, spacing=8)
        self.lin_results_title = ArabicLabel(text="حل النظام (Solution):", bold=True, size_hint_y=None, height=24)
        self.lin_results_content = ArabicLabel(
            text="أدخل معاملات النظام واضغط على زر الحل لعرض المتغيرات.",
            color=(0.7, 0.75, 0.82, 1),
            size_hint_y=None,
            height=70
        )
        self.lin_results_card.add_widget(self.lin_results_title)
        self.lin_results_card.add_widget(self.lin_results_content)
        self.content_box.add_widget(self.lin_results_card)

    def on_lin_method_change(self, spinner, text):
        selected = "Jacobi"
        for k, v in self.lin_map.items():
            if ar(k) == text or k == text:
                selected = v
                break
        self.current_submethod = selected

    def calculate_linear(self, *args):
        try:
            lines = [ln.strip() for ln in self.txt_linear_eqs.text.strip().split("\n") if ln.strip()]
            if not lines:
                raise ValueError("يرجى إدخال معادلة خطية واحدة على الأقل.")

            A = []
            b = []
            for ln in lines:
                parts = [float(p.strip()) for p in ln.replace("|", ",").split(",") if p.strip()]
                if len(parts) < 2:
                    raise ValueError(f"سطر غير مكتمل: {ln}")
                A.append(parts[:-1])
                b.append(parts[-1])

            n = len(A)
            for row in A:
                if len(row) != n:
                    raise ValueError(f"المصفوفة يجب أن تكون مربعة ({n}x{n})!")

            tol = float(self.txt_lin_tol.text.strip() or 0.001)
            max_iter = int(self.txt_lin_max_iter.text.strip() or 50)

            method = self.current_submethod
            if method == "Jacobi":
                sol, steps, conv, msg = jacobi(A, b, tol=tol, max_iter=max_iter)
            else:
                sol, steps, conv, msg = gauss_seidel(A, b, tol=tol, max_iter=max_iter)

            sol_formatted = ", ".join([f"x{i+1} = {val:.4f}" for i, val in enumerate(sol)])
            status_text = "تقارب بنجاح" if conv else "لم يتقارب"
            res_str = (
                f"الحالة: {status_text} | التكرارات: {len(steps)}\n"
                f"متجه الحل:\n{sol_formatted}\n"
                f"{msg}"
            )
            self.lin_results_content.set_arabic_text(res_str)
            self.lin_results_card.height = 170

        except Exception as e:
            self.lin_results_content.set_arabic_text(f"خطأ في حل النظام:\n{e}")
            self.lin_results_card.height = 120

    # =========================================================================
    # SECTION 3: REGRESSION & CURVE FITTING
    # =========================================================================
    def build_regression_section(self):
        selector_card = StyledCard(orientation="vertical", size_hint_y=None, height=84, padding=8, spacing=6)
        selector_card.add_widget(ArabicLabel(text="اختر نوع الانحدار ومواءمة المنحنى:", size_hint_y=None, height=20, font_size="13sp"))

        reg_map = {
            "Linear Regression (انحدار خطي)": "Linear",
            "Polynomial Regression (متعدد حدود)": "Polynomial",
            "Exponential Fitting (انحدار أسي)": "Exponential",
            "Power Fitting (انحدار قوى)": "Power"
        }
        self.reg_spinner = Spinner(
            text=ar("Linear Regression (انحدار خطي)"),
            values=[ar(k) for k in reg_map.keys()],
            size_hint_y=None,
            height=44,
            font_name=ARABIC_FONT,
            background_color=(0.18, 0.24, 0.35, 1)
        )
        self.reg_map = reg_map
        self.reg_spinner.bind(text=self.on_reg_method_change)
        selector_card.add_widget(self.reg_spinner)
        self.content_box.add_widget(selector_card)

        # Data Points Inputs
        self.reg_inputs_card = StyledCard(orientation="vertical", size_hint_y=None, height=210, padding=12, spacing=8)
        self.reg_inputs_card.add_widget(ArabicLabel(text="قيم X (مفصولة بفاصلة أو مسافة):", size_hint_y=None, height=20, font_size="12sp"))
        self.txt_reg_x = TextInput(text="1, 2, 3, 4, 5", multiline=False, size_hint_y=None, height=36, background_color=(0.09, 0.12, 0.18, 1), foreground_color=(1, 1, 1, 1))
        self.reg_inputs_card.add_widget(self.txt_reg_x)

        self.reg_inputs_card.add_widget(ArabicLabel(text="قيم Y (مفصولة بفاصلة أو مسافة):", size_hint_y=None, height=20, font_size="12sp"))
        self.txt_reg_y = TextInput(text="2.2, 2.8, 3.6, 4.5, 5.5", multiline=False, size_hint_y=None, height=36, background_color=(0.09, 0.12, 0.18, 1), foreground_color=(1, 1, 1, 1))
        self.reg_inputs_card.add_widget(self.txt_reg_y)

        poly_box = BoxLayout(size_hint_y=None, height=36, spacing=6)
        poly_box.add_widget(ArabicLabel(text="درجة متعدد الحدود (m):", font_size="11sp"))
        self.txt_reg_degree = TextInput(text="2", multiline=False, size_hint_y=None, height=34, background_color=(0.09, 0.12, 0.18, 1), foreground_color=(1, 1, 1, 1))
        poly_box.add_widget(self.txt_reg_degree)
        self.reg_inputs_card.add_widget(poly_box)
        self.content_box.add_widget(self.reg_inputs_card)

        # Fit button
        self.btn_fit_curve = ActionButton(text="مواءمة المنحنى (Fit Curve)", bg_color=(0.06, 0.72, 0.51, 1), height=48)
        self.btn_fit_curve.bind(on_release=self.calculate_regression)
        self.content_box.add_widget(self.btn_fit_curve)

        # Results
        self.reg_results_card = StyledCard(orientation="vertical", size_hint_y=None, height=140, padding=12, spacing=8)
        self.reg_results_title = ArabicLabel(text="معادلة المنحنى والمؤشرات:", bold=True, size_hint_y=None, height=24)
        self.reg_results_content = ArabicLabel(
            text="أدخل النقاط واضغط على مواءمة المنحنى لحساب النموذج ومعامل R².",
            color=(0.7, 0.75, 0.82, 1),
            size_hint_y=None,
            height=80
        )
        self.reg_results_card.add_widget(self.reg_results_title)
        self.reg_results_card.add_widget(self.reg_results_content)
        self.content_box.add_widget(self.reg_results_card)

    def on_reg_method_change(self, spinner, text):
        selected = "Linear"
        for k, v in self.reg_map.items():
            if ar(k) == text or k == text:
                selected = v
                break
        self.current_submethod = selected

    def calculate_regression(self, *args):
        try:
            import re
            x_raw = [float(v) for v in re.split(r'[,\s]+', self.txt_reg_x.text.strip()) if v]
            y_raw = [float(v) for v in re.split(r'[,\s]+', self.txt_reg_y.text.strip()) if v]

            if len(x_raw) != len(y_raw):
                raise ValueError("عدد قيم X يجب أن يطابق تماماً عدد قيم Y!")
            if len(x_raw) < 2:
                raise ValueError("يلزم نقطتان على الأقل لحساب المواءمة!")

            method = self.current_submethod
            if method == "Linear":
                a0, a1, r2, s_yx, eq = linear_regression(x_raw, y_raw)
            elif method == "Polynomial":
                deg = int(self.txt_reg_degree.text.strip() or 2)
                coeffs, r2, s_yx, eq = polynomial_regression(x_raw, y_raw, deg)
            elif method == "Exponential":
                a, b, r2, s_yx, eq = exponential_regression(x_raw, y_raw)
            elif method == "Power":
                a, b, r2, s_yx, eq = power_regression(x_raw, y_raw)
            else:
                return

            res_str = (
                f"معادلة النموذج:\n{eq}\n"
                f"معامل التحديد (R²): {r2:.4f} ({r2*100:.1f}%)\n"
                f"الخطأ المعياري للتقدير (Sy/x): {s_yx:.4f}"
            )
            self.reg_results_content.set_arabic_text(res_str)
            self.reg_results_card.height = 160

        except Exception as e:
            self.reg_results_content.set_arabic_text(f"خطأ في المواءمة:\n{e}")
            self.reg_results_card.height = 120

# ---------------------------------------------------------
# Application Entry Point
# ---------------------------------------------------------
class Math3MobileApp(App):
    """Kivy Application instance for Math 3 Numerical Methods Suite."""

    title = "Math 3 Numerical Methods"

    def build(self):
        Window.clearcolor = (0.06, 0.09, 0.16, 1)
        return MobileToolkitRoot()

def run_mobile_app():
    """Launch the Kivy mobile application instance."""
    app = Math3MobileApp()
    app.run()

if __name__ == "__main__":
    run_mobile_app()
