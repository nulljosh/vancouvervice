#!/bin/sh
# Rebuild Joshua end to end: fresh editor, MetaHuman body build, export body and face, cut polo, jeans and hair in
# Blender, reimport all three, apply the scene, take the photo.  sh unreal/avatar.sh out.jpg
# The body build peaks near 15 GB, so it always starts from a freshly launched editor.
set -e
HERE=$(cd "$(dirname "$0")" && pwd); OUT=${1:-/tmp/vv_avatar.jpg}; B=/Applications/Blender.app/Contents/MacOS/Blender
q() { QA_TIMEOUT=${2:-600} python3 "$HERE/qa.py" "$1"; }
echo "1/7 restart editor"
q 'unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True); print("saved")' 120 || true
pkill -x UnrealEditor || true; sleep 15; pkill -9 -x UnrealEditor 2>/dev/null || true; sleep 3
sh "$HERE/open.sh"
end=$(( $(date +%s) + 1500 )); until curl -s -o /dev/null -m 2 http://127.0.0.1:18000/mcp; do [ $(date +%s) -gt $end ] && { echo "editor never came up"; exit 1; }; sleep 10; done
sleep 30
echo "2/7 body build"; q "$(cat "$HERE/body_build.py")" 900
echo "3/7 export body and face"
q 'for src, dst in (("/Game/Unpacked/Joshua/Joshua/Body/SKM_Joshua_BodyMesh", "joshua_body_v2.fbx"), ("/Game/Unpacked/Joshua/Joshua/Face/SKM_Joshua_FaceMesh", "joshua_face_v2.fbx")):
    t=unreal.AssetExportTask(); t.object=unreal.load_asset(src); t.filename="'"$HERE"'/assets/"+dst; t.automated=True; t.replace_identical=True; t.prompt=False
    t.exporter=unreal.SkeletalMeshExporterFBX(); o=unreal.FbxExportOption(); o.set_editor_property("export_morph_targets", False); t.options=o
    print(dst, unreal.Exporter.run_asset_export_task(t))' 300
echo "4/7 Blender cuts"
for s in pants.py polo.py hair_shell.py; do $B -b --python "$HERE/$s" 2>&1 | grep -E "exported|Error" | head -2; done
echo "5/7 reimport"
q "$(cat "$HERE/reimport_clothes.py")" 400; q "$(cat "$HERE/hairshell_install.py")" 400
python3 "$HERE/mcp.py" tools/call "$(cat /tmp/vv_dsl.json)" >/dev/null
echo "6/7 scene"; q "$(cat "$HERE/scene_setup.py")" 300
swift "$HERE/dismiss.swift" >/dev/null 2>&1 || true
echo "7/7 photo"; sh "$HERE/photo.sh" "$OUT"
