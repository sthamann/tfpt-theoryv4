"""Generate the data-driven figures referenced by the TFPT documents.

Outputs (PDF, vector) into ../figures/:
  alpha_ablation.pdf   -- alpha^-1 vs budget M and vs N in c3=1/(N pi)
  mass_ladder.pdf      -- the nine fermion masses on a log axis vs word-length L
  action_tower.pdf     -- the EW / Hubble / Lambda action charges (1:5:10)
  status_heatmap.pdf   -- the status_ledger.csv claims coloured by status

Run:  python make_figures.py   (needs numpy, mpmath, matplotlib)
"""
import os
import csv
import numpy as np
import mpmath as mp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from tfpt_constants import phi0
from v3_em_alpha import make_F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "figures")
os.makedirs(OUT, exist_ok=True)

C = {"blue": "#1F4E79", "green": "#1E7B45", "red": "#9B2226",
     "gold": "#B8860B", "gray": "#555555"}
plt.rcParams.update({"font.size": 10, "axes.titlesize": 11, "figure.dpi": 140})


def ainv_of(M=41, Nfac=8):
    a = mp.findroot(make_F(1 / (Nfac * mp.pi), M, Nfac=Nfac), mp.mpf("0.0073"))
    return float(1 / a)


def fig_alpha_ablation():
    fig, (axM, axN) = plt.subplots(1, 2, figsize=(8.4, 3.3))
    codata = 137.035999177
    Ms = list(range(37, 46))
    yM = [ainv_of(M=M) for M in Ms]
    axM.axhline(codata, color=C["red"], lw=1.1, ls="--", label="CODATA-2022")
    axM.plot(Ms, yM, "o-", color=C["blue"], ms=4)
    axM.plot([41], [ainv_of(M=41)], "o", color=C["green"], ms=9,
             label="$M=41$ (TFPT)")
    axM.set_xlabel("budget $M=\\sum L+N_\\Phi$")
    axM.set_ylabel("$\\alpha^{-1}$")
    axM.set_title("(a) sensitivity to the integer budget $M$")
    axM.legend(fontsize=8)
    axM.grid(alpha=0.25)

    Ns = [6, 7, 8, 9, 10]
    yN = [ainv_of(Nfac=N) for N in Ns]
    axN.axhline(codata, color=C["red"], lw=1.1, ls="--", label="CODATA-2022")
    axN.plot(Ns, yN, "s-", color=C["blue"], ms=4)
    axN.plot([8], [ainv_of(Nfac=8)], "o", color=C["green"], ms=9,
             label="$N=8$ (TFPT, $c_3=1/8\\pi$)")
    axN.set_xlabel("$N$ in $c_3=1/(N\\pi)$")
    axN.set_yscale("log")
    axN.set_title("(b) sensitivity to the seam denominator $N$")
    axN.legend(fontsize=8)
    axN.grid(alpha=0.25)
    fig.suptitle("EM fixed point: only $M=41$ and $N=8$ land on $\\alpha^{-1}$",
                 fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(os.path.join(OUT, "alpha_ablation.pdf"))
    plt.close(fig)


def fig_mass_ladder():
    # PDG-ish charged-fermion masses (GeV); word-length L on the phi0-ladder
    data = [  # name, mass GeV, L, sector
        ("t", 172.69, 0, "up"), ("b", 4.18, 2, "down"), ("c", 1.27, 2, "up"),
        (r"$\tau$", 1.77686, 2, "lep"), ("s", 0.0934, 3, "down"),
        (r"$\mu$", 0.105658, 3, "lep"), ("u", 2.16e-3, 4, "up"),
        ("d", 4.67e-3, 4, "down"), ("e", 0.511e-3, 5, "lep")]
    col = {"up": C["blue"], "down": C["gold"], "lep": C["green"]}
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    for name, m, L, s in data:
        ax.scatter(L, m, s=70, color=col[s], zorder=3, edgecolor="k", lw=0.4)
        ax.annotate(name, (L, m), textcoords="offset points",
                    xytext=(7, 4), fontsize=10)
    # reference geometric ladder m ~ lambda_Y^L (lambda_Y = sqrt(phi0(1-phi0)))
    lamY = float(mp.sqrt(phi0 * (1 - phi0)))
    Ls = np.linspace(-0.3, 5.3, 50)
    ax.plot(Ls, 172.69 * lamY**Ls, color=C["gray"], ls=":", lw=1.2,
            label=r"$\propto\lambda_Y^{L},\ \lambda_Y=\sqrt{\varphi_0(1-\varphi_0)}=%.3f$" % lamY)
    ax.set_yscale("log")
    ax.set_xlabel(r"word-length $L$ on the $\varphi_0$-ladder")
    ax.set_ylabel("mass (GeV)")
    ax.set_title(r"Mass ladder: nine fermions on one $\varphi_0$-ladder")
    handles = [Patch(color=col[k], label=v) for k, v in
               {"up": "up-type", "down": "down-type", "lep": "charged lepton"}.items()]
    ax.legend(handles=handles + [plt.Line2D([], [], color=C["gray"], ls=":",
              label=r"$\propto\lambda_Y^{L}$")], fontsize=8, loc="upper right")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "mass_ladder.pdf"))
    plt.close(fig)


def fig_action_tower():
    ainv = ainv_of()
    # action charges A = q * ainv (+ small residue); q in {1/5, 1, 2}
    rungs = [("electroweak\n$v_{EW}/\\bar M_{Pl}$", 1, 27.53),
             ("Hubble\n$H_0/\\bar M_{Pl}$", 5, 138.68),
             ("cosm. const.\n$\\rho_\\Lambda/\\bar M_{Pl}^4$", 10, 276.65)]
    binom = [r[1] for r in rungs]
    A = [r[2] for r in rungs]
    fig, ax = plt.subplots(figsize=(7.0, 3.5))
    ax.plot(binom, A, "o-", color=C["blue"], ms=8, zorder=3)
    for (lab, b, a) in rungs:
        ax.annotate(lab, (b, a), textcoords="offset points", xytext=(10, -6),
                    fontsize=9)
    # ideal line A = (ainv/5) * binom
    xs = np.linspace(0.5, 10.5, 20)
    ax.plot(xs, (ainv / 5) * xs, color=C["red"], ls="--", lw=1.0,
            label=r"$A=(\alpha^{-1}/5)\cdot\binom{5}{k}$")
    ax.set_xticks([1, 5, 10])
    ax.set_xticklabels([r"$\binom{5}{0}{=}1$", r"$\binom{5}{1}{=}5$",
                        r"$\binom{5}{2}{=}10$"])
    ax.set_xlabel(r"Pascal exponent $1:5:10$ on the carrier $K_5$")
    ax.set_ylabel(r"action charge $A_x=-\ln x$")
    ax.set_title(r"Action tower: one engine $\alpha^{-1}$, three scales ($1:5:10$)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "action_tower.pdf"))
    plt.close(fig)


def fig_status_heatmap():
    rows = list(csv.DictReader(open(os.path.join(HERE, "status_ledger.csv"))))
    cat = {"Axiom": (C["gray"], 0), "Formal": (C["blue"], 1),
           "Lattice": (C["blue"], 1), "Numerical": (C["green"], 2),
           "Physical": (C["gold"], 3), "Open": (C["red"], 4)}

    def classify(s):
        for k, v in cat.items():
            if s.startswith(k):
                return v
        return (C["gray"], 0)
    rows = rows[::-1]
    fig, ax = plt.subplots(figsize=(8.4, 7.6))
    for i, r in enumerate(rows):
        superseded = r.get("active", "true") == "false"
        color, _ = classify(r["status"])
        # superseded rows are drawn dimmed; their canonical pointer is shown
        bar = "#cfcfcf" if superseded else color
        ax.barh(i, 1, color=bar, edgecolor="white", alpha=0.55 if superseded else 1.0)
        ax.text(0.02, i, f"{r['claim_id']}", va="center", ha="left",
                color="black" if superseded else "white", fontsize=8, fontweight="bold")
        label = r["status"] + ("  (superseded)" if superseded else "")
        ax.text(1.03, i, label, va="center", ha="left", fontsize=7.5,
                color=("#888888" if superseded else "black"))
    ax.set_xlim(0, 1.9)
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.set_yticks([])
    ax.set_xticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    legend = [Patch(color=C["gray"], label="Axiom"),
              Patch(color=C["blue"], label="Formal / Lattice"),
              Patch(color=C["green"], label="Numerical"),
              Patch(color=C["gold"], label="Physical / conditional"),
              Patch(color=C["red"], label="Open")]
    ax.legend(handles=legend, fontsize=8, ncol=5, loc="upper center",
              bbox_to_anchor=(0.5, 1.05), frameon=False)
    ax.set_title("Status heatmap (from verification/status_ledger.csv)", pad=22)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "status_heatmap.pdf"))
    plt.close(fig)


def fig_coxeter_circle():
    """E8 Coxeter element: eigenvalue phases exp(2 pi i m/30), m = exponents."""
    exps = [1, 7, 11, 13, 17, 19, 23, 29]
    fig, ax = plt.subplots(figsize=(4.3, 4.3))
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(th), np.sin(th), color=C["gray"], lw=0.8, alpha=0.6)
    pair_col = [C["blue"], C["green"], C["gold"], C["red"]]
    pairs = [(1, 29), (7, 23), (11, 19), (13, 17)]
    for (m1, m2), col in zip(pairs, pair_col):
        for m in (m1, m2):
            a = 2 * np.pi * m / 30
            ax.plot([0, np.cos(a)], [0, np.sin(a)], color=col, lw=1.0, alpha=0.5)
            ax.scatter([np.cos(a)], [np.sin(a)], s=70, color=col, zorder=3,
                       edgecolor="k", lw=0.4)
            ax.annotate(f"{m}", (np.cos(a), np.sin(a)), textcoords="offset points",
                        xytext=(6, 4), fontsize=8)
    ax.set_aspect("equal")
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.axhline(0, color="k", lw=0.4, alpha=0.3)
    ax.axvline(0, color="k", lw=0.4, alpha=0.3)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title("E$_8$ Coxeter element: order $30$\n"
                 "phases $e^{2\\pi i m/30}$, $m=$ exponents $=$ totatives of $30$",
                 fontsize=9.5)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "coxeter_circle.pdf"))
    plt.close(fig)


def fig_attractor():
    """Gapped boundary transport -> unique attractor; geometric rate (2/3)^6."""
    spec = np.array([1.0, (2 / 3) ** 6, (1 / 3) ** 6])
    V = np.array([[1, 1, 1], [0, 1, 2], [0, 0, 1]], float)
    T = V @ np.diag(spec) @ np.linalg.inv(V)
    fix = np.linalg.eig(T)[1][:, np.argmax(np.abs(np.linalg.eigvals(T)))].real
    fix = fix / np.linalg.norm(fix)

    def traj(v):
        v = v.astype(float)
        d = []
        for _ in range(14):
            v = T @ v
            v = v / np.linalg.norm(v)
            d.append(min(np.linalg.norm(v - fix), np.linalg.norm(v + fix)))
        return d
    starts = {"start A $(1,0,0)$": np.array([1., 0., 0.]),
              "start B $(0.1,0.7,0.2)$": np.array([0.1, 0.7, 0.2]),
              "start C $(0,0,1)$": np.array([0., 0., 1.])}
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ms = {0: "o", 1: "s", 2: "^"}
    for i, (lab, v) in enumerate(starts.items()):
        d = traj(v)
        ax.semilogy(range(1, len(d) + 1), d, ms[i] + "-", ms=4,
                    color=list(C.values())[i], label=lab)
    n = np.arange(1, 13)
    ax.semilogy(n, 0.7 * ((2 / 3) ** 6) ** (n - 1), "k--", lw=1.0,
                label="geometric rate $(2/3)^6$")
    ax.set_xlabel("cycle iteration $n$")
    ax.set_ylabel("distance to fixed direction")
    ax.set_title("Gapped boundary transport $\\Rightarrow$ one attractor "
                 "(any start, rate $(2/3)^6$)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.25, which="both")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "attractor.pdf"))
    plt.close(fig)


if __name__ == "__main__":
    fig_alpha_ablation()
    fig_mass_ladder()
    fig_action_tower()
    fig_status_heatmap()
    fig_coxeter_circle()
    fig_attractor()
    print("figures written to", os.path.normpath(OUT))
