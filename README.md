# Math 3 - Numerical Analysis Suite (CustomTkinter GUI)

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Arch%20Linux%20%7C%20Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)](https://github.com/mhmedreded-ai/numerical-methods-toolkit)
[![GUI Framework](https://img.shields.io/badge/GUI-CustomTkinter%206.0-darkblue.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![Math Engine](https://img.shields.io/badge/Engine-SymPy%201.14-orange.svg)](https://www.sympy.org/)
[![Visualization](https://img.shields.io/badge/Plotting-Matplotlib%203.11-success.svg)](https://matplotlib.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A high-performance, cross-platform numerical analysis desktop suite engineered with **Python**, **CustomTkinter**, **SymPy**, and **Matplotlib**. Designed for university-level engineering mathematics (Math 3 / Numerical Methods), it combines mathematically rigorous algorithm implementations, an interactive command-line interface (CLI), and a modern dark-themed Graphical User Interface (GUI) with embedded real-time curve plotting and bidirectional Arabic text rendering.

---

## Table of Contents

- [Architecture & Directory Structure](#architecture--directory-structure)
- [Mathematical Methods Explained](#mathematical-methods-explained)
  - [1. Root Finding](#1-root-finding)
    - [Bisection Method](#bisection-method)
    - [Newton-Raphson Method](#newton-raphson-method)
    - [Secant Method](#secant-method)
    - [Modified Secant Method](#modified-secant-method)
  - [2. Linear Systems Solvers](#2-linear-systems-solvers)
    - [Jacobi Iteration Method](#jacobi-iteration-method)
    - [Gauss-Seidel Method](#gauss-seidel-method)
    - [Strict Diagonal Dominance Condition](#strict-diagonal-dominance-condition)
  - [3. Regression & Curve Fitting](#3-regression--curve-fitting)
    - [Linear Regression](#linear-regression)
    - [Polynomial Regression](#polynomial-regression)
    - [Exponential Fitting](#exponential-fitting)
    - [Power Function Fitting](#power-function-fitting)
    - [Statistical Metrics](#statistical-metrics)
- [System Requirements & Arch Linux Setup](#system-requirements--arch-linux-setup)
  - [System Prerequisites](#system-prerequisites)
  - [Virtual Environment & Installation](#virtual-environment--installation)
  - [Arabic Text Rendering & BiDi Support](#arabic-text-rendering--bidi-support)
- [How to Run the Application](#how-to-run-the-application)
- [Status & Role of `main.py`](#status--role-of-mainpy)
- [Troubleshooting & Common Pitfalls](#troubleshooting--common-pitfalls)
  - [1. Missing Tkinter on Arch Linux](#1-missing-tkinter-on-arch-linux)
  - [2. IDE Interpreter Path Resolution](#2-ide-interpreter-path-resolution)
  - [3. Wayland / Hyprland Display Scaling](#3-wayland--hyprland-display-scaling)
- [License](#license)

---

## Architecture & Directory Structure

```
numerical-methods-toolkit/
├── app.py                  # Primary CustomTkinter Desktop Application (GUI entry point)
├── main.py                 # Interactive Terminal Menu Runner (CLI entry point)
├── math_utils.py           # SymPy parsing engine, safety lambdifier, diagonal dominance tools
├── bisection.py            # Bisection algorithm + CLI solver
├── newton_raphson.py       # Newton-Raphson algorithm with symbolic derivative + CLI solver
├── secant.py               # Classical Secant algorithm + CLI solver
├── modified_secant.py      # Modified Secant with fractional perturbation + CLI solver
├── jacobi.py               # Jacobi linear system solver + CLI solver
├── gauss_seidel.py         # Gauss-Seidel linear system solver + CLI solver
├── sedil.py                # Legacy redirect alias for gauss_seidel.py
├── regression.py           # Curve fitting engine (Linear, Poly, Exp, Power) + CLI solver
├── run.sh                  # One-click executable launcher for Linux and macOS
├── run.bat                 # One-click launcher for Windows (UTF-8 enabled)
├── requirements.txt        # Pinned and cross-platform compatible Python dependencies
├── README.md               # English technical documentation and manual
├── README_AR.md            # Complete Arabic documentation (النسخة العربية الكاملة)
└── LICENSE                 # MIT License file
```

### Module Responsibilities

| File | Type | Primary Role & Responsibility |
| :--- | :--- | :--- |
| [`app.py`](file:///home/myarch/Projects/math%203/app.py) | **GUI Core** | Implements `NumericalApp(ctk.CTk)`: 3 tabbed interfaces (Roots, Linear, Regression), Treeview styling, inputs, error popups, and embedded Matplotlib visualizer. |
| [`main.py`](file:///home/myarch/Projects/math%203/main.py) | **CLI Core** | Provides an 8-option interactive terminal menu to run all algorithms headlessly or launch the GUI. |
| [`math_utils.py`](file:///home/myarch/Projects/math%203/math_utils.py) | **Utility Engine** | SymPy string expression parser (with implicit multiplication like `2x`), safe mathematical evaluation guards, and diagonal dominance permutation algorithms. |
| [`bisection.py`](file:///home/myarch/Projects/math%203/bisection.py) | **Algorithm** | Implements the interval halving bracketing root-finding method. |
| [`newton_raphson.py`](file:///home/myarch/Projects/math%203/newton_raphson.py) | **Algorithm** | Implements analytical derivative projection root-finding. |
| [`secant.py`](file:///home/myarch/Projects/math%203/secant.py) | **Algorithm** | Implements two-point finite difference secant root-finding. |
| [`modified_secant.py`](file:///home/myarch/Projects/math%203/modified_secant.py) | **Algorithm** | Implements single-point fractional perturbation secant root-finding. |
| [`jacobi.py`](file:///home/myarch/Projects/math%203/jacobi.py) | **Algorithm** | Implements simultaneous relaxation for linear systems $A\mathbf{x} = \mathbf{b}$. |
| [`gauss_seidel.py`](file:///home/myarch/Projects/math%203/gauss_seidel.py) | **Algorithm** | Implements successive in-place displacements for linear systems. |
| [`regression.py`](file:///home/myarch/Projects/math%203/regression.py) | **Algorithm** | Implements Gaussian elimination with partial pivoting, normal equation generation, Least-Squares optimization, and statistical indicators ($R^2, S_{y/x}, \text{SSE}$). |

---

## Mathematical Methods Explained

### 1. Root Finding

Root-finding methods solve for real values $x^*$ such that $f(x^*) = 0$.

#### Bisection Method
- **Theory**: Based on Bolzano's Intermediate Value Theorem. Given continuous $f(x)$ on $[a, b]$ with $f(a) \cdot f(b) < 0$, the root is iteratively bracketed:
  $$c = \frac{a + b}{2}$$
- **Sub-interval Update**:
  - If $f(a) \cdot f(c) < 0 \implies b = c$.
  - Else $a = c$.
- **Stopping Criteria**: $|f(c)| < \text{tol}$ or $(b - a)/2 < \text{tol}$.
- **Convergence**: Guaranteed linear convergence with rate $\mathcal{O}(2^{-n})$. Error at step $n$ is bounded by $(b - a)/2^n$.

#### Newton-Raphson Method
- **Theory**: Derived from the 1st-order Taylor expansion $f(x) \approx f(x_n) + f'(x_n)(x - x_n)$. Projecting the tangent line to the $x$-axis yields:
  $$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$
- **Stopping Criteria**: $|f(x_{n+1})| < \text{tol}$ or $|x_{n+1} - x_n| < \text{tol}$.
- **Convergence**: Quadratic $\mathcal{O}(h^2)$ near simple roots.
- **Edge Cases**: Fails if derivative vanishes ($f'(x_n) \approx 0$).

#### Secant Method
- **Theory**: Replaces analytical differentiation in Newton-Raphson with the finite backward difference quotient across two points $x_{n-1}$ and $x_n$:
  $$x_{n+1} = x_n - f(x_n) \cdot \frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}$$
- **Stopping Criteria**: $|f(x_{n+1})| < \text{tol}$ or $|x_{n+1} - x_n| < \text{tol}$.
- **Convergence**: Superlinear with order equal to the golden ratio $\phi \approx 1.618$. Requires no derivatives.

#### Modified Secant Method
- **Theory**: Overcomes the two-point requirement of the classical secant method by perturbing a single point $x_i$ by a fractional fraction $\delta$ (default $\delta = 0.01$):
  $$x_{i+1} = x_i - \frac{\delta \cdot x_i \cdot f(x_i)}{f(x_i + \delta \cdot x_i) - f(x_i)}$$
- **Stopping Criteria**: $|f(x_{i+1})| < \text{tol}$ or $|x_{i+1} - x_i| < \text{tol}$.
- **Characteristics**: Only requires a single starting value $x_0$. Includes zero-pivot handling for $x_i \approx 0$ by setting perturbation step $h = \delta$.

---

### 2. Linear Systems Solvers

Iterative solvers approximate the solution $\mathbf{x} \in \mathbb{R}^n$ of the linear system:
$$A\mathbf{x} = \mathbf{b}$$

#### Jacobi Iteration Method
- **Theory**: Decomposes $A = D + L + U$ (Diagonal, strictly Lower, strictly Upper). All coordinates are updated simultaneously:
  $$x_i^{(k+1)} = \frac{1}{a_{ii}} \left( b_i - \sum_{j \neq i} a_{ij} x_j^{(k)} \right)$$
- **Memory**: Requires two separate state vectors ($\mathbf{x}^{(k)}$ and $\mathbf{x}^{(k+1)}$).

#### Gauss-Seidel Method
- **Theory**: Incorporates newly calculated components $x_j^{(k+1)}$ for $j < i$ immediately into the ongoing evaluation of row $i$:
  $$x_i^{(k+1)} = \frac{1}{a_{ii}} \left( b_i - \sum_{j < i} a_{ij} x_j^{(k+1)} - \sum_{j > i} a_{ij} x_j^{(k)} \right)$$
- **Memory**: Updates in-place using a single vector $\mathbf{x}$. Typically converges twice as fast as Jacobi.

#### Strict Diagonal Dominance Condition
A sufficient condition for both Jacobi and Gauss-Seidel convergence is that $A$ is **strictly diagonally dominant**:
$$|a_{ii}| > \sum_{j \neq i} |a_{ij}| \quad \forall i \in \{1, \dots, n\}$$
The toolkit includes [`make_diagonally_dominant(A, b)`](file:///home/myarch/Projects/math%203/math_utils.py) which automatically evaluates row sums and applies row permutations to ensure the convergence condition is met before solving.

---

### 3. Regression & Curve Fitting

Fits an empirical curve $y \approx f(x)$ to discrete observations $\{(x_i, y_i)\}_{i=1}^n$ by minimizing the residual sum of squares:
$$\min \sum_{i=1}^n (y_i - f(x_i))^2$$

#### Linear Regression
Fits $y = a_0 + a_1 x$ via analytical 2x2 normal equations:
$$a_1 = \frac{n \sum x_i y_i - \sum x_i \sum y_i}{n \sum x_i^2 - (\sum x_i)^2}, \quad a_0 = \bar{y} - a_1 \bar{x}$$

#### Polynomial Regression
Fits $y = a_0 + a_1 x + a_2 x^2 + \dots + a_m x^m$ by constructing the $(m+1) \times (m+1)$ symmetric normal equations system:
$$\begin{bmatrix}
n & \sum x_i & \dots & \sum x_i^m \\
\sum x_i & \sum x_i^2 & \dots & \sum x_i^{m+1} \\
\vdots & \vdots & \ddots & \vdots \\
\sum x_i^m & \sum x_i^{m+1} & \dots & \sum x_i^{2m}
\end{bmatrix}
\begin{bmatrix} a_0 \\ a_1 \\ \vdots \\ a_m \end{bmatrix}
=
\begin{bmatrix} \sum y_i \\ \sum x_i y_i \\ \vdots \\ \sum x_i^m y_i \end{bmatrix}$$
Solved via Gaussian elimination with partial pivoting in `regression.py`.

#### Exponential Fitting
Fits $y = a \cdot e^{b x}$ via logarithmic linearization $\ln(y) = \ln(a) + b x$ (requires $y_i > 0$).

#### Power Function Fitting
Fits $y = a \cdot x^b$ via logarithmic linearization $\ln(y) = \ln(a) + b \ln(x)$ (requires $x_i > 0, y_i > 0$).

#### Statistical Metrics
- **Total Sum of Squares**: $S_t = \sum (y_i - \bar{y})^2$
- **Residual Sum of Squares**: $S_r = \text{SSE} = \sum (y_i - \hat{y}_i)^2$
- **Coefficient of Determination**: $R^2 = \frac{S_t - S_r}{S_t} \in [0, 1]$
- **Correlation Coefficient**: $r = \pm \sqrt{R^2}$
- **Standard Error of the Estimate**: $S_{y/x} = \sqrt{\frac{S_r}{n - (m + 1)}}$

---

## System Requirements & Arch Linux Setup

### System Prerequisites
- **Operating System**: Arch Linux (Linux 6.x / 7.x), Wayland/Hyprland or X11. (Also fully supports Ubuntu, Fedora, Debian, Windows 10/11, macOS).
- **Python**: Version **3.10** or higher.
- **Tcl/Tk**: Required by Tkinter C-extensions on Linux.

### Arch Linux System Packages
Arch Linux packages Python and Tk separately. You must install `tk`:
```bash
sudo pacman -S tk python
```

### Virtual Environment & Installation
From the project root:

```bash
# 1. Create a dedicated virtual environment
python3 -m venv .venv

# 2. Activate the environment
source .venv/bin/activate

# 3. Upgrade pip to ensure latest wheel resolution
pip install --upgrade pip

# 4. Install all dependencies
pip install -r requirements.txt
```

### Arabic Text Rendering & BiDi Support
Tkinter on Linux natively lacks OpenType/Complex Text Layout (CTL) shaping for Arabic script, causing glyphs to appear disconnected and reversed from left to right (e.g. `ةلداعملا` instead of `المعادلة`).

This repository completely resolves this issue by incorporating:
1. `arabic-reshaper`: Connects Arabic characters according to their initial, medial, final, or isolated position in words.
2. `python-bidi`: Applies the Unicode Bidirectional Algorithm (UBA) to invert display order for Right-to-Left (RTL) reading.
3. Central `ar(text)` helper function: Automatically handles all static labels, placeholders, Treeview headers, and plot legends.

---

## How to Run the Application

### 1. Launch the Graphical Desktop App (Recommended)
```bash
# Ensure virtual environment is active
./.venv/bin/python app.py

# Alternatively, using the one-click shell script:
./run.sh
```

### 2. Launch the Interactive Terminal Interface (CLI)
```bash
./.venv/bin/python main.py
```

---

## Status & Role of `main.py`

An architectural audit of `main.py` confirms the following:
- **Status**: Active, fully tracked in Git (`main`), and synchronized with the latest methods.
- **Role**: `main.py` is the official **CLI entry point**. It is **not** legacy or obsolete.
- **Purpose**:
  - Serves terminal users who work in SSH, server, or headless environments without an active display server.
  - Option 8 in `main.py` (`Launch GUI`) allows seamless launching of `app.py` from within the CLI.
  - Each mathematical method provides both a pure algorithmic function (imported by `app.py`) and a user-friendly CLI driver (run by `main.py`).

---

## Troubleshooting & Common Pitfalls

### 1. Missing Tkinter on Arch Linux
- **Symptom**: `ImportError: libtk8.6.so: cannot open shared object file: No such file or directory` or `ModuleNotFoundError: No module named '_tkinter'`.
- **Cause**: Minimal or arch-based Linux installs do not include Tk by default.
- **Solution**: Install system Tk:
  ```bash
  sudo pacman -S tk
  ```
  *Note*: `app.py` also includes an automated fallback check in `.venv/lib` for bundled shared objects.

### 2. IDE Interpreter Path Resolution
- **Symptom**: Running from inside Antigravity or VS Code yields `ModuleNotFoundError: No module named 'customtkinter'`.
- **Cause**: The IDE selected the global system `/bin/python` instead of the project `.venv`.
- **Solution**: Configure the workspace to use `.venv`:
  - Verify `.vscode/settings.json`:
    ```json
    {
      "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
    }
    ```
  - Open the command palette (`Ctrl+Shift+P`), choose **Python: Select Interpreter**, and select `./.venv/bin/python`.

### 3. Wayland / Hyprland Display Scaling
- **Symptom**: Window appears too large, blurry, or tiny on 2K/4K monitors under Hyprland / Wayland.
- **Solution**: CustomTkinter widget scaling can be customized via the `CTK_SCALING` environment variable:
  ```bash
  CTK_SCALING=1.0 ./.venv/bin/python app.py
  # or for 125% scaling:
  CTK_SCALING=1.25 ./.venv/bin/python app.py
  ```

---

## License

This project is licensed under the [MIT License](LICENSE).
