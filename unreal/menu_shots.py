"""Startup-screen art from our own world: four golden-hour shots taken in the editor (Joshua at the Apple Store, the
getaway car with the cop, the skyline to the North Shore mountains, the waterfront), saved as PNGs for
tools/menu_art.py to grade and pack into T_MenuArt. The sun is dropped low for the shots and put back after.
Run: QA_TIMEOUT=600 python3 unreal/qa.py "$(cat unreal/menu_shots.py)". Output: Saved/Screenshots/MacEditor/menu_*.png"""
import unreal

EAS = unreal.EditorActorSubsystem(); acts = EAS.get_all_level_actors()
sun = next(a for a in acts if isinstance(a, unreal.DirectionalLight))
sun_rot = sun.get_actor_rotation()
sun.set_actor_rotation(unreal.Rotator(roll=0, pitch=-9, yaw=-60), False)  # low sun from the west-south-west
car = next(a for a in acts if a.get_class().get_name() == "BP_VehicleAdvSportsCar_C")
cop = next(a for a in acts if a.get_class().get_name() == "BP_CopCar_C")
cop_loc = cop.get_actor_location()
CL = car.get_actor_location()

hero = EAS.spawn_actor_from_class(unreal.SkeletalMeshActor, unreal.Vector(-487.5, 2936.1, -6838))
mc = hero.skeletal_mesh_component
mc.set_skinned_asset_and_update(unreal.load_asset("/Game/Characters/Joshua2/JoshuaHero_m/SkeletalMeshes/JoshuaHero_m"))
mc.set_animation_mode(unreal.AnimationMode.ANIMATION_SINGLE_NODE)
mc.override_animation_data(unreal.load_asset("/Game/Characters/Joshua2/JoshuaHero_m/SkeletalMeshes/JoshuaHero_mIdle"), True, True, 0.4, 1.0)
hero.set_actor_rotation(unreal.Rotator(0, 0, 200), False)
cop.set_actor_location(CL + unreal.Vector(-900, 250, 0), False, True)

cam = EAS.spawn_actor_from_class(unreal.CineCameraActor, unreal.Vector(0, 0, 0))
cam.get_cine_camera_component().set_editor_property("current_focal_length", 28.0)
SHOTS = [
    ("menu_hero", unreal.Vector(-487.5 - 330, 2936.1 - 120, -6838 + 150), unreal.Vector(-487.5, 2936.1, -6838 + 120)),
    ("menu_car", CL + unreal.Vector(520, -380, 70), CL + unreal.Vector(-300, 80, 60)),
    ("menu_skyline", unreal.Vector(-30000, 2000, -6840 + 9000), unreal.Vector(30000, 6000, -6840 + 2500)),
    ("menu_water", unreal.Vector(4000, -6000, -6840 + 2600), unreal.Vector(30000, -40000, -6840)),
]
for name, at, look in SHOTS:
    cam.set_actor_location(at, False, True)
    cam.set_actor_rotation(unreal.MathLibrary.find_look_at_rotation(at, look), False)
    unreal.AutomationLibrary.take_high_res_screenshot(1920, 1080, name + ".png", cam)
    print("shot", name)

def restore():
    sun.set_actor_rotation(sun_rot, False)
    cop.set_actor_location(cop_loc, False, True)
    EAS.destroy_actor(hero); EAS.destroy_actor(cam)
MENU_RESTORE = restore  # call after the screenshots land (they are taken on later frames)
