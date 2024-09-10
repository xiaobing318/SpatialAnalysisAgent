import os
import sys
import configparser

from openai import OpenAI

# Get the directory of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the directory to sys.path
if current_script_dir not in sys.path:
    sys.path.append(current_script_dir)

import SpatialAnalysisAgent_Codebase as codebase
import SpatialAnalysisAgent_helper as helper
from Tools_Documentations import documentation
from SpatialAnalysisAgent_Codebase import algorithms_dict, algorithm_names

def load_config():
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_script_dir, 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_path)
    return config

# Use the loaded configuration
config = load_config()

OpenAI_key = config.get('API_Key', 'OpenAI_key')
client = OpenAI(api_key=OpenAI_key)


# carefully change these prompt parts!
#*********************************************************************************************************************************************************************
#---------------------------------Identify Operation type------------------------------------------------------------------------------------------------------------
OperationIdentification_role = r''' A professional Geo-information scientist with high proficiency in Geographic Information System (GIS) operations. You also have excellent proficiency in QGIS to perform GIS operations. You are very familiar with QGIS Processing toolbox. You have super proficency in python programming. 
You are very good at identifying QGIS tools and functions that can be used to address a problem.
'''
OperationIdentification_task_prefix = rf' Identify if  any of the available processing tool algorithms is suitable or there is need for new algorithm in order to perform this task:'

other_QGIS_operations = ['Thematic Map Creation',
                         'Land Use Land Cover (LULC)']


OperationIdentification_requirements = [
    "Think step by step and skip any step that is not applicable for the task at hand",

    # rf"When creating a thematic map, select the tool named 'Thematic Map Creation'. It is more easier. The tool 'Set style for vector layer' requires a style file, therefore it may not the suitable tool to use.",
    # f"If you need to create a thematic map, select the customized tool from {other_QGIS_operations} named 'Thematic Map Creation'",
    f"Look through the available qgis processing tool algorithms in here and specify if any of the tools can be used for the task by saying either 'Yes' or 'No', {codebase.algorithm_names}. NOTE: DO NOT return the tool ID e.g, 'qgis:heatmapkerneldensityestimation'. This is not a tool name, it is an ID.",
    f"If your answer is 'Yes', then return the exact name of the tool as given in the list. But if your answer is 'No', return any QGIS operation you think is most appropriate from the list in {other_QGIS_operations} and return the exact name as listed in the list. NOTE: the name should be assigned to 'Selected tool', while 'Yes' should be assigned to 'Customized'. DO NOT select any existing QGIS tool for thematic map creation. E.g, do not select 'categorized renderer from styles'",
    "If a task directly mention creation of thematic map. NOTE: Thematic map creation is to be used. DO NOT select any existing QGIS tool for thematic map creation, rather select from {other_QGIS_operations} . E.g, do not select 'categorized renderer from styles'",
    # "Pay close attention to the task. You may need to perform more than one operation. For example, you may need to perform aggregation first before performing select by attribute",

#     "When performing the Inverse Distance Weighted (IDW) interpolation , the suitable tool to be used is the 'IDW interpolation' ('qgis:idwinterpolation')",
#     "When generating a Triangulated Irregular Network (TIN) interpolation map, DO NOT use the 'TIN Mesh creation tool', use 'TIN interpolation' instead",
    "If you need to perform more than one operation, put the explanation in a single reply while you make a list of the tools (if more than 1) and assign them to 'Selected tool'",
    "NOTE:  Algorithm `native:rastercalculator` is not the correct ID for Raster Calculator, the correct ID is `native:rastercalc`",
    "DO NOT provide Additional details of any tool",
    f"DO NOT make fake tool. If you cannot find any suitable qgis tool, return any tool you think is most appropriate from the list in {other_QGIS_operations}" ,#select from the return 'Unknown' as for the 'Selected tool' key in the reply JSON format. DO NOT use ```json and ```",

]

OperationIdentification_reply_example_1 = ''' {'Explanation': " To select the tracts with population above 3000, the tool suitable for the operation is found in the qgis processing tools and the name is  'Extract by attribute' tool. This tool create a new vector layer that only contains matching features from an input layer",
'Selected tool': 'Extract by attribute', 'QGIS Processing toolbox' :'Yes', 'Customized': 'No'
}'''
OperationIdentification_reply_example_2 = '''{'Explanation': " To create a thematic map there is no suitable tool within the qgis processing tool. Therefore, I will be performing operation using other tool different from qgis technique. I will be using 'Thematic map creation' operation to perform this task. This operation enables rendering a map using a specified attribute",
 ",'Selected tool': 'Thematic map creation', 'QGIS Processing toolbox' :'No', 'Customized': 'Yes'
 }
'''

other_QGIS_operations_dict = {
    "Thematic Map Creation": {"ID": "Thematic_Map_Creation"},
    "Land Use Land Cover (LULC)":{"ID":"LULC"},
    "scatterplot":{"ID":"ScatterPlot"},
    "Others": {"ID": "Others"}
}


# # ***********************************************************************************************************************************************************************
# #----------------------------------- Step ----------------------------------------

#--------------- CONSTANTS FOR GRAPH GENERATION -----------------------------------------------------------------------------------------------------------
graph_role = r'''A professional Geo-information scientist with high proficiency in using QGIS and programmer good at Python. You have worked on Geographic information science more than 20 years, and know every detail and pitfall when processing spatial data and coding. You know which QGIS tool suitable for a particular spatial analysis such as Spatial Join, vector selection, Buffering, overlay analysis and thematic map rendering. You have significant experence on graph theory, application, and implementation. You will be creating a solution graph based on the specific task.
'''

graph_task_prefix = r'Generate a graph (qgis graphical modeler) only, whose nodes are the operations/steps to solve this question: '

graph_reply_exmaple = r"""
```python
import networkx as nx

G = nx.DiGraph()


# Step 1: Access Loaded Data (Operation)
G.add_node("network_data", node_type="data", description="Loaded network data")
G.add_edge("load_network_data", "network_data")

# Step 2: Set Speed Limit as Edge Weight (Operation)
G.add_node("set_speed_limit_weight", node_type="operation", description="Assign speed limits as edge weights for road segments in the network")
G.add_edge("network_data", "set_speed_limit_weight")

G.add_node("weighted_edges", node_type="data", description="Road network with speed limits as edge weights")
G.add_edge("set_speed_limit_weight", "weighted_edges")



...
```
"""

graph_requirement = ["The graph should contain the basic steps to carry out the specified task",

                     "The task will be addressed by using python codes, particularly PYQGIS in QGIS enviroment. Therefore DO NOT include steps that involve opening of QGIS Software or opening of any tool in the QGIS software",
                     "DO NOT include the steps that involve QGIS environment setup and library installation",
                     "The input can be data paths or variables, and the output are temporary layer",
                     "If the data is already loaded in the QGIS instance, you can directly access the layer by its name and proceed with the other steps.",
                     "Intending to use the QGIS processing tool to perform tasks",
                     "The output should not be saved but should be loaded as a temporary layer within the QGIS",
                     "Display Output in QGIS",
                     "Steps and data (both input and output) form a graph stored in NetworkX. Disconnected components are NOT allowed.",
                     "There are two types of nodes: a) operation node, and b) data node (both input and output data). These nodes are also input nodes for the next operation node.",
                    "There must not be disconnected components",
                     "The input of each operation is the output of the previous operations, except the those need to load data from a path or need to collect data.",
                     "DO NOT alter or change the name of any given data path or variable that are given.  E.g, '/Data/Shape1' shold not be changed to '/Data/Shape_1'"
                     "You need to carefully name the output data node, making they human readable but not to long.",
                     "The data and operation form a graph.",

                     'The first operations are data loading or collection, and the output of the last operation is the final answer to the task.',
                     'Operation nodes need to connect via output data nodes, DO NOT connect the operation node directly.',
                     "The node attributes include: 1) node_type (data or operation), 2) data_path (data node only, set to '' if not given ), and description. E.g., {‘name’: 'County boundary', 'data_type': 'data', 'data_path': 'D:\Test\county.shp',  'description': 'County boundary for the study area'}.",
                     "The connection between a node and an operation node is an edge.",
                     "Add all nodes and edges, including node attributes to a NetworkX instance, DO NOT change the attribute names.",
                     "DO NOT generate code to implement the steps.",
                     # 'Join the attribute to the vector layer via a common attribute if necessary.',
                     "Put your reply into a Python code block, NO explanation or conversation outside the code block(enclosed by ```python and ```).",
                     "Note that GraphML writer does not support class dict or list as data values.",
                     # 'You need spatial data (e.g., vector or raster) to make a map.',
                     "Do not put the GraphML writing process as a step in the graph.",
                    "Do not put the graph creation as a step in the graph",
                     "Keep the graph concise, DO NOT use too many operation nodes.",
                     'Keep the graph concise, DO NOT over-split task into too many small steps'
                     ]

# other requirements prone to errors, not used for now
"""
'DO NOT over-split task into too many small steps, especially for simple problems. For example, data loading and data transformation/preprocessing should be in one step.',
"""



#****************************************************************************************************************************************************************
## CONSTANTS FOR OPERATION GENERATION ------------------------------------------

operation_role = r'''A professional Geo-information scientist with high proficiency in GIS operations. You are also proficient in using QGIS processing tool python functions to solve a particular task. You know when to use a particular tool and when not to.
'''
operation_task_prefix = r'You need to generate qgis Python function to do: '

operation_reply_example = """
```python',
def perform_idw_interpolation(input_layer_path, z_field): #cell_size=100, power=2.0):
'''
    #Perform IDW interpolation on a given point layer.
    
    #Define the parameters for IDW interpolation
    # Run the IDW interpolation algorithm
    # Add the output raster layer to the QGIS project
perform_idw_interpolation()

```
"""
operation_requirement = [
    "Think step by step",
    # "Pay close attention to the task. You may need to perform more than one operation. For example, you may need to perform aggregation first before performing select by attribute",
    "If you need to perform more than one operation, you must perform the operations step by step",
    "DO NOT include the QGIS initialization code in the script",
    "Intending to use the QGIS processing tool to perform tasks",
    "Put your reply into a Python code block, Explanation or conversation can be Python comments at the begining of the code block(enclosed by ```python and ```).",

    "The python code is only in a function named in with the operation name e.g 'perform_idw_interpolation()'. The last line is to execute this function.",
    "If you need to use `QVariant` should be imported from `PyQt5.Qtcore` and NOT `qgis.core`",
    "NOTE: `QgsVectorJoinInfo` may not always be available or accessible in recent QGIS installations, thus use `QgsVectorLayerJoinInfo` instead",
    "Put your reply into a Python code block (enclosed by python and ), NO explanation or conversation outside the code block.",
    "If you need to use `QgsVectorLayer`, it should always be imported from qgis.core.",
    "The output should not be saved but should be loaded as a virtual layer within the QGIS",
    # "Display Output in QGIS",
    "DO NOT add validity check and DO NOT raise any exception.",
    "DO NOT raise exceptions messages.",
    "If you need to use any field from the input shapefile layer, first access the fields (example code: `fields = input_layer.fields()`), then select the appropriate field carefully from the list of fields in the layer.",
    "If you need to load a raster layer, use this format `output_layer = QgsRasterLayer(output_path, 'Slope Output')`",
    "When using Raster calculator 'native:rastercalculator' is wrong rather the correct ID for the Raster Calculator algorithm is 'native:rastercalc'.",
    "When creating a scatterplot, 'native:scatterplot' and 'qgis:scatterplot' are not supported. The correct tool is qgis:vectorlayerscatterplot",
    "When loading a CSV layer as a layer, use this: `'f'file///{csv_path}?delimeter=,''`, assuming the csv is comma-separated, but use the csv_path directly for the Input parameter in join operations.",
    "When using the processing algorithm, you do not need to include the code to load a data",
    "Do not generate a layer for tasks that only require printing the answer, like questions of how, what, why, etc. e.g., for tasks like: 'How many counties are there in PA?', 'What is the distance from A to B', etc.",
    "When creating plots such as barplot, scatterplot etc., usually their result is a html file. Always save the html file into the specified output directory and print the output layer. Do not Load the output HTML in QGIS as a standalone resource.",# Always print out the result"
     "When using the processing algorithm, make the output parameter to be the user's specified output directory . And use `QgsVectorLayer` to load the feature as a new layer: For example `output_layer = QgsVectorLayer(result['OUTPUT'], 'Layer Name', 'ogr')` for the case of a shapefile.",
    "Ensure that temporary layer is not used as the output paarameter"
    # "When using the processing algorithm, make the output parameter a temporary layer by using `'OUTPUT':'memory:name_of_the_layer'` and load the output layer using `output_layer = result['OUTPUT']`.",

   #  "If using `QgsVectorLayerJoinInfo()` to create join information, always include the JoinLayer, and apply the join to the target layer using the following: `target_layer.addJoin(join_info)`"
   #  "Create a dictionary for fast lookups of CSV attributes, then Create a new layer to store the results with joined attributes.  Add all features to the new layer. The new layer must contain all the attributes of the each features. To ensure the joined attributes are included in the new layer, you must explicitly transfer the joined attributes to the new layer's attribute table. Load the new layer"
   # "Use the setter methods to set the join information (e.g. `join_info = QgsVectorLayerJoinInfo() join_info.setJoinFieldName('GEOID')` ; `join_info.setJoinLayer(join_layer)`"
   #  "Disable the prefix in field names and keep the original field names.",
    # "When accessing a field name from a joined layers, DO NOT include the layer name to any field name when you are trying to access any field (e.g `tract_Population` should not represent the field name `Population` of tracts)."
    # "If you performed join, always export the joined layer as a new shapefile and load the new shapefile. `QgsVectorFileWriter.writeAsVectorFormatV3()` is recommended to be used to export the joined layer. It is used in this format: `QgsVectorFileWriter.writeAsVectorFormatV3(layer, output, QgsProject.instance().transformContext(), options)`."
    # f"If you performed join, you can follow this tempelate to create your code: {codebase.attribute_join}"
]

# ------------- OPERATION_CODE REVIEW------------------------------------------------------
operation_code_review_role = r''' A professional Geo-information scientist and Python developer with over 20 years of experience in Geographic Information Science (GIS). You are highly knowledgeable about spatial data processing and coding, and you specialize in code review, particularly single functions. You are meticulous and enjoy identifying potential bugs and data misunderstandings in code.
'''

operation_code_review_task_prefix = r'''Review the code of a function to determine whether it meets its associated requirements and documentation. If it does not, correct it and return the complete corrected code.'''
operation_code_review_requirement = ["Review the codes very carefully to ensure it meets its requirement.",
                                    "Compare the code with the code example of any tool being used which is contained in the tool documentation (if provided), and ensure the parameters are set correctly.",
                                    "Ensure that QGIS initialization code are not included in the script.",
                                    "Put your reply into a Python code block, Explanation or conversation can be Python comments at the begining of the code block(enclosed by ```python and ```).",
                                     "The python code is only in a function named in with the operation name e.g 'perform_idw_interpolation()'. The last line is to execute this function.",
                                     # "Ensure that any intermediary layers are loaded, but avoid loading a layer when not neccessary.",
                                     "Do not generate a layer for tasks that only require printing the answer, like questions of how, what, why, etc. e.g., for tasks like 'How many counties are there in PA?', 'What is the distance from A to B', etc.",
                                     "The data needed for the task are already loaded in the qgis environment, so there is no need to load data; just use the provided data path.",
                                     "The code should not contain any validity check.",
                                     "The code is designed to be run within the QGIS Python environment, where the relevant QGIS libraries are available. However, if any third-party libraries needed, it should always be imported.",
                                     "Ensure that the data paths in the code examples are replaced with the data paths provided by the user approprately",
                                    "When using Raster calculator, 'native:rastercalculator' is wrong rather the correct ID for the Raster Calculator algorithm is 'native:rastercalc'.",
                                    "When creating plots such as barplot, scatterplot etc., usually their result is a html file. Always save the html file into the specified output directory and print the output layer. Do not Load the output HTML in QGIS as a standalone resource.",# Always print out the result"
                                    "When creating a scatter plot, 'native:scatterplot' and 'qgis:scatterplot' are not supported. The correct tool is qgis:vectorlayerscatterplot, ensure the correct tool is used",
                                    f"When using the processing algorithm, make the output parameter to be the user's specified output directory . And use `QgsVectorLayer` to load the feature as a new layer: For example `output_layer = QgsVectorLayer(result['OUTPUT'], 'Layer Name', 'ogr')` for the case of a shapefile.",
                                     "Ensure that temporary layer is not used as the output paarameter"
                                     ]



# --------------- CONSTANTS FOR DEBUGGING PROMPT GENERATION ---------------
debug_role = r'''A professional Geo-information scientist with high proficiency in using QGIS and programmer good at Python. You have worked on Geographic information science more than 20 years, and know every detail and pitfall when processing spatial data and coding. You have significant experience on code debugging. You like to find out debugs and fix code. Moreover, you usually will consider issues from the data side, not only code implementation.
'''

debug_task_prefix = r'You need to correct the code of a program based on the given error information, then return the complete corrected code.'
debug_requirement = [

    # "Correct the code. Revise the buggy parts, but need to keep program structure, i.e., the function name, its arguments, and returns."

    "Elaborate your reasons for revision.",
    "You must return the entire corrected program in only one Python code block(enclosed by ```python and ```); DO NOT return the revised part only.",
    # "Pay close attention to the task. You may need to perform more than one operation. For example, you may need to perform aggregation first before performing select by attribute",
    "If you need to perform more than one operation, you must perform the operations step by step",
    "When using `QgsVectorLayer`, it should always be imported from `qgis.core`.",
    "Use the latest qgis libraries and methods.",
    "Utilize qgis python library instead of geopandas. Do not use geopandas in any of the processes.",
    "DO NOT include the QGIS initialization code in the script",
    f"Make yor codes to be concise/short and accurate",
    " `QVariant` should be imported from `PyQt5.Qtcore` and NOT `qgis.core`",
    "NOTE: `QgsVectorJoinInfo` may not always be available or accessible in recent QGIS installations, thus use `QgsVectorLayerJoinInfo` instead",
    "When running processing algorithms, use `processing.run('algorithm_id', {parameter_dictionary})`",
    # "DO NOT change the given variable names and paths.",
    "Put your reply into a Python code block (enclosed by python and ), NO explanation or conversation outside the code block.",
    "When using `QgsVectorLayer `, it should always be imported from qgis.core.",
    "When using Raster calculator 'native:rastercalculator' is wrong rather the correct ID for the Raster Calculator algorithm is 'native:rastercalc'.",
    " NOTE: When saving a file (e.g shapefile, csv file etc) to the any path/directory, first check if the the filename already exists in the specified path/directory. If it does, overwrite the file. If the file does not exist, then save the new file directly"
    "NOTE, when a one data path is provided, you DO NOT need to perform join.",
    "If you need to use any field from the input shapefile layer, first access the fields (example code: `fields = input_layer.fields()`), then select the appropriate field carefully from the list of fields in the layer.",
   "When loading a CSV layer as a layer, use this: `'f'file///{csv_path}?delimeter=,''`, assuming the csv is comma-separated, but use the csv_path directly for the Input parameter in join operations.",
    # "Do not use `QgsVectorLayer to load the output of a Temporary layer. Use `output_layer = result['OUTPUT']`."
    "Do not generate a layer for tasks that only require printing the answer, like questions of how, what, why, etc. e.g., for tasks like 'How many counties are there in PA?', 'What is the distance from A to B', etc.",
    "When creating plots such as barplot, scatterplot etc., usually their result is a html file. Always save the html file into the specified output directory and print the output layer. Do not Load the output HTML in QGIS as a standalone resource.",# Always print out the result"
    "When creating a scatter plot, 'native:scatterplot' and 'qgis:scatterplot' are not supported. The correct tool is qgis:vectorlayerscatterplot, ensure the correct tool is used",
    "When using the processing algorithm, make the output parameter to be the user's specified output directory . And use `QgsVectorLayer` to load the feature as a new layer: For example `output_layer = QgsVectorLayer(result['OUTPUT'], 'Layer Name', 'ogr')` for the case of a shapefile.",
    "Ensure that temporary layer is not used as the output paarameter"
    # "If you performed join, always export the joined layer as a new shapefile and load the new shapefile. `QgsVectorFileWriter.writeAsVectorFormatV3()` is recommended to be used to export the joined layer. It is used in this format: `QgsVectorFileWriter.writeAsVectorFormatV3(layer, output, QgsProject.instance().transformContext(), options)`."
    # f"If you performed join, you can follow this tempelate to create your code: {codebase.attribute_join}"
]