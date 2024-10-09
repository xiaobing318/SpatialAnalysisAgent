

import json
#***************************************************************************
##Import package
import os
import re
import sys
from io import StringIO
import requests
import networkx as nx
from PyQt5.QtWidgets import QMessageBox
from pyvis.network import Network
from openai import OpenAI
from IPython.display import display, HTML, Code
from IPython.display import clear_output
from langchain_openai import ChatOpenAI
import asyncio
import nest_asyncio
import processing
from IPython.display import clear_output
from IPython import get_ipython
from qgis.utils import iface
# Enable autoreload
ipython = get_ipython()
if ipython:
    ipython.run_line_magic('load_ext', 'autoreload')
    ipython.run_line_magic('autoreload', '2')


# Get the directory of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))
SpatialAnalysisAgent_dir = os.path.join(current_script_dir, 'SpatialAnalysisAgent')
# print(LLMQGIS_dir)
if current_script_dir not in sys.path:
    sys.path.append(SpatialAnalysisAgent_dir)


import SpatialAnalysisAgent_Constants as constants
import SpatialAnalysisAgent_helper as helper
import SpatialAnalysisAgent_ToolsDocumentation as ToolsDocumentation

from SpatialAnalysisAgent_kernel import Solution
import SpatialAnalysisAgent_Codebase as codebase

from Tools_Documentations import documentation


OpenAI_key = helper.load_OpenAI_key()

#**********************************************************************************************************************
# isReview = True

def main(task, data_path):

    data_path = data_path.split(';')  # Assuming data locations are joined by a semicolon
    task = task

if __name__ == "__main__":
    # task_name = sys.argv[1]
    task = sys.argv[1]
    data_path = sys.argv[2]
    # OpenAI_key = sys.argv[3]
    model_name = sys.argv[3]
    workspace_directory = sys.argv[4]
    main(task, data_path,workspace_directory, model_name)


task_name = helper.generate_task_name_with_gpt(task)
DATA_LOCATIONS = data_path.split('\n')
# Define a global check_running function that references the flag
def check_running():
    global _is_running
    return _is_running

_is_running = True

if not check_running():
    print("AI: Script interrupted")
    sys.exit()

# save_dir = os.path.join(os.getcwd(), task_name)
# os.makedirs(save_dir, exist_ok=True)
#
# script_directory = os.path.dirname(os.path.abspath(__file__))
# save_dir = os.path.join(script_directory, "Solution", task_name)

# model_name = r'gpt-4o'
OpenAI_key = helper.load_OpenAI_key()
model = ChatOpenAI(api_key=OpenAI_key, model=model_name, temperature=1)



# ##*************************************** OPERATION IDENTIFICATION ************************************************
OperationIdentification_prompt_str = helper.create_OperationIdentification_promt(task=task , data_path= DATA_LOCATIONS)
print(f"OperationIdentification PROMPT ----------{OperationIdentification_prompt_str}")

from IPython.display import clear_output


chunks = asyncio.run(helper.fetch_chunks(model, OperationIdentification_prompt_str))

clear_output(wait=True)
# clear_output(wait=False)
LLM_reply_str = helper.convert_chunks_to_str(chunks=chunks)
# print(f"Work directory: {workspace_directory}")
# print("Select the QGIS tool: \n")
print(LLM_reply_str)
task_breakdown = LLM_reply_str
##*************************************** TOOL SELECT ***************************************************************
ToolSelect_prompt_str = helper.create_ToolSelect_prompt(task=task_breakdown, data_path=DATA_LOCATIONS)
print(f"TOOL SELECT PROMPT ---------------------: {ToolSelect_prompt_str}")
ToolSelect_chunks = asyncio.run(helper.fetch_chunks(model, ToolSelect_prompt_str))

clear_output(wait=True)
# Selected_Tools_reply =helper.extract_selected_tools(chunks=ToolSelect_chunks)
Selected_Tools_reply = helper.convert_chunks_to_str(chunks=ToolSelect_chunks)
print(Selected_Tools_reply)


#************************************************************************************************************************************************************
Refined_Selected_Tools_reply = helper.extract_dictionary_from_response(response=Selected_Tools_reply)
import ast
# Convert the string to an actual dictionary
try:
    Selected_Tools_Dict = ast.literal_eval(Refined_Selected_Tools_reply)
    print(f"\nSELECTED TOOLS: {Selected_Tools_Dict}\n")
except (SyntaxError, ValueError) as e:
    print("Error parsing the dictionary:", e)


# import json
# # select_operation = json.loads(Selected_Tools_reply)
# # print(select_operation)
# selection_operation1 = helper.parse_llm_reply(Selected_Tools_reply)
# selection_operation = json.loads(selection_operation1)
# Selected_Tools_Dict = ast.literal_eval(Selected_Tools_reply)

selected_tools = Selected_Tools_Dict['Selected tool']


# print(f"\nSELECTED TOOLS: {selected_tools}\n")

# # Check if the selected_tools is a string or a list
if isinstance(selected_tools, str):
    selected_tools = [selected_tools]
print(selected_tools)
Tools_Documentation_dir = os.path.join(current_script_dir, 'SpatialAnalysisAgent', 'Tools_Documentation')
# Iterate over each selected tool
selected_tool_IDs_list = []
SelectedTools = {}
all_documentation =[]
for selected_tool in selected_tools:

    if selected_tool in codebase.algorithm_names:
        selected_tool_ID = codebase.algorithms_dict[selected_tool]['ID']

    elif selected_tool in constants.tool_names_lists:
        selected_tool_ID = constants.CustomTools_dict[selected_tool]['ID']
        # print(f"Selected a tool from the customized folder")
    else:
        selected_tool_ID = selected_tool

    # Add the selected tool and its ID to the SelectedTools dictionary
    SelectedTools[selected_tool] = selected_tool_ID

    selected_tool_IDs_list.append(selected_tool_ID)
    # print(f"SELECTED TOOLS ID: {selected_tool_ID}")
    selected_tool_file_ID = re.sub(r'[ :?\/]', '_', selected_tool_ID)
    # print(F"TOOL_ID: {selected_tool_ID}")
    # print(f"Selected tool filename: {selected_tool_file_ID}")

    selected_tool_file_path = None
    # Walk through all subdirectories and files in the given directory
    for root, dirs, files in os.walk(Tools_Documentation_dir):
        for file in files:
            if file == f"{selected_tool_file_ID}.toml":
                selected_tool_file_path = os.path.join(root, file)
                break
        if selected_tool_file_path:
            break
    if not selected_tool_file_path:
        print(f"File {selected_tool_file_ID}.toml not found.")
        continue

    if selected_tool_file_path:
        # Print the tool information
        print(f"TOOL_ID: {selected_tool_ID}")
        print(f"Selected tool filename: {selected_tool_file_ID}")

    # Define the path to the file (you'll need to adjust this path as needed)
    # selected_file_path = os.path.join(Tools_Documentation_dir, f"{selected_tool_file_ID}.toml")

    # Step 1: Check if the file is free from errors
    if ToolsDocumentation.check_toml_file_for_errors(selected_tool_file_path):
        # If no errors, get the documentation
        print(f"File {selected_tool_file_ID} is free from errors.")
        documentation_str = ToolsDocumentation.tool_documentation_collection(tool_ID=selected_tool_file_ID)
    else:
        # Step 2: If there are errors, fix the file and then get the documentation
        print(f"File {selected_tool_file_ID} has errors. Attempting to fix...")
        ToolsDocumentation.fix_toml_file(selected_tool_file_path)

        # After fixing, try to retrieve the documentation
        print(f"Retrieving documentation after fixing {selected_tool_file_ID}.")
        documentation_str = ToolsDocumentation.tool_documentation_collection(tool_ID=selected_tool_file_ID)

    # Append the retrieved documentation to the list
    all_documentation.append(documentation_str)

# Print the list of all selected tool IDs after the loop is complete
print(f"List of selected tool IDs: {selected_tool_IDs_list}")
# Step 3: Join all the collected documentation into a single string
combined_documentation_str = '\n'.join(all_documentation)


current_script_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_script_dir)
SpatialAnalysisAgent_dir = os.path.join(current_script_dir, 'SpatialAnalysisAgent')
DataEye_path = os.path.join(SpatialAnalysisAgent_dir,'SpatialAnalysisAgent_DataEye')
# sys.path.append(os.path.append('SpatialAnalysisAgent_DataEye'))
if DataEye_path not in sys.path:
    sys.path.append(DataEye_path)


import data_eye



current_script_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_script_dir)
SpatialAnalysisAgent_dir = os.path.join(current_script_dir, 'SpatialAnalysisAgent')
DataEye_path = os.path.join(SpatialAnalysisAgent_dir)
# sys.path.append(os.path.append('SpatialAnalysisAgent_DataEye'))
if DataEye_path not in sys.path:
    sys.path.append(DataEye_path)
#
attributes_json, DATA_LOCATIONS = data_eye.add_data_overview_to_data_location(task=task, data_location_list=DATA_LOCATIONS, model=r'gpt-4o-2024-08-06')
print("DATA_LOCATIONS with data overviews:")
print(DATA_LOCATIONS)


# #%% --------------------------------------------------------SOLUTION GRAPH -----------------------------------------------
script_directory = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.join(script_directory, "graphs")
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
solution = Solution(
    task=task,
    task_explanation= LLM_reply_str,
    task_name = task_name,
    save_dir=save_dir,
    data_path=DATA_LOCATIONS,
    model=model_name,
)

task_explanation = LLM_reply_str
response_for_graph = solution.get_LLM_response_for_graph()
solution.graph_response = response_for_graph
solution.save_solution()

clear_output(wait=True)
exec(solution.code_for_graph)
solution_graph = solution.load_graph_file()

# # Show the graph
G = nx.read_graphml(solution.graph_file)
nt = helper.show_graph(G)
graphs_directory = save_dir
html_graph_path = os.path.join(graphs_directory ,f"{task_name}_solution_graph.html")
counter = 1
while os.path.exists(html_graph_path):
    html_graph_path = os.path.join(graphs_directory, f"{task_name}_solution_graph_{counter}.html")
    counter += 1
# nt.show_graph(html_graph_path)
nt.save_graph(html_graph_path)
print(f"GRAPH_SAVED:{html_graph_path}")

#%%***************************************** #Get code for operation without Solution graph ************************
# Create and print the operation prompt string for each selected tool
operation_prompt_str = helper.create_operation_prompt(task = task, data_path =DATA_LOCATIONS, workspace_directory =workspace_directory, selected_tools =SelectedTools, documentation_str=combined_documentation_str)
print(f"OPERATION PROMPT: {operation_prompt_str}")

Operation_prompt_str_chunks = asyncio.run(helper.fetch_chunks(model, operation_prompt_str))

clear_output(wait=True)
# clear_output(wait=False)
LLM_reply_str = helper.convert_chunks_to_code_str(chunks=Operation_prompt_str_chunks)
# print(LLM_reply_str)
#EXTRACTING CODE

print("\n ---------------------------EXTRACTED CODE:--------------------------------------\n")
print("```python")
extracted_code = helper.extract_code_from_str(LLM_reply_str, task)
print("```")

# #%% --------------------------------------------- CODE REVIEW ------------------------------------------------------
code_review_prompt_str = helper.code_review_prompt(extracted_code = extracted_code, data_path = DATA_LOCATIONS, selected_tool_dict= SelectedTools, workspace_directory = workspace_directory, documentation_str=combined_documentation_str)
# print(code_review_prompt_str)
code_review_prompt_str_chunks = asyncio.run(helper.fetch_chunks(model, code_review_prompt_str ))
clear_output(wait=True)
review_str_LLM_reply_str = helper.convert_chunks_to_code_str(chunks=code_review_prompt_str_chunks)
#EXTRACTING REVIEW_CODE
print("\n\n")
print(f"---------------------------FINAL REVIEWED CODE----------------------------------- \n\n")
print("```python")
reviewed_code = helper.extract_code_from_str(review_str_LLM_reply_str, task_explanation)
print("```")

# print(operation_prompt_str)

# print(review_str_LLM_reply_str)



# operation_prompt_str = helper.create_operation_prompt(task, data_path, selected_tool, selected_tool_ID,
#                                                           documentation_str)
# chunks = asyncio.run(fetch_chunks(model, operation_prompt_str))
#



#
# reviewed_code = solution.ask_LLM_to_review_operation_code_generated(extracted_code=operation_code, selected_tool_ID=selected_tool_ID, documentation_str=documentation_str)
# #
#

#%% EXECUTION OF THE CODE
code, output = helper.execute_complete_program(code=reviewed_code, try_cnt=3, task=task, model_name=model_name, documentation_str=combined_documentation_str, data_path= data_path, workspace_directory=workspace_directory, review=True)
# display(Code(code, language='python'))


# Display the captured output (like the file path) in your GUI or terminal
for line in output.splitlines():
    print(f"Captured Output: {line}")


print("-----Script completed-----")
#
#
# # # Display the captured output (like the file path) in your GUI or terminal
# # print(f"Captured Output: {output}")
# #
# # print("-----Script completed-----")













#
# #%%
# import sys
# import os
#
#
# # current_script_dir = os.path.dirname(os.path.abspath(__file__))
#
#
#
# current_script_dir = os.path.dirname(os.path.abspath(__file__))
# # parent_dir = os.path.dirname(current_script_dir)
# SpatialAnalysisAgent_dir = os.path.join(current_script_dir, 'SpatialAnalysisAgent')
# DataEye_path = os.path.join(SpatialAnalysisAgent_dir,'SpatialAnalysisAgent_DataEye')
# # sys.path.append(os.path.append('SpatialAnalysisAgent_DataEye'))
# if DataEye_path not in sys.path:
#     sys.path.append(DataEye_path)
#
# print(DataEye_path)
#
# import data_eye
# # #%%%
# task_name ='School walkability'
# TASK = r'''You need to compute the walkability scores for all schools in the Colubmia city. The steps are:
# 1) extract the road network near a school within 1 km buffer zone.
# 2) extract the sidewalks within 20 meters to the extracted road network in the step 1.
# 3) the school walkability scores is the ratio of the extracted sidewalk length to the extracted road network length.
# 4) Please draw a map for each school, using the school name and the walkability score as the map title, while showing the extracted sidewalks on a OpenStreetMap basemap.
# '''
#
# DATA_LOCATIONS = [
# r"D:/Case_Studies/Data/PovertyData/PovertyData.csv"
#
# ]
# # "https://github.com/gladcolor/spatial_data/raw/refs/heads/master/Everest_DOM.tif"
# # r"D:/Case_Studies/Data/PovertyData/PovertyData.csv"
# # "https://raw.githubusercontent.com/gladcolor/spatial_data/master/Demography/ACS2020_5year_county.csv."
# # "D:\Case_Studies\Data\PA_School.gpkg"
# # "D:\Case_Studies\Data\HW_Sites_EPSG4326.zip"
#
# model = r'gpt-4o'
#
# # Get data overview (column names, data types, and map projection)
#
# data_locations_prompt = data_eye.get_prompt_to_pick_up_data_locations(task = TASK, data_locations = DATA_LOCATIONS)
# # Reply = data_eye.add_data_overview_to_data_location(task = TASK, data_location_list=DATA_LOCATIONS)
# attributes_json, DATA_LOCATIONS = data_eye.add_data_overview_to_data_location(task=TASK, data_location_list=DATA_LOCATIONS, model=model)
# # print(DATA_LOCATIONS)
# print(data_locations_prompt)
# print(attributes_json)











