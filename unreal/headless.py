"""Applies source changes to the project with no editor window: runs menu_setup.py (fonts, logo, art), writes every
DSL graph, compiles and saves. Run by unreal/headless.sh inside UnrealEditor-Cmd -run=pythonscript.
VV_FIND="a,b" only prints matching node type ids (against the BP_Missions graph) and changes nothing."""
import os, re, sys, traceback, unreal
sys.stdout = open("/Volumes/LaCie/Unreal/scratch/headless.out", "w", buffering=1)  # print() never reaches the commandlet log
from editor_toolset.toolsets.blueprint import BlueprintTools

HERE = os.path.dirname(os.path.abspath(__file__))
GRAPHS = {
    "/Game/VancouverVice/BP_Missions.BP_Missions:EventGraph": "missions_graph.dsl",
    "/Game/VancouverVice/HUD/BP_VVHud.BP_VVHud:EventGraph": "hud.dsl",
    "/Game/VancouverVice/BP_TrafficCar.BP_TrafficCar:EventGraph": "traffic.dsl",
}

def graph(ref):
    unreal.load_asset(ref.split(":")[0])  # the Blueprint has to be loaded before its graph resolves
    g = unreal.load_object(None, ref)
    assert g is not None, "no graph " + ref
    return g

if os.environ.get("VV_FIND"):
    g = graph(next(iter(GRAPHS)))
    for term in os.environ["VV_FIND"].split(","):
        print("HEADLESS find", term, BlueprintTools.find_node_types(g, term)[:12])
else:
    try:
        exec(open(os.path.join(HERE, "menu_setup.py")).read())
    except Exception:
        print("HEADLESS menu_setup failed\n" + traceback.format_exc())
    for ref, f in GRAPHS.items():
        try:
            code = re.sub(r"^\s*; @include (\S+)\s*$", lambda m: open(os.path.join(HERE, m.group(1))).read(),
                          open(os.path.join(HERE, f)).read(), flags=re.M)
            BlueprintTools.write_graph_dsl(graph(ref), code)  # returns None through the tool wrapper
            bp = unreal.load_asset(ref.split(":")[0])
            BlueprintTools.compile_blueprint(bp)
            unreal.EditorAssetLibrary.save_loaded_asset(bp)
            print("HEADLESS wrote", f)
        except Exception:
            print("HEADLESS failed", f, "\n" + traceback.format_exc())
print("HEADLESS done")
if os.environ.get("VV_GUI"):  # one-time font import needs Slate: run hidden in the full editor, then quit
    unreal.SystemLibrary.quit_editor()
