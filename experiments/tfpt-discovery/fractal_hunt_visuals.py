#!/usr/bin/env python3
"""
FRACTAL.HUNT.03 -- graphics + time-evolution ANIMATIONS for the structures
found in fractal_selfsimilarity_hunt.py (discovery sandbox, nothing promoted).

Outputs (figures/):
  fractal_string_barcode.png   -- the transfer IFS generation by generation:
                                  interval lengths live on the rank-2 module
                                  {k*a + m*b} in -ln(length) (log-space barcode)
  anim_ifs_construction.gif    -- the Cantor-type construction of the transfer
                                  string refining itself, generation 0 -> 6
  anim_cascade_recovery.gif    -- a recovery curve R(t) building up as the
                                  cascade adds generations: from a smooth
                                  power law to the two-tone log-time ripple
  anim_diffraction_growth.gif  -- |zeta_N(sigma+i w)|^2 as generations N grow:
                                  the log-time quasicrystal Bragg peaks
                                  sharpening onto the complex dimensions
  anim_two_clocks.gif          -- the two incommensurate comb phasors
                                  (omega_1 vs omega_2, ratio = bend) never
                                  re-synchronising in ln t

All content derives from the frozen kernel a = 6 ln(3/2), b = 6 ln 3
(axioms-only); the animations are ILLUSTRATIONS of exact structures, not new
claims. Run:
  cd experiments/tfpt-discovery && .venv/bin/python fractal_hunt_visuals.py
"""
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

os.makedirs("figures", exist_ok=True)

# frozen kernel
A = 6 * math.log(1.5)              # 2.4328  = -ln lambda_T
B = 6 * math.log(3.0)              # 6.5917
R1, R2 = (2 / 3) ** 6, (1 / 3) ** 6
D_SIM = 1 / 6
OM1 = 2 * math.pi / A              # 2.5827 (known comb tone)
OM2 = 2 * math.pi / B              # 0.9532 (new second tone)
BEND = B / A                       # 2.70951 = om1/om2
EPS1 = math.exp(-math.pi ** 2 / A)

FPS = 12


def roots_complex_dimensions(t_max=13.0):
    """Newton roots of 1 - e^(-A s) - e^(-B s) with 0 < Im s <= t_max."""
    roots = {}
    t = 0.3
    while t <= t_max:
        s = complex(0.1, t)
        for _ in range(60):
            f = 1 - np.exp(-A * s) - np.exp(-B * s)
            fp = A * np.exp(-A * s) + B * np.exp(-B * s)
            step = f / fp
            s -= step
            if abs(step) < 1e-14:
                break
        if abs(1 - np.exp(-A * s) - np.exp(-B * s)) < 1e-10 and 0.05 < s.imag <= t_max:
            roots[round(s.imag, 6)] = s
        t += 0.25
    return sorted(roots.values(), key=lambda z: z.imag)


# =====================================================================
# 1. static: the fractal-string barcode (rank-2 module in log-space)
# =====================================================================
print("[1/5] fractal_string_barcode.png ...")
GENS = 7
fig, ax = plt.subplots(figsize=(10.5, 5.2))
for g in range(GENS + 1):
    xs, ws = [], []
    for k in range(g + 1):
        m = g - k
        xs.append(k * A + m * B)                     # -ln(length) of the piece
        ws.append(math.comb(g, k))                   # multiplicity
    ws = np.array(ws, float)
    ax.scatter(xs, np.full(len(xs), g), s=18 + 46 * np.log1p(ws) / np.log1p(ws.max() + 1),
               c="tab:purple", alpha=0.85, zorder=3)
    for x, w in zip(xs, ws):
        if w > 1 and g >= 4:
            ax.annotate(str(int(w)), (x, g), textcoords="offset points",
                        xytext=(0, 7), ha="center", fontsize=6, color="0.35")
# guide lines: pure-a progression (spacing A) and the b-jumps
for k in range(8):
    ax.axvline(k * A, color="tab:blue", lw=0.6, ls=":", alpha=0.55)
ax.set_xlabel(r"$-\ln(\mathrm{length}) = k\,a + m\,b$   with $a=6\ln(3/2)$, $b=6\ln 3$")
ax.set_ylabel("generation $g = k + m$")
ax.set_title("The transfer string is a rank-2 barcode in log-space:\n"
             r"every piece sits on $\{k a + m b\}$ (binomial weights); dotted lines = the pure-$a$ comb"
             " (the searched $\\omega_1$ ladder)")
plt.tight_layout()
plt.savefig("figures/fractal_string_barcode.png", dpi=130)
plt.close()

# =====================================================================
# 2. GIF: IFS construction generation by generation
# =====================================================================
print("[2/5] anim_ifs_construction.gif ...")
# intervals in [0,1]: S1 scales by R1 (left), S2 by R2 (right); log-x view
def gen_intervals(g):
    """List of (left, length) after g refinements, exact IFS on [0,1]."""
    iv = [(0.0, 1.0)]
    for _ in range(g):
        nxt = []
        for x0, ln in iv:
            nxt.append((x0, ln * R1))                          # left child
            nxt.append((x0 + ln * (1 - R2), ln * R2))          # right child
        iv = nxt
    return iv


MAXG = 6
fig, ax = plt.subplots(figsize=(9.5, 4.6))


def draw_ifs(frame):
    ax.clear()
    g = frame
    iv = gen_intervals(g)
    # log-magnified view: plot -ln(length) as bar height at midpoint (log-x)
    for x0, ln in iv:
        mid = x0 + 0.5 * ln
        ax.plot([max(x0, 1e-12), x0 + ln], [0, 0], lw=6, color="tab:purple",
                solid_capstyle="butt", alpha=0.9)
        ax.plot([mid], [-math.log(ln) if ln < 1 else 0], "o", ms=3.5,
                color="tab:red", alpha=0.8)
    ax.set_xscale("log")
    ax.set_xlim(1e-12, 1.3)
    ax.set_ylim(-2, MAXG * B + 4)
    ax.set_xlabel("position (log scale)")
    ax.set_ylabel(r"$-\ln(\mathrm{length})$ of each piece")
    ax.set_title(f"Transfer-IFS construction, generation g = {g}\n"
                 f"{2 ** g} pieces; contraction ratios $(2/3)^6$ and $(1/3)^6$ "
                 f"$\\Rightarrow$ Moran dimension exactly 1/6")
    return []


anim = FuncAnimation(fig, draw_ifs, frames=list(range(MAXG + 1)) + [MAXG] * 3,
                     interval=900, blit=False)
anim.save("figures/anim_ifs_construction.gif", writer=PillowWriter(fps=1.4), dpi=100)
plt.close()

# =====================================================================
# 3. GIF: cascade recovery curve building up over generations
# =====================================================================
print("[3/5] anim_cascade_recovery.gif ...")
# recovery signal: sum over cascade channels (k,m): weight = binomial branching
# (2/3 vs 1/3 per step), timescale tau_{km} = e^{k a + m b}; each channel
# relaxes exp(-t/tau). Detrended in ln t to expose the log-periodic ripple.
lt = np.linspace(0.0, 5.5 * A + 0.5 * B, 900)
tt = np.exp(lt)
MAX_GEN = 9


def cascade_signal(n_gen):
    sig = np.zeros_like(tt)
    for g in range(n_gen + 1):
        for k in range(g + 1):
            m = g - k
            w = math.comb(g, k) * (2 / 3) ** k * (1 / 3) ** m
            sig += w * np.exp(-tt / math.exp(k * A + m * B))
    return sig


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9.5, 6.4), sharex=True)


def draw_cascade(frame):
    n = min(frame, MAX_GEN)
    ax1.clear(); ax2.clear()
    sig = cascade_signal(n)
    pos = sig > 1e-300
    y = np.log(sig[pos])
    x = lt[pos]
    ax1.plot(x, y, lw=1.6, color="tab:purple")
    ax1.set_ylabel(r"$\ln R(t)$")
    ax1.set_title(f"Cascade recovery with generations 0..{n} "
                  f"({(2 ** (n + 1) - 1)} channels on the rank-2 grid)")
    # detrend with a cubic in ln t to expose the ripple
    P = np.vander(x, 4)
    ripple = y - P @ np.linalg.lstsq(P, y, rcond=None)[0]
    ax2.plot(x, ripple, lw=1.3, color="tab:red")
    for k in range(1, 6):
        ax2.axvline(k * A, color="tab:blue", lw=0.7, ls=":")
    ax2.set_ylim(-0.06, 0.06)
    ax2.set_xlabel(r"$\ln t$")
    ax2.set_ylabel("log-periodic residual")
    ax2.set_title(r"detrended ripple: teeth on the $a$-comb (dotted, spacing $6\ln(3/2)$)"
                  " emerge as the cascade deepens", fontsize=10)
    return []


anim = FuncAnimation(fig, draw_cascade, frames=list(range(MAX_GEN + 1)) + [MAX_GEN] * 3,
                     interval=800, blit=False)
anim.save("figures/anim_cascade_recovery.gif", writer=PillowWriter(fps=1.6), dpi=100)
plt.close()

# =====================================================================
# 4. GIF: diffraction growth -> complex dimensions
# =====================================================================
print("[4/5] anim_diffraction_growth.gif ...")
SIGMA0 = 0.20
om = np.linspace(0.02, 12.0, 5000)
s = SIGMA0 + 1j * om
roots = roots_complex_dimensions(12.5)
root_ts = [z.imag for z in roots]


def zeta_partial(n_gen):
    """Partial geometric zeta: sum over words up to generation n_gen."""
    z = np.zeros_like(s, dtype=complex)
    for g in range(n_gen + 1):
        for k in range(g + 1):
            m = g - k
            z += math.comb(g, k) * np.exp(-s * (k * A + m * B))
    return z


fig, ax = plt.subplots(figsize=(9.5, 5.0))
N_FRAMES = 13


def draw_diffr(frame):
    n = min(frame, N_FRAMES - 1)
    ax.clear()
    P = np.abs(zeta_partial(n)) ** 2
    ax.semilogy(om, P, lw=1.0, color="tab:red")
    for t0 in root_ts:
        ax.axvline(t0, color="tab:purple", lw=0.7, alpha=0.5)
    ax.axvline(OM1, color="tab:blue", ls=":", lw=1.6,
               label=r"$\omega_1=2.583$ (searched comb)")
    ax.set_xlabel(r"$\omega$ (log-time frequency)")
    ax.set_ylabel(r"$|\zeta_N(0.2+i\omega)|^2$")
    ax.set_ylim(3e-3, 3e2)
    ax.set_title(f"Log-time diffraction of the cascade, generations 0..{n}\n"
                 "purple lines = complex dimensions (the quasicrystal Bragg positions)")
    ax.legend(loc="upper right", fontsize=8)
    return []


anim = FuncAnimation(fig, draw_diffr, frames=list(range(N_FRAMES)) + [N_FRAMES - 1] * 3,
                     interval=700, blit=False)
anim.save("figures/anim_diffraction_growth.gif", writer=PillowWriter(fps=1.8), dpi=100)
plt.close()

# =====================================================================
# 5. GIF: the two incommensurate clocks (phasors) in ln t
# =====================================================================
print("[5/5] anim_two_clocks.gif ...")
N_F = 110
lt_max = 4.0 * B / (2 * math.pi) * (2 * math.pi)   # ~4 slow periods
lts = np.linspace(0.0, 26.0, N_F)
fig = plt.figure(figsize=(10.5, 4.6))
gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 2.2])
axp1 = fig.add_subplot(gs[0, 0], projection="polar")
axp2 = fig.add_subplot(gs[0, 1], projection="polar")
axs = fig.add_subplot(gs[0, 2])
trace_x, trace_y = [], []


def draw_clocks(frame):
    axp1.clear(); axp2.clear(); axs.clear()
    u = lts[frame]
    th1, th2 = OM1 * u, OM2 * u
    for axp, th, lab, col in ((axp1, th1, r"$\omega_1$ clock", "tab:blue"),
                              (axp2, th2, r"$\omega_2$ clock", "tab:green")):
        axp.plot([0, th], [0, 1], lw=2.6, color=col)
        axp.plot([th], [1], "o", ms=7, color=col)
        axp.set_yticklabels([]); axp.set_xticklabels([])
        axp.set_title(lab + f"\nphase = {math.degrees(th) % 360:5.0f}" + r"$^\circ$",
                      fontsize=9)
    # combined two-tone comb signal along ln t
    grid = np.linspace(0, 26.0, 700)
    y = EPS1 * np.cos(OM1 * grid) + (EPS1 ** BEND) * 40 * np.cos(OM2 * grid)
    axs.plot(grid, y, lw=1.1, color="0.4")
    axs.axvline(u, color="tab:red", lw=1.4)
    axs.set_xlim(0, 26); axs.set_ylim(-0.05, 0.05)
    axs.set_xlabel(r"$\ln t$")
    axs.set_title("two-tone comb: ratio $\\omega_1/\\omega_2$ = bend = 2.70951... "
                  "(irrational)\nthe clocks NEVER re-synchronise "
                  "$\\Rightarrow$ log-time quasicrystal, not a periodic comb",
                  fontsize=9)
    return []


anim = FuncAnimation(fig, draw_clocks, frames=N_F, interval=90, blit=False)
anim.save("figures/anim_two_clocks.gif", writer=PillowWriter(fps=FPS), dpi=95)
plt.close()

print("done: figures/fractal_string_barcode.png + 4 GIFs in figures/")
