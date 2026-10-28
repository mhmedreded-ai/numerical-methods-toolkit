# Numerical Methods & Analysis Toolkit (Math 3)

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-CustomTkinter-darkblue.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![Engine](https://img.shields.io/badge/Math%20Engine-SymPy-orange.svg)](https://www.sympy.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A comprehensive Python toolkit and numerical computing suite designed for solving non-linear algebraic equations, finding roots, and solving systems of linear equations. The project combines rigorous mathematical algorithms with both an interactive terminal interface (CLI) and a sleek, modern dark-themed Graphical User Interface (GUI).

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Algorithms Implemented](#algorithms-implemented)
  - [1. Root-Finding Methods](#1-root-finding-methods)
    - [Bisection Method (`bisection.py`)](#bisection-method-bisectionpy)
    - [Newton-Raphson Method (`newton_raphson.py`)](#newton-raphson-method-newton_raphsonpy)
    - [Secant Method (`secant.py`)](#secant-method-secantpy)
  - [2. Linear Systems Solvers](#2-linear-systems-solvers)
    - [Jacobi Iteration Method (`jacobi.py`)](#jacobi-iteration-method-jacobipy)
    - [Gauss-Seidel Method (`gauss_seidel.py` / `sedil.py`)](#gauss-seidel-method-gauss_seidelpy--sedilpy)
  - [3. Utilities & Interfaces](#3-utilities--interfaces)
    - [Mathematical Utilities Engine (`math_utils.py`)](#mathematical-utilities-engine-math_utilspy)
    - [Modern GUI (`app.py`)](#modern-gui-apppy)
    - [Interactive CLI (`main.py`)](#interactive-cli-mainpy)
- [Project Structure](#project-structure)
- [Installation & Requirements](#installation--requirements)
- [Usage & Examples](#usage--examples)
  - [Launching via Terminal Menu](#launching-via-terminal-menu)
  - [Launching the Desktop GUI](#launching-the-desktop-gui)
  - [Sample Terminal Walkthroughs](#sample-terminal-walkthroughs)
- [Convergence & Theoretical Comparison](#convergence--theoretical-comparison)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Numerical analysis is at the heart of engineering and scientific computation. Real-world equations often lack analytical closed-form solutions or require iterative approximations for high-dimensional linear systems. 

**Math 3 Numerical Methods Suite** provides:
1. Exact and reliable numerical approximations for single-variable non-linear roots.
2. Iterative solvers for linear equation systems $A\mathbf{x} = \mathbf{b}$ with automated conditioning.
3. Flexible math expression parsing that supports natural human syntax like `2x`, `e^x`, `sin(x)`, and `x^3`.
4. Dual interaction modes: a lightweight command-line interface for terminal users and a reactive desktop GUI with iteration tracking tables.

---

## Key Features

- **Robust Expression Parser**: Evaluates mathematical strings into symbolic expressions and numerical functions using SymPy, with support for implicit multiplication, standard transcendental functions, and Euler's constant ($e$).
- **Automated Matrix Conditioning**: Automatically detects strictly and weakly diagonally dominant matrices and applies permutation algorithms to reorder rows for guaranteed iterative convergence.
- **Detailed Iteration Tracking**: Tabulates iteration counter, intermediate variable values, function residuals, and absolute/relative errors at every step.
- **Fault-Tolerant Execution**: Safeguards against division by zero, stationary points with zero derivative, diverging iterations, and invalid bracket intervals.
- **Modern Dark-Mode UI**: Built with `CustomTkinter` featuring tabbed layouts, custom styled Treeview data grids, and responsive user feedback.

---

## Algorithms Implemented

### 1. Root-Finding Methods

Root-finding algorithms locate values of $x$ such that $f(x) = 0$.

#### Bisection Method (`bisection.py`)
- **Theory**: Based on Bolzano's Intermediate Value Theorem. If a continuous function $f(x)$ on $[a, b]$ satisfies $f(a) \cdot f(b) < 0$, at least one root exists in the interval. The interval is repeatedly halved:
  $$c = \frac{a + b}{2}$$
- **Characteristics**:
  - Guaranteed linear convergence with rate $\mathcal{O}(2^{-n})$.
  - Absolute error bound: $\text{Error} = \frac{b - a}{2^n}$.
  - Robust against erratic initial guesses as long as the root is bracketed.
- **File**: `bisection.py`

#### Newton-Raphson Method (`newton_raphson.py`)
- **Theory**: Uses first-order Taylor expansion and the tangent line to iteratively project toward the $x$-intercept:
  $$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$
- **Characteristics**:
  - Automatically computes exact symbolic analytical derivatives $f'(x)$ using SymPy.
  - Quadratic convergence $\mathcal{O}(h^2)$ near simple roots.
  - Includes checks for zero derivatives ($f'(x) \approx 0$) to avoid division by zero.
- **File**: `newton_raphson.py`

#### Secant Method (`secant.py`)
- **Theory**: Eliminates the requirement to compute the derivative by approximating $f'(x_n)$ with the finite difference secant line between two previous estimates $x_{n-1}$ and $x_n$:
  $$x_{n+1} = x_n - f(x_n) \frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}$$
- **Characteristics**:
  - Superlinear convergence rate of the golden ratio $\phi \approx 1.618$.
  - Requires two initial points $x_0, x_1$, but does not require bracketing.
  - Includes divergence monitoring to prevent floating-point runaway.
- **File**: `secant.py`

---

### 2. Linear Systems Solvers

Iterative solvers find the solution vector $\mathbf{x} \in \mathbb{R}^n$ for systems of the form:
$$A\mathbf{x} = \mathbf{b}$$

#### Jacobi Iteration Method (`jacobi.py`)
- **Theory**: Decomposes $A$ into diagonal ($D$), strictly lower triangular ($L$), and strictly upper triangular ($U$) components. Updates all coordinates simultaneously based strictly on values from the previous iteration $k$:
  $$x_i^{(k+1)} = \frac{1}{a_{ii}} \left( b_i - \sum_{j \neq i} a_{ij} x_j^{(k)} \right)$$
- **Characteristics**:
  - Simultaneous/parallelizable updates.
  - Verifies diagonal dominance condition $\sum_{j \ne i} |a_{ij}| < |a_{ii}|$.
  - Reports maximum norm error $\max_i |x_i^{(k+1)} - x_i^{(k)}|$.
- **File**: `jacobi.py`

#### Gauss-Seidel Method (`gauss_seidel.py` / `sedil.py`)
- **Theory**: Uses successive displacements where newly calculated components $x_j^{(k+1)}$ for $j < i$ are immediately incorporated into the current iteration:
  $$x_i^{(k+1)} = \frac{1}{a_{ii}} \left( b_i - \sum_{j < i} a_{ij} x_j^{(k+1)} - \sum_{j > i} a_{ij} x_j^{(k)} \right)$$
- **Characteristics**:
  - Typically converges twice as fast as Jacobi for diagonally dominant or symmetric positive-definite systems.
  - Requires less memory as state updates occur in place.
- **Files**: `gauss_seidel.py` (primary implementation) and `sedil.py` (legacy alias redirect).

---

### 3. Utilities & Interfaces

#### Mathematical Utilities Engine (`math_utils.py`)
Acts as the algorithmic backbone for both the CLI and GUI modules:
- `parse_math_expression(expr_str)`:
  - Cleans and transforms text expressions into SymPy symbols and executable Python functions.
  - Translates implicit multiplications (e.g., `3x` $\to$ `3*x`, `x(x+1)` $\to$ `x*(x+1)`).
  - Handles exponent notation (`^` $\to$ `**`), mathematical constants (`e`, `pi`), and natural logarithm (`ln`).
  - Wraps the generated function in domain and numerical overflow checks.
- `check_diagonally_dominant(A)`:
  - Determines if matrix $A$ is strictly or weakly diagonally dominant.
- `make_diagonally_dominant(A, b)`:
  - Applies row permutation algorithms (exhaustive permutation for $n \le 8$ and greedy maximum-pivot selection for larger $n$) to restructure matrices for optimal convergence.

#### Modern GUI (`app.py`)
- Graphical application developed using `CustomTkinter` and `ttk.Treeview`.
- Features two primary tabs:
  1. **Root Finding**: Select algorithm, input $f(x)$, specify initial bounds/points, and view an interactive iteration table.
  2. **Linear Systems**: Select system dimensions ($2 \times 2$ to $5 \times 5$), input matrix coefficients and constant vectors, inspect diagonal dominance status, and view per-iteration convergence data.

#### Interactive CLI (`main.py`)
- Terminal entry point with an interactive numerical menu.
- Prompts for required numerical parameters, verifies conditions, formats results into ASCII tables, and provides a direct shortcut to launch the GUI.

---

## Project Structure

```text
math 3/
├── .gitignore              # Ignores __pycache__, .venv, .idea, and build artifacts
├── README.md               # Project documentation and user manual
├── requirements.txt        # Third-party dependencies
├── app.py                  # CustomTkinter GUI application
├── main.py                 # CLI interactive launcher and terminal menu
├── math_utils.py           # SymPy parsing, safe lambdification, and matrix heuristics
├── bisection.py            # Bisection root-finding algorithm
├── newton_raphson.py       # Newton-Raphson root-finding algorithm
├── secant.py               # Secant root-finding algorithm
├── jacobi.py               # Jacobi linear system solver
├── gauss_seidel.py         # Gauss-Seidel linear system solver
└── sedil.py                # Backward compatibility redirect to gauss_seidel.py
```

---

## Installation & Requirements

### Prerequisites
- **Python**: Version 3.10 or higher.
- **Tkinter**: Included in standard Python distributions on Windows/macOS. On Linux, ensure `python3-tk` is installed (`sudo pacman -S tk` on Arch, or `sudo apt install python3-tk` on Ubuntu/Debian).

### Step-by-Step Setup

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd "math 3"
   ```

2. **Create and activate a virtual environment:**
   - **Linux / macOS:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - **Windows:**
     ```cmd
     python -m venv .venv
     .venv\Scripts\activate
     ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## Usage & Examples

### Launching via Terminal Menu

Execute the main CLI runner:
```bash
python main.py
```

You will be presented with the interactive menu:
```text
==================================================
     حاسبة طرق Math 3 (التحليل العددي الشامل)
==================================================
1. Bisection Method (طريقة تنصيف الفترات)
2. Newton-Raphson Method (طريقة نيوتن-رافسون)
3. Secant Method (طريقة القاطع)
4. Jacobi Method (طريقة جاكوبي للأنظمة الخطية)
5. Gauss-Seidel Method (طريقة جاوس-سيدل)
6. تشغيل الواجهة الرسومية الحديثة (Launch GUI)
0. خروج
==================================================
```

### Launching the Desktop GUI

You can start the visual interface directly:
```bash
python app.py
```

---

### Sample Terminal Walkthroughs

#### Example 1: Bisection Method ($x^3 - x - 2 = 0$)
```text
اختر رقم الطريقة المطلوبة: 1

أدخل المعادلة بدلالة x: x^3 - x - 2
أدخل بداية الفترة (a): 1
أدخل نهاية الفترة (b): 2
أدخل نسبة الخطأ المطلوبة (افتراضي 0.001): 0.001
أقصى عدد تكرارات (افتراضي 50): 20

---------------------------------------------------------------------------
Iter  a           b           c (التقريب)      f(c)            Error       
---------------------------------------------------------------------------
1     1.00000     2.00000     1.500000        -0.125000       0.500000    
2     1.50000     2.00000     1.750000        1.609375        0.250000    
...
10    1.52051     1.52148     1.520996        -0.003906       0.000977    
---------------------------------------------------------------------------
[+] تم الوصول للحل: الجذر التقريبي = 1.520996 بعد 10 تكرار (الخطأ = 0.000977).
```

#### Example 2: Newton-Raphson Method ($e^x - 3x = 0$)
```text
اختر رقم الطريقة المطلوبة: 2

أدخل المعادلة بدلالة x: e^x - 3x
الدالة المقبولة:   f(x)  = exp(x) - 3*x
المشتقة المحسوبة: f'(x) = exp(x) - 3
أدخل النقطة الابتدائية (x0): 0
أدخل نسبة الخطأ المطلوبة (افتراضي 0.001): 0.0001

---------------------------------------------------------------------------
Iter  x_n           f(x_n)        f'(x_n)       x_(n+1)       Error       
---------------------------------------------------------------------------
1     0.00000       1.00000       -2.00000      0.50000       0.500000    
2     0.50000       0.14872       -1.35128      0.61006       0.110059    
3     0.61006       0.00994       -1.15949      0.61863       0.008575    
4     0.61863       0.00005       -1.14352      0.61906       0.000429    
5     0.61906       0.00000       -1.14324      0.61906       0.000001    
---------------------------------------------------------------------------
[+] تم الوصول للحل: الجذر التقريبي = 0.619061 بعد 5 تكرارات (الخطأ = 0.000001).
```

#### Example 3: Gauss-Seidel Method ($3 \times 3$ System)
Consider the linear system:
$$\begin{aligned}
4x_1 - x_2 + x_3 &= 7 \\
4x_1 - 8x_2 + x_3 &= -21 \\
-2x_1 + x_2 + 5x_3 &= 15
\end{aligned}$$

```text
اختر رقم الطريقة المطلوبة: 5

أدخل عدد المعادلات/المتغيرات (n): 3
معاملات المعادلة 1: 4 -1 1
معاملات المعادلة 2: 4 -8 1
معاملات المعادلة 3: -2 1 5
القيم: 7 -21 15

[معاينة السيادة القطرية]: المصفوفة مهيمنة قطرياً بشكل صارم
----------------------------------------------------------------------
Iter  المتجه x                                       Max Error      
----------------------------------------------------------------------
1     [1.75, 3.5, 3.0]                               3.500000       
2     [1.875, 3.9375, 2.9625]                        0.437500       
3     [1.99375, 3.99219, 2.99906]                    0.118750       
...
----------------------------------------------------------------------
[+] تم الوصول للحل بعد 7 تكرارات بنسبة خطأ 0.00052:
x1 = 2.000000
x2 = 4.000000
x3 = 3.000000
```

---

## Convergence & Theoretical Comparison

| Algorithm | Type | Requirements | Convergence Order | Guarantee |
| :--- | :--- | :--- | :--- | :--- |
| **Bisection** | Root-Finding | Continuous $f(x)$, $f(a) \cdot f(b) < 0$ | Linear ($\mathcal{O}(2^{-n})$) | Always guaranteed if bracketed |
| **Newton-Raphson** | Root-Finding | Differentiable $f(x)$, $f'(x) \neq 0$ | Quadratic ($\mathcal{O}(h^2)$) | Sensitive to initial guess $x_0$ |
| **Secant** | Root-Finding | Continuous $f(x)$, two initial points | Superlinear ($\approx 1.618$) | Faster than bisection, no derivatives |
| **Jacobi** | Linear Solver | Diagonally dominant $A$ | Linear | Guaranteed for strictly dominant $A$ |
| **Gauss-Seidel** | Linear Solver | Diagonally dominant or SPD $A$ | Linear (faster than Jacobi) | Guaranteed for strictly dominant $A$ |

---

## Contributing

Contributions, bug reports, and pull requests are welcome! If you encounter issues or have suggestions for additional methods (e.g., Runge-Kutta, LU Decomposition, Lagrange Interpolation), feel free to open an issue or submit a PR.

---

## License

This project is licensed under the [MIT License](LICENSE).
