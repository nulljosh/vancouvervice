"""Title screen assets: the key art (site/img/key-art.png, downscaled to 2048 wide in /Volumes/LaCie/Unreal/dl/menu) as
a UI texture, and Anton (site/fonts/anton.woff2 decompressed to TTF) as a runtime font for HUD DrawText.
Run once: python3 unreal/qa.py "$(cat unreal/menu_setup.py)"."""
import unreal

EAL = unreal.EditorAssetLibrary; AT = unreal.AssetToolsHelpers.get_asset_tools(); D = "/Game/VancouverVice/HUD"
SRC = "/Volumes/LaCie/Unreal/dl/menu/"
for f in ("T_KeyArt.png", "Anton.ttf"):
    t = unreal.AssetImportTask(); t.filename = SRC + f; t.destination_path = D; t.automated = True; t.save = True; t.replace_existing = True
    AT.import_asset_tasks([t]); print("imported", t.imported_object_paths)

tex = EAL.load_asset(D + "/T_KeyArt")
tex.set_editor_property("lod_group", unreal.TextureGroup.TEXTUREGROUP_UI)
tex.set_editor_property("mip_gen_settings", unreal.TextureMipGenSettings.TMGS_NO_MIPMAPS)
tex.set_editor_property("never_stream", True)
EAL.save_loaded_asset(tex)

face = EAL.load_asset(D + "/Anton")
if not isinstance(face, unreal.FontFace):
    face = [EAL.load_asset(p) for p in EAL.list_assets(D, False) if isinstance(EAL.load_asset(p), unreal.FontFace)][0]
if not EAL.does_asset_exist(D + "/F_Anton"):
    AT.create_asset("F_Anton", D, unreal.Font, unreal.FontFactory())
font = EAL.load_asset(D + "/F_Anton")
font.set_editor_property("font_cache_type", unreal.FontCacheType.RUNTIME)
font.set_editor_property("legacy_font_size", 48)
cf = font.get_editor_property("composite_font")  # Typeface isn't exposed to Python, so set it as text
cf.import_text('(DefaultTypeface=(Fonts=((Name="Regular",Font=(FontFaceAsset="/Script/Engine.FontFace\'%s\'")))))' % face.get_path_name())
font.set_editor_property("composite_font", cf)
EAL.save_loaded_asset(font)
print("MENU assets", tex.get_path_name(), face.get_path_name(), font.get_path_name())
