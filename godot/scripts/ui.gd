extends CanvasLayer
## Everything you see on top of the city: the opening, the title screen, settings, the pause card and the HUD.
## Look: Rockstar's black-and-red restraint, Wes Anderson's symmetry and pastel frame. Upright Seawall for the
## wordmark, Futura for everything you read. Centered, calm, no italics.

const NIGHT := Color("#0c0d10")
const ASPHALT := Color("#15171c")
const FOG := Color("#a3a6ad")
const PAPER := Color("#f3f1ec")
const RED := Color("#e0362c")
const PINK := Color("#f2b8c6")

var main: Node
var display: Font
var body: SystemFont
var hud: Label
var toast: Label
var mode := ""
var screen: Control
var _intro: Tween

func _ready() -> void:
	layer = 10
	display = load("res://assets/Seawall.ttf")
	body = SystemFont.new(); body.font_names = PackedStringArray(["Futura", "Helvetica Neue"])
	hud = _label("", 18, PAPER, HORIZONTAL_ALIGNMENT_LEFT); hud.position = Vector2(24, 18)
	hud.add_theme_constant_override("outline_size", 6); hud.add_theme_color_override("font_outline_color", Color(0, 0, 0, .8)); hud.visible = false; add_child(hud)
	toast = _label("", 18, PAPER); toast.set_anchors_preset(Control.PRESET_CENTER_BOTTOM); toast.position.y -= 90; toast.modulate.a = 0; add_child(toast)

# --- pieces ---------------------------------------------------------------

func _spaced(f: Font, px: int) -> FontVariation:
	var v := FontVariation.new(); v.base_font = f; v.spacing_glyph = px; return v

func _label(text: String, size: int, col: Color, align := HORIZONTAL_ALIGNMENT_CENTER, font: Font = null) -> Label:
	var l := Label.new(); l.text = text; l.horizontal_alignment = align
	l.add_theme_font_override("font", font if font else body); l.add_theme_font_size_override("font_size", size); l.add_theme_color_override("font_color", col)
	return l

func _caps(text: String, size: int, col: Color) -> Label:
	return _label(text, size, col, HORIZONTAL_ALIGNMENT_CENTER, _spaced(body, 6))

func _wordmark(size: int) -> VBoxContainer:
	var v := VBoxContainer.new(); v.alignment = BoxContainer.ALIGNMENT_CENTER; v.add_theme_constant_override("separation", -int(size * 0.22))
	v.add_child(_label("VANCOUVER", size, PAPER, HORIZONTAL_ALIGNMENT_CENTER, display))
	v.add_child(_label("VICE", size, RED, HORIZONTAL_ALIGNMENT_CENTER, display))
	return v

func _rule(w := 260) -> Control:
	var c := CenterContainer.new(); var v := VBoxContainer.new(); v.add_theme_constant_override("separation", 3)
	for i in 2:
		var r := ColorRect.new(); r.color = PINK; r.custom_minimum_size = Vector2(w, 1); v.add_child(r)
	c.add_child(v); return c

func _box(bg: Color, border: Color, pad := 24) -> StyleBoxFlat:
	var s := StyleBoxFlat.new(); s.bg_color = bg; s.border_color = border; s.set_border_width_all(2 if border.a > 0 else 0)
	s.set_content_margin_all(pad); return s

func _card() -> PanelContainer:
	var p := PanelContainer.new(); p.add_theme_stylebox_override("panel", _box(Color(ASPHALT, .94), PINK, 26))
	p.custom_minimum_size = Vector2(380, 0); return p

func _button(text: String, cb: Callable) -> Button:
	var b := Button.new(); b.text = text; b.custom_minimum_size = Vector2(320, 50); b.focus_mode = Control.FOCUS_ALL
	b.add_theme_font_override("font", body); b.add_theme_font_size_override("font_size", 21)
	b.add_theme_color_override("font_color", PAPER); b.add_theme_color_override("font_hover_color", PAPER); b.add_theme_color_override("font_focus_color", PAPER)
	b.add_theme_stylebox_override("normal", _box(Color(0, 0, 0, 0), Color(0, 0, 0, 0), 10))
	b.add_theme_stylebox_override("hover", _box(RED, Color(0, 0, 0, 0), 10))
	b.add_theme_stylebox_override("focus", _box(Color(RED, .85), Color(0, 0, 0, 0), 10))
	b.add_theme_stylebox_override("pressed", _box(RED.darkened(.2), Color(0, 0, 0, 0), 10))
	b.mouse_entered.connect(b.grab_focus); b.pressed.connect(cb); return b

func _screen(shade: float) -> VBoxContainer:
	if screen: screen.queue_free()
	screen = Control.new(); screen.set_anchors_preset(Control.PRESET_FULL_RECT); add_child(screen); move_child(screen, 0)
	var bg := ColorRect.new(); bg.color = Color(NIGHT, shade); bg.set_anchors_preset(Control.PRESET_FULL_RECT); bg.mouse_filter = Control.MOUSE_FILTER_IGNORE; screen.add_child(bg)
	var cc := CenterContainer.new(); cc.set_anchors_preset(Control.PRESET_FULL_RECT); screen.add_child(cc)
	var v := VBoxContainer.new(); v.alignment = BoxContainer.ALIGNMENT_CENTER; v.add_theme_constant_override("separation", 14); cc.add_child(v)
	return v

func _focus_first(c: Node) -> void:
	for b in c.find_children("*", "Button", true, false): (b as Button).grab_focus.call_deferred(); return

func say(text: String) -> void:
	toast.text = text; toast.modulate.a = 1
	create_tween().tween_property(toast, "modulate:a", 0.0, 0.6).set_delay(1.4)

func clear() -> void:
	if screen: screen.queue_free(); screen = null
	mode = ""

# --- screens ---------------------------------------------------------------

func loading() -> void:
	mode = "loading"; var v := _screen(1.0); v.add_child(_caps("LOADING VANCOUVER", 16, FOG))

## About ten seconds, any key skips: a card, the city from the air, a place name, the wordmark.
func intro() -> void:
	mode = "intro"; _screen(0.0)
	var black := ColorRect.new(); black.color = NIGHT; black.set_anchors_preset(Control.PRESET_FULL_RECT); screen.add_child(black)
	var pres := _caps("JAYBULB  PRESENTS", 18, PINK); pres.set_anchors_preset(Control.PRESET_FULL_RECT); pres.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	var place := _caps("VANCOUVER,  BRITISH COLUMBIA", 16, PAPER); place.set_anchors_preset(Control.PRESET_FULL_RECT); place.vertical_alignment = VERTICAL_ALIGNMENT_BOTTOM; place.offset_bottom = -70
	var mark := _wordmark(120); var cc := CenterContainer.new(); cc.set_anchors_preset(Control.PRESET_FULL_RECT); cc.add_child(mark)
	for n in [pres, place, cc]: n.modulate.a = 0; screen.add_child(n)
	var skip := _label("Press any key", 13, FOG); skip.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT); skip.position += Vector2(-150, -40); screen.add_child(skip)
	_intro = create_tween()
	_intro.tween_property(pres, "modulate:a", 1.0, 1.0).set_delay(0.4)
	_intro.tween_property(pres, "modulate:a", 0.0, 0.7).set_delay(1.0)
	_intro.tween_property(black, "color:a", 0.0, 1.8)
	_intro.tween_property(place, "modulate:a", 1.0, 0.9)
	_intro.tween_property(place, "modulate:a", 0.0, 0.9).set_delay(1.8)
	_intro.tween_property(cc, "modulate:a", 1.0, 1.2)
	_intro.tween_interval(1.6)
	_intro.tween_callback(main.show_title)

func title(continue_text: String) -> void:
	mode = "title"; var v := _screen(0.45)
	v.add_child(_caps("A  JAYBULB  GAME", 14, PINK))
	v.add_child(_wordmark(104))
	v.add_child(_rule())
	v.add_child(_label("Welcome to Vancouver. Don't get caught.", 20, PAPER))
	var gap := Control.new(); gap.custom_minimum_size.y = 8; v.add_child(gap)
	var cc := CenterContainer.new(); var card := _card(); cc.add_child(card); v.add_child(cc)
	var b := VBoxContainer.new(); b.add_theme_constant_override("separation", 6); card.add_child(b)
	if continue_text != "":
		b.add_child(_button("Continue", main.continue_game))
		var s := _label(continue_text, 14, FOG); b.add_child(s)
	b.add_child(_button("New game", main.new_game))
	b.add_child(_button("Settings", func(): settings(title.bind(continue_text))))
	b.add_child(_button("Quit", main.quit_game))
	var foot := _label("Native build 0.1", 13, FOG); foot.set_anchors_preset(Control.PRESET_CENTER_BOTTOM); foot.position.y -= 40; screen.add_child(foot)
	_focus_first(b)

func pause() -> void:
	mode = "pause"; var v := _screen(0.55)
	v.add_child(_label("PAUSED", 56, PAPER, HORIZONTAL_ALIGNMENT_CENTER, display))
	v.add_child(_rule(180))
	var cc := CenterContainer.new(); var card := _card(); cc.add_child(card); v.add_child(cc)
	var b := VBoxContainer.new(); b.add_theme_constant_override("separation", 6); card.add_child(b)
	b.add_child(_button("Resume", main.resume))
	b.add_child(_button("Save game", func(): main.save_game(); say("Saved")))
	b.add_child(_button("Settings", func(): settings(pause)))
	b.add_child(_button("Quit to title", main.to_title))
	_focus_first(b)

func settings(back: Callable) -> void:
	var was := mode; mode = "settings_" + was; var v := _screen(0.6 if was == "pause" else 0.45)
	v.add_child(_label("SETTINGS", 56, PAPER, HORIZONTAL_ALIGNMENT_CENTER, display))
	v.add_child(_rule(180))
	var cc := CenterContainer.new(); var card := _card(); cc.add_child(card); v.add_child(cc)
	var g := GridContainer.new(); g.columns = 2; g.add_theme_constant_override("h_separation", 24); g.add_theme_constant_override("v_separation", 16); card.add_child(g)
	var S: Dictionary = main.settings
	var slider := func(label: String, key: String, lo: float, hi: float, step: float):
		g.add_child(_label(label, 18, PAPER, HORIZONTAL_ALIGNMENT_LEFT))
		var s := HSlider.new(); s.min_value = lo; s.max_value = hi; s.step = step; s.value = S[key]; s.custom_minimum_size = Vector2(200, 28)
		s.value_changed.connect(func(x): main.set_setting(key, x)); g.add_child(s)
	var toggle := func(label: String, key: String):
		g.add_child(_label(label, 18, PAPER, HORIZONTAL_ALIGNMENT_LEFT))
		var c := CheckButton.new(); c.button_pressed = S[key]; c.toggled.connect(func(x): main.set_setting(key, x)); g.add_child(c)
	slider.call("Mouse speed", "sens", 0.3, 3.0, 0.1)
	slider.call("View distance", "view", 600.0, 3000.0, 100.0)
	toggle.call("Shadows", "shadows")
	toggle.call("Full screen", "fullscreen")
	var bc := CenterContainer.new(); var back_b := _button("Back", back); bc.add_child(back_b); v.add_child(bc); back_b.grab_focus.call_deferred()
	set_meta("back", back)

func _unhandled_input(e: InputEvent) -> void:
	var key: bool = (e is InputEventKey and e.pressed and not e.echo) or (e is InputEventMouseButton and e.pressed)
	if mode == "intro" and key:
		if _intro: _intro.kill()
		main.show_title(); get_viewport().set_input_as_handled()
	elif mode.begins_with("settings_") and e.is_action_pressed("ui_cancel"):
		(get_meta("back") as Callable).call(); get_viewport().set_input_as_handled()
	elif mode == "pause" and e.is_action_pressed("ui_cancel"):
		main.resume(); get_viewport().set_input_as_handled()
