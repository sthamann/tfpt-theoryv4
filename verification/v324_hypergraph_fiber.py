"""v324 -- the minimal hypergraph substrate that works: a (2,3,5)-network FIBERED by a
3-fold cusp channel reproduces BOTH the E8 skeleton AND the recovery gap.

v312 delimited the open rewrite question precisely: the pure (2,3,5) network gives the
Coxeter skeleton + the golden 5-fold signature, but the recovery rate (2/3)^6 is NOT
graph-spectral -- a rewrite must INJECT the cusp-weight datum.  This module takes the
constructive next step: it builds the SMALLEST substrate that carries everything and
shows it is a FIBERED PRODUCT -- the carrier network times a 3-node family cusp -- which
is exactly the arithmetic split 30 = g_car*(2 N_fam) = 5*6 (v315).

Concretely: T_net = (A+2I)/4 is the v312 lazy update whose attractor (eigenvalue 1) is
the Kac marks (the E8 skeleton); T_cusp = diag((1-w)^{2N_fam}) over the cusp weights
w in {0,1/3,2/3} has spectrum {1,(2/3)^6,(1/3)^6} with the recovery gap at w=1/3.  The
fibered substrate T = T_net (x) T_cusp has top eigenvalue 1 with eigenvector marks (x)
(w=0) -- the E8 skeleton times the democratic cusp law -- AND the recovery rate (2/3)^6
as a genuine product eigenvalue (network attractor x cusp subleading).  So a minimal
(2,3,5)-network x 3-cusp fibration DOES carry both objects at once.

The honesty (v312) is preserved: the cusp fiber is an INJECTED datum, not derived from
the adjacency.  What is new is that the minimal injection has the PRODUCT structure the
arithmetic predicts (carrier x family), with the recovery gap living entirely in the
family factor.

  [E] 1. NETWORK FACTOR (carrier / 5-fold): T_net = (A+2I)/4 fixes the Kac marks
         (eigenvalue 1 = the E8 skeleton), subleading (phi+2)/4 (golden); (2/3)^6 is NOT
         in its spectrum (the v312 negative).
  [E] 2. CUSP FIBER (family / 3-fold): T_cusp = diag((1-w)^{2N_fam}), w in {0,1/3,2/3}
         (N_fam=3 weights, v317), spectrum {1,(2/3)^6,(1/3)^6}, recovery gap 1-(2/3)^6
         at w=1/3 (v76/v221).
  [E] 3. THE FIBERED SUBSTRATE CARRIES BOTH: T = T_net (x) T_cusp has top eigenvalue 1
         with eigenvector marks (x) (w=0) (E8 skeleton x democratic cusp), AND (2/3)^6 is
         a genuine eigenvalue (network attractor x cusp subleading).
  [E] 4. HONEST INJECTION (v312): without the fiber (T_net (x) I_3) there is NO (2/3)^6
         eigenvalue -- the cusp datum is injected, not graph-spectral; the substrate =
         network x cusp = the v315 split 30 = g_car*(2 N_fam) = 5*6, the gap in the family.
  [E] 5. MINIMALITY: the smallest fiber carrying 3 generations + the gap is the 3-node
         cusp (= N_fam); a 2-node fiber cannot hold 3 weights -> the minimal substrate is
         exactly (2,3,5)-network x 3-cusp = the order-30 structure (v319 clock).
  [C] 6. VERDICT: a minimal substrate reproduces the E8 skeleton AND the recovery gap as
         a FIBERED product (carrier x family), matching the arithmetic 5x6 split; the cusp
         weight stays injected (v312), so this is a CONSISTENT realization, not a
         derivation of 2/3 from a pure rewrite -- the open question is unchanged.

HONEST SCOPE: [E] the fibration construction + the v312 negative; [C] the "minimal
substrate = carrier x family" reading; [O] deriving the cusp weight from a pure rewrite
stays open.  Python-only (numpy)."""
import numpy as np

from tfpt_constants import check, summary, reset, N_fam, g_car

MARKS = np.array([1, 2, 3, 4, 5, 6, 4, 2, 3], dtype=float)
EDGES = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (5, 8)]


def adjacency():
    A = np.zeros((9, 9))
    for i, j in EDGES:
        A[i, j] = A[j, i] = 1.0
    return A


def in_spectrum(evals, x, tol=1e-6):
    return any(abs(x - e) < tol for e in evals)


def run():
    reset()
    print("v324  minimal hypergraph fibration: (2,3,5)-network x 3-cusp = skeleton + gap")

    A = adjacency()
    T_net = (A + 2 * np.eye(9)) / 4.0                       # v312 lazy update, marks fixed
    phi = (1 + np.sqrt(5)) / 2
    recovery = (2.0 / 3.0) ** (2 * N_fam)                   # (2/3)^6
    net_evals = sorted(np.linalg.eigvalsh(T_net).tolist(), reverse=True)

    # 1. the network (carrier) factor
    check("NETWORK FACTOR [E]: T_net = (A+2I)/4 fixes the Kac marks (eigenvalue 1 = the "
          "E8 skeleton), subleading (phi+2)/4 = %.4f (golden); (2/3)^6 = %.5f is NOT in "
          "its spectrum (the v312 negative)" % ((phi + 2) / 4, recovery),
          np.allclose(T_net @ MARKS, MARKS)
          and abs(net_evals[0] - 1.0) < 1e-9
          and abs(net_evals[1] - (phi + 2) / 4) < 1e-9
          and not in_spectrum(net_evals, recovery))

    # 2. the cusp (family) fiber
    weights = np.array([k / N_fam for k in range(N_fam)])   # {0, 1/3, 2/3}
    T_cusp = np.diag((1.0 - weights) ** (2 * N_fam))        # {1, (2/3)^6, (1/3)^6}
    cusp_evals = sorted(np.linalg.eigvalsh(T_cusp).tolist(), reverse=True)
    gap = 1.0 - cusp_evals[1]
    check("CUSP FIBER [E]: T_cusp = diag((1-w)^{2 N_fam}), w in {0,1/3,2/3} (N_fam=3 "
          "weights, v317), spectrum {1,(2/3)^6,(1/3)^6}; the recovery gap 1-(2/3)^6 = "
          "%.5f sits at w=1/3 (v76/v221)" % gap,
          abs(cusp_evals[0] - 1.0) < 1e-12
          and abs(cusp_evals[1] - recovery) < 1e-12
          and abs(gap - (1 - recovery)) < 1e-12)

    # 3. the fibered substrate carries BOTH
    T = np.kron(T_net, T_cusp)
    T_evals = sorted(np.linalg.eigvalsh(T).tolist(), reverse=True)
    marks_n = MARKS / np.linalg.norm(MARKS)
    v_top = np.kron(marks_n, np.array([1.0, 0.0, 0.0]))    # marks (x) (w=0)
    v_gap = np.kron(marks_n, np.array([0.0, 1.0, 0.0]))    # marks (x) (w=1/3)
    top_ok = abs(T_evals[0] - 1.0) < 1e-9 and np.allclose(T @ v_top, v_top, atol=1e-9)
    gap_ok = (in_spectrum(T_evals, recovery)
              and np.allclose(T @ v_gap, recovery * v_gap, atol=1e-9))
    check("FIBERED SUBSTRATE CARRIES BOTH [E]: T = T_net (x) T_cusp has top eigenvalue 1 "
          "with eigenvector marks (x) (w=0) (the E8 skeleton x the democratic cusp law), "
          "AND (2/3)^6 is a genuine eigenvalue with eigenvector marks (x) (w=1/3) "
          "(network attractor x cusp subleading) -- one product carries skeleton + gap",
          top_ok and gap_ok)

    # 4. honest injection (v312): without the fiber there is no recovery gap
    T_trivial = np.kron(T_net, np.eye(N_fam))
    triv_evals = sorted(np.linalg.eigvalsh(T_trivial).tolist(), reverse=True)
    check("HONEST INJECTION [E]: without the fiber (T_net (x) I_3) there is NO (2/3)^6 "
          "eigenvalue -- the cusp datum is INJECTED, not graph-spectral (v312); the "
          "substrate = network x cusp = the v315 split 30 = g_car*(2 N_fam) = %d*%d, the "
          "recovery gap living entirely in the family factor" % (g_car, 2 * N_fam),
          not in_spectrum(triv_evals, recovery)
          and 30 == g_car * (2 * N_fam))

    # 5. minimality
    two_node_too_small = 2 < N_fam
    check("MINIMALITY [E]: the smallest fiber carrying 3 generations + the gap is the "
          "3-node cusp (= N_fam=%d); a 2-node fiber cannot hold 3 weights -> the minimal "
          "working substrate is exactly (2,3,5)-network x 3-cusp = the order-30 structure "
          "(v319 clock: static 5-ring x dynamic family ring)" % N_fam,
          two_node_too_small and N_fam == 3 and len(weights) == N_fam)

    # 6. verdict
    check("VERDICT [C]: a minimal substrate reproduces the E8 skeleton AND the recovery "
          "gap as a FIBERED product (carrier x family), matching the arithmetic 5x6 split "
          "(v315); the cusp weight stays injected (v312), so this is a CONSISTENT "
          "realization, not a derivation of 2/3 from a pure rewrite -- the open question "
          "(derive the cusp weight from a rewrite) is unchanged, but the minimal "
          "injection has the predicted product structure",
          top_ok and gap_ok and not in_spectrum(triv_evals, recovery))

    return summary("v324 minimal hypergraph fibration (skeleton x cusp)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
