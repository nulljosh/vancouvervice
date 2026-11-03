"""Writes a .dsl file into a Blueprint graph through the Unreal MCP (editor open), expanding `; @include <file>` lines
with that file from this folder. Usage: python3 unreal/write_dsl.py <graph refPath> <file.dsl>
e.g. python3 unreal/write_dsl.py "/Game/VancouverVice/HUD/BP_VVHud.BP_VVHud:EventGraph" unreal/hud.dsl"""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
code = re.sub(r"^\s*; @include (\S+)\s*$", lambda m: open(os.path.join(HERE, m.group(1))).read(), open(sys.argv[2]).read(), flags=re.M)
args = {"name": "call_tool", "arguments": {"toolset_name": "editor_toolset.toolsets.blueprint.BlueprintTools", "tool_name": "write_graph_dsl",
        "arguments": {"graph": {"refPath": sys.argv[1]}, "code": code}}}
print(subprocess.run([sys.executable, os.path.join(HERE, "mcp.py"), "tools/call", json.dumps(args)], capture_output=True, text=True).stdout[:4000])
