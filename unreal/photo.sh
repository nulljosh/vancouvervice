#!/bin/sh
# Front photo of the player in Play: starts Play, waits for tiles, views through the PhotoCam actor in front of the
# Apple Store spawn, screenshots the editor window, stops Play.  sh unreal/photo.sh out.jpg
HERE=$(cd "$(dirname "$0")" && pwd); OUT=${1:-/tmp/vv_photo.jpg}
open -a /Volumes/LaCie/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app
python3 -c "import sys; sys.path.insert(0,'$HERE'); import qa; qa.mcp('EditorToolset.EditorAppToolset','StartPIE',{'options':{'bSimulate':False,'playMode':'PlayMode_InViewPort','warmupSeconds':5}})"
sleep 40
QA_TIMEOUT=60 python3 "$HERE/qa.py" 'w=unreal.UnrealEditorSubsystem().get_game_world()
p=unreal.GameplayStatics.get_player_pawn(w,0); pc=unreal.GameplayStatics.get_player_controller(w,0)
unreal.SystemLibrary.execute_console_command(w, "r.HairStrands.BoundsMode 2")
cam=[a for a in unreal.GameplayStatics.get_all_actors_of_class(w, unreal.CameraActor) if a.get_actor_label()=="PhotoCam"][0]
p.set_actor_rotation(unreal.Rotator(roll=0,pitch=0,yaw=134.7), False)
g=p.get_components_by_class(unreal.GroomComponent)
print("hair", g[0].get_attach_parent().get_name() if g else None, g[0].get_world_location() if g else None, "visible", g[0].is_visible() if g else None)
pc.set_view_target_with_blend(cam, 0.0)'
open -a /Volumes/LaCie/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app; sleep 8
screencapture -x -o -l "$(swift "$HERE/wid.swift" | awk '/Unreal Editor/{print $1}')" /tmp/vv_photo_raw.png
magick /tmp/vv_photo_raw.png -crop 1600x900+130+140 -resize 1200x "$OUT"
python3 -c "import sys; sys.path.insert(0,'$HERE'); import qa; qa.mcp('EditorToolset.EditorAppToolset','StopPIE',{})"
echo "photo: $OUT"
