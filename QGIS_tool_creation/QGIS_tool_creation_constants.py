#*********************************************************************************************************************************************************************
#---------------------------------Tool selection------------------------------------------------------------------------------------------------------------
CodeSample_role = r''' You have excellent proficiency in writing pyqgis codes to perform QGIS operations. You are very familiar with QGIS Processing toolbox. 

'''
CodeSample_prefix = rf' I will provide you with examples of some code for QGIS processing tool algorithm. I want you to generate a python code sample too for the processing tool algorithm for these tool parameter: '

CodeSample_example1 = """ 
```python
import processing
from qgis.core import QgsProject,QgsVectorLayer
def select_by_attribute(input_layer_path):
    # Define the parameters
    input_layer = QgsVectorLayer(input_layer_path, "Input Layer", "ogr")

    # Define the parameters Example below:
    parameters = {
        'INPUT': input_layer_path,
        'FIELD': 'Population',
        'OPERATOR': 4,  # Select the appropriate operator based on the task. Many different operators are available: ['0': '=', '1': '!=', '2': '>', '3':'>=', '4':'<', '5':'<=', '6': 'begins with', '7': 'contains', '8':'is null', '9': 'is not null', '10':'does not contain 
        'VALUE': 3000,
        'OUTPUT': output_layer_path
    }
    # Perform the extract by attribute operation
    result = processing.run("native:extractbyattribute", parameters)
    # Load the selected features as a new layer
    
    output_layer = QgsVectorLayer(output_path, 'Population_less_than_3000', 'ogr')
    QgsProject.instance().addMapLayer(output_layer)
input_layer_path = "D:/Data/PrevalenceData.shp"  # path to the input shapefile
output_layer_path ="D:/workspace_directory/output_layer.shp"
extractbyattribute(input_layer_path)
    
```
"""

CodeSample_reply_example2 = """
```python
# Import necessary modules
from qgis.core import QgsVectorLayer, QgsProject
import processing

def generate_centroids():
    # Define input and output paths
    input_path = 'D:/Data/Data.shp'
    output_path = 'C:/output_path/output_layer.shp'
  

    # Load the shapefile as a vector layer
    input_layer = QgsVectorLayer(input_path, 'Census Tracts', 'ogr')

    # Run the Centroids algorithm
    result = processing.run('native:centroids', {
        'INPUT': input_layer,
        'ALL_PARTS': False,  # Generates centroid for each feature (geom in multi-part geometries)
        'OUTPUT': output_path
    })

    # Load the centroid layer to QGIS
    centroids_layer = QgsVectorLayer(result['OUTPUT'], 'Centroids', 'ogr')
    QgsProject.instance().addMapLayer(centroids_layer)

# Execute the function
generate_centroids()
```
"""


CodeSample_requirements = ["Only provide the code sample for the tool based on the parameters given",
                           "Follow the logical flow of the examples of other tools provided",
                           "Do not add any explanation",
                           "The parameter values are not set separately. The value to each parameter should be set directly within the parameters dictionary. BUT, Do not add any comment when defining a parameter",

                           "If a parameter has other values options, the options should be specified as a comment when defining the parameter.",
                           "The output_path should be use in the 'OUTPUT' parameter",
                           "Your reply should only be the python code sample for the tool"

]