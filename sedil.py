"""
Legacy compatibility alias module for Gauss-Seidel.

Maintains backward compatibility with earlier course naming conventions ('sedil.py')
by re-exporting the implementation from gauss_seidel.py.
"""

from gauss_seidel import gauss_seidel, solve_gauss_seidel

__all__ = ["gauss_seidel", "solve_gauss_seidel"]

if __name__ == "__main__":
    solve_gauss_seidel()
