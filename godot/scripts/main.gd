extends Node3D
## Vancouver Vice, native. Builds the real downtown map, plays the opening over it, then the title screen.
## In game: Tab switches between Joshua and Dad, Esc pauses. Saves and settings live in user://.
## QA: Godot --path godot -- --qa /tmp/shot   (walks through intro, title, play and pause, writes _1.._6.png, quits)

const HEROES := {
	"Joshua": {"scene": "res://assets/joshua.glb", "at": Vector2(8, 16),
		"anims": {"idle": "Idle", "walk": "Casual_Walk", "run": "Run_02", "jump": "Regular_Jump", "turn": PI}},
	"Brian": {"scene": "res://assets/brian.glb", "at": Vector2(-2668, 1636),
		"anims": {"idle": "walk", "walk": "walk", "freeze_idle": true, "strip_root": "Bip01"}},
}
var SAVE := "user://save.json"  # QA runs use their own file so they never touch a real save
const CFG := "user://settings.json"

var city: Node3D
var player: CharacterBody3D
var ui: CanvasLayer
var sun: DirectionalLight3D
var env: Environment
var drone: Camera3D
var state := "boot"
var who := "Joshua"
var spots := {}
var settings := {"sens": 1.0, "view": 1800.0, "shadows": true, "fullscreen": false}
var played := 0.0
var drone_t := 0.0
var qa := ""
var qa_t := 0.0

func _ready() -> void:
	DisplayServer.window_set_title("Vancouver Vice")
	for a in [["forward", KEY_W], ["back", KEY_S], ["left", KEY_A], ["right", KEY_D], ["run", KEY_SHIFT], ["jump", KEY_SPACE], ["swap", KEY_TAB]]:
		InputMap.add_action(a[0]); var ev := InputEventKey.new(); ev.physical_keycode = a[1]; InputMap.action_add_event(a[0], ev)
	var args := OS.get_cmdline_user_args(); var i := args.find("--qa")
	if i >= 0 and i + 1 < args.size(): qa = args[i + 1]; SAVE = "user://qa_save.json"; DirAccess.remove_absolute(SAVE)
	var f := FileAccess.get_file_as_string(CFG)
	if f != "": settings.merge(JSON.parse_string(f), true)
	_sky()
	ui = preload("res://scripts/ui.gd").new(); ui.main = self; add_child(ui)
	ui.loading()
	await get_tree().process_frame; await get_tree().process_frame
	var path := "res://data/downtown.json"
	if not FileAccess.file_exists(path): path = ProjectSettings.globalize_path("res://").path_join("../site/data/downtown.json")
	var t0 := Time.get_ticks_msec()
	city = preload("res://scripts/city.gd").new(); add_child(city)
	city.build(JSON.parse_string(FileAccess.get_file_as_string(path)))
	print("city built in ", Time.get_ticks_msec() - t0, " ms")
	for h in HEROES: spots[h] = city.open_spot(HEROES[h].at)
	drone = Camera3D.new(); drone.far = 4000; drone.fov = 55; add_child(drone); drone.current = true
	for k in settings: set_setting(k, settings[k], false)
	_dusk(true); state = "intro"; ui.intro()

func _sky() -> void:
	env = Environment.new(); var sky := Sky.new(); var mat := ProceduralSkyMaterial.new()
	mat.sky_top_color = Color("#4f7fb5"); mat.sky_horizon_color = Color("#c4d4e4"); mat.ground_horizon_color = Color("#c4d4e4")
	sky.sky_material = mat; env.background_mode = Environment.BG_SKY; env.sky = sky
	env.ambient_light_source = Environment.AMBIENT_SOURCE_SKY; env.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	env.fog_enabled = true; env.fog_light_color = Color("#c4d4e4"); env.fog_density = 0.0008; env.fog_sky_affect = 0.2
	var we := WorldEnvironment.new(); we.environment = env; add_child(we)
	sun = DirectionalLight3D.new(); sun.rotation_degrees = Vector3(-40, -35, 0); sun.shadow_enabled = true
	sun.directional_shadow_max_distance = 120.0; sun.light_energy = 1.2; add_child(sun)

## The opening and title sit in a pink Vancouver dusk; the game itself is a clear day.
func _dusk(on: bool) -> void:
	var m: ProceduralSkyMaterial = env.sky.sky_material
	m.sky_top_color = Color("#5a6fa8") if on else Color("#4f7fb5")
	m.sky_horizon_color = Color("#f2b8c6") if on else Color("#c4d4e4"); m.ground_horizon_color = m.sky_horizon_color
	env.fog_light_color = m.sky_horizon_color; env.fog_density = (0.45 if on else 1.4) / settings.view
	sun.light_color = Color("#ffd2b8") if on else Color.WHITE; sun.rotation_degrees = Vector3(-18 if on else -40, -35, 0)

# --- flow ------------------------------------------------------------------

func show_title() -> void:
	_dusk(true)
	state = "title"; ui.hud.visible = false; drone.current = true; Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	if player: player.visible = false; _freeze(true)
	ui.title(_save_summary())

func new_game() -> void:
	spots.clear(); for h in HEROES: spots[h] = city.open_spot(HEROES[h].at)
	who = "Joshua"; played = 0.0; _start()

func continue_game() -> void:
	var s = JSON.parse_string(FileAccess.get_file_as_string(SAVE))
	if typeof(s) != TYPE_DICTIONARY: new_game(); return
	who = s.get("who", "Joshua"); played = s.get("played", 0.0)
	for h in s.get("spots", {}): spots[h] = Vector2(s.spots[h][0], s.spots[h][1])
	_start()

func _start() -> void:
	_dusk(false)
	if not player:
		player = preload("res://scripts/player.gd").new(); add_child(player)
	player.visible = true; player.sens = settings.sens
	_become(who, false)
	ui.clear(); ui.hud.visible = true; state = "play"; _freeze(false)
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func pause_game() -> void:
	state = "pause"; _freeze(true); Input.mouse_mode = Input.MOUSE_MODE_VISIBLE; ui.pause()

func resume() -> void:
	ui.clear(); state = "play"; _freeze(false); Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func to_title() -> void:
	save_game(); show_title()

func quit_game() -> void:
	if player and state != "title": save_game()
	get_tree().quit()

func _freeze(on: bool) -> void:
	if not player: return
	player.set_physics_process(not on); player.set_process_unhandled_input(not on)
	if player.anim: player.anim.speed_scale = 0.0 if on else 1.0

func _become(name: String, keep := true) -> void:
	if keep and player: spots[who] = Vector2(player.global_position.x, player.global_position.z)
	who = name
	var h: Dictionary = HEROES[name]
	player.wear(load(h.scene), h.anims)
	var p: Vector2 = spots[name]
	player.global_position = Vector3(p.x, 0.2, p.y); player.velocity = Vector3.ZERO
	player.cam_pivot.global_position = player.global_position + Vector3(0, 1.6, 0)
	player.arm.get_child(0).current = true

# --- saves and settings --------------------------------------------------------

func save_game() -> void:
	if not player: return
	spots[who] = Vector2(player.global_position.x, player.global_position.z)
	var out := {"who": who, "played": played, "time": Time.get_unix_time_from_system(), "street": city.street(spots[who]), "spots": {}}
	for h in spots: out.spots[h] = [spots[h].x, spots[h].y]
	var f := FileAccess.open(SAVE, FileAccess.WRITE); f.store_string(JSON.stringify(out))

func _save_summary() -> String:
	var s = JSON.parse_string(FileAccess.get_file_as_string(SAVE)) if FileAccess.file_exists(SAVE) else null
	if typeof(s) != TYPE_DICTIONARY: return ""
	var name: String = "Dad" if s.get("who") == "Brian" else s.get("who", "Joshua")
	var mins := int(s.get("played", 0.0) / 60.0)
	return "%s on %s, %d min played" % [name, s.get("street", "the street") if s.get("street", "") != "" else "the street", mins]

func set_setting(k: String, v, store := true) -> void:
	settings[k] = v
	match k:
		"sens": if player: player.sens = v
		"view": city.set_view(v); drone.far = v + 600.0; env.fog_density = 1.4 / v
		"shadows": sun.shadow_enabled = v
		"fullscreen": DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_FULLSCREEN if v else DisplayServer.WINDOW_MODE_WINDOWED)
	if store: FileAccess.open(CFG, FileAccess.WRITE).store_string(JSON.stringify(settings))

# --- per frame -------------------------------------------------------------------

func _unhandled_input(e: InputEvent) -> void:
	if state != "play": return
	if e.is_action_pressed("ui_cancel"): pause_game(); get_viewport().set_input_as_handled()
	elif e is InputEventMouseButton and e.pressed: Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	elif e.is_action_pressed("swap"): _become("Brian" if who == "Joshua" else "Joshua")

func _process(dt: float) -> void:
	if state in ["intro", "title"] and drone: _fly(dt)
	if state == "play":
		played += dt
		var p := Vector2(player.global_position.x, player.global_position.z)
		ui.hud.text = "%s   %s\nW A S D move   Shift run   Space jump   Tab switch   Esc pause" % [("Dad" if who == "Brian" else who).to_upper(), city.street(p)]
		if int(played) % 60 == 0 and int(played - dt) % 60 != 0: save_game()
	if qa != "": _qa(dt)

## The opening and the title screen float over downtown: one slow glide in, then a wide, slow circle.
func _fly(dt: float) -> void:
	drone_t += dt
	var c := Vector3(-250, 0, 250)
	if state == "intro":
		var k := clampf(drone_t / 11.0, 0.0, 1.0); k = k * k * (3.0 - 2.0 * k)
		drone.global_position = Vector3(900, 260, 1100).lerp(Vector3(-150, 110, 520), k)
		drone.look_at(c.lerp(Vector3(-200, 20, 0), k))
	else:
		var a := drone_t * 0.035
		drone.global_position = c + Vector3(cos(a) * 560, 190, sin(a) * 560)
		drone.look_at(c + Vector3(0, 40, 0))

func _qa(dt: float) -> void:
	qa_t += dt
	var headless := DisplayServer.get_name() == "headless"
	var at := func(s: float) -> bool: return qa_t >= s and qa_t - dt < s
	var shot := func(n: String):
		if not headless: get_viewport().get_texture().get_image().save_png(qa + n)
		print("qa ", n, " ", state, " fps ", Engine.get_frames_per_second(), " mem ", int(OS.get_static_memory_usage() / 1048576.0), " MB")
	var check := func(ok: bool, what: String):
		print("PASS " if ok else "FAIL ", what)
		if not ok: set_meta("failed", true)
	if at.call(2.0): shot.call("_1.png"); check.call(state == "intro", "opening plays after the city loads")
	if at.call(6.0): shot.call("_2.png"); show_title(); check.call(state == "title" and ui.mode == "title", "title screen shows")
	if at.call(8.0):
		shot.call("_3.png"); new_game(); player.qa_forward = true; set_meta("p0", player.global_position)
		check.call(state == "play" and who == "Joshua", "new game starts as Joshua")
	if at.call(11.0):
		shot.call("_4.png"); player.qa_forward = false
		var moved: float = player.global_position.distance_to(get_meta("p0"))
		check.call(moved > 3.0, "Joshua walks (%.1f m in 3 s)" % moved)
		check.call(city.street(Vector2(player.global_position.x, player.global_position.z)) != "", "HUD names the street")
		_become("Brian"); check.call(who == "Brian" and player.model != null, "Tab switches to Dad")
	if at.call(12.0):
		var p0 := player.global_position; player.global_position = Vector3(city.open_spot(Vector2(8, 16)).x, 0.2, city.open_spot(Vector2(8, 16)).y); set_meta("wall", player.global_position)
		player.qa_forward = true
	if at.call(13.0):
		player.qa_forward = false; shot.call("_5.png"); pause_game(); set_meta("p1", player.global_position)
		save_game(); check.call(FileAccess.file_exists(SAVE) and _save_summary().begins_with("Dad"), "save writes Dad's position")
	if at.call(14.0):
		check.call(player.global_position == get_meta("p1") and ui.mode == "pause", "pause freezes the player")
		shot.call("_6.png"); resume(); to_title(); continue_game()
		check.call(who == "Brian" and state == "play", "continue restores the save")
		var tris := 0; var meshes := 0
		for c in city.get_children():
			if c is MeshInstance3D and c.mesh is ArrayMesh: meshes += 1; tris += c.mesh.surface_get_array_len(0) / 3
		print("BENCH meshes ", meshes, " triangles ", tris, " mem ", int(OS.get_static_memory_usage() / 1048576.0), " MB, frame ", "%.2f" % (Performance.get_monitor(Performance.TIME_PROCESS) * 1000.0), " ms process")
		print("QA ", "FAILED" if has_meta("failed") else "ALL PASS")
		get_tree().quit(1 if has_meta("failed") else 0)
