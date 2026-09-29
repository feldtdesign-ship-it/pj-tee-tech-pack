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

BODY_WIDEN, BODY_FLATTEN = 0.11, 0.14
SHOULDER_OUT, SHOULDER_DROP = 1.4, 0.9
SLEEVE_LONGER, SLEEVE_FULLER = 0.24, 0.18

def ss(a, b, x):
    if x <= a: return 0.0
    if x >= b: return 1.0
    t = (x - a) / (b - a); return t * t * (3 - 2 * t)

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
        body = (1 - fs) * ss(4.0, 8.0, t)                       # body from just above the armhole down
        # sleeves: fuller toward the cuff only (not the cap), then longer
        if fs > 0:
            full = SLEEVE_FULLER * fs * ss(9.0, 11.5, au)
            c = tcent(au); t = c + (t - c) * (1 + full); w = w * (1 + full * .8)
            if au > 8: au = 8 + (au - 8) * (1 + SLEEVE_LONGER * fs)
        # dropped, broader shoulder: everything outside the neck moves out; the edge drops
        sh = ss(3.0, 7.0, au) * (1 - ss(9.0, 12.0, t))
        au = au + SHOULDER_OUT * max(sh, fs * (1 - ss(9.0, 12.0, t)))
        t = t + SHOULDER_DROP * ss(4.0, 9.0, au) * (1 - ss(9.0, 12.0, t))
        # body: wider and flatter, straight sides
        au = au * (1 + BODY_WIDEN * body); w = w * (1 - BODY_FLATTEN * body)
        out.append((cx + sg * au * IN, cy + w * IN, ztop - t * IN))
    for v, p in zip(vs, out): v.co = p
    o.data.update()
    return o

if __name__ == "__main__" or True:
    ob = build()
    print("SHGD_Boxy_Tee rebuilt:", len(ob.data.vertices), "verts")
