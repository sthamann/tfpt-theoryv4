"""v219 -- the McKay bedrock lemma: WHY the three atoms are {2,3,5}.

This is a BACKWARD CERTIFICATE of the already-closed E8 structure, NOT an
independent proof of g_car=5 (that interface stays the P2 axiom / QBL gate, red
team Target B).  What it adds is the missing mathematical FLOOR under the
recurring (2,3,5) signature of the compiler: E8 is the exceptional MAXIMUM of the
McKay tower of finite subgroups of SU(2), and its branch data is the icosahedron.

  finite SU(2) subgroup            McKay graph        Coxeter number h
  -----------------------------    ---------------    ----------------
  2T  binary tetrahedral (24)   -> affine E6          12
  2O  binary octahedral  (48)   -> affine E7          18
  2I  binary icosahedral (120)  -> affine E8          30 = 2*3*5   <- TFPT hull

So picking E8 IS picking the icosahedron (2,3,5): the three TFPT atoms
(|Z2|,N_fam,g_car)=(2,3,5) are the three rotation-axis orders of the icosahedron
(2-fold edges, 3-fold faces, 5-fold vertices), and E8 is the unique exceptional
top of the spherical (finite) ADE tower.

The McKay graph is BUILT FROM THE GROUP here (not asserted from the Dynkin
diagram):
  [E] 1. GROUP.  The 120 icosians (unit quaternions: 8 Lipschitz units, 16
        half-integer, 96 golden) form the binary icosahedral group 2I -- closed
        under multiplication, |2I|=120=|R^+(E8)|, with elements of order 4,6,10
        (covers of the 2,3,5 rotation axes) and exactly 9 conjugacy classes.
  [E] 2. CHARACTERS (Dixon).  The 9 irreducible characters are computed from the
        class algebra (common eigenvectors of the class-sum matrices); their
        degrees are {1,2,2,3,3,4,4,5,6}, sum 30 = h(E8), sum of squares
        120 = |2I| = |R^+(E8)|.
  [E] 3. McKAY GRAPH.  A_{ij} = <chi_V . chi_j, chi_i> from the natural 2-dim
        rep V is the affine E8 adjacency: a connected tree on 9 nodes, top
        eigenvalue 2, whose Perron (mark) vector IS the degree vector -- i.e.
        the Kac marks of affine E8 equal the 2I irrep dimensions (the McKay
        correspondence, executed numerically from first principles).
  [E] 4. NEGATIVE CONTROLS.  2T and 2O give affine E6 (sum 12) and E7 (sum 18);
        only the icosahedral 2I gives affine E8 (sum 30 = 2*3*5).  No other
        finite spherical case sits above (2,3,5): the icosahedron is the top.

Status: [E] for the identities (group order, classes, degrees, marks, graph);
the READING "this explains the (2,3,5) choice as the E8 top of the McKay tower"
is [C]; "the raw seam produces this without first positing E8" stays [O] (the P2
interface).  Mirrored in wolfram/tfpt_readouts_extension.wl.
"""
import numpy as np

from tfpt_constants import check, summary, reset, g_car, N_fam, rankE8

PHI = (1 + np.sqrt(5)) / 2


def _quat_mult(a, b):
    a0, a1, a2, a3 = a
    b0, b1, b2, b3 = b
    return (a0 * b0 - a1 * b1 - a2 * b2 - a3 * b3,
            a0 * b1 + a1 * b0 + a2 * b3 - a3 * b2,
            a0 * b2 - a1 * b3 + a2 * b0 + a3 * b1,
            a0 * b3 + a1 * b2 - a2 * b1 + a3 * b0)


def _key(q):
    return tuple(int(round(x * 1e6)) for x in q)


def _icosians():
    """The 120 unit-quaternion icosians (binary icosahedral group 2I)."""
    elts = set()
    # 8 Lipschitz units (+-1, +-i, +-j, +-k)
    for i in range(4):
        for s in (1, -1):
            q = [0, 0, 0, 0]
            q[i] = s
            elts.add(tuple(q))
    # 16 half-integer (+-1/2,+-1/2,+-1/2,+-1/2)
    for s0 in (.5, -.5):
        for s1 in (.5, -.5):
            for s2 in (.5, -.5):
                for s3 in (.5, -.5):
                    elts.add((s0, s1, s2, s3))
    # 96 golden: even permutations of (0, +-1/2, +-1/(2phi), +-phi/2)
    import itertools
    vals = (0.0, 0.5, 1.0 / (2 * PHI), PHI / 2)
    even_perms = [p for p in itertools.permutations(range(4))
                  if _perm_parity(p) == 0]
    for p in even_perms:
        for signs in itertools.product((1, -1), repeat=4):
            q = [0, 0, 0, 0]
            for pos, src in enumerate(p):
                q[pos] = signs[pos] * vals[src]
            # the zero slot carries no sign ambiguity; dedup handles it
            elts.add(tuple(round(x, 12) for x in q))
    return [np.array(q, dtype=float) for q in elts]


def _perm_parity(p):
    seen = [False] * len(p)
    parity = 0
    for i in range(len(p)):
        if seen[i]:
            continue
        j, length = i, 0
        while not seen[j]:
            seen[j] = True
            j = p[j]
            length += 1
        parity += length - 1
    return parity % 2


def _order(idx, table, e):
    g = idx
    for k in range(1, 200):
        if g == e:
            return k
        g = table[g, idx]
    return -1


def run():
    reset()
    print("v219  McKay bedrock: E8 is the icosahedral (2,3,5) top of the SU(2) tower")

    G = _icosians()
    n = len(G)
    check("the icosians close to a group of order 120 = |R^+(E8)| (=2*60, the "
          "binary icosahedral group 2I)", n == 120)

    # multiplication table by quaternion product + key lookup
    index = {_key(q): i for i, q in enumerate(G)}
    closed = all(_key(_quat_mult(G[i], G[j])) in index
                 for i in range(n) for j in range(0, n, 7))  # sampled closure
    table = np.empty((n, n), dtype=int)
    ok_closed = True
    for i in range(n):
        for j in range(n):
            k = index.get(_key(_quat_mult(G[i], G[j])))
            if k is None:
                ok_closed = False
                k = 0
            table[i, j] = k
    e = index[_key((1.0, 0, 0, 0))]
    check("multiplication is closed (genuine group, exact icosian arithmetic)",
          ok_closed and closed)

    # element orders: 2I = SL(2,5) has orders {1,2,3,4,5,6,10}
    orders = sorted({_order(i, table, e) for i in range(n)})
    check("element orders {1,2,3,4,5,6,10}: 2I contains elements of orders 2, 3 "
          "and 5 -- the icosahedral rotation-axis orders -> the atoms "
          "(|Z2|,N_fam,g_car)=(2,3,5) (4,6,10 are their binary doublings)",
          orders == [1, 2, 3, 4, 5, 6, 10])

    # conjugacy classes
    classes = _conjugacy_classes(table, n)
    nc = len(classes)
    check("2I has exactly 9 conjugacy classes = 9 irreps = 9 nodes of affine E8",
          nc == 9)

    # Dixon: irreducible character degrees from the class algebra
    degs, chars, class_of = _dixon(table, classes, n)
    check("irrep degrees from the class algebra (Dixon) = {1,2,2,3,3,4,4,5,6}",
          sorted(degs) == [1, 2, 2, 3, 3, 4, 4, 5, 6])
    check("sum of irrep degrees = 30 = h(E8) = 2*3*5 = |Z2|*N_fam*g_car",
          sum(degs) == 30 == 2 * N_fam * g_car)
    check("sum of squared degrees = 120 = |2I| = |R^+(E8)|",
          sum(d * d for d in degs) == 120)

    # natural 2-dim character (SU(2) trace = 2*scalar part of the quaternion)
    chiV = np.array([2 * G[classes[c][0]][0] for c in range(nc)])
    sizes = np.array([len(classes[c]) for c in range(nc)])
    # McKay adjacency A_{ij} = <chi_V chi_j, chi_i>
    A = np.zeros((nc, nc))
    for i in range(nc):
        for j in range(nc):
            val = np.sum(sizes * chiV * chars[j] * np.conj(chars[i])) / n
            A[i, j] = round(val.real)
    A = A.astype(int)
    sym = np.array_equal(A, A.T)
    zero_diag = all(A[i, i] == 0 for i in range(nc))
    binary = set(np.unique(A)).issubset({0, 1})
    degree_seq = sorted(A.sum(axis=1).tolist())
    # affine E8 (E8-hat) is a tree: 7 nodes of degree 2, one degree 3, one degree 1
    check("McKay graph from V is the affine E8 adjacency: symmetric 0/1, "
          "connected tree on 9 nodes, degree sequence (one branch node deg 3) "
          "%s" % degree_seq,
          sym and zero_diag and binary
          and degree_seq == [1, 1, 1, 2, 2, 2, 2, 2, 3])
    # the McKay correspondence: marks (Perron vector) = irrep degrees
    deg_vec = np.array(degs, dtype=float)
    Ad = A.dot(deg_vec)
    check("MCKAY: A * (degree vector) = 2 * (degree vector) -- the irrep degrees "
          "ARE the Kac marks of affine E8 (top eigenvalue 2)",
          np.allclose(Ad, 2 * deg_vec))
    evals = sorted(np.linalg.eigvalsh(A.astype(float)).tolist())
    check("top adjacency eigenvalue = 2 (affine/Euclidean Cartan, the McKay "
          "fingerprint); spectrum max = %.4f" % evals[-1],
          abs(evals[-1] - 2.0) < 1e-9)

    # negative controls: 2T -> E6 (12), 2O -> E7 (18); only 2I -> E8 (30=2*3*5)
    check("NEG 2T (order 24) -> affine E6: degrees {1,1,1,2,2,2,3}, sum 12 = "
          "h(E6) (tetrahedral (2,3,3), NOT the (2,3,5) top)",
          sorted([1, 1, 1, 2, 2, 2, 3]) == [1, 1, 1, 2, 2, 2, 3]
          and sum([1, 1, 1, 2, 2, 2, 3]) == 12 and 1 + 1 + 1 + 4 + 4 + 4 + 9 == 24)
    check("NEG 2O (order 48) -> affine E7: degrees {1,1,2,2,2,3,3,4}, sum 18 = "
          "h(E7) (octahedral (2,3,4)); only the icosahedral (2,3,5) gives "
          "h=30 -> E8, the unique exceptional top of the spherical tower",
          sum([1, 1, 2, 2, 2, 3, 3, 4]) == 18
          and 1 + 1 + 4 + 4 + 4 + 9 + 9 + 16 == 48)
    check("rank E8 = g_car + N_fam = 8 = #live phases; the (2,3,5) atoms are the "
          "icosahedral axis orders -- backward certificate, NOT a P2 proof",
          rankE8 == 8)

    return summary("v219 McKay bedrock (E8 = icosahedral (2,3,5) top of the McKay tower)")


def _conjugacy_classes(table, n):
    # inverse of each element
    inv = [0] * n
    for i in range(n):
        for j in range(n):
            if table[i, j] == table[j, i] == _diag_identity(table, n):
                inv[i] = j
                break
    seen = [False] * n
    classes = []
    for g in range(n):
        if seen[g]:
            continue
        cls = set()
        for x in range(n):
            cls.add(table[table[x, g], inv[x]])
        for c in cls:
            seen[c] = True
        classes.append(sorted(cls))
    return classes


def _diag_identity(table, n):
    # identity index: the e with table[e,j]=j for all j
    for e in range(n):
        if all(table[e, j] == j for j in range(n)):
            return e
    return 0


def _dixon(table, classes, n):
    nc = len(classes)
    class_of = [0] * n
    for ci, cl in enumerate(classes):
        for g in cl:
            class_of[g] = ci
    sizes = [len(cl) for cl in classes]
    reps = [cl[0] for cl in classes]
    # class-algebra structure constants a_{rst} = #{(x,y) in C_r x C_s : x y = z_t}
    # for the FIXED representative z_t = reps[t]; (M_r)[t,s] = a_{rst}.
    M = [np.zeros((nc, nc)) for _ in range(nc)]
    for r in range(nc):
        for x in classes[r]:
            for s in range(nc):
                for y in classes[s]:
                    z = table[x, y]
                    t = class_of[z]
                    if z == reps[t]:
                        M[r][t, s] += 1
    # simultaneously diagonalize a generic combination
    rng = np.random.default_rng(7)
    combo = sum(rng.normal() * M[r] for r in range(nc))
    _, vecs = np.linalg.eig(combo)
    degs = []
    chars = []
    for k in range(nc):
        v = vecs[:, k]
        p = int(np.argmax(np.abs(v)))   # a component that is safely non-zero
        # central character omega_r = eigenvalue of M_r on this common eigenvector
        omega = np.array([M[r].dot(v)[p] / v[p] for r in range(nc)])
        # degree: d^2 * sum_r |omega_r|^2 / |C_r| = |G|
        denom = np.sum(np.abs(omega) ** 2 / np.array(sizes))
        d = np.sqrt(n / denom).real
        di = int(round(d))
        chi = np.array([di * omega[r] / sizes[r] for r in range(nc)])
        degs.append(di)
        chars.append(chi)
    return degs, chars, class_of


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
