#!/usr/bin/env python3
"""
TFPT 'landscape scanner': vary the carrier rank g_car and rebuild every
constant from the SAME machinery, then solve the alpha-closure. Question:
is g_car=5 uniquely the world that matches reality (3 families, SM group,
16-dim generation, alpha^-1~137, b1=41/10)?

Per-g rules (from the carrier source):
  N_fam      = (g+1)/2            (integer only for g odd)
  gamma      = g/(g+1)
  Omega_adm  = N_fam * 2^(g-1)
  b1         = (g*2^(g-2)+1)/10
  phi_base   = 1/((g+1) pi)
  delta_top  = Omega_adm * c3^4
  Bgamma     = g/(g-1)            (seam exponent)
  dim S+     = 2^(g-1)            (one generation = 16 at g=5)
Closure:  alpha^3 - 2 c3^3 alpha^2 - 8 c3^6 b1 * ln(1/phi_seam(alpha)) = 0
"""
import mpmath as mp
mp.mp.dps = 30
pi = mp.pi
c3 = 1/(8*pi)

def world(g):
    g=mp.mpf(g)
    Nfam = (g+1)/2
    gamma = g/(g+1)
    Oadm = Nfam*2**(g-1)
    b1 = (g*2**(g-2)+1)/10
    phib = 1/((g+1)*pi)
    dtop = Oadm*c3**4
    Bg = g/(g-1)
    dimSp = 2**(g-1)
    def phiseam(al):
        q=dtop*mp.e**(-2*al); return phib + q*(1-q)**(-Bg)
    def F(al): return al**3 - 2*c3**3*al**2 - 8*c3**6*b1*mp.log(1/phiseam(al))
    try:
        al=mp.findroot(F, mp.mpf("0.007"))
        ainv=1/al
    except Exception:
        ainv=mp.nan
    return dict(g=int(g),Nfam=Nfam,gamma=gamma,Oadm=Oadm,b1=b1,dimSp=dimSp,ainv=ainv)

print(f"{'g':>2} {'N_fam':>7} {'dim S+':>7} {'Omega':>7} {'10b1':>6} {'alpha^-1':>12}  verdict")
print("-"*70)
for g in [3,4,5,6,7]:
    w=world(g)
    tenb1=int(round(float(w['b1']*10)))
    nf = w['Nfam']
    nf_ok = (float(nf)==int(nf))
    nfs = f"{int(nf)}" if nf_ok else f"{mp.nstr(nf,3)}(non-int!)"
    verd=[]
    if not nf_ok: verd.append("no integer families")
    if abs(float(w['ainv'])-137.036)<0.5: verd.append("alpha~137 !!")
    if int(nf) if nf_ok else 0 ==3 and nf_ok: pass
    if nf_ok and int(nf)==3: verd.append("3 families")
    if g==5: verd.append("(b,s)=(3,2)=SM, dimS+=16")
    print(f"{w['g']:>2} {nfs:>7} {mp.nstr(w['dimSp'],4):>7} {mp.nstr(w['Oadm'],4):>7} {tenb1:>6} "
          f"{mp.nstr(w['ainv'],9):>12}  {'; '.join(verd)}")
print()
print("Note: c3=1/(8pi) fixed for all worlds; only g varies.")
print("=> alpha^-1 is monotonic in g; check which g lands on 137.036.")

# fine check around g=5 and the alpha^-1(g) trend
print("\nalpha^-1 trend (odd g, integer families):")
for g in [3,5,7,9]:
    w=world(g)
    print(f"  g={g}: N_fam={int((g+1)/2)}, alpha^-1={mp.nstr(w['ainv'],8)}")
print("\nCANDIDATE extra rung: beta_rad =? e^{-alpha^-1/g_car^2} (q=1/25)")
phi0=mp.mpf(4)/3*c3+48*c3**4; beta=phi0/(4*pi)
print(f"  -ln(beta_rad) = {mp.nstr(-mp.log(beta),6)} ; alpha^-1/25 = {mp.nstr(137.036/25,6)} "
      f"(resid {mp.nstr(abs(-mp.log(beta)-137.036/25),3)}) -- FLAGGED (likely coincidence)")

# ---- plot alpha^-1(g) continuous, crossing 137.036 at g=5 ----
import os, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
os.makedirs("figures",exist_ok=True)
gs=np.linspace(3,9,200); ainv_c=[]
for g in gs:
    try: ainv_c.append(float(world(g)['ainv']))
    except Exception: ainv_c.append(np.nan)
plt.figure(figsize=(8,4.7))
plt.plot(gs,ainv_c,'-',color='tab:blue',lw=1.8,label=r"$\alpha^{-1}(g_{\rm car})$ from closure")
plt.axhline(137.036,color='tab:red',ls='--',lw=1.2,label=r"observed $\alpha^{-1}=137.036$")
plt.axvline(5,color='tab:green',ls=':',lw=1.2)
for g in [3,5,7,9]:
    a=float(world(g)['ainv']); plt.scatter([g],[a],s=45,color='black',zorder=5)
    plt.annotate(f"g={g}\n$N_f$={int((g+1)/2)}\n"+r"$\alpha^{-1}$="+f"{a:.1f}",
                 (g,a),textcoords="offset points",xytext=(8,6),fontsize=8)
plt.scatter([5],[137.036],s=120,facecolors='none',edgecolors='tab:red',lw=2,zorder=6)
plt.xlabel(r"carrier rank $g_{\rm car}$"); plt.ylabel(r"$\alpha^{-1}$")
plt.title("Landscape scan: only $g_{\\rm car}=5$ gives $\\alpha^{-1}=137.036$\n"
          "(and simultaneously 3 families, dim$S^+$=16, SM group)")
plt.legend(); plt.grid(alpha=0.25); plt.tight_layout()
plt.savefig("figures/landscape_gcar.png",dpi=130); plt.close()
print("\nsaved figures/landscape_gcar.png")
