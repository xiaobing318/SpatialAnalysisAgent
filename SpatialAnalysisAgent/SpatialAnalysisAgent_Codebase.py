import processing

Thematic_map_creation_sample = r'''
#Importing necessary modules
from qgis.core import QgsVectorLayer, QgsProject, QgsVectorLayerJoinInfo, QgsGraduatedSymbolRenderer, QgsMapSettings, QgsSymbol
from qgis.PyQt.QtCore import QVariant, QSize
from qgis.PyQt.QtGui import QImage, QPainter, QColor
    
def Thematic_Map_Creation():
    # Load the shapefile
    path_to_layer = 'D:\\Data\\Data.shp'
    layer = QgsVectorLayer(path_to_layer, "Population_Distribution", "ogr")
    QgsProject.instance().addMapLayer(layer)
    
    # Create a Graduated Symbol Renderer using 'Population' field
    symbol = QgsSymbol.defaultSymbol(layer.geometryType())
    renderer = QgsGraduatedSymbolRenderer('', [])
    renderer.setClassAttribute('Population')
    renderer.setMode(QgsGraduatedSymbolRenderer.Quantile)
    renderer.updateClasses(layer, 5)
    
    # Set the color ramp (green gradient)
    from qgis.core import QgsGradientColorRamp
    color1 = QColor(144, 238, 144) # light green
    color2 = QColor(0, 128, 0)     # dark green
    color_ramp = QgsGradientColorRamp(color1, color2)
    renderer.updateColorRamp(color_ramp)

    layer.setRenderer(renderer)
    layer.triggerRepaint()
    QgsProject.instance().addMapLayer(layer)

# Execute the function
Thematic_Map_Creation()

'''
Extract_by_attribute_example = r'''
import processing
from qgis.core import QgsProject

# Define the parameters
input_layer_path = 'path/to/input_layer.shp' # path to the input shapefile
output_path = 'path/to/save/selected_features.shp'  # Path to save the new shapefile

input_layer = QgsVectorLayer(input_layer_path, "Input Layer", "ogr")
QgsProject.instance().addMapLayer(input_layer)

#Define the parameters Example below:
field_name = 'Area'
operator = 4  # Select the appropriate operator based on the task. Many different operators are available: ['0': '=', '1': '!=', '2': '>', '3':'>=', '4':'<', '5':'<=', '6': 'begins with'  etc] 
value = '4'
parameters = {
    'INPUT': input_layer_path,
    'FIELD': field_name,
    'OPERATOR': operator,
    'VALUE': value,
    'OUTPUT': 'memory:'  # Use 'memory:' to create a temporary layer in memory
}
# Perform the extract by attribute operation
result = processing.run("native:extractbyattribute", parameters)

# Load the selected features as a new layer
output_layer = result['OUTPUT']
QgsProject.instance().addMapLayer(output_layer)

# Save the selected features to a new shapefile
options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName = "ESRI Shapefile"
options.fileEncoding = "UTF-8"
transform_context = QgsProject.instance().transformContext()

# Write the vector layer to a new shapefile
QgsVectorFileWriter.writeAsVectorFormatV3(output_layer, output_path, transform_context, options)

#loading the saved_selecteded layer
selected_layer = QgsVectorLayer(output_path, "Selected Layer", "ogr")
QgsProject.instance().addMapLayer(selected_layer)

'''

Extract_by_attribute_parameters = r'''
INPUT - Layer to extract features from
FIELD - Filtering field of the layer
OPERATOR - Many different operators are available: ['0': '=', '1': '!=', '2': '>', '3':'>=', '4':'<', '5':'<=', '6': 'begins with'  etc] 
VALUE - Value to be evaluated (Optional)
OUTPUT - Default: [Create Temporary Layer], specify the output vector layer for matching features.
'''



attribute_join = r"""
```
from qgis.core import QgsVectorLayer, QgsProject, QgsVectorLayerJoinInfo, QgsVectorFileWriter
from PyQt5.QtCore import QVariant

# Load PA tract boundary shapefile
# tract_boundary_path = 'D:/LLM_Geo_QGIS/Case_Study1/data/tract_42_EPSG4326/tract_42_EPSG4326.shp'
tract_boundary_path = r"D:/SpatialAnalysisAgent/Data/SouthCarolinaCounties/SouthCarolinaCounties.shp"
tract_boundary = QgsVectorLayer(tract_boundary_path, "PA Tract Boundary", "ogr")
QgsProject.instance().addMapLayer(tract_boundary)

# Load CSV data file
# csv_data_path = 'D:/LLM_Geo_QGIS/Case_Study1/data/PA_Data.csv'
csv_data_path = 'D:/SpatialAnalysisAgent/Data/SouthCarolinaCounties/CensusData.csv'
csv_layer = QgsVectorLayer(f'file:///{csv_data_path}?delimiter=,', 'csv_data', 'delimitedtext')
QgsProject.instance().addMapLayer(csv_layer)

# Setup join information
join_info = QgsVectorLayerJoinInfo()
join_info.setJoinLayer(csv_layer)
join_info.setTargetFieldName("GEOID")
join_info.setJoinFieldName("GEOID")
join_info.setPrefix("")

# Apply join to the tract boundary layer
tract_boundary.addJoin(join_info)

# Export the joined layer as a new shapefile and load it into the project
# output_path = 'D:/LLM_Geo_QGIS/Case_Study1/data/joined_tract_boundary.shp'
output_path =os.path.join("D:/SpatialAnalysisAgent/Data/SouthCarolinaCounties/Temporary_Joined_Layer.shp")
options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName = 'ESRI Shapefile'
options.fileEncoding = "UTF-8"

QgsVectorFileWriter.writeAsVectorFormatV3(tract_boundary, output_path, QgsProject.instance().transformContext(), options)

joined_layer = QgsVectorLayer(output_path, "Joined Tract Boundary", "ogr")
QgsProject.instance().addMapLayer(joined_layer)
```
"""
from qgis import processing
from qgis.core import *
# Algorithm name to search for
from qgis.core import QgsApplication




from qgis.core import QgsApplication

# Create a list to store the algorithm names
algorithm_names = []
for alg in QgsApplication.processingRegistry().algorithms():
    algorithm_names.append(alg.displayName())
# print("algorithms names: ", algorithm_names)

algorithm_IDs = []
for alg in QgsApplication.processingRegistry().algorithms():
    algorithm_names.append(alg.id())


algorithms_dict = {}
# Iterate through the algorithms in the processing registry
for alg in QgsApplication.processingRegistry().algorithms():
    algorithms_dict[alg.displayName()] = {'ID': alg.id()}
# print(algorithms_dict)

# Check if the selected tool exists in the dictionary
def documentation (selected_tool_ID,algorithm_names):
    if selected_tool_ID in algorithm_names:
        selected_tool_handbook = processing.algorithmHelp(selected_tool_ID)
        print(f"Handbook for {selected_tool_ID} ):\n{selected_tool_handbook}")
    else:
        print("Tool not found")


#************************************************************************************************************************






