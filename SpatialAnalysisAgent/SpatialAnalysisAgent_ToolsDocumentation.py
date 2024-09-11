import os
import tomllib


current_script_dir = os.path.dirname(os.path.abspath(__file__))
Tools_Documentation_dir = os.path.join(current_script_dir, 'SpatialAnalysisAgent', 'Tools_Documentation')

def tool_documentation_collection(tool_ID, tool_dir=Tools_Documentation_dir):
    handbook_file = os.path.join(tool_dir, f'{tool_ID}.toml')
    with open(handbook_file, "rb") as f:
        handbook = tomllib.load(f)
    handbook_total_str = handbook['handbook']
    return handbook_total_str