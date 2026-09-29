"""Measure a tee in Blender and export it for the web viewer. Run INSIDE Blender (Text Editor or the Blender MCP).

    measure(obj)            -> {"chest", "length", "front_drop", "back_drop", "W", "H"} in export inches
    export(obj, out_path)   -> writes the .glb the viewer needs

Viewer rules (same as the unisex and women's base tees):
  1 unit = 1 in (Blender units treated as metres, divided by 0.0254), centred in x and depth, top of collar at 0,
  front facing forward (Blender -Y -> glTF +Z), about 40k points (decimated copy), normal map only (small file).
Chest = half the distance around the body just below the armhole (a flat tee's chest), measured on the model.
The object is never modified: everything happens on a temporary copy, which is removed after export
(the source object in the .blend is the asset; the .glb is the output).
"""
import bpy, math, os
from mathutils import Vector

IN = 0.0254

def _hull(pts):
    pts = sorted(set(pts))
    if len(pts) < 3: return pts
    cr = lambda o, a, b: (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]

def measure(obj):
    M = obj.matrix_world; vs = [M @ v.co for v in obj.data.vertices]
    zt = max(v.z for v in vs); zb = min(v.z for v in vs); H = zt - zb
    cx = (min(v.x for v in vs) + max(v.x for v in vs)) / 2; cy = (min(v.y for v in vs) + max(v.y for v in vs)) / 2
    # armhole = the lowest height where the sleeves still widen the silhouette sharply
    def width(f):
        b = [v for v in vs if abs((v.z - zb) / H - f) < .006]
        return (max(v.x for v in b) - min(v.x for v in b)) if b else 0
    body_w = width(.35)
    arm = next(f for f in [i / 200 for i in range(60, 190)] if width(f) > body_w * 1.25)
    f_chest = arm - (1.0 * IN * (29.0 / (H / IN))) / H if False else arm - .03   # ~1 in below the armhole
    band = [(round(v.x, 4), round(v.y, 4)) for v in vs if abs((v.z - zb) / H - f_chest) < .006]
    h = _hull(band); per = sum(math.dist(h[i], h[(i + 1) % len(h)]) for i in range(len(h)))
    mid = [v for v in vs if abs(v.x - cx) < .01 * H]
    front = max(v.z for v in mid if v.y < cy); back = max(v.z for v in mid if v.y > cy)   # front faces -Y
    xs = [v.x for v in vs]
    return {"chest": round(per / 2 / IN, 2), "length": round(H / IN, 2), "front_drop": round((zt - front) / IN, 2),
            "back_drop": round((zt - back) / IN, 2), "W": round((max(xs) - min(xs)) / IN, 2), "H": round(H / IN, 2),
            "armhole_below_top": round((1 - arm) * H / IN, 2)}

def export(obj, out_path, target_verts=39250):
    assert not os.path.exists(out_path), f"won't overwrite {out_path}"
    src_mat = obj.data.materials[0]
    nimg = next(n.image for n in src_mat.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image and 'normal' in n.image.name.lower())
    mat = bpy.data.materials.new("TMP_export_normal_only"); mat.use_nodes = True; nt = mat.node_tree
    b = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'); b.inputs["Base Color"].default_value = (.95, .94, .9, 1)
    ti = nt.nodes.new("ShaderNodeTexImage"); ti.image = nimg
    nm = nt.nodes.new("ShaderNodeNormalMap"); nt.links.new(ti.outputs["Color"], nm.inputs["Color"]); nt.links.new(nm.outputs["Normal"], b.inputs["Normal"])
    t = obj.copy(); t.data = obj.data.copy(); t.name = "TMP_export_copy"
    bpy.context.scene.collection.objects.link(t); t.hide_viewport = False; t.hide_set(False)
    t.data.materials.clear(); t.data.materials.append(mat)
    d = t.modifiers.new("dec", "DECIMATE"); d.ratio = min(1.0, target_verts / len(t.data.vertices))
    bpy.ops.object.select_all(action='DESELECT'); t.select_set(True); bpy.context.view_layer.objects.active = t
    bpy.ops.object.modifier_apply(modifier="dec")
    me = t.data; M = t.matrix_world
    for v in me.vertices: v.co = M @ v.co
    t.matrix_world.identity()
    xs = [v.co.x for v in me.vertices]; ys = [v.co.y for v in me.vertices]; zs = [v.co.z for v in me.vertices]
    off = Vector(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, max(zs)))
    for v in me.vertices: v.co = (v.co - off) / IN
    me.update()
    try:
        bpy.ops.export_scene.gltf(filepath=out_path, use_selection=True, export_format='GLB', export_apply=True, export_yup=True)
    finally:
        m2 = t.data; bpy.data.objects.remove(t); bpy.data.meshes.remove(m2); bpy.data.materials.remove(mat)
    return os.path.getsize(out_path)
