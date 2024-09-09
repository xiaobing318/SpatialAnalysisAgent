
#***************************************************************************
##Import package
import os
import sys

from io import StringIO

import requests
import networkx as nx
from PyQt5.QtWidgets import QMessageBox
#import pandas as pd
#import geopandas as gpd
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

from SpatialAnalysisAgent_kernel import Solution
import SpatialAnalysisAgent_Codebase as codebase
from Tools_Documentations import documentation
# from LLMQGIS_Codebase import algorithm_names, algorithms_dict



# OpenAI_key = helper.load_OpenAI_key()

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
    main(task, data_path, model_name)


task_name = helper.generate_task_name_with_gpt(task)

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

##*************************************** OPERATION IDENTIFICATION *******************************************************
OperationIdentification_prompt_str = helper.create_OperationIdentification_promt(task=task)
# print(OperationIdentification_prompt_str)

# print(algorithm_names)
from IPython.display import clear_output


# async def fetch_chunks(model, prompt_str):
#     chunks = []
#     async for chunk in model.astream(prompt_str):
#         chunks.append(chunk)
#         # print(chunk.content, end="", flush=True)
#     return chunks
# nest_asyncio.apply()

chunks = asyncio.run(helper.fetch_chunks(model, OperationIdentification_prompt_str))

clear_output(wait=True)
# clear_output(wait=False)
LLM_reply_str = helper.convert_chunks_to_str(chunks=chunks)

print("Select the QGIS tool: \n")
print(LLM_reply_str)
#************************************************************************************************************************************************************
import ast
select_operation = ast.literal_eval(LLM_reply_str)

selected_tools = select_operation['Selected tool']


# Check if the selected_tools is a string or a list
if isinstance(selected_tools, str):
    selected_tools = [selected_tools]


# Iterate over each selected tool
for selected_tool in selected_tools:
    # if not check_running():
    #     print("Task was interrupted")
    #     break
    if selected_tool in codebase.algorithm_names:
        selected_tool_ID = codebase.algorithms_dict[selected_tool]['ID']
    elif selected_tool in constants.other_QGIS_operations:
        selected_tool_ID = constants.other_QGIS_operations_dict[selected_tool]['ID']
    else:
        selected_tool_ID = None

    documentation_list = documentation.get(f"{selected_tool_ID}", [])
    documentation_str = '\n'.join([f"{idx + 1}. {line}" for idx, line in enumerate(documentation_list)])

    # Create and print the operation prompt string for each selected tool
    operation_prompt_str = helper.create_operation_prompt(task, data_path, selected_tool, selected_tool_ID,
                                                          documentation_str)
    # print(operation_prompt_str)


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
    data_path=data_path,
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
nt.show(html_graph_path)
print(f"GRAPH_SAVED:{html_graph_path}")


# #%%***************************************** #Get code for operation without Solution graph ************************
# from IPython.display import clear_output
# async def fetch_LLM_str(model, operation_prompt_str):
#     chunks = []
#
#     async for chunk in model.astream(operation_prompt_str):
#         # if not check_running():
#         #     print("Task was interrupted")
#         #     break
#         chunks.append(chunk)
#         print(chunk.content, end="", flush=True)
#     return chunks
# nest_asyncio.apply()
Operation_prompt_str_chunks = asyncio.run(helper.fetch_chunks(model, operation_prompt_str))

clear_output(wait=True)
# clear_output(wait=False)
LLM_reply_str = helper.convert_chunks_to_str(chunks=Operation_prompt_str_chunks)
# print(LLM_reply_str)
#EXTRACTING CODE
print("```python")
print("\n ---------------------------EXTRACTED_CODE:--------------------------------------\n")
extracted_code = helper.extract_code_from_str(LLM_reply_str, task)
print("```")

# print("\n\n")
# print(f"Code extracted---------------------------: \n\n{extracted_code}")
# display(Code(code, language='python'))

#%% --------------------------------------------- CODE REVIEW ------------------------------------------------------
code_review_prompt_str = helper.code_review_prompt(extracted_code, data_path, selected_tool_ID, documentation_str)
# print(code_review_prompt_str)
code_review_prompt_str_chunks = asyncio.run(helper.fetch_chunks(model, code_review_prompt_str ))
clear_output(wait=True)
review_str_LLM_reply_str = helper.convert_chunks_to_str(chunks=code_review_prompt_str_chunks)
#EXTRACTING REVIEW_CODE
print("\n\n")
print(f"------------REVIEWED_EXTRACTED_CODE-----------------------------------: \n\n")
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
code, output = helper.execute_complete_program(code=reviewed_code, try_cnt=5, task=task, model_name=model_name, documentation_str=documentation_str, data_path= data_path, review=True)
# display(Code(code, language='python'))


# Display the captured output (like the file path) in your GUI or terminal
print(f"Captured Output: {output}")

print("-----Script completed-----")


# # Display the captured output (like the file path) in your GUI or terminal
# print(f"Captured Output: {output}")
#
# print("-----Script completed-----")




























# isReview = False
# task_explanation = LLM_reply_str
# operation_code = helper.get_code_for_operation(task_description = task_explanation, data_path=data_path,
#                                                selected_tool= selected_tool, selected_tool_ID =selected_tool_ID, documentation_str = documentation_str, review= isReview)
#
# # operation_code = solution.get_code_for_operation(task_description = task_explanation, selected_tool= selected_tool, selected_tool_ID =selected_tool_ID, documentation_str = documentation_str)
#
#
# # display(Code(operation_code, language='python'))
#
# # reviewed_code = solution.ask_LLM_to_review_operation_code_generated(extracted_code=operation_code, selected_tool_ID=selected_tool_ID, documentation_str=documentation_str)
#
#
# # # from IPython.display import clear_output
# # # async def fetch_download_str(model, operation_prompt_str):
# # #     chunks = []
# # #
# # #     async for chunk in model.astream(operation_prompt_str):
# # #         # if not check_running():
# # #         #     print("Task was interrupted")
# # #         #     break
# # #         chunks.append(chunk)
# # #         print(chunk.content, end="", flush=True)
# # #     return chunks
# # # nest_asyncio.apply()
# # # chunks = asyncio.run(fetch_chunks(model, operation_prompt_str))
# # #
# # # clear_output(wait=True)
# # # # clear_output(wait=False)
# # # LLM_reply_str = helper.convert_chunks_to_str(chunks=chunks)
# # # print(LLM_reply_str)
# #
# #
# #
# #************************************************************************************************************************
# #Executing code
# # code = helper.extract_code_from_str(LLM_reply_str, task)
# # display(Code(code, language='python'))
# #
# #
# # code = helper.execute_complete_program(code=code, try_cnt=5, task=task, model_name=model_name, documentation_str=documentation_str)
# # display(Code(code, language='python'))
# #
# # # First, run the code and capture both the compiled code and the output buffer
# # # code, output_capture = helper.execute_complete_program(code=code, try_cnt=5, task=task, model_name=model_name, documentation_str=documentation_str)
# # # display(Code(code, language='python'))
# # # Capture the output of the code execution
# # output = helper.capture_print_output(code=code)
# # # output = helper.capture_print_output(code=code)
# # # # # display(Code(code, language='python'))
# # # #
# # # # # Display the captured output (like the file path) in your GUI or terminal
# # print(f"Captured Output: {output}")
# # # # print(output)
# #
#
#
# code, output = helper.execute_complete_program(code=operation_code, try_cnt=5, task=task, model_name=model_name, documentation_str=documentation_str)
# # display(Code(code, language='python'))
#
# # Display the captured output (like the file path) in your GUI or terminal
# print(f"Captured Output: {output}")
#
# print("-----Script completed-----")
#
#
# # # Show the compiled code in a dialog window
# # msg_box = QMessageBox()
# # msg_box.setText(f"Compiled Code:\n{code}")
# # msg_box.exec_()
#
