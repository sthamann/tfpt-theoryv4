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
WEB = os.path.join(HERE, "..", "website", "public", "figures")   # PNG copies for the site
os.makedirs(WEB, exist_ok=True)

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


def fig_translation_clock():
    """The discrete<->dynamic translation clock: the order-30 Coxeter element as
    two coprime hands -- a static carrier ring (Z/5, golden, no rate) and a dynamic
    family ring (Z/6, the recovery rate (2/3)^6), read law-inclusive (0..5) or
    live-only (1..5).  Backs v319_translation_clock.py."""
    fig, ax = plt.subplots(figsize=(5.6, 5.6))
    th = np.linspace(0, 2 * np.pi, 400)

    # --- outer ring: the dynamic 6-hand (Z/6 = 2 N_fam), ticks 0..5 ---
    Rd = 1.0
    ax.plot(Rd * np.cos(th), Rd * np.sin(th), color=C["blue"], lw=1.1, alpha=0.55)
    for k in range(6):
        a = np.pi / 2 - 2 * np.pi * k / 6          # start at top, clockwise
        x, y = Rd * np.cos(a), Rd * np.sin(a)
        law = (k == 0)
        ax.scatter([x], [y], s=160 if law else 110,
                   color=C["red"] if law else C["blue"], zorder=4,
                   edgecolor="k", lw=0.5)
        ax.text(x, y, str(k), ha="center", va="center", fontsize=8.5,
                color="white", fontweight="bold", zorder=6)
    # mark the conserved law at position 0
    ax.annotate("law (rate 0)\n= attractor", (0, Rd),
                textcoords="offset points", xytext=(0, 12), ha="center",
                fontsize=8, color=C["red"])

    # --- inner ring: the static 5-hand (Z/5 = g_car), ticks 1..5 ---
    Rs = 0.56
    ax.plot(Rs * np.cos(th), Rs * np.sin(th), color=C["gold"], lw=1.1, alpha=0.6)
    for k in range(5):
        a = np.pi / 2 - 2 * np.pi * k / 5
        x, y = Rs * np.cos(a), Rs * np.sin(a)
        ax.scatter([x], [y], s=110, color=C["gold"], zorder=4,
                   edgecolor="k", lw=0.5)
        ax.text(x, y, str(k + 1), ha="center", va="center", fontsize=8.5,
                color="white", fontweight="bold", zorder=6)

    ax.text(0, 0, r"$\mathbb{Z}/30$" "\n" r"$=5\times6$", ha="center",
            va="center", fontsize=10, fontweight="bold", color=C["gray"])

    # legends as text below
    ax.text(0, -1.30, r"dynamic hand $\mathbb{Z}/6=2N_{\rm fam}$ (0..5): "
            r"rate $(2/3)^6$, exponent $6$", ha="center", fontsize=8.2,
            color=C["blue"])
    ax.text(0, -1.46, r"static hand $\mathbb{Z}/5=g_{\rm car}$ (1..5): "
            r"golden $\sqrt{5}$, no rate", ha="center", fontsize=8.2,
            color=C["gold"])

    ax.set_aspect("equal")
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.6, 1.45)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title("The translation clock: discrete $\\leftrightarrow$ dynamic\n"
                 "order-$30$ Coxeter element $=$ static $5$ $\\times$ dynamic $6$",
                 fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "translation_clock.pdf"))
    fig.savefig(os.path.join(WEB, "translation_clock.png"), dpi=150)
    plt.close(fig)


def fig_galois_cp_hexagon():
    """The Galois CP lock: both CP phases are powers of one hexagonal unit rho=zeta_6,
    delta_CKM,lead = arg(rho) = pi/3 and delta_PMNS = arg(rho^4) = 4pi/3, locked by
    rho^4 = -rho to delta_PMNS = delta_CKM,lead + pi.  The 3 generations are the even
    vertices (cube roots zeta_3); the family Galois Z2 (zeta_6 -> conj) = CP conjugation.
    Backs v320_galois_cp_relation.py / v316 / v317."""
    fig, ax = plt.subplots(figsize=(5.6, 5.6))
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(th), np.sin(th), color=C["gray"], lw=0.8, alpha=0.4)

    # the six zeta_6 powers k=0..5 at angles 60*k deg
    pts = {k: (np.cos(np.pi * k / 3), np.sin(np.pi * k / 3)) for k in range(6)}
    # hexagon edges
    hx = [pts[k][0] for k in range(6)] + [pts[0][0]]
    hy = [pts[k][1] for k in range(6)] + [pts[0][1]]
    ax.plot(hx, hy, color=C["gray"], lw=1.0, alpha=0.55)

    # the 3 generations = cube roots zeta_3 = even vertices (0,2,4): inner triangle
    tri = [pts[k] for k in (0, 2, 4)] + [pts[0]]
    ax.plot([p[0] for p in tri], [p[1] for p in tri], color=C["green"],
            lw=1.0, alpha=0.5, ls="--")
    for k in (0, 2, 4):
        ax.scatter([pts[k][0]], [pts[k][1]], s=70, color=C["green"], zorder=3,
                   edgecolor="k", lw=0.4)

    # the CP lock: rho^1 (CKM) and rho^4 (PMNS), diametrically opposite
    ax.plot([pts[1][0], pts[4][0]], [pts[1][1], pts[4][1]],
            color=C["red"], lw=2.0, zorder=2)
    ax.scatter([pts[1][0]], [pts[1][1]], s=150, color=C["blue"], zorder=5,
               edgecolor="k", lw=0.6)
    ax.scatter([pts[4][0]], [pts[4][1]], s=150, color=C["red"], zorder=5,
               edgecolor="k", lw=0.6)
    ax.annotate(r"$\delta_{\rm CKM}^{\rm lead}=\arg\rho=\pi/3$ $(60^\circ)$",
                pts[1], textcoords="offset points", xytext=(8, 8),
                fontsize=8.5, color=C["blue"])
    ax.annotate(r"$\delta_{\rm PMNS}=\arg\rho^4=4\pi/3$ $(240^\circ)$",
                pts[4], textcoords="offset points", xytext=(-12, -16),
                ha="right", fontsize=8.5, color=C["red"])
    ax.annotate(r"$\rho^4=-\rho$:  $\delta_{\rm PMNS}=\delta_{\rm CKM}^{\rm lead}+\pi$",
                (0, 0), textcoords="offset points", xytext=(0, 6), ha="center",
                fontsize=8.6, color=C["red"], fontweight="bold")

    # the sheet generator rho^3 = -1 and rho^0 = 1
    for k, lab in ((0, r"$1$"), (3, r"$-1=\rho^3$ (sheet $\mathbb{Z}_2$)")):
        ax.scatter([pts[k][0]], [pts[k][1]], s=55, color=C["gray"], zorder=3)
    ax.annotate(r"$-1=\rho^3$ (sheet)", pts[3], textcoords="offset points",
                xytext=(-8, 6), ha="right", fontsize=7.6, color=C["gray"])

    ax.text(0, -1.34, r"generations $=$ cube roots $\{1,\zeta_3,\zeta_3^2\}$ "
            r"(green); Galois $\mathbb{Z}_2:\zeta_6\!\mapsto\!\bar\zeta_6=$ CP conj.",
            ha="center", fontsize=8.0, color=C["green"])

    ax.set_aspect("equal")
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.45)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title(r"The Galois CP lock on $\rho=\zeta_6$: "
                 r"$\delta_{\rm PMNS}=\delta_{\rm CKM}^{\rm lead}+\pi$", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "galois_cp_hexagon.pdf"))
    fig.savefig(os.path.join(WEB, "galois_cp_hexagon.png"), dpi=150)
    plt.close(fig)


def fig_seed_hyperplane():
    """The seed-hyperplane test: each scorecard observable inverts to the SAME latent
    seed phi0.  Back-solving phi0 from each measured channel (with its error) and
    overlaying the axiom seed phi0 = 1/(6pi)+48 c3^4 shows one latent seed, not five
    independent fits; sin^2 theta13 is the honest ~2 sigma pressure point.  Backs
    v306_seed_crossval.py (the leave-one-out cross-validation)."""
    p0 = float(phi0)
    # inverse readouts phi0(observable): (label, central, sigma, inverse fn, source)
    # repo-documented current bests (same provenance as v306/v307)
    inv = [
        ("$\\lambda_C$", 0.2245, 0.0005,
         lambda x: (1 - np.sqrt(1 - 4 * x * x)) / 2, "PDG 2024"),
        ("$\\sin^2\\theta_{12}$", 0.307, 0.012,
         lambda x: 2 * (1 / 3 - x), "NuFIT 6.0"),
        ("$\\sin^2\\theta_{13}$", 0.02195, 0.00058,
         lambda x: np.exp(5 / 6) * x, "NuFIT 6.0"),
        ("$\\beta$ [deg]", 0.215, 0.074,
         lambda x: 4 * np.pi * (x * np.pi / 180), "ACT DR6"),
        ("$\\Omega_b$", 0.0493, 0.0006,
         lambda x: x / (1 - 1 / (4 * np.pi)), "Planck 2018"),
    ]
    labels, vals, errs, sigs = [], [], [], []
    for name, c, s, f, src in inv:
        v = float(f(c))
        e = abs(float(f(c + s)) - float(f(c - s))) / 2
        labels.append(f"{name}\n({src})")
        vals.append(v)
        errs.append(e)
        sigs.append((v - p0) / e if e > 0 else 0.0)
    w = [1 / e ** 2 for e in errs]
    mean = sum(wi * vi for wi, vi in zip(w, vals)) / sum(w)

    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    ys = list(range(len(labels)))[::-1]
    for yi, v, e, sg in zip(ys, vals, errs, sigs):
        col = C["red"] if abs(sg) >= 2 else (C["gold"] if abs(sg) >= 1 else C["blue"])
        ax.errorbar(v, yi, xerr=e, fmt="o", color=col, ms=6, capsize=3, lw=1.3, zorder=3)
        ax.annotate(f"{sg:+.1f}$\\sigma$", (v, yi), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=7.5, color=col)
    ax.axvline(p0, color=C["green"], lw=1.7, zorder=2,
               label=f"axiom $\\varphi_0=\\frac{{1}}{{6\\pi}}+48c_3^4={p0:.6f}$")
    ax.axvline(mean, color=C["gray"], lw=1.0, ls="--", zorder=2,
               label=f"error-weighted mean $={mean:.6f}$")
    ax.set_yticks(ys)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_ylim(-0.6, len(labels) - 0.2)
    ax.set_xlabel(r"back-solved seed $\varphi_0$ (each channel inverted independently)")
    ax.set_title("Seed-hyperplane test: every channel projects onto one latent "
                 "$\\varphi_0$ (v306)", fontsize=10)
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "seed_hyperplane.pdf"))
    fig.savefig(os.path.join(WEB, "seed_hyperplane.png"), dpi=150)
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


def _sds_horizons(mm):
    """Black-hole and cosmological horizon radii (units 1/sqrt(Lambda))
    for dimensionless mass m in [0, 1/3]: roots of r^3 - 3r + 6m."""
    rb, rc = [], []
    for m in mm:
        roots = np.sort(np.roots([1.0, 0.0, -3.0, 6.0 * m]).real)
        rb.append(max(roots[1], 0.0))   # black-hole horizon (smaller >= 0)
        rc.append(roots[2])             # cosmological horizon
    return np.array(rb), np.array(rc)


def fig_sds_cover():
    """SdS horizons over the mass line: two sheets merging at Nariai."""
    mm = np.linspace(0, 1 / 3, 400)
    rb, rc = _sds_horizons(mm)
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    ax.plot(mm, rc, color=C["blue"], lw=1.8,
            label="cosmological horizon $r_c$")
    ax.plot(mm, rb, color=C["gold"], lw=1.8,
            label="black-hole horizon $r_b$")
    ax.plot(mm, -(rb + rc), color=C["gray"], lw=1.2, ls=":",
            label="virtual third root $-(r_b{+}r_c)$")
    ax.scatter([1 / 3], [1.0], s=80, color=C["red"], zorder=4,
               edgecolor="k", lw=0.5)
    ax.scatter([1 / 3], [-2.0], s=50, color=C["red"], zorder=4,
               edgecolor="k", lw=0.5)
    ax.annotate("Nariai $m=\\frac{1}{3}=\\frac{1}{N_{\\rm fam}}$:\n"
                "roots $(1,1,-2)$ $=$ traceless anchor",
                (1 / 3, 1.0), textcoords="offset points", xytext=(-150, 14),
                fontsize=9, color=C["red"])
    ax.axvline(1 / 3, color=C["red"], lw=0.7, ls="--", alpha=0.5)
    ax.axhline(0, color="k", lw=0.4, alpha=0.4)
    ax.set_xlabel("dimensionless mass $m = M\\sqrt{\\Lambda}$")
    ax.set_ylabel("horizon radii  $r\\sqrt{\\Lambda}$")
    ax.set_title("SdS mass line as a double cover: two horizon sheets merge "
                 "at the anchor point\n(disc $\\propto(1{-}3m)(1{+}3m)$: "
                 "branch points $\\pm1/N_{\\rm fam}$, separation "
                 "$2/3=|\\mathbb{Z}_2|/N_{\\rm fam}$)", fontsize=9.5)
    ax.legend(fontsize=8, loc="center left")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "sds_cover.pdf"))
    plt.close(fig)


def fig_nariai_entropy():
    """Entropy interpolation S_total/S_dS and the Koide-form root quotient."""
    xx = np.linspace(0, 1, 300)
    s_tot = (xx**2 + 1) / (xx**2 + xx + 1)
    s_bh = xx**2 / (xx**2 + xx + 1)
    s_cos = 1 / (xx**2 + xx + 1)
    q_geom = (xx**2 + (xx + 1)**2 + 1) / (4 * (xx + 1)**2)
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.5))
    ax.plot(xx, s_tot, color=C["blue"], lw=2.0, label="total")
    ax.plot(xx, s_cos, color=C["green"], lw=1.3, ls="--",
            label="cosmological sheet")
    ax.plot(xx, s_bh, color=C["gold"], lw=1.3, ls="--",
            label="black-hole sheet")
    ax.axhline(2 / 3, color=C["red"], lw=1.0, ls=":",
               label="Nariai bound $2/3=|\\mathbb{Z}_2|/N_{\\rm fam}$")
    ax.axhline(1 / 3, color=C["gray"], lw=0.8, ls=":", alpha=0.7)
    ax.scatter([1], [2 / 3], s=70, color=C["red"], zorder=4,
               edgecolor="k", lw=0.5)
    ax.set_xlabel("$x = r_b/r_c$")
    ax.set_ylabel("$S/S_{dS}$")
    ax.set_title("(a) $S_{\\rm tot}/S_{dS}=\\frac{x^2+1}{x^2+x+1}$ "
                 "(denominator $=\\Phi_3$)", fontsize=9.5)
    ax.legend(fontsize=7.5)
    ax.grid(alpha=0.25)

    ax2.plot(xx, q_geom, color=C["blue"], lw=2.0)
    ax2.axhline(1 / 2, color=C["green"], lw=1.0, ls=":",
                label="$1/2=\\delta=|\\mathbb{Z}_2|/|\\mu_4|$ (pure dS)")
    ax2.axhline(3 / 8, color=C["red"], lw=1.0, ls=":",
                label="$3/8=p_2(a)/e_1(a)^2$ (Nariai)")
    ax2.scatter([0, 1], [0.5, 3 / 8], s=60, color=[C["green"], C["red"]],
                zorder=4, edgecolor="k", lw=0.5)
    ax2.set_xlabel("$x = r_b/r_c$")
    ax2.set_ylabel("$Q_{\\rm geom}$")
    ax2.set_title("(b) Koide-form quotient of the three roots:\nrange "
                  "$[3/8,\\,1/2]$ $=$ the nonzero $SU(4)_1$ weights",
                  fontsize=9.5)
    ax2.legend(fontsize=7.5)
    ax2.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "nariai_entropy.pdf"))
    plt.close(fig)


def fig_cover_twins():
    """The flavor double cover and the SdS mass-line cover, side by side."""
    fig, (axf, axg) = plt.subplots(1, 2, figsize=(8.8, 3.7))
    # flavor: y^2 = (3x+2)(3x+5)
    xs = np.linspace(-2.6, 0.4, 700)
    det = (3 * xs + 2) * (3 * xs + 5)
    pos = det >= 0
    for s in (+1, -1):
        axf.plot(np.where(pos, xs, np.nan), s * np.sqrt(np.abs(det)),
                 color=C["blue"], lw=1.6)
        axf.plot(np.where(~pos, xs, np.nan), s * np.sqrt(np.abs(det)),
                 color=C["gray"], lw=1.1, ls=":")
    for bp, lab in ((-2 / 3, "Koide $-\\frac{2}{3}$"),
                    (-5 / 3, "carrier $-\\frac{5}{3}$")):
        axf.scatter([bp], [0], s=70, color=C["red"], zorder=4,
                    edgecolor="k", lw=0.5)
        axf.annotate(lab, (bp, 0), textcoords="offset points",
                     xytext=(-12, -16), fontsize=9, color=C["red"])
    axf.axhline(0, color="k", lw=0.4, alpha=0.4)
    axf.set_title("flavor: $y^2=\\det B_{K+xQ}=(3x{+}2)(3x{+}5)$\n"
                  "two sheets, branch points $-\\frac{2}{3},-\\frac{5}{3}$",
                  fontsize=9.5)
    axf.set_xlabel("pencil coordinate $x$")
    axf.set_ylabel("$y$  (dotted: imaginary cut)")
    axf.grid(alpha=0.25)
    # gravity: w^2 = (1-3m)(1+3m)
    ms = np.linspace(-0.55, 0.55, 700)
    d2 = (1 - 3 * ms) * (1 + 3 * ms)
    pos2 = d2 >= 0
    for s in (+1, -1):
        axg.plot(np.where(pos2, ms, np.nan), s * np.sqrt(np.abs(d2)),
                 color=C["blue"], lw=1.6)
        axg.plot(np.where(~pos2, ms, np.nan), s * np.sqrt(np.abs(d2)),
                 color=C["gray"], lw=1.1, ls=":")
    for bp, lab in ((1 / 3, "Nariai $+\\frac{1}{3}$"),
                    (-1 / 3, "$-\\frac{1}{3}$")):
        axg.scatter([bp], [0], s=70, color=C["red"], zorder=4,
                    edgecolor="k", lw=0.5)
        axg.annotate(lab, (bp, 0), textcoords="offset points",
                     xytext=(-12, -16), fontsize=9, color=C["red"])
    axg.axhline(0, color="k", lw=0.4, alpha=0.4)
    axg.set_title("gravity: $w^2\\propto\\mathrm{disc}=(1{-}3m)(1{+}3m)$\n"
                  "branch points $\\pm\\frac{1}{3}=\\pm 1/N_{\\rm fam}$",
                  fontsize=9.5)
    axg.set_xlabel("dimensionless mass $m=M\\sqrt{\\Lambda}$")
    axg.set_ylabel("$w$")
    axg.grid(alpha=0.25)
    fig.suptitle("Twin double covers: the same split $N_{\\rm fam}$-linear "
                 "form in flavor and in classical gravity", fontsize=10.5)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(os.path.join(OUT, "cover_twins.pdf"))
    plt.close(fig)


def fig_orientation():
    """The orientation theorem: anchor = stationary repeller, both sectors."""
    fig, (axf, axg) = plt.subplots(1, 2, figsize=(8.8, 3.7))
    Delta = 6 * np.log(1.5)
    qs = np.linspace(0.8, 6.2, 500)
    V = -(Delta / 3) * (qs**3 / 3 - 3.5 * qs**2 + 10 * qs)
    V = V - V.min()
    axf.plot(qs, V, color=C["blue"], lw=1.8)
    q2 = -(Delta / 3) * (2**3 / 3 - 3.5 * 4 + 20)
    q5 = -(Delta / 3) * (5**3 / 3 - 3.5 * 25 + 50)
    Vmin = (-(Delta / 3) * (qs**3 / 3 - 3.5 * qs**2 + 10 * qs)).min()
    axf.scatter([2], [q2 - Vmin], s=80, color=C["green"], zorder=4,
                edgecolor="k", lw=0.5)
    axf.scatter([5], [q5 - Vmin], s=80, color=C["red"], zorder=4,
                edgecolor="k", lw=0.5)
    axf.annotate("Koide $q{=}2$ (attractor)\n$V''=+\\Delta$",
                 (2, q2 - Vmin), textcoords="offset points",
                 xytext=(-28, 30), fontsize=9, color=C["green"])
    axf.annotate("carrier $q{=}5$ (repeller)\n$V''=-\\Delta$",
                 (5, q5 - Vmin), textcoords="offset points",
                 xytext=(-10, -34), fontsize=9, color=C["red"])
    axf.annotate("", xy=(2.6, q2 - Vmin + 0.35), xytext=(4.3, q2 - Vmin + 1.55),
                 arrowprops=dict(arrowstyle="->", color=C["gray"], lw=1.4))
    axf.text(2.9, q2 - Vmin + 1.35, "relaxation", fontsize=8.5,
             color=C["gray"])
    axf.set_xlabel("branch coordinate $q$")
    axf.set_ylabel("$V(q)$")
    axf.set_title("flavor: gradient flow in a cubic potential\n"
                  "stationary points $=$ the two branch points", fontsize=9.5)
    axf.grid(alpha=0.25)

    xs = np.linspace(0, 1, 400)
    S = (xs**2 + 1) / (xs**2 + xs + 1)
    axg.plot(xs, S, color=C["blue"], lw=1.8)
    axg.scatter([1], [2 / 3], s=80, color=C["red"], zorder=4,
                edgecolor="k", lw=0.5)
    axg.scatter([0], [1], s=80, color=C["green"], zorder=4,
                edgecolor="k", lw=0.5)
    axg.annotate("Nariai $x{=}1$ (anchor):\nstationary, $S''=\\frac{2}{9}"
                 "=|\\mathbb{Z}_2|/N_{\\rm fam}^2$",
                 (1, 2 / 3), textcoords="offset points", xytext=(-165, 36),
                 fontsize=9, color=C["red"])
    axg.annotate("pure dS (democratic):\nentropy maximum", (0, 1),
                 textcoords="offset points", xytext=(8, -20), fontsize=9,
                 color=C["green"])
    axg.annotate("", xy=(0.25, (0.25**2 + 1) / (0.25**2 + 1.25) + 0.012),
                 xytext=(0.7, (0.7**2 + 1) / (0.7**2 + 1.7) + 0.012),
                 arrowprops=dict(arrowstyle="->", color=C["gray"], lw=1.4))
    axg.text(0.42, 0.93, "evaporation\n(entropy ascent)", fontsize=8.5,
             color=C["gray"])
    axg.set_xlabel("sheet ratio $x=r_b/r_c$")
    axg.set_ylabel("$S_{\\rm tot}/S_{dS}$")
    axg.set_title("gravity: entropy ascent away from the anchor\n"
                  "stationary point $=$ Nariai", fontsize=9.5)
    axg.grid(alpha=0.25)
    fig.suptitle("One orientation: the anchor is the stationary repeller in "
                 "both sectors", fontsize=10.5)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(os.path.join(OUT, "orientation.pdf"))
    plt.close(fig)


def fig_seam_units():
    """Black-hole mechanics in seam units: one graphic table."""
    rows = [
        ("Einstein equations", "$G_{\\mu\\nu}=8\\pi\\,T_{\\mu\\nu}$",
         "$G_{\\mu\\nu}=T_{\\mu\\nu}/c_3$", "$c_3=1/(8\\pi)$ (P1)"),
        ("first law", "$dM=\\frac{\\kappa}{8\\pi}dA$",
         "$dM=c_3\\,\\kappa\\,dA$", "seam constant"),
        ("Smarr (Schw.)", "$M=\\frac{\\kappa A}{4\\pi}$",
         "$M=2c_3\\,\\kappa A$", ""),
        ("temperature", "$T_H=\\frac{\\kappa}{2\\pi}$",
         "$T_H=4c_3\\,\\kappa$", "$1/(2\\pi)=4c_3$"),
        ("entropy", "$S=\\frac{A}{4}$", "$S=2\\pi c_3 A$",
         "$1/4=1/|\\mu_4|$"),
        ("Bekenstein bound", "$S\\leq 2\\pi E R$", "$S\\leq ER/(4c_3)$", ""),
        ("Hawking power", "$P=\\frac{1}{15360\\,\\pi M^2}$",
         "$P=\\frac{c_3}{1920\\,M^2}$", "$1920=|W(D_5)|$"),
        ("lifetime", "$\\tau=5120\\,\\pi M^3$",
         "$\\tau=128\\,g_{\\rm car}M^3/c_3$",
         "$128=2^7$, $7=$ scalaron"),
        ("Kerr extremal", "$A_{\\rm ext}=8\\pi M^2$",
         "$A_{\\rm ext}=M^2/c_3$",
         "$A_{\\rm ext}/A_{\\rm Schw}=1/|\\mathbb{Z}_2|$"),
        ("area quantum (Hod)", "$\\Delta A=4\\ln 3$",
         "$\\Delta A=\\ln(N_{\\rm fam}^4)$",
         "$81=$ disc of the cover"),
        ("Nariai bound", "$S_N=\\frac{2\\pi}{\\Lambda}$",
         "$S_N=\\frac{2}{3}S_{dS}$",
         "$2/3=|\\mathbb{Z}_2|/N_{\\rm fam}$ (Koide)"),
    ]
    fig, ax = plt.subplots(figsize=(8.6, 0.46 * len(rows) + 1.1))
    ax.axis("off")
    cols = ["quantity", "standard form", "seam form", "compiler atom"]
    xpos = [0.01, 0.24, 0.52, 0.78]
    ax.text(0.5, 1.0, "Black-hole mechanics in seam units "
            "($c_3=1/(8\\pi)$): every coefficient is a compiler atom",
            ha="center", va="top", fontsize=11, fontweight="bold",
            transform=ax.transAxes)
    for j, cname in enumerate(cols):
        ax.text(xpos[j], 0.92, cname, fontsize=9, fontweight="bold",
                color=C["blue"], transform=ax.transAxes)
    for i, row in enumerate(rows):
        y = 0.86 - 0.082 * i
        if i % 2 == 0:
            ax.axhspan(y - 0.030, y + 0.045, xmin=0.0, xmax=1.0,
                       color=C["blue"], alpha=0.05)
        for j, cell in enumerate(row):
            ax.text(xpos[j], y, cell, fontsize=8.6, transform=ax.transAxes)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "seam_units.pdf"))
    plt.close(fig)


def fig_trisection():
    """The trisection normal form: mass and entropy as pure (co)sines."""
    psi = np.linspace(0, np.pi / 2, 400)
    mm = np.cos(psi) / 3
    sg = 4 / 3 - (2 / 3) * np.cos(2 * psi / 3)
    fig, ax = plt.subplots(figsize=(7.4, 3.8))
    ax.plot(psi, mm, color=C["gold"], lw=1.8,
            label="mass $m=\\cos(\\psi)/N_{\\rm fam}$")
    ax.plot(psi, sg, color=C["blue"], lw=2.0,
            label="entropy $S_{\\rm tot}/S_{dS}="
                  "\\frac{4}{3}-\\frac{2}{3}\\cos(2\\psi/3)$")
    ax.axhline(2 / 3, color=C["red"], lw=0.9, ls=":",
               label="Nariai bound $2/3$")
    ax.scatter([0, 0], [1 / 3, 2 / 3], s=70,
               color=[C["gold"], C["red"]], zorder=4, edgecolor="k", lw=0.5)
    ax.scatter([np.pi / 2, np.pi / 2], [0, 1], s=70,
               color=[C["gold"], C["green"]], zorder=4,
               edgecolor="k", lw=0.5)
    ax.annotate("anchor ($\\psi{=}0$):\n$m=\\frac{1}{3}$, "
                "$\\sigma''=(\\frac{2}{3})^3$",
                (0, 2 / 3), textcoords="offset points", xytext=(8, 26),
                fontsize=9, color=C["red"])
    ax.annotate("pure dS ($\\psi{=}\\pi/2$)", (np.pi / 2, 1),
                textcoords="offset points", xytext=(-104, 6),
                fontsize=9, color=C["green"])
    ax.set_xlabel("canonical trisection angle $\\psi$  "
                  "($\\cos(3\\theta)=-3m$, centered)")
    ax.set_ylabel("dimensionless value")
    ax.set_title("The trisection normal form: one cosine of glue atoms "
                 "(mean $\\frac{|\\mu_4|}{N_{\\rm fam}}$, amplitude & "
                 "frequency $\\frac{|\\mathbb{Z}_2|}{N_{\\rm fam}}$)",
                 fontsize=10)
    ax.legend(fontsize=8, loc="center right")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "trisection.pdf"))
    plt.close(fig)


def fig_rg_running():
    """The F_transfer running: gauge couplings (b1=41/10, confinement) and the
    Higgs near-criticality (free-seam lambda -> 0).  Backs v159/v164/v166;
    two-loop SM betas are PyR@TE-sourced (verification/v166_higgs_free_seam.py)."""
    from v166_higgs_free_seam import _betas, G1_MZ, G2_MZ, G3_MZ, M_Z, V_EW

    Mbar = 2.435323203e18
    scal = (1.0 / (8 * np.pi))**3.5 * Mbar         # scalaron c3^{7/2} Mbar
    yt0, lam0 = 0.95, 125.25**2 / (2 * V_EW**2)
    # integrate M_Z -> Mbar
    n = 6000
    t0, t1 = np.log(M_Z), np.log(Mbar)
    dt = (t1 - t0) / n
    g1, g2, g3, yt, lam = G1_MZ, G2_MZ, G3_MZ, yt0, lam0
    xs, a1, a2, a3, lams, bls = [], [], [], [], [], []
    for i in range(n + 1):
        mu = np.exp(t0 + i * dt)
        xs.append(np.log10(mu))
        a1.append(4 * np.pi / g1**2); a2.append(4 * np.pi / g2**2); a3.append(4 * np.pi / g3**2)
        lams.append(lam); bls.append(_betas(g1, g2, g3, yt, lam)[4])
        b = _betas(g1, g2, g3, yt, lam)
        g1 += b[0]*dt; g2 += b[1]*dt; g3 += b[2]*dt; yt += b[3]*dt; lam += b[4]*dt

    fig, (axg, axl) = plt.subplots(1, 2, figsize=(8.6, 3.4))

    # alpha_3 confinement leg below M_Z (n_f thresholds, one-loop; v164)
    xd, a3d = [], []
    inv3, mu = 4 * np.pi / G3_MZ**2, M_Z
    fac = 0.985
    while mu > 0.35:
        nf = 5 if mu > 4.18 else (4 if mu > 1.27 else 3)
        inv3 += (11 - 2*nf/3) / (2*np.pi) * np.log(fac)    # d(1/a3)=+(b0/2pi) dln mu
        mu *= fac
        if inv3 <= 0:
            xd.append(np.log10(mu)); a3d.append(0.0); break
        xd.append(np.log10(mu)); a3d.append(inv3)

    # -- panel 1: gauge couplings --
    axg.plot(xs, a1, color=C["blue"], lw=2, label=r"$\alpha_1^{-1}$ (U(1)$_Y$, GUT)")
    axg.plot(xs, a2, color=C["green"], lw=2, label=r"$\alpha_2^{-1}$ (SU(2)$_L$)")
    axg.plot(xs, a3, color=C["red"], lw=2, label=r"$\alpha_3^{-1}$ (SU(3)$_c$)")
    axg.plot(xd, a3d, color=C["red"], lw=1.4, ls="--")
    axg.annotate(r"slope $b_1=\frac{41}{10}$", xy=(xs[len(xs)//2], a1[len(a1)//2]),
                 xytext=(6, -28), textcoords="offset points", fontsize=9, color=C["blue"])
    if xd:
        axg.annotate(r"$\alpha_3^{-1}\!\to\!0$: $\Lambda_{\rm QCD}\!\approx\!0.4$ GeV"
                     "\n(confinement, v164)", xy=(xd[-1], 0), xytext=(8, 30),
                     textcoords="offset points", fontsize=7.5, color=C["red"],
                     arrowprops=dict(arrowstyle="->", color=C["red"], lw=0.8))
    for x, lab in ((np.log10(scal), "scalaron"), (np.log10(Mbar), r"$\bar M_{\rm Pl}$")):
        axg.axvline(x, color=C["gray"], ls=":", lw=1)
        axg.text(x, 62, lab, rotation=90, va="top", ha="right", fontsize=7, color=C["gray"])
    axg.set_xlabel(r"$\log_{10}(\mu/\mathrm{GeV})$")
    axg.set_ylabel(r"$\alpha_i^{-1}(\mu)$")
    axg.set_title("Gauge running: $b_1=41/10$, confinement, no SM unification", fontsize=9.5)
    axg.legend(fontsize=8, loc="upper center"); axg.grid(alpha=0.25)

    # -- panel 2: Higgs quartic --
    imin = int(np.argmin(lams))
    axl.plot(xs, lams, color=C["gold"], lw=2, label=r"$\lambda(\mu)$")
    axl.axhline(0, color=C["gray"], lw=0.8)
    axl.axhspan(-0.01, 0.01, color=C["green"], alpha=0.12)
    axl.plot(xs[imin], lams[imin], "o", color=C["red"], ms=5)
    axl.annotate(r"$\beta_\lambda=0$, $\lambda\!\approx\!0.002$"
                 "\n(free-seam near-criticality, v166)",
                 xy=(xs[imin], lams[imin]), xytext=(-150, 34),
                 textcoords="offset points", fontsize=8, color=C["red"],
                 arrowprops=dict(arrowstyle="->", color=C["red"], lw=0.8))
    for x, lab in ((np.log10(scal), "scalaron"), (np.log10(Mbar), r"$\bar M_{\rm Pl}$")):
        axl.axvline(x, color=C["gray"], ls=":", lw=1)
        axl.text(x, 0.125, lab, rotation=90, va="top", ha="right", fontsize=7, color=C["gray"])
    axl.set_xlabel(r"$\log_{10}(\mu/\mathrm{GeV})$")
    axl.set_ylabel(r"$\lambda(\mu)$")
    axl.set_title(r"Higgs quartic: free seam $\Rightarrow\lambda(\bar M_{\rm Pl})\!\approx\!0$",
                  fontsize=10)
    axl.legend(fontsize=8, loc="upper right"); axl.grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "rg_running.pdf"))
    fig.savefig(os.path.join(WEB, "rg_running.png"), dpi=150)   # standalone for the website
    plt.close(fig)


def fig_slice_compression():
    """E8 slice compression (v170): the seven 248-slices as one projection of two
    alphabets -- anchor power sums P (blue) and Sheet-Diamond determinants D (gold);
    green = symmetric/mixed data. Each block is coloured by its ALPHABET source
    (distinct from the physics-module colouring of the tfpt_3 TikZ atlas)."""
    P = "P"; D = "D"; S = "S"          # alphabet tags: power sums, determinants, symmetric
    col = {P: C["blue"], D: C["gold"], S: C["green"]}
    # each slice: list of (value, alphabet-tag, label)
    slices = {
        r"$D_8$": [(120, P, r"$p_0p_1p_3$"), (128, D, r"$p_1\det F$")],
        r"$D_5{\times}A_3$": [(45, P, "45"), (15, P, "15"), (60, P, r"$p_2p_3$"),
                              (64, S, r"$e_1\dim S^+$"), (64, S, "")],
        r"$E_6{\times}A_2$": [(78, P, r"$p_2\Delta$"), (8, D, r"$\det R$"),
                              (81, D, r"$\sum\det$"), (81, S, "sheet")],
        r"$E_7{\times}A_1$": [(133, P, r"$p_0p_1p_3{+}\Delta$"), (3, P, r"$p_0$"),
                              (112, D, r"$\det R\det C$")],
        r"$F_4{\times}G_2$": [(52, P, r"$p_1^2{+}p_2^2$"), (14, D, r"$\det C$"),
                              (182, D, r"$\Delta\det C$")],
        r"$A_4{\times}A_4$": [(24, P, r"$2p_1p_2$"), (224, S, r"$4e_2p_3{+}24$")],
        r"$A_8$": [(80, D, r"$\det K\det L$"), (168, D, r"$2p_2\det C$")],
    }
    fig, ax = plt.subplots(figsize=(8.6, 4.0))
    names = list(slices.keys())
    for row, nm in enumerate(names):
        x = 0
        for val, tag, lab in slices[nm]:
            ax.barh(row, val, left=x, height=0.66, color=col[tag],
                    edgecolor="white", linewidth=0.6)
            if val >= 12:
                ax.text(x + val/2, row, f"{val}", ha="center", va="center",
                        color="white", fontsize=7.5, fontweight="bold")
            x += val
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=9)
    ax.set_xlim(0, 248)
    ax.set_xlabel(r"$\dim E_8 = 248$ (each slice sums to 248)")
    ax.invert_yaxis()
    ax.set_title("E$_8$ slice compression: seven slices, two alphabets "
                 r"$P=(3,4,6,10)$, $D=(3,4,8,14,20,32)$", fontsize=10)
    handles = [Patch(color=col[P], label="power-sum block $P$"),
               Patch(color=col[D], label=r"determinant block $D$ ($\sum\det=81=N_{\rm fam}^4$)"),
               Patch(color=col[S], label="symmetric / glue block")]
    ax.legend(handles=handles, fontsize=8, loc="lower right", framealpha=0.95)
    ax.grid(axis="x", alpha=0.2)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "slice_compression.pdf"))
    fig.savefig(os.path.join(WEB, "slice_compression.png"), dpi=150)
    plt.close(fig)


def fig_gauge_running():
    """Gauge-only single panel for tfpt_2 (b1=41/10, confinement, non-unification).
    Backs v159/v164; the two-loop SM gauge betas are PyR@TE-confirmed."""
    from v166_higgs_free_seam import _betas, G1_MZ, G2_MZ, G3_MZ, M_Z, V_EW

    Mbar = 2.435323203e18
    scal = (1.0 / (8 * np.pi))**3.5 * Mbar
    yt, lam = 0.95, 125.25**2 / (2 * V_EW**2)
    n = 6000
    t0, t1 = np.log(M_Z), np.log(Mbar)
    dt = (t1 - t0) / n
    g1, g2, g3 = G1_MZ, G2_MZ, G3_MZ
    xs, a1, a2, a3 = [], [], [], []
    for i in range(n + 1):
        xs.append(np.log10(np.exp(t0 + i * dt)))
        a1.append(4*np.pi/g1**2); a2.append(4*np.pi/g2**2); a3.append(4*np.pi/g3**2)
        b = _betas(g1, g2, g3, yt, lam)
        g1 += b[0]*dt; g2 += b[1]*dt; g3 += b[2]*dt; yt += b[3]*dt; lam += b[4]*dt
    # confinement leg below M_Z (n_f thresholds, one-loop; v164)
    xd, a3d, inv3, mu, fac = [], [], 4*np.pi/G3_MZ**2, M_Z, 0.985
    while mu > 0.35:
        nf = 5 if mu > 4.18 else (4 if mu > 1.27 else 3)
        inv3 += (11 - 2*nf/3) / (2*np.pi) * np.log(fac)
        mu *= fac
        xd.append(np.log10(mu)); a3d.append(max(inv3, 0.0))
        if inv3 <= 0:
            break

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(xs, a1, color=C["blue"], lw=2, label=r"$\alpha_1^{-1}$ (U(1)$_Y$, GUT)")
    ax.plot(xs, a2, color=C["green"], lw=2, label=r"$\alpha_2^{-1}$ (SU(2)$_L$)")
    ax.plot(xs, a3, color=C["red"], lw=2, label=r"$\alpha_3^{-1}$ (SU(3)$_c$)")
    ax.plot(xd, a3d, color=C["red"], lw=1.4, ls="--")
    ax.annotate(r"slope $b_1=\dfrac{41}{10}$", xy=(xs[len(xs)//2], a1[len(a1)//2]),
                xytext=(8, -30), textcoords="offset points", fontsize=9, color=C["blue"])
    if xd:
        ax.annotate(r"$\alpha_3^{-1}\!\to\!0$: $\Lambda_{\rm QCD}\!\approx\!0.4$ GeV (v164)",
                    xy=(xd[-1], 0), xytext=(10, 26), textcoords="offset points",
                    fontsize=7.5, color=C["red"],
                    arrowprops=dict(arrowstyle="->", color=C["red"], lw=0.8))
    for x, lab in ((np.log10(scal), "scalaron"), (np.log10(Mbar), r"$\bar M_{\rm Pl}$")):
        ax.axvline(x, color=C["gray"], ls=":", lw=1)
        ax.text(x, 62, lab, rotation=90, va="top", ha="right", fontsize=7, color=C["gray"])
    ax.set_xlabel(r"$\log_{10}(\mu/\mathrm{GeV})$")
    ax.set_ylabel(r"$\alpha_i^{-1}(\mu)$")
    ax.set_title(r"Gauge running from the carrier content: $b_1=41/10$ (v159), "
                 r"$\Lambda_{\rm QCD}$ (v164)", fontsize=9)
    ax.legend(fontsize=8, loc="upper center"); ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "gauge_running.pdf"))
    plt.close(fig)


def fig_residual_chain():
    """The structural-residual reduction chain v175 -> v181: how the whole
    'quantum gravity' residual collapses, step by machine-checked step, to one
    definitional geometric premise. PDF for tfpt_research_contracts + PNG for the site."""
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    steps = [
        ("start", "Naive residual", "''build a quantum-gravity measure''", C["gray"]),
        ("v175", "Net existence + full-cone RP", "discharged to [E] (CAR functor)", C["green"]),
        ("v176-v181", "One geometric premise", "QGEO.SYM.01: carrier mu4 clock = seam conformal deck", C["green"]),
        ("v194-v201", "Non-circular form", "state-invariance w o rho = w; DtN mark-local (Z4)", C["green"]),
        ("v234-v235", "ONE condition: holomorphy", "no abelian sector <=> det K=1 (the Kitaev E8 tower)", C["green"]),
        ("v276", "Flat all-orders closure (Lean)", "flat tau=i => [rho,H]=0 to ALL orders (FORM.QGEO.03)", C["green"]),
        ("v282", "Two faces, ONE object", "chi_E8(i)=12: flat tau=i geometry = (E8)_1 holomorphy", C["green"]),
        ("v284-v285", "Two routes, one open lemma", "RP-uniqueness 5/6 + condensation 3/4; open lemmas coincide", C["green"]),
        ("v286-v288", "SEAM.EQUIV.01 named + attacked", "import firewall (v286); Route A 4/5 (v287); Route B proves full-L2 Z4 lift (v288)", C["green"]),
        ("v289-v297", "Flat-Away: 3 routes reduced", "heat a2 closed+Lean (v292/v295/v296), spectral Hessian PD (v293), Troyanov (v294); Route A citable stack (v297)", C["green"]),
        ("v300-v302", "Closing arc: shared fact pinned", "Flat-Away hard+pin from (E8)_1 Steklov (v300); Route A invertible via free fermions (v301); gap = derived 6ln(3/2)>0 (v302)", C["green"]),
        ("v335-v379", "Closed modulo cited theorems", "QGEO.SYM.01 = corollary of SEAM.EQUIV.01 (v335); gapped lattice model (v367/v368) + S3 stack (v376-v379), Lean-pinned MMST", C["green"]),
        ("BEDROCK", "No TFPT-internal assumption left", "SEAM.EQUIV.01 residual = cited continuum scaling-limit existence (v336) over established facts; stays [O] (not machine-proved end-to-end)", C["gold"]),
    ]
    n = len(steps)
    fig, ax = plt.subplots(figsize=(8.2, 6.6))
    ax.set_xlim(0, 10.4); ax.set_ylim(0, n + 0.5); ax.axis("off")
    ax.set_title("Structural-residual reduction chain: the whole ''quantum gravity'' question\n"
                 "collapses to one falsifiable physical statement -- is the seam (E8)_1 at tau=i?",
                 fontsize=10.5, color=C["blue"])
    bw, bh = 8.4, 0.62
    centers = []
    for i, (tag, head, sub, col) in enumerate(steps):
        y = n - i - 0.1
        x = 0.5 + i * 0.10                      # slight diagonal descent
        box = FancyBboxPatch((x, y - bh / 2), bw, bh,
                             boxstyle="round,pad=0.04,rounding_size=0.12",
                             linewidth=1.6, edgecolor=col,
                             facecolor=col, alpha=0.10 if tag != "BEDROCK" else 0.20)
        ax.add_patch(box)
        ax.text(x + 0.18, y, tag, fontsize=8.6, fontweight="bold", va="center", color=col)
        ax.text(x + 1.45, y + 0.10, head, fontsize=8.4, va="center", fontweight="bold",
                color="#222")
        ax.text(x + 1.45, y - 0.16, sub, fontsize=6.9, va="center", color=C["gray"])
        centers.append((x + bw / 2, y))
    for i in range(n - 1):
        x0, y0 = centers[i]; x1, y1 = centers[i + 1]
        ax.add_patch(FancyArrowPatch((x0 - 2.4, y0 - bh / 2), (x1 - 2.4, y1 + bh / 2),
                                     arrowstyle="-|>", mutation_scale=11,
                                     color=C["gray"], lw=1.0))
    ax.text(5.2, 0.10, "Everything above is a theorem, a Lean proof or an established citation; the bedrock, once a\n"
            "definition (QGEO.SYM.01), is now one falsifiable physical question: is the raw seam (E8)_1 at tau=i?",
            fontsize=6.8, ha="center", va="bottom", style="italic", color=C["gray"])
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "residual_chain.pdf"))
    fig.savefig(os.path.join(WEB, "residual_chain.png"), dpi=150)
    plt.close(fig)


def fig_script_timeline():
    """The development timeline of the ~235 verification scripts: the phases of
    the journey, what each did mathematically and physically. PDF + PNG."""
    from matplotlib.patches import FancyBboxPatch

    phases = [
        ("v1-v23", "Foundations", "carrier D5+A3+mu4, E8 glue, alpha^-1 fixed point,\n"
         "anchor a=(1,1,2) -> {c3,g_car} reduce to {a,pi}", C["blue"]),
        ("v24-v53", "Standard-Model readouts", "phi0 mass ladder, flavor (Q,K,R,L), lepton/quark\n"
         "ratios, hypercharge, compiler core (5,3)", C["green"]),
        ("v54-v100", "Seam = horizon", "one-sided Gauss-Bonnet c3=1/(8pi), Coxeter-30 cycle,\n"
         "gapped attractor (2/3)^6, frozen registry + null-MC", C["gold"]),
        ("v101-v140", "Horizon + flavor geometry", "Nariai=anchor, monodromy=W(A3)=S4, cusp\n"
         "weights {0,1/3,2/3}, H^1 cohomology, canonical map", C["blue"]),
        ("v141-v158", "R1-R5 + premise (A)", "deck selection, EH mechanism, No-Unit Theorem,\n"
         "simple-current (E8)1, free c=8 fixed point isolated/stable", C["green"]),
        ("v159-v169", "PyR@TE cross-checks", "SM gauge/Yukawa/Higgs RGEs confirmed (b1=41/10),\n"
         "Lambda_QCD, m_H near-criticality, eta_B leptogenesis", C["red"]),
        ("v170-v174", "AQFT bridges", "E8 slice compression, OS moment/Sugawara, trace\n"
         "anomaly seed 4/3, strong-CP Pfaffian, Fock readings", C["gold"]),
        ("v175-v181", "AQFT closure -> geometric bedrock", "net existence + full-cone RP [E];\n"
         "residual -> one premise: carrier mu4 clock = seam conformal deck", C["blue"]),
        ("v182-v213", "F_transfer functor + frontier", "reviewer residual map; F_transfer = one typed\n"
         "functor (Koide, eta_B, axion, m_p/m_e) + machine guard", C["red"]),
        ("v214-v218", "Pillowcase + Sheet Diamond", "QGEO pillowcase (cross-ratio 2 => j=1728), four\n"
         "marks from Gauss-Bonnet, the Sheet Diamond axis geometry", C["gold"]),
        ("v219-v237", "Icosahedral capstone", "McKay why {2,3,5}, CM norms 41/7, CP triality, Kleinian\n"
         "seam, det K=1 = Kitaev E8; the (2,3,5) Brieskorn generates ALL", C["green"]),
        ("v238-v261", "NCG / Modular Spectral Closure", "96-dim spectral triple, Dirac = covariance induction,\n"
         "cutoff = KMS weight, seam/carrier/E8 on one K3: one relative object", C["blue"]),
        ("v262-v275", "Frontier closure + QFT4D fork", "F_QCD m_p/m_e, M_nu seesaw, S_pert (EG, 1-loop + gauge\n"
         "betas), scale over-determination, the QG.AMB roadmap", C["red"]),
        ("v276-v299", "The Gral: SEAM.EQUIV.01 + Flat-Away", "seam = (E8)_1 at tau=i named as ONE theorem;\n"
         "both routes reduced to one shared input (Flat-Away), heat a2 proved+Lean (v295/v296)", C["gold"]),
        ("v300-v302", "Closing arc: residual pinned", "Flat-Away hard+pin from (E8)_1 (v300); Route A invertible\n"
         "via free fermions (v301); gap = derived 6ln(3/2)>0 (v302); no TFPT-internal assumption left", C["gold"]),
        ("v303-v407", "Solvers + parameter-free gravity + closure", "typed F_transfer solvers (Koide/eta_B/m_p-me/axion, v371-v375/v402);\n"
         "parameter-free Einstein eq. full nonlinear (v359); QG.AMB a [C] redundancy (v369)", C["green"]),
    ]
    fig, ax = plt.subplots(figsize=(7.8, 10.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, len(phases) + 0.4); ax.axis("off")
    ax.set_title("TFPT verification suite: the journey of ~400 machine-checked scripts",
                 fontsize=10.5, color=C["blue"])
    ax.plot([0.7, 0.7], [0.3, len(phases) + 0.1], color=C["gray"], lw=1.4, zorder=0)
    for i, (rng, head, sub, col) in enumerate(phases):
        y = len(phases) - i - 0.1
        ax.plot(0.7, y, "o", color=col, ms=9, zorder=3)
        box = FancyBboxPatch((1.15, y - 0.34), 8.4, 0.68,
                             boxstyle="round,pad=0.04,rounding_size=0.10",
                             linewidth=1.4, edgecolor=col, facecolor=col, alpha=0.09)
        ax.add_patch(box)
        ax.text(1.35, y + 0.13, f"{rng}  -  {head}", fontsize=8.7, fontweight="bold",
                va="center", color=col)
        ax.text(1.35, y - 0.16, sub, fontsize=7.0, va="center", color="#333")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "script_timeline.pdf"))
    fig.savefig(os.path.join(WEB, "script_timeline.png"), dpi=150)
    plt.close(fig)


def fig_qft_skeleton():
    """The emergent-QFT skeleton (v238-v246): how the seam chiral net becomes a
    QFT, each step machine-checked, with the two honest open items flagged red.
    PDF for the papers + PNG for the site."""
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    steps = [
        ("v156/v175", "Seam chiral net $(E_8)_1$, $c=8$", "a 2d chiral QFT exists [E/F]", C["green"]),
        ("v238/v239", "Modular flow = KMS time", "$\\sigma_t=e^{it\\Lambda}$, $\\beta=1$; gap $=6\\ln(3/2)$", C["green"]),
        ("v240", "GNS/OS: Hilbert space + $H\\geq 0$", "$H_{OS}=-L\\geq 0$, gap $=$ mass gap", C["green"]),
        ("v241-v243", "Particles = DHR sectors; S-mat", "$\\mathbb{Z}_4\\times\\mathbb{Z}_4$; braiding (Yang-Baxter)", C["green"]),
        ("v244-v257", "Spectral triple $\\to$ 4d", "$\\mathbf{16}=$ one anomaly-free gen.; $\\sin^2\\theta_W=3/8$", C["green"]),
        ("v258-v261", "Modular Spectral Closure", "one relative object: $D_F=$cov.\\ induction, cutoff$=$KMS, K3", C["green"]),
        ("v269-v278", "Perturbative $S_{\\mathrm{pert}}$ (EG)", "1-loop quartic + gauge $\\beta=(41/10,-19/6,-7)$; LSZ unitary", C["green"]),
        ("v265", "4D fork (frozen)", "boundary-only default; PS UV branch; SM-only GUT killed", C["gold"]),
        ("v304-v380", "QG: ghost resolved, measure a redundancy", "Stelle ghost = truncation artefact; graviton unitarity [C]; QG.AMB [C] redundancy", C["gold"]),
        ("OPEN", "SEAM.EQUIV.01 = seam$=(E_8)_1$ at $\\tau{=}i$", "closed modulo cited theorems (v367-v379); residual [O] = cited continuum (v336)", C["red"]),
    ]
    n = len(steps)
    fig, ax = plt.subplots(figsize=(8.0, 6.8))
    ax.set_xlim(0, 10); ax.set_ylim(0, n + 0.5); ax.axis("off")
    ax.set_title("The emergent-QFT skeleton on the seam (v238-v407):\n"
                 "each step machine-checked; the one residual cited-continuum item in red",
                 fontsize=10.5, color=C["blue"])
    bw, bh = 8.6, 0.60
    centers = []
    for i, (tag, head, sub, col) in enumerate(steps):
        y = n - i - 0.1
        x = 0.4
        box = FancyBboxPatch((x, y - bh / 2), bw, bh,
                             boxstyle="round,pad=0.04,rounding_size=0.12",
                             linewidth=1.6, edgecolor=col,
                             facecolor=col, alpha=0.20 if tag == "OPEN" else 0.10)
        ax.add_patch(box)
        ax.text(x + 0.18, y, tag, fontsize=8.4, fontweight="bold", va="center", color=col)
        ax.text(x + 1.65, y + 0.10, head, fontsize=8.4, va="center", fontweight="bold", color="#222")
        ax.text(x + 1.65, y - 0.16, sub, fontsize=7.0, va="center", color=C["gray"])
        centers.append((x + bw / 2, y))
    for i in range(n - 1):
        x0, y0 = centers[i]; x1, y1 = centers[i + 1]
        ax.add_patch(FancyArrowPatch((x0 - 3.2, y0 - bh / 2), (x1 - 3.2, y1 + bh / 2),
                                     arrowstyle="-|>", mutation_scale=10, color=C["gray"], lw=0.9))
    ax.text(5.0, 0.06, "Residual = the cited continuum scaling-limit existence (v336); nothing here is marked experimentally confirmed.",
            fontsize=6.8, ha="center", va="bottom", style="italic", color=C["gray"])
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "qft_skeleton.pdf"))
    fig.savefig(os.path.join(WEB, "qft_skeleton.png"), dpi=150)
    plt.close(fig)


def fig_qft_unification():
    """Honest data cross-check (v246): the spectral-action boundary condition
    g1=g2=g3 / sin^2=3/8 is NOT met by the SM run (1- AND 2-loop) -- the three
    couplings miss. TFPT has SM gauge content and no new states, so there is no
    admissible threshold source. A falsifiable tension, not a fit. PDF + PNG."""
    MZ = 91.1876
    ainv = np.array([59.01, 29.59, 8.47]); b1 = np.array([41 / 10, -19 / 6, -7.0])
    b2 = np.array([[199 / 50, 27 / 10, 44 / 5], [9 / 10, 35 / 6, 12.0], [11 / 10, 9 / 2, -26.0]])
    ts = np.linspace(0, np.log(1e18 / MZ), 600)
    one = np.array([ainv - b1 / (2 * np.pi) * t for t in ts])        # 1-loop

    def deriv(ai):
        a = 1.0 / ai
        return -b1 / (2 * np.pi) - (b2 @ a) / (8 * np.pi**2)
    two = []; ai = ainv.copy(); dt = ts[1] - ts[0]
    for _ in ts:
        two.append(ai.copy())
        k1 = deriv(ai); k2 = deriv(ai + 0.5 * dt * k1)
        k3 = deriv(ai + 0.5 * dt * k2); k4 = deriv(ai + dt * k3)
        ai = ai + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    two = np.array(two)
    x = np.log10(MZ * np.exp(ts))

    fig, ax = plt.subplots(figsize=(6.8, 4.6))
    labels = [r"$\alpha_1^{-1}$ (U(1)$_Y$)", r"$\alpha_2^{-1}$ (SU(2))", r"$\alpha_3^{-1}$ (SU(3))"]
    cols = [C["blue"], C["green"], C["red"]]
    for i in range(3):
        ax.plot(x, one[:, i], color=cols[i], lw=1.6, label=labels[i])
        ax.plot(x, two[:, i], color=cols[i], lw=1.1, ls="--", alpha=0.85)
    ax.plot([], [], color=C["gray"], lw=1.6, label="1-loop (solid)")
    ax.plot([], [], color=C["gray"], lw=1.1, ls="--", label="2-loop (dashed)")
    ax.annotate("they MISS\n(1- and 2-loop)", xy=(15.0, 43), xytext=(10.4, 30),
                fontsize=8.5, color=C["red"], arrowprops=dict(arrowstyle="->", color=C["red"]))
    ax.set_xlabel(r"$\log_{10}(\mu/\mathrm{GeV})$"); ax.set_ylabel(r"$\alpha_i^{-1}$")
    ax.set_title("Spectral-action unification vs measured couplings (v246):\n"
                 "1- and 2-loop both MISS -- a tension, no rescue (SM content, no new state)",
                 fontsize=9.2, color=C["blue"])
    ax.legend(fontsize=7.5, loc="upper right"); ax.grid(alpha=0.25)
    ax.text(0.5, -0.20, "$g_1{=}g_2{=}g_3$, $\\sin^2\\theta_W{=}3/8$ is the spectral-action prediction; with SM content "
            "and no new states there is no\nadmissible threshold source -- the 4d-GUT route is in tension (like NCG-SM), "
            "not closed (QFT4D.RGTEST.01).",
            transform=ax.transAxes, ha="center", fontsize=6.4, style="italic", color=C["gray"])
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "qft_unification.pdf"))
    fig.savefig(os.path.join(WEB, "qft_unification.png"), dpi=150)


def fig_ftransfer_dynamics():
    """F_transfer = one shape, four rates: each instance is a gapped relaxation to a
    UNIQUE attractor; only F_pole's rate is the seam eigenvalue (2/3)^6 (v303)."""
    fig, axes = plt.subplots(2, 2, figsize=(8.6, 6.2))
    fig.subplots_adjust(hspace=0.42, wspace=0.28, top=0.88, bottom=0.13,
                        left=0.09, right=0.97)

    gap = 6 * np.log(1.5)                       # seam gap = -ln (2/3)^6 = 2.4328

    # --- F_pole (Koide): continuous flow of the seam transfer, rate = the seam gap ---
    ax = axes[0, 0]
    t = np.linspace(0, 2.8, 200)
    xstar = 2.0
    ax.plot(t, xstar + (5 - xstar) * np.exp(-gap * t), color=C["gold"], lw=2.4)
    ax.scatter([0, 1, 2], [5] + [xstar + (5 - xstar) * (2 / 3) ** (6 * n) for n in (1, 2)],
               color=C["gold"], s=22, zorder=5)
    ax.axhline(xstar, ls="--", color=C["gray"], lw=1.2)
    ax.text(2.7, xstar + 0.18, "attractor $q^\\ast{=}2$", ha="right", fontsize=8.5, color=C["gray"])
    ax.set_title("F$_{\\rm pole}$ (Koide) — SEAM rate $(2/3)^6$", color=C["gold"], fontweight="bold")
    ax.set_xlabel("flow time $t$"); ax.set_ylabel("branch coord $q$")
    ax.text(0.5, 4.4, "Möbius map, $F'{=}(2/3)^6{=}\\lambda_2$\n(= seam clock eigenvalue)", fontsize=8)
    for s in ax.spines.values():
        s.set_color(C["gold"]); s.set_linewidth(1.6)

    # --- F_Boltzmann (eta_B): thermal washout to the balance (H-theorem) ---
    ax = axes[0, 1]
    z = np.linspace(0, 6, 200)
    W = 1.3
    ax.plot(z, (1 - np.exp(-W * z)), color=C["blue"], lw=2.2)
    ax.axhline(1.0, ls="--", color=C["gray"], lw=1.2)
    ax.text(5.9, 0.93, "balance $S/W$", ha="right", fontsize=8.5, color=C["gray"])
    ax.set_title("F$_{\\rm Boltzmann}$ ($\\eta_B$) — thermal washout", color=C["blue"])
    ax.set_xlabel("$z=M_1/T$"); ax.set_ylabel("asymmetry $Y/Y^\\ast$")
    ax.text(2.0, 0.30, "$\\kappa_f\\in(0,1)$\nrate thermal", fontsize=8)

    # --- F_relic (axion): damped misalignment -> frozen comoving number ---
    ax = axes[1, 0]
    t = np.linspace(0, 14, 500)
    env = np.exp(-0.16 * t)
    ax.plot(t, env * np.cos(2.2 * t), color=C["green"], lw=1.4, alpha=0.85)
    ax.plot(t, env, ls=":", color=C["green"], lw=1.2)
    ax.axhline(0.0, ls="--", color=C["gray"], lw=1.0)
    ncom = 0.5 * env[-1] ** 2 * np.ones_like(t)   # comoving number ~ const at late time
    ax.text(13.5, 0.55, "$n_a a^3 \\to$ const\n(adiabatic freeze)", ha="right", fontsize=8, color=C["green"])
    ax.set_title("F$_{\\rm relic}$ (axion) — cosmological freeze", color=C["green"])
    ax.set_xlabel("time ($H\\!\\downarrow$)"); ax.set_ylabel("$\\theta(t)$")
    ax.text(5.4, -0.62, "seed $\\theta_i{=}3\\pi/5$, rate cosmological", fontsize=8)

    # --- F_QCD (m_p/m_e): RG flow to the Gaussian UV fixed point (asymptotic freedom) ---
    ax = axes[1, 1]
    b0 = 7.0
    lnmu = np.linspace(0, 14, 200)               # ln(mu/M_Z), toward the UV
    aMZ = 0.118
    al = aMZ / (1 + aMZ * (b0 / (2 * np.pi)) * lnmu)
    ax.plot(lnmu, al, color=C["red"], lw=2.2)
    ax.axhline(0.0, ls="--", color=C["gray"], lw=1.2)
    ax.text(13.5, 0.012, "UV attractor $\\alpha_s\\to0$", ha="right", fontsize=8.5, color=C["gray"])
    ax.set_title("F$_{\\rm QCD}$ ($m_p/m_e$) — RG flow, $b_3{=}{-}7$", color=C["red"])
    ax.set_xlabel("$\\ln(\\mu/M_Z)$ (toward UV)"); ax.set_ylabel("$\\alpha_s(\\mu)$")
    ax.text(4.0, 0.085, "asymptotic freedom\n$\\Lambda_{\\rm QCD}$ generated", fontsize=8)

    fig.suptitle("$F_{\\rm transfer}$: one shape, four rates — a gapped relaxation to a UNIQUE attractor",
                 fontsize=13, fontweight="bold")
    fig.text(0.5, 0.03,
             "Only F$_{\\rm pole}$'s rate is the seam eigenvalue $(2/3)^6$; the other three share the "
             "shape with external rates (v303).",
             ha="center", fontsize=8.5, color=C["gray"])
    fig.savefig(os.path.join(OUT, "ftransfer_dynamics.pdf"))
    fig.savefig(os.path.join(WEB, "ftransfer_dynamics.png"), dpi=150)
    plt.close(fig)
    plt.close(fig)


def fig_coxeter_galois():
    """The order-30 Coxeter clock and its Galois gear (v419): the flavor clocks
    (sheet/family/carrier/CP) are powers of zeta30 on the cyclic dial (order
    h(E8)=30), while the seam mu4 (i) is NOT on the dial -- 30 is squarefree so
    4 does not divide it -- but the Galois group (Z/30)^x = mu4 x Z2 =
    Aut(Q(zeta5)) x Aut(Q(zeta3)) = the carrier-pentagon automorphisms x CP
    conjugation.  Backs v419 / v417 / v418."""
    fig, (axc, axg) = plt.subplots(1, 2, figsize=(9.8, 5.0),
                                   gridspec_kw={"width_ratios": [1.15, 1.0]})

    # ---- left: the cyclic 30-dial with the four flavor hands ----
    th = np.linspace(0, 2 * np.pi, 400)
    axc.plot(np.cos(th), np.sin(th), color=C["gray"], lw=0.8, alpha=0.4)
    for k in range(30):
        a = 2 * np.pi * k / 30
        r0 = 0.88 if k % 5 == 0 else 0.93
        axc.plot([r0 * np.cos(a), np.cos(a)], [r0 * np.sin(a), np.sin(a)],
                 color=C["gray"], lw=0.6, alpha=0.5)
    hands = [(15, r"sheet $-1=\zeta_{30}^{15}$ (ord 2)", C["gray"]),
             (10, r"family $\omega=\zeta_{30}^{10}$ (ord 3)", C["green"]),
             (6,  r"carrier $\zeta_5=\zeta_{30}^{6}$ (ord 5)", C["gold"]),
             (5,  r"CP $\zeta_6=\zeta_{30}^{5}$ (ord 6)", C["red"])]
    for k, lab, col in hands:
        a = 2 * np.pi * k / 30
        axc.annotate("", xy=(np.cos(a), np.sin(a)), xytext=(0, 0),
                     arrowprops=dict(arrowstyle="->", color=col, lw=2.0))
        axc.scatter([np.cos(a)], [np.sin(a)], s=70, color=col, zorder=4,
                    edgecolor="k", lw=0.4)
    axc.scatter([0], [0], s=18, color="k", zorder=5)
    for i, (k, lab, col) in enumerate(hands):
        axc.text(-1.52, 1.30 - 0.21 * i, lab, fontsize=7.8, color=col)
    axc.set_aspect("equal"); axc.set_xlim(-1.58, 1.5); axc.set_ylim(-1.4, 1.55)
    axc.set_xticks([]); axc.set_yticks([])
    for sp in axc.spines.values():
        sp.set_visible(False)
    axc.set_title(r"Cyclic dial $\langle\zeta_{30}\rangle$, order $h(E_8){=}30$",
                  fontsize=9.5)

    # ---- right: the Galois gears (seam mu4 + CP Z2) ----
    axg.axis("off")
    sq = np.array([[1, 1], [-1, 1], [-1, -1], [1, -1], [1, 1]]) * 0.5 \
        + np.array([-0.55, 0.45])
    axg.plot(sq[:, 0], sq[:, 1], color=C["blue"], lw=2.2)
    for v in sq[:4]:
        axg.scatter([v[0]], [v[1]], s=55, color=C["blue"], zorder=3,
                    edgecolor="k", lw=0.4)
    axg.text(-0.55, 0.45, r"$\mu_4$", ha="center", va="center", fontsize=14,
             color=C["blue"])
    axg.text(-0.55, 1.18, r"SEAM $=\mathrm{Gal}\,\mathbb{Q}(\zeta_5)=(\mathbb{Z}/5)^\times$",
             ha="center", fontsize=8.0, color=C["blue"])
    axg.text(-0.55, -0.32, r"$i:\ \zeta_5\!\mapsto\!\zeta_5^2$ (Frobenius)",
             ha="center", fontsize=7.6, color=C["blue"])
    axg.plot([0.75, 1.7], [0.45, 0.45], color=C["green"], lw=2.2)
    axg.scatter([0.75, 1.7], [0.45, 0.45], s=55, color=C["green"], zorder=3,
                edgecolor="k", lw=0.4)
    axg.text(1.22, 0.66, r"$\mathbb{Z}_2$", ha="center", fontsize=12,
             color=C["green"])
    axg.text(1.22, 0.16, r"CP $=\mathrm{Gal}\,\mathbb{Q}(\zeta_3)=(\mathbb{Z}/3)^\times$",
             ha="center", fontsize=7.6, color=C["green"])
    axg.text(0.35, -1.05,
             r"$(\mathbb{Z}/30)^\times=\mu_4\times\mathbb{Z}_2$, order "
             r"$\varphi(30){=}8{=}\mathrm{rank}\,E_8$", ha="center",
             fontsize=8.4, fontweight="bold")
    axg.set_xlim(-1.45, 1.95); axg.set_ylim(-1.3, 1.55)
    axg.set_title(r"Galois gears, order $\mathrm{rank}\,E_8{=}8$",
                  fontsize=9.5)

    fig.suptitle(r"$30$ squarefree $\Rightarrow$ the seam $\mu_4$ is not a hand "
                 r"($4\nmid30$) but the carrier's Galois group", fontsize=10.5)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(OUT, "coxeter_galois.pdf"))
    fig.savefig(os.path.join(WEB, "coxeter_galois.png"), dpi=150)


def fig_safeguard_layers():
    """The seven-layer defense against coincidence (overview schematic)."""
    fig, ax = plt.subplots(figsize=(7.8, 4.4))
    layers = [
        ("7  Red team", "tfpt_5 \u00b7 Targets A\u2013F \u00b7 named kill tests", C["red"]),
        ("6  Two independent paths", "Wolfram 116+327 \u00b7 Lean\u00a04 kernel proof", C["gold"]),
        ("5  Frozen registry + null model", "v84 \u00b7 v100 Monte-Carlo \u00b7 v375 scorecard", C["gold"]),
        ("4  Firewall + No-Unit", "v187/v213 \u00b7 v153 (v_geo theorem-forbidden)", C["green"]),
        ("3  Over-determination map", "v427/v428 \u00b7 seven readouts compress one (2,3,5)/E8 object", C["green"]),
        ("2  No free pattern + reverse audit", "v305 \u00b7 E8.REVERSE.AUDIT (3/8 readout)", C["blue"]),
        ("1  Status calculus", "[E]/[C]/[O]/[X] \u00b7 ledger single source \u00b7 audit_sync", C["blue"]),
    ]
    n = len(layers)
    for i, (title, sub, col) in enumerate(layers):
        ax.add_patch(plt.Rectangle((0.1, i + 0.08), 9.8, 0.84, facecolor=col,
                                   alpha=0.15, edgecolor=col, lw=1.3))
        ax.text(0.35, i + 0.58, title, fontsize=10.5, fontweight="bold", color=col)
        ax.text(0.35, i + 0.24, sub, fontsize=8.2, color=C["gray"])
    ax.set_xlim(0, 10); ax.set_ylim(0, n + 0.1)
    ax.axis("off")
    ax.set_title("The layered defense \u2014 a load-bearing claim must pass all seven",
                 fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "safeguard_layers.pdf"))
    fig.savefig(os.path.join(WEB, "safeguard_layers.png"), dpi=150)
    plt.close(fig)


def fig_alpha_uniqueness():
    """alpha^-1 over the declared F_U(1) integer-budget variants: exactly one in window."""
    fig, ax = plt.subplots(figsize=(7.8, 3.6))
    codata = 137.035999177
    Ms = list(range(30, 56))
    ys = [ainv_of(M=M) for M in Ms]               # real root-solves at N=8
    ax.axhspan(codata - 0.6, codata + 0.6, color=C["red"], alpha=0.12,
               label="CODATA region (band widened for visibility;\ntrue window $4\\times10^{-8}$)")
    ax.plot(Ms, ys, "o-", color=C["blue"], ms=3, lw=0.8)
    ax.plot([41], [ainv_of(M=41)], "o", color=C["green"], ms=11,
            label="$M{=}41,\\ N{=}8$ (TFPT) \u2014 the only hit")
    ax.set_xlabel("integer budget $M=\\sum L+N_\\Phi$  (at $c_3=1/8\\pi$)")
    ax.set_ylabel("$\\alpha^{-1}$ (root of $F_{U(1)}$)")
    ax.set_title("$\\alpha^{-1}$ is a unique fixed point: of 94,500 declared "
                 "$F_{U(1)}$ variants exactly one lands in the window (v100)",
                 fontsize=9.6)
    ax.legend(fontsize=7.6, loc="upper right")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "safeguard_alpha_uniqueness.pdf"))
    fig.savefig(os.path.join(WEB, "safeguard_alpha_uniqueness.png"), dpi=150)
    plt.close(fig)


def fig_reverse_audit():
    """E8's 8 Casimir degrees: 3 feed a readout, 5 are hull overhead."""
    degs = [2, 8, 12, 14, 18, 20, 24, 30]
    readout = {2: "metric", 8: "$c_3{=}1/8\\pi$", 30: "$g_{\\rm car}{=}5$"}
    fig, ax = plt.subplots(figsize=(7.8, 3.0))
    for i, d in enumerate(degs):
        is_r = d in readout
        col = C["green"] if is_r else C["gray"]
        ax.bar(i, 1.0, color=col, alpha=0.85 if is_r else 0.30,
               edgecolor=col, lw=1.2, width=0.8)
        ax.text(i, 1.05, str(d), ha="center", fontsize=9.5, fontweight="bold")
        if is_r:
            ax.text(i, 0.5, readout[d], ha="center", va="center", rotation=90,
                    fontsize=8, color="white", fontweight="bold")
    ax.text(0.5, -0.22, "3 / 8 primary readouts (green)        "
            "5 / 8 hull overhead (grey: 12,14,18,20,24)",
            transform=ax.transAxes, ha="center", fontsize=8.6, color=C["gray"])
    ax.set_xlim(-0.7, 7.7); ax.set_ylim(0, 1.2)
    ax.axis("off")
    ax.set_title("Reverse audit (E8.REVERSE.AUDIT.01): how much $E_8$ carries "
                 "NO readout \u2014 published, not hidden", fontsize=9.8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "safeguard_reverse_audit.pdf"))
    fig.savefig(os.path.join(WEB, "safeguard_reverse_audit.png"), dpi=150)
    plt.close(fig)


def fig_witness_map():
    """The CORRECTED over-determination map (v428): the seven arithmetic readouts are
    facets of ONE (2,3,5)/E8 object (compression); what genuinely multiplies is the
    input forced four independent ways (the '8') plus the foreign witness alpha^-1."""
    fig, ax = plt.subplots(figsize=(8.6, 5.0))

    # ---- left panel: COMPRESSION (seven facets -> one (2,3,5)/E8 object) ----
    wit = [
        ("Gauss $\\mathbb{Z}[i]$  $N{=}13$", "2"),
        ("Eisenstein $\\mathbb{Z}[\\omega]$  $N{=}7$", "3"),
        ("Cyclotomy $\\mathbb{Q}(\\zeta_5)$  $N{=}55$", "5"),
        ("Galois $(\\mathbb{Z}/5)^\\times{=}4$", "5"),
        ("Pascal $2^4{=}16$", "2"),
        ("Coxeter $\\varphi(30){=}8$", "30"),
        ("$|\\mathrm{det\\,Cartan}(E_8)|{=}1$", "E_8"),
    ]
    n = len(wit)
    sx, sy = 3.55, (n - 1) / 2.0
    ax.add_patch(plt.Circle((sx, sy), 0.78, facecolor=C["gold"], alpha=0.16,
                            edgecolor=C["gold"], lw=1.8))
    ax.text(sx, sy + 0.20, "ONE object", ha="center", fontsize=8.8,
            fontweight="bold", color=C["gold"])
    ax.text(sx, sy - 0.16, "$(2,3,5)/E_8$", ha="center", fontsize=9.2, color=C["gold"])
    ax.text(sx, sy - 0.52, "(v236)", ha="center", fontsize=7.6, color=C["gold"])
    for i, (g, facet) in enumerate(wit):
        y = n - 1 - i
        ax.text(0.05, y, g, fontsize=8.0, fontweight="bold", color=C["blue"], va="center")
        ax.text(2.45, y, "facet $%s$" % facet, fontsize=7.4, color=C["gray"], va="center")
        ax.annotate("", xy=(sx - 0.78, sy), xytext=(3.05, y),
                    arrowprops=dict(arrowstyle="->", color=C["gold"], lw=0.8, alpha=0.65))
    ax.text(sx, -1.15, "seven readings of one generator\n$\\Rightarrow$ COMPRESS "
            "(not independent)", ha="center", fontsize=8.4, color=C["gold"],
            fontweight="bold")

    ax.plot([4.9, 4.9], [-1.4, n - 0.2], color=C["gray"], lw=0.7, ls=":", alpha=0.6)

    # ---- right panel: what genuinely MULTIPLIES ----
    forced = [("$\\mathrm{rank}\\,E_8$", "8"), ("$h(D_5){=}2(5{-}1)$", "8"),
              ("$\\varphi(30)$", "8"), ("Milnor $(2,3,5)$", "8")]
    bx = 6.9
    by0 = sy + 1.95
    ax.text(bx, by0 + 0.95, "what genuinely MULTIPLIES", ha="center", fontsize=8.8,
            fontweight="bold", color=C["green"])
    for i, (lab, val) in enumerate(forced):
        y = by0 - i * 0.62
        ax.text(5.45, y, lab, fontsize=8.0, color=C["blue"], va="center")
        ax.annotate("", xy=(bx + 0.18, by0 - 0.93), xytext=(bx - 0.05, y),
                    arrowprops=dict(arrowstyle="->", color=C["green"], lw=0.8, alpha=0.6))
    ax.add_patch(plt.Circle((bx + 0.45, by0 - 0.93), 0.5, facecolor=C["green"],
                            alpha=0.18, edgecolor=C["green"], lw=1.6))
    ax.text(bx + 0.45, by0 - 0.93, "$8$ in\n$c_3{=}\\frac{1}{8\\pi}$", ha="center",
            va="center", fontsize=8.0, fontweight="bold", color=C["green"])
    ax.text(bx, by0 - 1.95, "input forced four\nindependent ways", ha="center",
            fontsize=7.8, color=C["green"])
    ax.text(bx, -0.55, "$+$ foreign witness", ha="center", fontsize=8.2,
            color=C["red"], fontweight="bold")
    ax.text(bx, -1.35, "$\\alpha^{-1}\\!\\approx\\!137$ (prime,\nnot in the $(2,3,5)$ skeleton)",
            ha="center", fontsize=7.8, color=C["red"])

    ax.set_xlim(0, 8.7); ax.set_ylim(-2.0, n + 0.4)
    ax.axis("off")
    ax.set_title("Corrected over-determination map (v428): seven arithmetic readouts "
                 "COMPRESS one $(2,3,5)/E_8$ object;\nthe input forced four ways "
                 "$+$ the foreign $\\alpha^{-1}$ are what multiply", fontsize=9.2)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "safeguard_witness_map.pdf"))
    fig.savefig(os.path.join(WEB, "safeguard_witness_map.png"), dpi=150)
    plt.close(fig)


def fig_null_model():
    """Look-elsewhere null model (v100): TFPT 13/13 vs MC pseudo-theories and controls."""
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    labels = ["TFPT", "best MC\npseudo-theory", "$\\varphi_0\\,{\\pm}10\\%$\ncontrol",
              "data shuffle\n(mean)"]
    vals = [13, 5, 6, 1.2]
    cols = [C["green"], C["gray"], C["gold"], C["gray"]]
    ax.bar(labels, vals, color=cols, alpha=0.85, edgecolor=cols)
    ax.axhline(13, color=C["green"], ls=":", lw=0.8)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.25, f"{v}", ha="center", fontsize=9.5, fontweight="bold")
    ax.set_ylabel("observables hit (of 13)")
    ax.set_ylim(0, 14.5)
    ax.set_title("Look-elsewhere null model (v100): $2{\\times}200$k pseudo-theories "
                 "hit $\\leq 5/13$; TFPT $13/13$\njoint $\\prod p_i{=}10^{-25.8}$, "
                 "with $\\alpha$ uniqueness $\\leq 10^{-30.7}$ ($\\sim$102 bits)",
                 fontsize=9.2)
    ax.grid(alpha=0.2, axis="y")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "safeguard_null_model.pdf"))
    fig.savefig(os.path.join(WEB, "safeguard_null_model.png"), dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    fig_alpha_ablation()
    fig_mass_ladder()
    fig_action_tower()
    fig_status_heatmap()
    fig_coxeter_circle()
    fig_translation_clock()
    fig_galois_cp_hexagon()
    fig_coxeter_galois()
    fig_seed_hyperplane()
    fig_attractor()
    fig_sds_cover()
    fig_nariai_entropy()
    fig_cover_twins()
    fig_orientation()
    fig_seam_units()
    fig_trisection()
    fig_rg_running()
    fig_gauge_running()
    fig_slice_compression()
    fig_residual_chain()
    fig_script_timeline()
    fig_qft_skeleton()
    fig_qft_unification()
    fig_ftransfer_dynamics()
    fig_safeguard_layers()
    fig_alpha_uniqueness()
    fig_reverse_audit()
    fig_witness_map()
    fig_null_model()
    print("figures written to", os.path.normpath(OUT))
