#!/usr/bin/env python3
"""
(b2) PySR-based discovery pipeline for TFPT decoders.

PySR fits y = f(X) over data, so the legitimate use here is to have it
REDISCOVER the TFPT decoder functions from samples (proof that an automated
symbolic-regression engine recovers the theory's closed forms), and then to
point the same engine at residuals / gaps.

Run (inside the venv):  python pysr_pipeline.py
First run triggers a one-time Julia backend install + precompile (minutes).

Tasks:
  T1  rediscover  lambda_C(phi0) = sqrt(phi0*(1-phi0))
  T2  rediscover  Omega_b(phi0)  = phi0*(1 - 1/(4*pi))      (linear)
  T3  rediscover  beta_rad(phi0) = phi0/(4*pi)
Each prints PySR's best low-complexity equation; success = it recovers the
known TFPT form. The point: a generic ML tool, given only numeric samples,
reconstructs the theory's decoders -> the grammar is learnable, and the same
loop can be aimed at the open gaps (theta12, ...) with proper significance
control (see symbolic_search.py for the look-elsewhere discipline).
"""
import numpy as np

PI = np.pi

def make_models():
    from pysr import PySRRegressor
    return PySRRegressor(
        niterations=60,
        binary_operators=["+", "-", "*", "/"],
        unary_operators=["sqrt", "square"],
        maxsize=14,
        population_size=40,
        progress=False,
        verbosity=0,
        model_selection="accuracy",
        constraints={"sqrt": 4, "square": 4},
    )

def run_task(name, xgen, yfun, truth):
    from pysr import PySRRegressor
    X = xgen()
    y = yfun(X)
    m = make_models()
    m.fit(X, y)
    best = m.get_best()
    print(f"\n[{name}] truth: {truth}")
    print(f"  PySR best: {best['equation']}   (loss={best['loss']:.2e}, complexity={best['complexity']})")
    return m

if __name__ == "__main__":
    try:
        import pysr  # noqa
    except Exception as e:
        print("PySR not importable:", e)
        raise SystemExit(1)

    # sample phi0 over a neighbourhood of the TFPT value
    def xgen():
        rng = np.random.default_rng(0)
        return rng.uniform(0.02, 0.09, size=(200, 1))  # column: phi0

    print("Task T1: rediscover lambda_C = sqrt(phi0*(1-phi0))")
    run_task("T1 lambda_C", xgen,
             lambda X: np.sqrt(X[:,0]*(1-X[:,0])), "sqrt(x*(1-x))")

    print("\nTask T2: rediscover Omega_b = phi0*(1 - 1/(4pi))")
    run_task("T2 Omega_b", xgen,
             lambda X: X[:,0]*(1-1/(4*PI)), "x*(1 - 1/(4*pi)) = 0.92042*x")

    print("\nTask T3: rediscover beta_rad = phi0/(4pi)")
    run_task("T3 beta_rad", xgen,
             lambda X: X[:,0]/(4*PI), "x/(4*pi) = 0.079577*x")

    print("\nDONE. If PySR recovered sqrt(x*(1-x)) and the linear maps, the "
          "engine reconstructs TFPT decoders from numbers alone. Aim the same "
          "loop at residuals; gate every hit with symbolic_search.py's "
          "look-elsewhere significance before claiming anything.")
