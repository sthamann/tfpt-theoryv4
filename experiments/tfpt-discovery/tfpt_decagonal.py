#!/usr/bin/env python3
"""
TFPT-specific 5->3 cut-and-project model set (the 'crystal fingerprint').

- Ambient: Z^5 with the [5,4,2] even-parity condition  sum n_i even
    => this sublattice IS the D_5 (checkerboard) root lattice.
- Natural Z_5 (g_car=5) decomposition of R^5 (DFT basis):
    v0 = (1,1,1,1,1)/sqrt5            'trace' axis (periodic)
    (v1c,v1s) 2D plane, 5-fold (72 deg)   visible quasiperiodic plane
    (v2c,v2s) 2D plane, 144 deg           INTERNAL window space
- Visible E_vis = span(v0,v1c,v1s) (3 dims, matches TFPT '3 visible');
  Internal E_int = span(v2c,v2s)  (2 dims, matches TFPT '2 internal').
- Accept n if internal projection lies in a disk window.
Result: a DECAGONAL quasicrystal (periodic trace-axis x 5-fold plane) with
10-fold Bragg diffraction. Run in venv: python tfpt_decagonal.py
"""
import numpy as np, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
os.makedirs("figures", exist_ok=True)
rng=np.arange(5)
v0 =np.ones(5)/np.sqrt(5)
v1c=np.sqrt(2/5)*np.cos(2*np.pi*1*rng/5); v1s=np.sqrt(2/5)*np.sin(2*np.pi*1*rng/5)
v2c=np.sqrt(2/5)*np.cos(2*np.pi*2*rng/5); v2s=np.sqrt(2/5)*np.sin(2*np.pi*2*rng/5)
B=np.vstack([v0,v1c,v1s,v2c,v2s])
print("orthonormal basis check (max |B B^T - I|):", np.abs(B@B.T-np.eye(5)).max())

K=14
ax=np.arange(-K,K+1)
grids=np.meshgrid(*([ax]*5), indexing='ij')
N=np.stack([g.ravel() for g in grids],axis=1)          # (M,5)
N=N[(N.sum(axis=1)==0)]                                 # one D_5 layer = A_4 root lattice
xi = N@np.vstack([v2c,v2s]).T                           # internal (window) coords
R=1.15                                                  # small acceptance window => sparse, discrete
acc = (xi[:,0]**2+xi[:,1]**2) < R**2
A=N[acc]
vis = A@np.vstack([v1c,v1s]).T                          # visible pentagonal plane
print(f"A_4 layer (sum n_i=0) points in box: {len(N)}; accepted (window R={R}): {len(A)}")

fig,ax2=plt.subplots(1,2,figsize=(11,5.4))
ax2[0].scatter(vis[:,0],vis[:,1],s=10,color='tab:purple')
ax2[0].set_aspect('equal'); ax2[0].set_title(
  "TFPT 5$\\to$3 model set, one trace layer ($A_4$):\npentagonal quasicrystal ($\\mathbb{Z}_5$ cut-and-project)")
ax2[0].set_xlabel("$v_{1c}$ proj"); ax2[0].set_ylabel("$v_{1s}$ proj")

# direct Bragg diffraction I(k)=|sum exp(i k.P)|^2 on a 2D k-grid (crisp peaks)
m=360; ext=8.0
kx=np.linspace(-ext,ext,m); KX,KY=np.meshgrid(kx,kx)
Kv=np.stack([KX.ravel(),KY.ravel()],axis=1)            # (m^2,2)
ph=Kv@vis.T                                            # (m^2, Npts)
I=(np.abs(np.exp(1j*ph).sum(axis=1))**2).reshape(m,m)/len(vis)**2
ax2[1].imshow(np.log1p(I),cmap='inferno',origin='lower',extent=[-ext,ext,-ext,ext])
ax2[1].set_title("Diffraction $|\\sum e^{ik\\cdot r}|^2$ (log):\n10-fold Bragg peaks $\\Rightarrow$ pentagonal/decagonal")
ax2[1].set_xlabel("$k_x$"); ax2[1].set_ylabel("$k_y$")
plt.tight_layout(); plt.savefig("figures/tfpt_decagonal.png",dpi=130); plt.close()
print("saved figures/tfpt_decagonal.png")
print("FINGERPRINT: matter parity [5,4,2] = D_5 lattice; one layer = A_4 root lattice;")
print(" Z_5 3+2 cut-and-project => pentagonal/decagonal quasicrystal, 10-fold Bragg.")
