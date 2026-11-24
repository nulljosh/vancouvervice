shader_type spatial;
render_mode cull_disabled;
// Window grid from world position: floors every 3.4 m, bays every 2.8 m, so no UVs or textures.
varying vec3 wpos;
varying vec3 wn;
void vertex() { wpos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz; wn = NORMAL; }
void fragment() {
	float wall = 1.0 - step(0.5, abs(wn.y));
	float along = abs(wn.x) > abs(wn.z) ? wpos.z : wpos.x;
	float fl = fract(wpos.y / 3.4), bay = fract(along / 2.8);
	float win = wall * step(0.3, fl) * step(fl, 0.8) * step(0.18, bay) * step(bay, 0.82) * step(1.2, wpos.y);
	ALBEDO = mix(pow(COLOR.rgb, vec3(2.2)), vec3(0.13, 0.18, 0.25), win * 0.85);
	ROUGHNESS = mix(0.85, 0.12, win);
	METALLIC = win * 0.4;
}
