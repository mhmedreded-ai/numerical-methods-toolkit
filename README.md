# Numerical Methods & Analysis Toolkit (Math 3)

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/mhmedreded-ai/numerical-methods-toolkit)
[![GUI](https://img.shields.io/badge/GUI-CustomTkinter-darkblue.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![Engine](https://img.shields.io/badge/Math%20Engine-SymPy-orange.svg)](https://www.sympy.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A comprehensive, fully cross-platform Python numerical analysis suite for root-finding, solving linear systems, and performing regression and curve fitting. The project pairs rigorous mathematical algorithms with both an interactive terminal interface (CLI) and a modern dark-themed Graphical User Interface (GUI) with embedded Matplotlib visualizations.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Algorithms Implemented](#algorithms-implemented)
  - [1. Root-Finding Methods](#1-root-finding-methods)
    - [Bisection Method (`bisection.py`)](#bisection-method-bisectionpy)
    - [Newton-Raphson Method (`newton_raphson.py`)](#newton-raphson-method-newton_raphsonpy)
    - [Secant Method (`secant.py`)](#secant-method-secantpy)
    - [Modified Secant Method (`modified_secant.py`)](#modified-secant-method-modified_secantpy)
  - [2. Linear Systems Solvers](#2-linear-systems-solvers)
    - [Jacobi Iteration Method (`jacobi.py`)](#jacobi-iteration-method-jacobipy)
    - [Gauss-Seidel Method (`gauss_seidel.py` / `sedil.py`)](#gauss-seidel-method-gauss_seidelpy--sedilpy)
  - [3. Curve Fitting & Regression](#3-curve-fitting--regression)
    - [Linear Regression](#linear-regression)
    - [Polynomial Regression](#polynomial-regression)
    - [Exponential Fitting](#exponential-fitting)
    - [Power Function Fitting](#power-function-fitting)
  - [4. Interfaces & Engine](#4-interfaces--engine)
    - [Mathematical Utilities Engine (`math_utils.py`)](#mathematical-utilities-engine-math_utilspy)
    - [Modern GUI (`app.py`)](#modern-gui-apppy)
    - [Interactive CLI (`main.py`)](#interactive-cli-mainpy)
- [Cross-Platform Installation](#cross-platform-installation)
  - [Windows](#windows)
  - [Linux (Ubuntu, Debian, Arch, Fedora)](#linux-ubuntu-debian-arch-fedora)
  - [macOS](#macos)
- [Usage & Examples](#usage--examples)
  - [One-Click Launchers](#one-click-launchers)
  - [Terminal Menu Walkthrough](#terminal-menu-walkthrough)
- [Convergence & Theoretical Comparison](#convergence--theoretical-comparison)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Numerical analysis is at the heart of engineering and scientific computation. Real-world mathematical equations often lack analytical closed-form solutions or require iterative approximations for linear systems and empirical data fitting.

**Math 3 Numerical Methods Suite** provides:
1. Exact and reliable numerical approximations for single-variable non-linear roots.
2. Iterative solvers for linear equation systems $A\mathbf{x} = \mathbf{b}$ with automated conditioning.
3. High-precision curve fitting and regression models with comprehensive statistical correlation metrics ($R^2$, $S_{y/x}$, $\text{SSE}$).
4. Flexible math expression parsing that supports natural human syntax like `2x`, `e^x`, `sin(x)`, and `x^3`.
5. Seamless cross-platform execution on Windows, Linux, and macOS with bidirectional Arabic shaping (`arabic-reshaper` + `python-bidi`).

---

## Key Features

- **Robust Expression Parser**: Evaluates mathematical strings into symbolic expressions and numerical functions using SymPy, with support for implicit multiplication, standard transcendental functions, and Euler's constant ($e$).
- **Automated Matrix Conditioning**: Automatically detects strictly and weakly diagonally dominant matrices and applies permutation algorithms to reorder rows for guaranteed iterative convergence.
- **Statistical Quality Metrics**: Computes model coefficients, standard error of the estimate ($S_{y/x}$), coefficient of determination ($R^2$), and residual sum of squares ($S_r$).
- **Detailed Iteration Tracking**: Tabulates iteration counter, intermediate variable values, function residuals, and absolute/relative errors at every step.
- **Fault-Tolerant Execution**: Safeguards against division by zero, stationary points with zero derivative, diverging iterations, and invalid bracket intervals.
- **Embedded Visualizer**: Embedded Matplotlib canvas styled in dark theme (`#23272e` / `#1e2227`) for real-time scatter and regression curve plotting.
- **Cross-Platform Compatibility**: Native font fallback (Segoe UI on Windows, Geeza Pro on macOS, Noto Sans / DejaVu on Linux) and UTF-8 terminal encoding configuration.

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
- **File**: [`bisection.py`](file:///home/myarch/Projects/math%203/bisection.py)

#### Newton-Raphson Method (`newton_raphson.py`)
- **Theory**: Uses first-order Taylor expansion and the tangent line to iteratively project toward the $x$-intercept:
  $$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$
- **Characteristics**:
  - Automatically computes exact symbolic analytical derivatives $f'(x)$ using SymPy.
  - Quadratic convergence $\mathcal{O}(h^2)$ near simple roots.
  - Includes checks for zero derivatives ($f'(x) \approx 0$) to avoid division by zero.
- **File**: [`newton_raphson.py`](file:///home/myarch/Projects/math%203/newton_raphson.py)

#### Secant Method (`secant.py`)
- **Theory**: Eliminates the requirement to compute the derivative by approximating $f'(x_n)$ with the finite difference secant line between two previous estimates $x_{n-1}$ and $x_n$:
  $$x_{n+1} = x_n - f(x_n) \frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}$$
- **Characteristics**:
  - Superlinear convergence rate of the golden ratio $\phi \approx 1.618$.
  - Requires two initial points $x_0, x_1$, but does not require bracketing.
  - Includes divergence monitoring to prevent floating-point runaway.
- **File**: [`secant.py`](file:///home/myarch/Projects/math%203/secant.py)

#### Modified Secant Method (`modified_secant.py`)
- **Theory**: Uses a single initial estimate $x_i$ and a fractional perturbation parameter $\delta$ (default $0.01$) rather than requiring two separate points:
  $$x_{i+1} = x_i - \frac{\delta \cdot x_i \cdot f(x_i)}{f(x_i + \delta \cdot x_i) - f(x_i)}$$
- **Characteristics**:
  - Only needs a single starting value $x_0$.
  - Avoids computing analytical derivatives while converging with superlinear efficiency.
  - Gracefully handles stationary denominators.
- **File**: [`modified_secant.py`](file:///home/myarch/Projects/math%203/modified_secant.py)

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
- **File**: [`jacobi.py`](file:///home/myarch/Projects/math%203/jacobi.py)

#### Gauss-Seidel Method (`gauss_seidel.py` / `sedil.py`)
- **Theory**: Uses successive displacements where newly calculated components $x_j^{(k+1)}$ for $j < i$ are immediately incorporated into the current iteration:
  $$x_i^{(k+1)} = \frac{1}{a_{ii}} \left( b_i - \sum_{j < i} a_{ij} x_j^{(k+1)} - \sum_{j > i} a_{ij} x_j^{(k)} \right)$$
- **Characteristics**:
  - Typically converges twice as fast as Jacobi for diagonally dominant or symmetric positive-definite systems.
  - Requires less memory as state updates occur in place.
- **Files**: [`gauss_seidel.py`](file:///home/myarch/Projects/math%203/gauss_seidel.py) and [`sedil.py`](file:///home/myarch/Projects/math%203/sedil.py) (legacy alias redirect).

---

### 3. Curve Fitting & Regression (`regression.py`)

Implements standard curve fitting methods via normal equations and logarithmic linearization:

- **Linear Regression**:
  $$y = a_0 + a_1 x$$
- **Polynomial Regression**:
  $$y = a_0 + a_1 x + a_2 x^2 + \dots + a_m x^m$$
  Builds and solves the $(m+1) \times (m+1)$ Vandermonde-normal system using Gaussian elimination with partial pivoting.
- **Exponential Regression**:
  $$y = a \cdot e^{b x} \quad \Longleftarrow \quad \ln(y) = \ln(a) + b x$$
- **Power Function Regression**:
  $$y = a \cdot x^b \quad \Longleftarrow \quad \ln(y) = \ln(a) + b \ln(x)$$

**Computed Statistical Indicators:**
- $S_t = \sum (y_i - \bar{y})^2$ (Total sum of squares)
- $S_r = \text{SSE} = \sum (y_i - \hat{y}_i)^2$ (Residual sum of squares)
- $S_{y/x} = \sqrt{\frac{S_r}{n - (m + 1)}}$ (Standard error of the estimate)
- $R^2 = \frac{S_t - S_r}{S_t}$ (Coefficient of determination)
- Residual evaluation table comparing actual $y_i$ vs predicted $\hat{y}_i$ and residuals $e_i$.
- **File**: [`regression.py`](file:///home/myarch/Projects/math%203/regression.py)

---

### 4. Interfaces & Engine

#### Mathematical Utilities Engine (`math_utils.py`)
- `parse_math_expression(expr_str)`: Normalizes implicit multiplication, transforms powers, maps constants, and builds callable numerical lambdas.
- `check_diagonally_dominant(A)`: Evaluates strict and weak diagonal dominance.
- `make_diagonally_dominant(A, b)`: Applies optimal row permutations to ensure convergence before iterative solving.
- **File**: [`math_utils.py`](file:///home/myarch/Projects/math%203/math_utils.py)

#### Modern GUI (`app.py`)
- Built with `CustomTkinter`, `ttk.Treeview`, and `matplotlib.backends.backend_tkagg.FigureCanvasTkAgg`.
- Three main tabs:
  1. **Root Finding (جذور المعادلات)**: Bisection, Newton-Raphson, Secant, and Modified Secant.
  2. **Linear Systems (الأنظمة الخطية)**: Jacobi and Gauss-Seidel with automated diagonal dominance validation.
  3. **Regression & Curve Fitting (الانحدار ومواءمة المنحنيات)**: Model selector, degree spinner, residual data grid, and interactive dark-themed Matplotlib plot.
- **File**: [`app.py`](file:///home/myarch/Projects/math%203/app.py)

#### Interactive CLI (`main.py`)
- Terminal-driven numerical suite menu with 8 selectable workflows.
- Fully compatible with standard UTF-8 terminals across Windows, Linux, and macOS.
- **File**: [`main.py`](file:///home/myarch/Projects/math%203/main.py)

---

## Cross-Platform Installation

### Windows
1. Install **Python 3.10+** from [python.org](https://www.python.org/downloads/) (check the box **"Add Python to PATH"** during setup).
2. Clone or download the repository:
   ```cmd
   git clone https://github.com/mhmedreded-ai/numerical-methods-toolkit.git
   cd numerical-methods-toolkit
   ```
3. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
4. Double-click `run.bat` or run:
   ```cmd
   python app.py
   ```

### Linux (Ubuntu, Debian, Arch, Fedora)
Tkinter requires the standard `tk` system package on Linux:
- **Ubuntu / Debian**:
  ```bash
  sudo apt update && sudo apt install python3 python3-pip python3-tk
  ```
- **Arch Linux**:
  ```bash
  sudo pacman -S tk python
  ```
- **Fedora**:
  ```bash
  sudo dnf install python3 python3-tkinter
  ```

Then install the dependencies:
```bash
pip install -r requirements.txt
./run.sh
# or
python3 app.py
```

### macOS
1. Install Python via Homebrew (recommended) to include Tkinter bindings:
   ```bash
   brew install python python-tk
   ```
2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
3. Launch via:
   ```bash
   ./run.sh
   # or
   python3 app.py
   ```

---

## Usage & Examples

### One-Click Launchers
- **Windows**: Double-click [`run.bat`](file:///home/myarch/Projects/math%203/run.bat)
- **Linux / macOS**: Run `./run.sh`

### Terminal Menu Walkthrough
Execute `python main.py` to open the terminal menu:
```text
==================================================
     حاسبة طرق Math 3 (التحليل العددي الشامل)
==================================================
1. Bisection Method (طريقة تنصيف الفترات)
2. Newton-Raphson Method (طريقة نيوتن-رافسون)
3. Secant Method (طريقة القاطع)
4. Modified Secant Method (طريقة القاطع المعدلة)
5. Jacobi Method (طريقة جاكوبي للأنظمة الخطية)
6. Gauss-Seidel Method (طريقة جاوس-سيدل)
7. Curve Fitting & Regression (الانحدار ومواءمة المنحنيات)
8. تشغيل الواجهة الرسومية الحديثة (Launch GUI)
0. خروج
==================================================
```

---

## Convergence & Theoretical Comparison

| Algorithm | Domain | Key Requirements | Convergence Order | Guarantee |
| :--- | :--- | :--- | :--- | :--- |
| **Bisection** | Root Finding | Continuous $f(x)$, $f(a) \cdot f(b) < 0$ | Linear ($\mathcal{O}(2^{-n})$) | Guaranteed if bracketed |
| **Newton-Raphson** | Root Finding | Differentiable $f(x)$, $f'(x) \neq 0$ | Quadratic ($\mathcal{O}(h^2)$) | Fast near simple root |
| **Secant** | Root Finding | Continuous $f(x)$, 2 initial points | Superlinear ($\approx 1.618$) | Derivative-free |
| **Modified Secant**| Root Finding | Continuous $f(x)$, 1 point $x_0$, perturbation $\delta$ | Superlinear ($\approx 1.618$) | 1 point, derivative-free |
| **Jacobi** | Linear Systems| Strictly diagonally dominant $A$ | Linear | Simultaneous updates |
| **Gauss-Seidel** | Linear Systems| Strictly diagonally dominant or SPD $A$ | Linear ($\approx 2\times$ Jacobi) | Successive updates |
| **Regression** | Curve Fitting | $n \ge m + 1$ data points | Direct algebraic solution | Optimal least-squares fit |

---

## Contributing

Contributions, bug reports, and pull requests are welcome! If you encounter issues or have suggestions for additional methods (e.g., Runge-Kutta, LU Decomposition, Lagrange Interpolation), feel free to open an issue or submit a PR.

---

## License

This project is licensed under the [MIT License](LICENSE).
