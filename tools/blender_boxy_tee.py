"""Boxy / oversized tee shape (for the Shaka Wear SHGD) from the unisex source tee. Run INSIDE Blender
(Text Editor > Run, or exec via the Blender MCP) with blender/Shirts_fabric_bake.blend open.

It rebuilds object 'SHGD_Boxy_Tee' in scene 'SHGD Boxy' from 'SOURCE_Comfortable_Tee' every time, so
changing a number below and re-running is safe. The source tee is never modified.

Shape changes, all in viewer inches (the source tee = 29 in long):
  BODY_WIDEN / BODY_FLATTEN   straighter, wider, flatter body from the armhole down (boxy, not round)
  SHOULDER_OUT / SHOULDER_DROP  shoulder line extends further and sits lower at the edge (dropped shoulder)
  SLEEVE_LONGER / SLEEVE_FULLER  longer sleeve toward the elbow, fuller toward the cuff (cap left alone)
Sleeve-cap widening made puffy caps in the first try (2026-09-28), so fullness only starts past the cap.
"""
import bpy
from mathutils import Vector

# v1 widened from just above the armhole (ss 4..8 in down) and flattened 14%: the upper chest bulged into a barrel
# and the front looked pressed flat (Michael, 2026-09-29: "the chest look weird"). v2 widens from below the armhole,
# growing toward the hem (straight boxy sides, natural chest), and barely flattens.
BODY_WIDEN, BODY_FLATTEN = 0.11, 0.03
# Structured 7.5 oz knit: fewer, softer folds than the source tee (Michael, 2026-09-29). Smooths the body only
# (not collar, hem band or sleeves) by averaging each point with its neighbours, FOLD_SMOOTH passes of FOLD_K.
FOLD_SMOOTH, FOLD_K = 30, 0.5
SEAM_TOL = 0.01   # inches
BODY_FROM, BODY_TO = 9.0, 17.0   # inches down from the top where the widening starts / is full
# v1 pushed everything outside the neck out 1.4 in down to the armhole: a broad, linebacker upper chest.
# v2: less, and on the body only along the shoulder line (top ~4 in); the sleeve carries the rest.
SHOULDER_OUT, SHOULDER_DROP = 0.8, 0.6
# SLEEVE_FULLER was 0.18 in v1. Michael, 2026-09-29: the full sleeves looked wrong. This is a bust form, not a
# body with arms, so sleeves hang flat; fullness can come back when there's a model wearing it. v1 is kept in
# the .blend as SHGD_Boxy_Tee_v1_full_sleeves.
SLEEVE_LONGER, SLEEVE_FULLER = 0.24, 0.0

def ss(a, b, x):
    if x <= a: return 0.0
    if x >= b: return 1.0
    t = (x - a) / (b - a); return t * t * (3 - 2 * t)

def smooth_folds(o, cx, ztop, IN):
    if not FOLD_SMOOTH: return
    import numpy as np, collections
    me = o.data; n = len(me.vertices)
    co = np.empty(n * 3); me.vertices.foreach_get("co", co); co = co.reshape(n, 3)
    ed = np.empty(len(me.edges) * 2, dtype=np.int64); me.edges.foreach_get("vertices", ed); ed = ed.reshape(-1, 2)
    au = np.abs(co[:, 0] - cx) / IN; t = (ztop - co[:, 2]) / IN; H = t.max()
    s_ = lambda a, b, x: np.clip((x - a) / (b - a), 0, 1) ** 2 * (3 - 2 * np.clip((x - a) / (b - a), 0, 1))
    # everything below the collar rib and above the hem band, sleeves included (Michael, 2026-09-29: armpit creases
    # too heavy, then sleeve seams crumpled at half strength). Starts below the front rib, which it used to round off.
    wgt = s_(3.6, 5.2, t) * (1 - s_(H - 2.6, H - 1.4, t)) * FOLD_K
    # The tee is sewn panels: seam points exist twice (one per panel) at the same spot. Smooth them as one cloth
    # (merge coincident points), so seams move with the fabric. Pinning seams instead left a groove that read as an
    # open side seam (2026-09-29). Only real openings (neck, hem, sleeve ends) are pinned.
    # points within SEAM_TOL of each other are the same point (rounding to a grid split some pairs: hairline cracks)
    from mathutils.kdtree import KDTree
    kd = KDTree(n)
    for i in range(n): kd.insert(co[i], i)
    kd.balance()
    par = np.arange(n)
    def root(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for i in range(n):
        for (_, j, _) in kd.find_range(co[i], SEAM_TOL * IN):
            ra, rb = root(i), root(j)
            if ra != rb: par[max(ra, rb)] = min(ra, rb)
    roots = np.array([root(i) for i in range(n)])
    rep, inv = np.unique(roots, return_inverse=True); inv = inv.ravel()
    m = len(rep)
    ef = np.zeros(len(me.edges), dtype=np.int64)
    ek = {tuple(sorted(e)): i for i, e in enumerate(ed.tolist())}
    for poly in me.polygons:
        for k in poly.edge_keys: ef[ek[k]] += 1
    E = np.unique(np.sort(inv[ed], axis=1), axis=0); E = E[E[:, 0] != E[:, 1]]
    # an edge on a real opening has one face in total across all its copies
    bf = collections.Counter()
    for (a0, b0), n_ in zip(np.sort(inv[ed], axis=1).tolist(), ef.tolist()): bf[(a0, b0)] += n_
    free = np.ones(m)
    for (a0, b0), n_ in bf.items():
        if n_ == 1: free[a0] = 0; free[b0] = 0
    dg = np.bincount(E.ravel(), minlength=m).astype(float); dg[dg == 0] = 1
    for _ in range(4):   # ease the weight in from the openings
        acc = np.zeros(m); np.add.at(acc, E[:, 0], free[E[:, 1]]); np.add.at(acc, E[:, 1], free[E[:, 0]])
        free = np.minimum(free, acc / dg)
    P = co[rep].copy(); W = np.zeros(m); np.maximum.at(W, inv, wgt); W *= free
    for _ in range(FOLD_SMOOTH):
        acc = np.zeros_like(P)
        np.add.at(acc, E[:, 0], P[E[:, 1]]); np.add.at(acc, E[:, 1], P[E[:, 0]])
        P += (acc / dg[:, None] - P) * W[:, None]
    co = P[inv]
    me.vertices.foreach_set("co", co.ravel())

def build():
    src = bpy.data.objects["SOURCE_Comfortable_Tee"]
    scn = bpy.data.scenes.get("SHGD Boxy") or bpy.data.scenes.new("SHGD Boxy")
    old = bpy.data.objects.get("SHGD_Boxy_Tee")
    keep_loc = None
    if old:
        me = old.data; bpy.data.objects.remove(old); bpy.data.meshes.remove(me)
    o = src.copy(); o.data = src.data.copy(); o.name = "SHGD_Boxy_Tee"; o.data.name = "SHGD_Boxy_Tee_mesh"
    scn.collection.objects.link(o); o.hide_viewport = False; o.hide_render = False
    M = o.matrix_world.copy()
    for v in o.data.vertices: v.co = M @ v.co
    o.matrix_world.identity()
    vs = o.data.vertices
    xs = [v.co.x for v in vs]; ys = [v.co.y for v in vs]; zs = [v.co.z for v in vs]
    cx = (min(xs) + max(xs)) / 2; cy = (min(ys) + max(ys)) / 2; ztop = max(zs); IN = (ztop - min(zs)) / 29.0
    # sleeve centre line: mean depth-below-top of the outer points, per 0.5 in across
    bins = {}
    for v in vs:
        u = abs(v.co.x - cx) / IN; t = (ztop - v.co.z) / IN
        if u > 7 and t < 14: bins.setdefault(round(u * 2) / 2, []).append(t)
    tc = {k: sum(b) / len(b) for k, b in bins.items()}
    def tcent(u):
        k = round(u * 2) / 2
        while k not in tc and k > 7: k -= .5
        return tc.get(k, 6.0)
    out = []
    for v in vs:
        u = (v.co.x - cx) / IN; w = (v.co.y - cy) / IN; t = (ztop - v.co.z) / IN; au = abs(u); sg = 1 if u >= 0 else -1
        fs = ss(7.0, 9.0, au) * (1 - ss(12.5, 14.5, t))        # sleeve
        body = (1 - fs) * ss(BODY_FROM, BODY_TO, t)             # body: from below the armhole, growing to the hem
        # sleeves: fuller toward the cuff only (not the cap), then longer
        if fs > 0:
            full = SLEEVE_FULLER * fs * ss(9.0, 11.5, au)
            c = tcent(au); t = c + (t - c) * (1 + full); w = w * (1 + full * .8)
            if au > 8: au = 8 + (au - 8) * (1 + SLEEVE_LONGER * fs)
        # dropped, broader shoulder: everything outside the neck moves out; the edge drops
        sh = ss(3.0, 7.0, au) * (1 - ss(2.5, 5.5, t))
        au = au + SHOULDER_OUT * max(sh, fs * (1 - ss(9.0, 12.0, t)))
        t = t + SHOULDER_DROP * ss(4.0, 9.0, au) * (1 - ss(9.0, 12.0, t))
        # body: wider and flatter, straight sides
        au = au * (1 + BODY_WIDEN * body); w = w * (1 - BODY_FLATTEN * body)
        out.append((cx + sg * au * IN, cy + w * IN, ztop - t * IN))
    for v, p in zip(vs, out): v.co = p
    smooth_folds(o, cx, ztop, IN)
    o.data.update()
    return o

if __name__ == "__main__" or True:
    ob = build()
    print("SHGD_Boxy_Tee rebuilt:", len(ob.data.vertices), "verts")
