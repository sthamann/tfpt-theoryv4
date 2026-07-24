"""EXPLORATION (experiments/ only -- NOT a suite module, NOT in the ledger/papers).

Question (user): "what happens when TFPT's signatures are applied to PI itself --
once, and recursively?"

Here "signatures" = the compiler's defining transformations, read as maps of the
continuous input x (the circle constant, canonical value x = pi):

    S(x)   = 1/(8x)                       seam normalizer      (c3 at x=pi)
    M(x)   = 1/(6x)                       Moebius tree seed    (phi_base at x=pi)
    D(x)   = 48*S(x)^4 = 3/(256 x^4)      topological top-form (dtop at x=pi)
    Phi(x) = M(x) + D(x)                  retained seed        (phi0 at x=pi)
    A(x)   = root a of F_U1(a; pi:=x)     EM closure           (alpha at x=pi)

Related prior sandbox work (NOT duplicated here):
  * pi_information_e8_exploration.py -- pi as compiler fuel (single constant),
    Library-of-Babel rejection of the digit-oracle reading.
  * recursive_crystal.py -- recursion in SEED/ALPHA space (Catalan attractor,
    alpha settling).  This probe instead iterates the maps in PI-SPACE.

Firewall: discovery sandbox.  Digit-level "signature scans" on pi's expansion are
information-theoretically vacuous (normality => every finite pattern occurs) and
are NOT performed; see the Library-of-Babel verdict in the earlier probe.  Any
numeric fixed-point constant found here is guarded by a look-elsewhere MC null
(v100 spirit) before even being CALLED a coincidence.  Nothing here is a claim.

Run:  cd experiments/tfpt-discovery && .venv/bin/python pi_signature_self_application_probe.py
"""
import random

import mpmath as mp

mp.mp.dps = 40
PI = mp.pi
C3 = 1 / (8 * PI)
PHIBASE = 1 / (6 * PI)
DTOP = 48 * C3**4
PHI0 = PHIBASE + DTOP
B1 = mp.mpf(41) / 10

# frozen coincidence-scan targets (compiler constants + canonical readouts);
# used ONLY to ask "does a new fixed-point constant accidentally hit TFPT?"
TARGETS = {
    "c3=1/(8pi)": C3,
    "phi_base=1/(6pi)": PHIBASE,
    "dtop=3/(256pi^4)": DTOP,
    "phi0": PHI0,
    "alpha*": mp.mpf("0.00729735256220985"),
    "alpha^-1": mp.mpf("137.0359992168407"),
    "lambda_C=sqrt(phi0(1-phi0))": mp.sqrt(PHI0 * (1 - PHI0)),
    "xi=3/4": mp.mpf(3) / 4,
    "4/3": mp.mpf(4) / 3,
    "2/3": mp.mpf(2) / 3,
    "(2/3)^6": (mp.mpf(2) / 3)**6,
    "b1=41/10": B1,
    "pi": PI,
}


def S(x):
    return 1 / (8 * x)


def M(x):
    return 1 / (6 * x)


def D(x):
    return 3 / (256 * x**4)


def Phi(x):
    return M(x) + D(x)


def Phi_prime(x):
    return -1 / (6 * x**2) - 3 / (64 * x**5)


def em_closure_roots(x, n_grid=600):
    """All positive roots a of F_U1(a; pi:=x) on the Q<1 branch.

    F(a) = a^3 - 2 cc^3 a^2 - (4/5) cc^6 * 41 * ln(1/phiseam(a)),
    cc = 1/(8x), pb = 1/(6x), dt = 48 cc^4, Q = dt e^{-2a},
    phiseam = pb + Q (1-Q)^{-5/4}   (canonical v3 form).
    The (1-Q)^{-5/4} branch requires Q < 1, i.e. a > ln(dt)/2 when dt > 1.
    Sign-scan on a log grid + bisection refinement; returns the sorted roots.
    """
    cc = 1 / (8 * x)
    pb = 1 / (6 * x)
    dt = 48 * cc**4
    if dt > 1:
        a_min = mp.log(dt) / 2 * mp.mpf("1.000001")
    else:
        # the physical root scales like cc^2; keep the grid floor well below it
        a_min = min(mp.mpf("1e-12"), cc**2 * mp.mpf("1e-8"))

    def F(a):
        Q = dt * mp.e**(-2 * a)
        ps = pb + Q * (1 - Q)**(mp.mpf(-5) / 4)
        if ps <= 0:
            return None
        return a**3 - 2 * cc**3 * a**2 - (mp.mpf(4) / 5) * cc**6 * 41 * mp.log(1 / ps)

    lo, hi = mp.log(a_min), mp.log(mp.mpf("1e7"))
    grid = [mp.e**(lo + (hi - lo) * k / n_grid) for k in range(n_grid + 1)]
    roots = []
    prev_a, prev_f = None, None
    for a in grid:
        f = F(a)
        if f is None:
            prev_a, prev_f = None, None
            continue
        if prev_f is not None and mp.sign(f) != mp.sign(prev_f) and prev_f != 0:
            aa, bb, fa = prev_a, a, prev_f
            for _ in range(200):
                mid = (aa + bb) / 2
                fm = F(mid)
                if fm is None:
                    break
                if mp.sign(fm) == mp.sign(fa):
                    aa, fa = mid, fm
                else:
                    bb = mid
            roots.append((aa + bb) / 2)
        prev_a, prev_f = a, f
    return roots


def sec(t):
    print("\n" + "=" * 76 + "\n" + t + "\n" + "=" * 76)


def main():
    sec("(1) EINMALIG: one application of every signature to pi = the compiler")
    print(f"S(pi)   = {mp.nstr(S(PI), 12)}   (c3        {mp.nstr(C3, 12)})")
    print(f"M(pi)   = {mp.nstr(M(PI), 12)}   (phi_base  {mp.nstr(PHIBASE, 12)})")
    print(f"D(pi)   = {mp.nstr(D(PI), 12)}   (dtop      {mp.nstr(DTOP, 12)})")
    print(f"Phi(pi) = {mp.nstr(Phi(PI), 12)}   (phi0      {mp.nstr(PHI0, 12)})")
    roots_pi = em_closure_roots(PI)
    print(f"A(pi):  roots of F_U1 = {[mp.nstr(r, 12) for r in roots_pi]}"
          f"  -> alpha^-1 = {mp.nstr(1 / roots_pi[0], 13)}")
    ok = (len(roots_pi) == 1
          and abs(1 / roots_pi[0] - TARGETS["alpha^-1"]) < mp.mpf("1e-9"))
    print(f"  unique root and alpha^-1 = 137.0359992168:  {'PASS' if ok else 'FAIL'}")
    print("  -> applied ONCE, the signatures reproduce exactly the canonical")
    print("     compiler constants. That IS the theory content; nothing new appears.")
    print("  (logistic decoder x(1-x): domain [0,1] -- NOT applicable to pi itself;")
    print("   it acts downstream on phi0, see recursive_crystal.py RECURSION 1.)")

    sec("(2) EXACT ALGEBRA: the linear signatures form an infinite dihedral group")
    print(f"S(S(pi)) - pi = {mp.nstr(S(S(PI)) - PI, 5)}   (S is an involution)")
    print(f"M(M(pi)) - pi = {mp.nstr(M(M(PI)) - PI, 5)}   (M is an involution)")
    print(f"(S o M)(x) = 6x/8 = (3/4) x   exactly;  3/4 = xi = c3/phi_tree (v205 [E])")
    print(f"(M o S)(x) = 8x/6 = (4/3) x   exactly;  4/3 = useed/c3 factor")
    print("  -> <S, M> is the infinite dihedral group; its translation (scaling)")
    print("     subgroup is generated by multiplication with xi = 3/4. The")
    print("     gravitational 3/4 is literally the RECURSION RATIO of the two seeds.")
    print("\nOrbit of pi under <S,M>:  {(3/4)^n pi}  u  {(3/4)^n / (8 pi)},  n in Z")
    hits, near = [], []
    for name, t in TARGETS.items():
        best = None
        for n in range(-40, 41):
            for fam, base in (("(3/4)^n*pi", PI), ("(3/4)^n*c3", C3)):
                v = (mp.mpf(3) / 4)**n * base
                d = abs(v - t) / t
                if best is None or d < best[0]:
                    best = (d, n, fam)
        d, n, fam = best
        (hits if d < mp.mpf("1e-30") else near).append((name, fam, n, d))
    print("exact orbit hits (rel dev < 1e-30):")
    for name, fam, n, d in hits:
        print(f"  {name:28s} = {fam} at n={n:3d}")
    print("nearest misses (look-elsewhere bait -- NOT claims):")
    for name, fam, n, d in sorted(near, key=lambda r: r[3])[:4]:
        print(f"  {name:28s} ~ {fam} at n={n:3d}, rel dev {mp.nstr(d, 3)}")
    print("  -> the orbit contains exactly the theory's own seeds (c3, phi_base, pi)")
    print("     and NOTHING else; phi0 itself is NOT in the orbit (see (3c)).")

    sec("(3a) REKURSIV, S and M alone: 2-cycles through pi; neutral fixed points")
    print(f"S: pi -> {mp.nstr(S(PI), 8)} -> {mp.nstr(S(S(PI)), 8)}"
          "   (2-cycle {pi, c3}; recursion returns pi)")
    print(f"M: pi -> {mp.nstr(M(PI), 8)} -> {mp.nstr(M(M(PI)), 8)}"
          "   (2-cycle {pi, phi_base})")
    fpS = 1 / mp.sqrt(8)
    fpM = 1 / mp.sqrt(6)
    print(f"fixed point of S: x = 1/(8x) => x* = 2^(-3/2) = {mp.nstr(fpS, 12)}")
    print(f"   (the 'self-seam' point: the seam identity 8*pi*c3 = 1 read at x = x*)")
    print(f"fixed point of M: x* = 6^(-1/2) = {mp.nstr(fpM, 12)}")
    print(f"|S'(x*)| = {mp.nstr(abs(-1 / (8 * fpS**2)), 6)},"
          f" |M'(x*)| = {mp.nstr(abs(-1 / (6 * fpM**2)), 6)}"
          "  (neutral -- every orbit is a 2-cycle, nothing converges to x*)")

    sec("(3b) REKURSIV, alternating S,M: the xi = 3/4 ladder (log-periodic decay)")
    x = PI
    lad = []
    for _ in range(6):
        x = S(M(x))  # S after M: x -> (3/4) x
        lad.append(x)
    print("  (S o M)^n (pi):  " + ", ".join(mp.nstr(v, 8) for v in lad) + ", ...")
    print("  -> geometric ladder (3/4)^n pi -> 0: no attractor, pure discrete scale")
    print("     invariance with ratio exactly xi = 3/4 (ln-period ln(4/3) = "
          f"{mp.nstr(mp.log(mp.mpf(4) / 3), 8)}).")

    sec("(3c) REKURSIV, Phi = M + D: the top-form term destroys recursive closure")
    xstar = mp.findroot(lambda x: Phi(x) - x, mp.mpf("0.5"))
    mult = Phi_prime(xstar)
    print(f"unique fixed point (Phi strictly decreasing): x* = {mp.nstr(xstar, 12)}")
    print(f"multiplier Phi'(x*) = {mp.nstr(mult, 8)}  => |Phi'| > 1: REPELLING")
    x, orbit = PI, []
    for _ in range(8):
        x = Phi(x)
        orbit.append(x)
        if x > mp.mpf("1e50"):
            break
    print("orbit from pi: " + ", ".join(mp.nstr(v, 6) for v in orbit))
    echo = abs(M(Phi(PI)) - PI) / PI
    print(f"two-step echo: M(Phi(pi)) = {mp.nstr(M(Phi(PI)), 10)} -- back to pi up to")
    print(f"  rel dev {mp.nstr(echo, 6)} = dtop/phi0 (the retained top-form share);")
    print("  the D-term (~x^-4) is amplified at small x and drives the oscillating")
    print("  super-exponential blow-up. The compiler applies D exactly ONCE at the")
    print("  seed; as a recursion in pi-space it is ill-conditioned by construction.")

    sec("(3d) REKURSIV, full EM closure: pi sits in the unique-root window;"
        " recursion leaves it")
    print("root count of F_U1(.; pi:=x) on a log grid in x:")
    windows = []
    for k in range(-20, 21):
        xv = PI * mp.mpf(10)**(mp.mpf(k) / 8)
        n = len(em_closure_roots(xv, n_grid=300))
        windows.append((xv, n))
    desc = ", ".join(f"x={mp.nstr(xv, 4)}:{n}" for xv, n in windows[::4])
    print("  " + desc)
    uniq = [xv for xv, n in windows if n == 1]
    print(f"  unique-root x-window on this grid: [{mp.nstr(min(uniq), 6)}, "
          f">= {mp.nstr(max(uniq), 6)} (grid end)]  (pi = {mp.nstr(PI, 6)} inside)")
    # (i) iterate x -> alpha(x): one step leaves the window
    r1 = em_closure_roots(PI)
    x1 = r1[0]
    r2 = em_closure_roots(x1)
    print(f"alpha-map: pi -> {mp.nstr(x1, 8)}; at x1 the closure has {len(r2)} roots"
          f" {[mp.nstr(r, 6) for r in r2]}")
    print("  -> after ONE recursion step existence/uniqueness (the v3 lemma) is")
    print("     lost and the physical small-alpha branch is gone: ILL-POSED.")
    # (ii) iterate x -> alpha^-1(x): monotone super-exponential divergence
    x, traj = PI, [PI]
    for _ in range(5):
        rr = em_closure_roots(x)
        if len(rr) != 1:
            print(f"  alpha^-1-map stopped: {len(rr)} roots at x = {mp.nstr(x, 6)}")
            break
        x = 1 / rr[0]
        traj.append(x)
        if x > mp.mpf("1e30"):
            break
    print("alpha^-1-map: " + " -> ".join(mp.nstr(v, 7) for v in traj)
          + (" -> ... (super-exponential)" if traj[-1] > mp.mpf("1e10") else ""))
    gaps = []
    for xv, n in windows:
        if n != 1:
            continue
        rr = em_closure_roots(xv, n_grid=300)
        gaps.append(1 / rr[0] - xv)
    print(f"  alpha^-1(x) - x on the unique window: min = {mp.nstr(min(gaps), 6)} > 0")
    print("  -> alpha^-1(x) > x everywhere on the scanned window: NO fixed point,")
    print("     no 'self-consistent circle constant'. pi is NOT a fixed point of")
    print("     its own closure -- it is the external input the closure consumes.")

    sec("(4) COINCIDENCE GUARD (v100 spirit): are the new fixed-point constants"
        " 'TFPT numbers'?")
    rng = random.Random(41)
    for label, y in (("2^(-3/2) [fix S]", fpS), ("6^(-1/2) [fix M]", fpM),
                     (f"x*_Phi = {mp.nstr(xstar, 8)}", xstar)):
        yf = float(y)
        d_obs = min(abs(yf - float(t)) / float(t) for t in TARGETS.values())
        import math
        n_mc, worse = 20000, 0
        lo, hi = math.log10(yf) - 1, math.log10(yf) + 1
        for _ in range(n_mc):
            yr = 10**rng.uniform(lo, hi)
            d = min(abs(yr - float(t)) / float(t) for t in TARGETS.values())
            if d <= d_obs:
                worse += 1
        print(f"  {label:26s} min rel dist to targets = {d_obs:.4f},"
              f"  MC look-elsewhere p = {worse / n_mc:.3f}")
    print("  -> none of the recursion-generated constants lands on a TFPT target")
    print("     beyond chance; no new 'signature constant' is being smuggled in.")

    sec("VERDICT (honest, firewall)")
    print("EINMALIG: applying TFPT's signatures to pi once IS the compiler --")
    print("  it reproduces exactly {c3, phi_base, dtop, phi0, alpha} and nothing else.")
    print("REKURSIV, three regimes:")
    print("  (i)  linear seeds S, M: involutions -> every orbit is a 2-cycle through")
    print("       pi; their composition scales by exactly xi = 3/4 (v205's [E] tree")
    print("       identity re-read as the recursion ratio of the seed group). The")
    print("       orbit of pi contains only the theory's own seeds; no new hits.")
    print("  (ii) seed map Phi = M + D: unique fixed point x* ~ 0.5067 is REPELLING")
    print("       (|Phi'| ~ 2.05); from pi the orbit blows up super-exponentially.")
    print("       The top-form term is a ONE-SHOT correction, not an iterable law.")
    print("  (iii) EM closure: pi lies inside the unique-root window, but one")
    print("       recursion step exits it (existence/uniqueness lost) and the")
    print("       alpha^-1-map diverges monotonically -- there is NO self-consistent")
    print("       circle constant. pi is the external continuous input, not a fixed")
    print("       point of the theory's own dynamics.")
    print("CONCLUSION: TFPT's signature maps are a one-pass evaluation pipeline in")
    print("  pi-space, not a dynamical system with pi as attractor. The only exact")
    print("  recursive structure is the dihedral seed group with ratio 3/4 -- which")
    print("  is already theory content (v205). No promotion candidate; stays here.")


if __name__ == "__main__":
    main()
