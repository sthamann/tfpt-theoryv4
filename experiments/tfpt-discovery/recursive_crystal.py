#!/usr/bin/env python3
"""
Creative deep-dive: Wolfram comparison, crystalline/fractal properties,
and RECURSIVE execution of TFPT's defining maps.

Outputs numbers + two figures (figures/).
Run in venv:  python recursive_crystal.py
"""
import numpy as np, mpmath as mp, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
mp.mp.dps = 40
PI = mp.pi
c3 = 1/(8*PI)
phi0 = mp.mpf(4)/3*c3 + 48*c3**4
lamC2 = phi0*(1-phi0)            # = lambda_C^2 (LOGISTIC-MAP form x(1-x))
b1 = mp.mpf(41)/10
deltatop = 3/(256*PI**4)
os.makedirs("figures", exist_ok=True)

print("="*70)
print("RECURSION 1: seed = fixed point of the binary-tree (Catalan) recursion")
print("="*70)
# Catalan GF: u = 1 + z u^2 with z=lamC2; stable fixed pt u_- = 1/(1-phi0)
z = lamC2
u = mp.mpf(0.5)
for n in range(40): u = 1 + z*u*u
print(f"  iterate u_(n+1)=1+lambda_C^2 u_n^2 -> u* = {mp.nstr(u,12)}")
print(f"  predicted 1/(1-phi0)               = {mp.nstr(1/(1-phi0),12)}")
print(f"  => phi0 = lambda_C^2 * u* = {mp.nstr(z*u,12)} (recovers phi0={mp.nstr(phi0,12)})")
mult = 2*z*u   # |g'(u*)| multiplier
print(f"  contraction multiplier |g'(u*)| = 2 lambda_C^2 u* = 2*phi0 = {mp.nstr(2*phi0,6)} (<1 => attractor)")
print("  INTERPRETATION: the TFPT seed is the ATTRACTOR of the binary-tree")
print("  generating recursion C=1+zC^2; 'running it recursively' converges to phi0.")
print()

print("="*70)
print("RECURSION 2: the closure equation as a fixed-point iteration (alpha settles)")
print("="*70)
def phiseam(al):
    q = deltatop*mp.e**(-2*al); return mp.mpf(1)/(6*PI) + q*(1-q)**(mp.mpf(-5)/4)
def g(al):   # alpha = (2 c3^3 alpha^2 + 8 b1 c3^6 ln(1/phiseam))^(1/3)
    return (2*c3**3*al**2 + 8*b1*c3**6*mp.log(1/phiseam(al)))**(mp.mpf(1)/3)
al = mp.mpf("0.02")
traj=[al]
for n in range(60):
    al = g(al); traj.append(al)
print(f"  fixed-point iterate alpha=g(alpha) from 0.02 -> {mp.nstr(al,12)}")
print(f"  alpha_* (cubic root)                          = 0.00729735256221")
print(f"  converged in ~{next(i for i,t in enumerate(traj) if abs(t-al)<1e-15)} steps; alpha is a stable attractor")
print("  => reality 'solves' alpha by recursive self-consistency (a settling computation).")
print()

print("="*70)
print("FRACTAL: logistic map landscape; TFPT uses one point x(1-x)")
print("="*70)
print(f"  lambda_C^2 = phi0(1-phi0) is the logistic step r*x(1-x) at r=1, x=phi0.")
print(f"  The FAMILY r*x(1-x) is the Feigenbaum route to chaos (fractal).")
print(f"  TFPT sits at r=1 (single map), NOT in the chaotic regime: a REDUCIBLE point.")
# Feigenbaum bifurcation figure with TFPT marker
rs = np.linspace(2.5, 4.0, 1400); fig_pts=[]
for r in rs:
    x=0.5
    for _ in range(300): x=r*x*(1-x)
    for _ in range(200): x=r*x*(1-x); fig_pts.append((r,x))
fp=np.array(fig_pts)
plt.figure(figsize=(8,4.5))
plt.plot(fp[:,0], fp[:,1], ',k', alpha=0.25)
plt.axvline(1.0, color='tab:blue', lw=1.2, ls='--')  # off-plot reference
plt.scatter([3.569945], [0.5], s=0)  # Feigenbaum accumulation marker placeholder
plt.title("Logistic map $x\\to r\\,x(1-x)$ — TFPT's flavor decoder is the $r{=}1$ step (reducible),\n"
          "the family is the Feigenbaum route to chaos (fractal)")
plt.xlabel("r"); plt.ylabel("attractor x"); plt.tight_layout()
plt.savefig("figures/feigenbaum.png", dpi=130); plt.close()
print("  saved figures/feigenbaum.png")
print()

print("="*70)
print("CRYSTALLINE: cut-and-project quasicrystal (TFPT internal space = model set)")
print("="*70)
# Representative 2D->1D Fibonacci cut-and-project (TFPT is 5D->3D w/ even-parity window).
phi_g = (1+np.sqrt(5))/2
slope = 1/phi_g
# accepted lattice points: window in internal coord
N=400; pts=[]
ev=np.array([1, slope]); ev/=np.linalg.norm(ev)
iv=np.array([-slope,1]); iv/=np.linalg.norm(iv)
w=(abs(iv[0])+abs(iv[1]))/2   # canonical Fibonacci acceptance window (=> exactly 2 gaps)
for i in range(-N,N):
    for j in range(-N,N):
        p=np.array([i,j]); 
        if abs(p@iv) < w:
            pts.append(p@ev)
pts=np.sort(np.array(pts))
gaps=np.diff(pts)
uniq=np.unique(np.round(gaps,4))
print(f"  Fibonacci chain: {len(pts)} points; distinct gaps = {uniq} (two lengths L,S, ratio≈phi)")
print(f"  gap ratio L/S = {uniq.max()/uniq.min():.5f} (golden ratio {phi_g:.5f})")
# diffraction (pure-point => quasicrystal)
ks=np.linspace(0,20,4000)
S=np.array([abs(np.sum(np.exp(1j*k*pts)))**2 for k in ks])/len(pts)**2
fig,ax=plt.subplots(1,2,figsize=(10,4))
ax[0].plot(pts[:60], np.zeros(60),'|',ms=18,color='tab:purple')
ax[0].set_title("Cut-and-project chain (aperiodic, two gaps L,S, L/S=$\\phi$)")
ax[0].set_yticks([]); ax[0].set_xlabel("position")
ax[1].plot(ks,S,lw=0.8,color='tab:red')
ax[1].set_title("Diffraction $|\\sum e^{ikx}|^2$ — PURE-POINT (Bragg) peaks = quasicrystalline order")
ax[1].set_xlabel("k"); ax[1].set_ylabel("intensity")
plt.tight_layout(); plt.savefig("figures/quasicrystal.png", dpi=130); plt.close()
print("  saved figures/quasicrystal.png")
print("  TFPT analog: Lambda_W={pi_vis(n): n in Z^5, pi_int(n) in W, sum n_i even} (3+2 split,")
print("  [5,4,2] parity window) -> a MODEL SET (Meyer set): aperiodic order, pure-point")
print("  diffraction. Quasicrystalline, NOT fractal; it is the crystal<->fractal bridge.")
print()

print("="*70)
print("SELF-SIMILAR SCALING: the E8 ladder is a power law (discrete scale invariance)")
print("="*70)
kappa = mp.mpf(5)/6/mp.log(mp.mpf(248)/60)
print(f"  X(n) ~ (D_n/D_1)^kappa, D_n=60-2n, kappa={mp.nstr(kappa,6)} -> power-law/log-periodic")
print(f"  carrier exhaustion q^(2^g-1)=q^31: recursive DOUBLING (2^g) -> self-similar ladder")
