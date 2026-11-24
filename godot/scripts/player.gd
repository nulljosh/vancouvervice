extends CharacterBody3D
## Third-person hero: camera-relative W A S D, Shift run, Space jump, mouse look. Tab swaps who you are.

const WALK := 2.4
const RUN := 6.5
const JUMP := 5.0
const GRAV := 18.0

var model: Node3D
var anim: AnimationPlayer
var map := {}
var yaw := 0.0
var pitch := -0.2
var cam_pivot: Node3D
var arm: SpringArm3D
var qa_forward := false
var sens := 1.0
var turn := 0.0
var freeze_idle := false

func _ready() -> void:
	var cs := CollisionShape3D.new(); var cap := CapsuleShape3D.new(); cap.radius = 0.35; cap.height = 1.8
	cs.shape = cap; cs.position.y = 0.9; add_child(cs)
	cam_pivot = Node3D.new(); cam_pivot.top_level = true; add_child(cam_pivot)
	arm = SpringArm3D.new(); arm.spring_length = 4.2; arm.margin = 0.3; arm.add_excluded_object(get_rid()); cam_pivot.add_child(arm)
	var cam := Camera3D.new(); cam.fov = 70; cam.far = 3000; arm.add_child(cam); cam.current = true

func wear(scene: PackedScene, anims: Dictionary) -> void:
	if model: model.queue_free()
	model = scene.instantiate(); add_child(model); map = anims
	turn = anims.get("turn", 0.0); freeze_idle = anims.get("freeze_idle", false)
	model.rotation.y = yaw + PI + turn
	var found := model.find_children("*", "AnimationPlayer", true, false)
	anim = found[0] if found.size() else null
	if anim:
		for k in ["idle", "walk", "run"]:
			if not anim.has_animation(map.get(k, "")): continue
			var a := anim.get_animation(map[k]); a.loop_mode = Animation.LOOP_LINEAR
			if map.get("strip_root", "") != "": # walk cycles that also move the body: keep the legs, drop the drift
				for ti in range(a.get_track_count() - 1, -1, -1):
					if a.track_get_type(ti) == Animation.TYPE_POSITION_3D and String(a.track_get_path(ti)).ends_with(map.strip_root): a.remove_track(ti)
		_play("idle")

func _play(k: String, speed := 1.0) -> void:
	if not anim: return
	if k == "idle" and freeze_idle: # no usable idle clip: hold a feet-together frame of the walk
		if anim.current_animation != map.walk or anim.speed_scale != 0.0: anim.play(map.walk, 0.2); anim.seek(anim.current_animation_length * 0.125, true)
		anim.speed_scale = 0.0; return
	var n: String = map.get(k, map.get("walk", ""))
	if anim.current_animation != n: anim.play(n, 0.2)
	anim.speed_scale = speed

func _unhandled_input(e: InputEvent) -> void:
	if e is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		yaw -= e.relative.x * 0.004 * sens; pitch = clamp(pitch - e.relative.y * 0.003 * sens, -1.2, 0.5)

func _physics_process(dt: float) -> void:
	var inp := Input.get_vector("left", "right", "forward", "back")
	if qa_forward: inp = Vector2(0, -1)
	var dir := Basis(Vector3.UP, yaw) * Vector3(inp.x, 0, inp.y)
	var running := Input.is_action_pressed("run")
	var speed := RUN if running else WALK
	velocity.x = dir.x * speed; velocity.z = dir.z * speed
	if is_on_floor():
		if Input.is_action_just_pressed("jump"): velocity.y = JUMP
	else: velocity.y -= GRAV * dt
	move_and_slide()
	if model and dir.length() > 0.1: model.rotation.y = lerp_angle(model.rotation.y, atan2(dir.x, dir.z) + turn, 12.0 * dt)
	if not is_on_floor() and map.has("jump"): _play("jump")
	elif dir.length() > 0.1: _play("run" if running else "walk", 1.0 if map.has("run") or not running else 2.0)
	else: _play("idle")

func _process(dt: float) -> void:
	cam_pivot.global_position = cam_pivot.global_position.lerp(global_position + Vector3(0, 1.6, 0), min(1.0, 14.0 * dt))
	cam_pivot.rotation = Vector3(pitch, yaw, 0)
