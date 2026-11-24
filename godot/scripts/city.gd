extends Node3D
## Builds a city from map data in the web game's format (site/data/*.json, or osm.gd for anywhere on Earth):
## metres, +x east, +y south (Godot +z). Buildings become extruded, windowed blocks merged into chunks;
## roads, parks and water become flat ribbons and polygons. Also answers "is this spot inside a building"
## and "what street is this" from small spatial grids.

const CHUNK := 250.0
const GRID := 50.0
const ROAD_W := {"trunk": 16.0, "primary": 14.0, "secondary": 12.0, "tertiary": 10.0, "residential": 8.0, "unclassified": 8.0,
	"living_street": 6.0, "service": 5.0, "pedestrian": 5.0, "footway": 2.5}
const PALETTE := [Color("#c9ced3"), Color("#aeb5bc"), Color("#8f979f"), Color("#d8dde1"), Color("#9aa7b3"), Color("#7d8a96")]
const TOWER := [Color("#5d7489"), Color("#6f8799"), Color("#4f6275"), Color("#8197a8")]

var origin := Vector2.ZERO          # lat, lon of (0, 0)
var _blocks := {}                   # Vector2i -> Array[PackedVector2Array]
var _streets := {}                  # Vector2i -> Array[[Vector2, Vector2, String]]
var _road_pts: Array[Vector2] = []  # midpoints of named drivable roads, for spawns and parked cars
var _wall_mat: ShaderMaterial
var _flat_mat: StandardMaterial3D

func clear() -> void:
	for c in get_children(): c.queue_free()
	_blocks.clear(); _streets.clear(); _road_pts.clear()

func build(d: Dictionary) -> void:
	clear()
	if d.has("origin"): origin = Vector2(d.origin[0], d.origin[1])
	_wall_mat = ShaderMaterial.new(); _wall_mat.shader = load("res://scripts/building.gdshader")
	_flat_mat = StandardMaterial3D.new(); _flat_mat.vertex_color_use_as_albedo = true; _flat_mat.vertex_color_is_srgb = true; _flat_mat.roughness = 0.95
	_ground()
	_flats(d.get("parks", []), Color("#4f7a4a"), 0.02)
	_flats(d.get("water", []), Color("#2f5f86"), 0.03)
	_roads(d.get("roads", []))
	_buildings(d.get("buildings", []))

func _key(x: float, z: float, size: float) -> Vector2i:
	return Vector2i(floori(x / size), floori(z / size))

func _ground() -> void:
	var m := MeshInstance3D.new(); var p := PlaneMesh.new(); p.size = Vector2(20000, 20000)
	var mat := StandardMaterial3D.new(); mat.albedo_color = Color("#5c6267"); mat.roughness = 1.0; p.material = mat
	m.mesh = p; add_child(m)
	var body := StaticBody3D.new(); var s := CollisionShape3D.new(); s.shape = WorldBoundaryShape3D.new(); body.add_child(s); add_child(body)

func _poly(src: Array) -> PackedVector2Array:
	var poly := PackedVector2Array()
	for p in src: poly.append(Vector2(p[0], p[1]))
	if poly.size() > 2 and poly[0].distance_to(poly[poly.size() - 1]) < 0.01: poly.remove_at(poly.size() - 1)
	return poly

func _flats(polys: Array, col: Color, y: float) -> void:
	var chunks := {}
	for src in polys:
		var poly := _poly(src)
		if poly.size() < 3: continue
		var idx := Geometry2D.triangulate_polygon(poly)
		if idx.is_empty(): continue
		var k := _key(poly[0].x, poly[0].y, CHUNK * 4)
		if not chunks.has(k): chunks[k] = PackedVector3Array()
		var v: PackedVector3Array = chunks[k]
		for i in range(0, idx.size(), 3):
			v.append(Vector3(poly[idx[i]].x, y, poly[idx[i]].y)); v.append(Vector3(poly[idx[i + 2]].x, y, poly[idx[i + 2]].y)); v.append(Vector3(poly[idx[i + 1]].x, y, poly[idx[i + 1]].y))
		chunks[k] = v
	for k in chunks: _flat_mesh(chunks[k], col)

func _flat_mesh(v: PackedVector3Array, col: Color) -> void:
	if v.is_empty(): return
	var n := PackedVector3Array(); n.resize(v.size()); n.fill(Vector3.UP)
	var c := PackedColorArray(); c.resize(v.size()); c.fill(col)
	var arr := []; arr.resize(Mesh.ARRAY_MAX); arr[Mesh.ARRAY_VERTEX] = v; arr[Mesh.ARRAY_NORMAL] = n; arr[Mesh.ARRAY_COLOR] = c
	var mesh := ArrayMesh.new(); mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr); mesh.surface_set_material(0, _flat_mat)
	var mi := MeshInstance3D.new(); mi.mesh = mesh; mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF; add_child(mi)

func _roads(roads: Array) -> void:
	var asphalt := PackedVector3Array(); var walk := PackedVector3Array(); var lines := PackedVector3Array()
	for r in roads:
		var kind: String = r.get("k", "residential")
		var foot := kind in ["footway", "pedestrian"]
		var w: float = r.get("w", ROAD_W.get(kind, 8.0)) if not foot else ROAD_W.get(kind, 2.5)
		var y := 0.04 if foot else 0.05
		var pts := _poly(r.p)
		var name: String = r.get("n", "")
		for i in pts.size() - 1:
			var a := pts[i]; var b := pts[i + 1]
			if a.distance_to(b) < 0.1: continue
			var side := (b - a).normalized().orthogonal() * w * 0.5
			var out := walk if foot else asphalt
			_quad(out, a + side, b + side, b - side, a - side, y)
			if not foot and w >= 10.0: # centre line, dashed every 6 m
				var len := a.distance_to(b); var dir := (b - a) / len; var t := 0.0; var s2 := dir.orthogonal() * 0.08
				while t + 3.0 < len:
					var p0 := a + dir * t; var p1 := a + dir * (t + 3.0)
					_quad(lines, p0 + s2, p1 + s2, p1 - s2, p0 - s2, y + 0.01); t += 6.0
			if name != "" and not foot:
				var seg := [a, b, name]
				for k in _cells(a, b):
					if not _streets.has(k): _streets[k] = []
					_streets[k].append(seg)
				if kind in ["primary", "secondary", "tertiary", "residential"] and a.distance_to(b) > 20.0: _road_pts.append((a + b) * 0.5)
	_flat_mesh(walk, Color("#8d9399"))
	_flat_mesh(asphalt, Color("#2c3034"))
	_flat_mesh(lines, Color("#e8c547"))

func _cells(a: Vector2, b: Vector2) -> Array:
	var out := {}
	var steps := int(ceil(a.distance_to(b) / GRID)) + 1
	for i in steps + 1:
		var p := a.lerp(b, float(i) / steps); out[_key(p.x, p.y, GRID)] = true
	return out.keys()

func _quad(v: PackedVector3Array, a: Vector2, b: Vector2, c: Vector2, d: Vector2, y: float) -> void:
	var A := Vector3(a.x, y, a.y); var B := Vector3(b.x, y, b.y); var C := Vector3(c.x, y, c.y); var D := Vector3(d.x, y, d.y)
	_tri(v, A, B, C, Vector3.UP); _tri(v, A, C, D, Vector3.UP)

## Godot treats clockwise triangles as front faces, so wind each one to face its normal.
func _tri(v: PackedVector3Array, a: Vector3, b: Vector3, c: Vector3, n: Vector3) -> void:
	if (b - a).cross(c - a).dot(n) > 0.0: v.append(a); v.append(c); v.append(b)
	else: v.append(a); v.append(b); v.append(c)

func _buildings(list: Array) -> void:
	var chunks := {}  # Vector2i -> [verts, normals, colors, collision]
	var rng := RandomNumberGenerator.new(); rng.seed = 604
	for b in list:
		var poly := _poly(b.p)
		if poly.size() < 3: continue
		var h: float = max(float(b.get("h", 9.0)), 3.0)
		var cx := Vector2.ZERO
		for p in poly: cx += p
		cx /= poly.size()
		var k := _key(cx.x, cx.y, CHUNK)
		if not chunks.has(k): chunks[k] = [PackedVector3Array(), PackedVector3Array(), PackedColorArray(), PackedVector3Array()]
		var ch: Array = chunks[k]
		var col: Color = (TOWER[rng.randi() % TOWER.size()] if h > 40.0 else PALETTE[rng.randi() % PALETTE.size()])
		var area := 0.0
		for i in poly.size(): area += poly[i].cross(poly[(i + 1) % poly.size()])
		var verts: PackedVector3Array = ch[0]; var norms: PackedVector3Array = ch[1]; var cols: PackedColorArray = ch[2]; var coll: PackedVector3Array = ch[3]
		var n0 := verts.size()
		for i in poly.size():
			var a := poly[i]; var c := poly[(i + 1) % poly.size()]
			var e := (c - a)
			if e.length() < 0.05: continue
			var out := Vector3(e.y, 0, -e.x).normalized() * (-1.0 if area > 0.0 else 1.0)
			var A := Vector3(a.x, 0, a.y); var C := Vector3(c.x, 0, c.y); var Ah := A + Vector3(0, h, 0); var Ch := C + Vector3(0, h, 0)
			var m := verts.size()
			_tri(verts, A, C, Ch, out); _tri(verts, A, Ch, Ah, out)
			for j in verts.size() - m: norms.append(out)
			for j in range(m, verts.size()): coll.append(verts[j])
		var idx := Geometry2D.triangulate_polygon(poly)
		var m2 := verts.size()
		for i in range(0, idx.size(), 3):
			_tri(verts, Vector3(poly[idx[i]].x, h, poly[idx[i]].y), Vector3(poly[idx[i + 1]].x, h, poly[idx[i + 1]].y), Vector3(poly[idx[i + 2]].x, h, poly[idx[i + 2]].y), Vector3.UP)
		for j in verts.size() - m2: norms.append(Vector3.UP)
		for j in verts.size() - n0: cols.append(col)
		var bk := _key(cx.x, cx.y, GRID)
		var r := 0.0
		for p in poly: r = max(r, p.distance_to(cx))
		for gx in range(floori((cx.x - r) / GRID), floori((cx.x + r) / GRID) + 1):
			for gz in range(floori((cx.y - r) / GRID), floori((cx.y + r) / GRID) + 1):
				var g := Vector2i(gx, gz)
				if not _blocks.has(g): _blocks[g] = []
				_blocks[g].append(poly)
	for k in chunks:
		var ch: Array = chunks[k]
		var arr := []; arr.resize(Mesh.ARRAY_MAX); arr[Mesh.ARRAY_VERTEX] = ch[0]; arr[Mesh.ARRAY_NORMAL] = ch[1]; arr[Mesh.ARRAY_COLOR] = ch[2]
		var mesh := ArrayMesh.new(); mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr); mesh.surface_set_material(0, _wall_mat)
		var mi := MeshInstance3D.new(); mi.mesh = mesh; mi.visibility_range_end = 1800.0; add_child(mi)
		var body := StaticBody3D.new(); var cs := CollisionShape3D.new(); var shape := ConcavePolygonShape3D.new()
		shape.backface_collision = true; shape.set_faces(ch[3]); cs.shape = shape; body.add_child(cs); add_child(body)

func set_view(d: float) -> void:
	for c in get_children():
		if c is MeshInstance3D and c.visibility_range_end > 0.0: c.visibility_range_end = d

func blocked(p: Vector2) -> bool:
	for poly in _blocks.get(_key(p.x, p.y, GRID), []):
		if Geometry2D.is_point_in_polygon(p, poly): return true
	return false

func street(p: Vector2) -> String:
	var best := ""; var bd := 40.0
	var k := _key(p.x, p.y, GRID)
	for dx in [-1, 0, 1]:
		for dz in [-1, 0, 1]:
			for s in _streets.get(k + Vector2i(dx, dz), []):
				var d := p.distance_to(Geometry2D.get_closest_point_to_segment(p, s[0], s[1]))
				if d < bd: bd = d; best = s[2]
	return best

## Nearest point on a named road that isn't inside a building: where people and cars spawn.
func open_spot(p: Vector2) -> Vector2:
	var best := p; var bd := INF
	for q in _road_pts:
		var d := q.distance_squared_to(p)
		if d < bd and not blocked(q): bd = d; best = q
	return best

func road_points_near(p: Vector2, r: float) -> Array[Vector2]:
	var out: Array[Vector2] = []
	for q in _road_pts:
		if q.distance_to(p) < r and not blocked(q): out.append(q)
	return out
