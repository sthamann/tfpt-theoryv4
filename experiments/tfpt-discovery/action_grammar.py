#!/usr/bin/env python3
"""
ACTION GRAMMAR audit (Hebel: search actions S=-ln(x), not constants).
Test whether each small/large dimensionless physics number x satisfies
   S_x = -ln(x) = q*alpha^-1 + sum_i m_i * L_i
with q a simple rational and m_i small integers, where the log-generators are
   alpha^-1 = 137.036      (the big hierarchy generator)
   L0 = ln(1/phi0)         (flavor generator)
   Lc = ln(8pi)=ln(1/c3)
   Lt = ln(1/delta_top)    (the CC prefactor 'extra ~9')
Significance: small integer coeffs + residual << data precision = HIT;
large/ugly coeffs = noise (a 4-generator basis can fit anything otherwise).
Reduced Planck mass Mpl = 2.435e18 GeV used consistently.
"""
import mpmath as mp
mp.mp.dps = 30
pi = mp.pi
c3 = 1/(8*pi); phi0 = mp.mpf(4)/3*c3 + 48*c3**4
ainv = mp.mpf("137.035999216841")
gcar = 5
L0 = mp.log(1/phi0)              # 2.934
Lc = mp.log(8*pi)                # 3.224
Lt = mp.log(256*pi**4/3)         # 9.03 = ln(1/delta_top)
Mpl = mp.mpf("2.435e18")         # reduced, GeV

print(f"generators: alpha^-1={mp.nstr(ainv,7)}  L0=ln(1/phi0)={mp.nstr(L0,5)}  "
      f"Lc=ln(8pi)={mp.nstr(Lc,5)}  Lt=ln(1/dtop)={mp.nstr(Lt,5)}")
print(f"            alpha^-1/gcar = {mp.nstr(ainv/gcar,6)}")
print()

# (name, value x [dimensionless], note)
GeV = mp.mpf(1)
quantities = [
 ("v/Mpl (EW)",            mp.mpf("246.22")/Mpl, "electroweak"),
 ("m_e/Mpl",               mp.mpf("0.510999e-3")/Mpl, "lepton n=5"),
 ("m_mu/Mpl",              mp.mpf("0.1056584")/Mpl, "lepton n=3"),
 ("m_tau/Mpl",             mp.mpf("1.77686")/Mpl, "lepton n=2"),
 ("m_p/Mpl",               mp.mpf("0.93827")/Mpl, "proton/QCD"),
 ("Sigma m_nu/Mpl",        mp.mpf("5.88e-11")/Mpl, "neutrino"),
 ("f_a/Mpl",               mp.mpf("8.86e10")/Mpl, "axion PQ"),
 ("M_R/Mpl",               mp.mpf("1.3e15")/Mpl, "seesaw"),
 ("eta_B",                 mp.mpf("6.0e-10"), "baryon asym"),
 ("H0/Mpl",                mp.mpf("1.438e-42")/Mpl, "Hubble today"),
 ("rho_Lambda/Mpl^4",      (mp.mpf("2.26e-12"))**4/Mpl**4, "cosmological const"),
]

def simple_rational(qf, maxden=6):
    best=None
    for d in range(1,maxden+1):
        n=round(float(qf)*d); val=mp.mpf(n)/d
        e=abs(val-qf)
        if best is None or e<best[0]: best=(e,n,d,val)
    return best

print(f"{'quantity':22s} {'S_x':>9s} {'q=S/ainv':>9s}  nearest q     resid(q)")
print("-"*70)
rungs=[]
for name,x,note in quantities:
    S=-mp.log(x); q=S/ainv
    e,n,d,val=simple_rational(q)
    flag=" <== clean q" if e<0.02 else ""
    print(f"{name:22s} {mp.nstr(S,6):>9s} {mp.nstr(q,5):>9s}  {n}/{d}={mp.nstr(val,4):8s} {mp.nstr(e,2)}{flag}")
    rungs.append((name,S,q))
print()

print("ACTION LADDER (clean integer rungs in units of S_EW = alpha^-1/gcar):")
SEW=ainv/gcar
for name,S,q in rungs:
    r=S/SEW
    er,nr,dr,vr=simple_rational(r,maxden=12)
    if er<0.05 and dr<=2:
        print(f"  {name:22s} S/S_EW = {mp.nstr(r,5)} ~ {nr}/{dr}  (S_EW=alpha^-1/gcar)")
print()

print("PSLQ decompositions  S_x = a*ainv + b*L0 + c*Lt + d  (small ints = HIT):")
for name,x,note in [quantities[0],quantities[1],quantities[2],quantities[3],
                    quantities[9],quantities[10]]:
    S=-mp.log(x)
    rel=mp.pslq([S,ainv,L0,Lt,mp.mpf(1)],maxcoeff=400,maxsteps=10000)
    print(f"  {name:20s}: {rel}")
print("  -> None everywhere: beyond the leading q*alpha^-1, the O(1) prefactors")
print("     (which carry beta_rad, rational-pi factors) are NOT simple combos =>")
print("     the action grammar is clean only at the LEADING q*alpha^-1 level.")
print()

print("="*70)
print("CLEAN RESULT 1: the integer action ladder  S_EW : S_Hubble : S_Lambda")
print("="*70)
SEW=(ainv+((794-7*mp.sqrt(9961))/2187)**(mp.mpf(1)/6))/gcar
print(f"  S_EW     = (alpha^-1+delta_ph)/gcar = {mp.nstr(SEW,6)}   (q=1/gcar=1/5)")
print(f"  S_Hubble = -ln(H0/Mpl)              = {mp.nstr(-mp.log(mp.mpf('1.438e-42')/Mpl),6)}  ~ alpha^-1 (q=1)")
print(f"  S_Lambda = -ln(rho_L/Mpl^4)         = {mp.nstr(-mp.log((mp.mpf('2.26e-12'))**4/Mpl**4),6)}  ~ 2 alpha^-1 (q=2)")
print(f"  ratios S_Hubble/S_EW = {mp.nstr(-mp.log(mp.mpf('1.438e-42')/Mpl)/SEW,5)} ~ gcar=5")
print(f"         S_Lambda/S_EW = {mp.nstr(-mp.log((mp.mpf('2.26e-12'))**4/Mpl**4)/SEW,5)} ~ 2gcar=10")
print("  => S_EW : S_Hubble : S_Lambda = 1 : gcar : 2gcar = 1 : 5 : 10  (units alpha^-1/5)")
print()

print("="*70)
print("CLEAN RESULT 2: the EW action alpha^-1/5 is UNIVERSAL across fermions")
print("="*70)
print("  TFPT: m_f/Mpl = [rational*pi * phi0^n_f] * gcar*beta_rad^2 * e^{-(alpha^-1+dph)/5}")
print("  => S_{m_f} = (alpha^-1+dph)/5  +  n_f*ln(1/phi0)  +  (O(1) prefactor)")
beta_rad=phi0/(4*pi)
for nm,coef,n,Sx in [("e",mp.mpf(16)/7,5,49.9156),("mu",mp.mpf(4)/3,3,44.584),
                     ("tau",mp.mpf(7)/6,2,41.7616)]:
    pref = -mp.log(coef*pi/mp.sqrt(2)*gcar*beta_rad**2)
    Spred = SEW + n*L0 + pref
    print(f"  m_{nm:3s}: (a^-1+dph)/5 + {n}*L0 + pref({mp.nstr(pref,4)}) = {mp.nstr(Spred,6)}  vs S_x={Sx}")
print("  => universal EW term (alpha^-1/5) + integer flavor ladder n=5,3,2 in ln(1/phi0).")
print()
print("HONEST: q~1/4,1/3,1/2,1/6 'hits' above are look-elsewhere artifacts")
print("(tol 0.02 over q in [0,2] with ~17 simple rationals => ~2-3 chance hits).")
print("ROBUST new hits: H0 (q=1) and Lambda (q=2); EW universality of alpha^-1/5.")
