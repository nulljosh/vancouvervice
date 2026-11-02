# Imports a rigged hero GLB (metre scale, see tools/hero_unscale in the scratch notes), builds an IK rig, retargets
# the third-person movement set (ABP_Unarmed) from Manny onto it. Run inside the editor: python3 unreal/qa.py "$(cat unreal/import_hero.py)"
SRC, DST, NAME = "/Volumes/LaCie/Unreal/dl/hero/JoshuaHero_m.glb", "/Game/Characters/Joshua2", "JoshuaHero_m"
AT = unreal.AssetToolsHelpers.get_asset_tools(); R = "/Game/Characters/Retarget"
unreal.EditorAssetLibrary.delete_directory(DST)
t = unreal.AssetImportTask(); t.filename = SRC; t.destination_path = DST; t.automated = True; t.save = True; t.replace_existing = True
AT.import_asset_tasks([t])
mp = [p for p in unreal.EditorAssetLibrary.list_assets(DST, True, False) if unreal.EditorAssetLibrary.find_asset_data(p).asset_class_path.asset_name == "SkeletalMesh"][0]
josh = unreal.load_asset(mp.split(".")[0]); print("mesh", mp, josh.get_bounds().box_extent)
for n in ["IK_Joshua2", "RTG_Manny_Joshua2"]: unreal.EditorAssetLibrary.delete_asset(R + "/" + n)
rig = AT.create_asset("IK_Joshua2", R, unreal.IKRigDefinition, unreal.IKRigDefinitionFactory())
c = unreal.IKRigController.get_controller(rig); c.set_skeletal_mesh(josh); print("auto", c.apply_auto_generated_retarget_definition())
manny = unreal.load_asset("/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple")
rtg = AT.create_asset("RTG_Manny_Joshua2", R, unreal.IKRetargeter, unreal.IKRetargetFactory()); rc = unreal.IKRetargeterController.get_controller(rtg)
S, T = unreal.RetargetSourceOrTarget.SOURCE, unreal.RetargetSourceOrTarget.TARGET
rc.set_ik_rig(S, unreal.load_asset(R + "/IK_Manny")); rc.set_ik_rig(T, rig); rc.set_preview_mesh(S, manny); rc.set_preview_mesh(T, josh)
rc.add_default_ops(); rc.assign_ik_rig_to_all_ops(S, unreal.load_asset(R + "/IK_Manny")); rc.assign_ik_rig_to_all_ops(T, rig)
rc.auto_map_chains(unreal.AutoMapChainType.FUZZY, True); rc.auto_align_all_bones(T)
unreal.EditorAssetLibrary.save_loaded_asset(rtg); unreal.EditorAssetLibrary.save_loaded_asset(rig)
abp = unreal.EditorAssetLibrary.find_asset_data("/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed")
out = unreal.IKRetargetBatchOperation.duplicate_and_retarget([abp], manny, josh, rtg, "", "", "", "_J2", DST + "/Anims", False, True, True)
print("retargeted", len(out))
