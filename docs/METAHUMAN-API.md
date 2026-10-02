# MetaHuman Character plugin, Python API notes

What we learned driving the UE 5.8 MetaHuman Character plugin from `unreal/qa.py`. Read this before touching `/Game/Joshua`. Every line here cost real time on 2026-10-01.

## The asset

`/Game/Joshua` is a `MetaHumanCharacter`. Face came from the iPhone scan (`unreal/face_scan.py`). Building it writes skeletal meshes to `/Game/Unpacked/Joshua/Joshua/Body/SKM_Joshua_BodyMesh` and `.../Face/SKM_Joshua_FaceMesh` (note the doubled `Joshua`; the older `/Game/Unpacked/Joshua/Body` is the September build and is stale). The player Blueprint must be repointed at these after every build; `unreal/body_build.py` does it.

## Rules that hold

- Every subsystem call runs inside `with ScopedMetaHumanCharacterEditor(character=mh):` from `metahuman_character_test_utils`. Set, commit and build in one scope, in one `qa.py` call.
- `build_meta_human(mh, params)` needs real params or it asserts `OutFaceMesh && OutBodyMesh` and kills the editor:
  `pipeline_type = MetaHumanDefaultPipelineType.OPTIMIZED`, `pipeline_quality = MetaHumanQualityLevel.MEDIUM`, `absolute_build_path = "/Game/Unpacked/Joshua"`, `common_folder_path = "/Game/Unpacked/Joshua/Common"`.
- `commit_body_state(mh)` before the build, or the build is a no-op.
- A build peaks near 15 GB. Start it from a freshly launched editor with nothing else open (`unreal/avatar.sh` does the restart).
- Body constraints: match names exactly (`Height`, `Chest`, `Waist`, `Hip`, `Across Shoulder`, `Masculine/Feminine`, `Muscularity`, `Fat`). Substring matching once set `Shoulder Height` and `Neck to Waist` by accident. Set `is_active=False` on everything you are not driving. Ranges come back from `get_body_constraints`.
- `Masculine/Feminine` runs -2 to 2 and **+2 is masculine**. Every build before 2026-10-01 used -2 and came out with a bust. Checked with a live preview (below).
- **The build ignores the body state.** With Masculine/Feminine +2 committed and the preview actor showing a man, `build_meta_human` still wrote the old female body to `/Game/Unpacked/Joshua/Joshua/Body` (2026-10-01, three builds). Do not fight it: the preview actor's transient meshes export to FBX (`SkeletalMeshExporterFBX` on `component.skinned_asset`), reimport onto `metahuman_base_skel` as `/Game/VancouverVice/Joshua/Body/SKM_BodyMale`, copy the `materials` array from the built body (same UVs), and point the player at it. No build, no restart. The exported mesh objects are named `BodyMesh_N_LOD0..3`, not `SKM_Joshua_BodyMesh_*`, so Blender scripts pick the mesh by type.
- Live preview without a build: `sub.try_add_object_to_edit(mh)`, set constraints, `commit_body_state`, then `a = sub.spawn_meta_human_actor(mh)` puts a preview actor in the level. Frame it with `set_level_viewport_camera_info` and `HighResShot` (the window capture does not repaint). Destroy the actor before saving the level.
- Fixed bodies do not apply: `conform_body_to_target` from the FixedCompatibility DNA returns INVALID_INPUT_DATA and `import_body_whole_rig` returns COMBINED_BODY_CANNOT_BE_IMPORTED_AS_WHOLE_RIG on this scanned (combined) character. The plugin ships fixed bodies in `Plugins/MetaHuman/MetaHumanCharacter/Content/Optional/Body/FixedCompatibility/` (`m_tal_unw.dna` is male, tall, underweight; `f_`/`m_`, `srt`/`med`/`tal`, `unw`/`nrw`/`ovw`). Conform to one before shaping:
  `r, verts = sub.get_mesh_for_body_conforming_from_dna(mh, dna, "")`, `r2, jt, jr = sub.get_joints_for_body_conforming_from_dna(dna)`, `sub.conform_body_to_target(mh, verts, jr, False, False)`.
  `SetMetaHumanBodyType` exists in C++ but is not exposed to Python.
- Grooms: the plugin bindings (`Optional/Grooms/Bindings/Hair/*_Binding`) assert in HairStrands on the scanned face and crash the editor. A groom with no binding never renders in Play. The groom card mesh renders only with groom-specific textures. What works: a skinned hair shell cut from the scalp in Blender (`unreal/hair_shell.py`), imported onto the face skeleton and driven by leader pose like the clothes.
- Skin tone is `skin_settings.skin.u`; 0.10 is fair. See UNREAL.md 2026-09-23.
- `EditorAppToolset.CaptureAssetImage(assetPath=...)` returns a base64 PNG of the asset thumbnail. Cheap way to check a body or face mesh without Play.

## Pipeline

`sh unreal/avatar.sh out.jpg`: restart editor, build body (`body_build.py`), export body and face FBX, cut polo, jeans and hair in Blender, reimport (`reimport_clothes.py`, `hairshell_install.py`), apply the scene (`scene_setup.py`), photo (`photo.sh`). About 30 minutes, most of it the editor boot off the LaCie.
