from qgis.core import QgsVectorLayer, QgsProject, QgsVectorFileWriter, QgsGraduatedSymbolRenderer, QgsSymbol, QgsGradientColorRamp
import processing
import os
from PyQt5.QtGui import QColor

def perform_fastfood_analysis():
    # Define paths
    fastfoods_path = r"D:\Case_Studies\Data\Pennsylvania\PA_Fastfoods_XY.shp"
    counties_path = r"D:/Case_Studies/Data/Pennsylvania/PennsylvaniaCounties.shp"
    output_directory = r"C:\Users\AKINBOYEWA TEMITOPE\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\SpatialAnalysisAgent-master\Default_workspace"

    # Load layers
    fastfoods_layer = QgsVectorLayer(fastfoods_path, "FastFoodLocations", "ogr")
    counties_layer = QgsVectorLayer(counties_path, "PennsylvaniaCounties", "ogr")

    # 1. Count the fast food restaurants in each county
    count_output_path = os.path.join(output_directory, "CountyFastFoodCount.shp")

    if os.path.exists(count_output_path):
        base, ext = os.path.splitext(count_output_path)
        count_output_path = f"{base}_1{ext}"

    params_count_points = {
        'POLYGONS': counties_layer,
        'POINTS': fastfoods_layer,
        'WEIGHT': '',
        'CLASSFIELD': '',
        'FIELD': 'Count',
        'OUTPUT': count_output_path
    }

    result_count = processing.run("native:countpointsinpolygon", params_count_points)
    counted_layer = QgsVectorLayer(result_count['OUTPUT'], 'Counted', 'ogr')
    QgsProject.instance().addMapLayer(counted_layer)

    # 2. Calculate the fast food accessibility score for each county
    score_output_path = os.path.join(output_directory, "CountyAccessibilityScore.shp")

    if os.path.exists(score_output_path):
        base, ext = os.path.splitext(score_output_path)
        score_output_path = f"{base}_1{ext}"

    params_field_calculator = {
        'INPUT': counted_layer,
        'FIELD_NAME': 'Score',
        'FIELD_TYPE': 0,  # Decimal (double)
        'FIELD_LENGTH': 10,
        'FIELD_PRECISION': 3,
        'FORMULA': '("Count" / "Population") * 1000',
        'OUTPUT': score_output_path
    }

    result_score = processing.run("native:fieldcalculator", params_field_calculator)
    scored_layer = QgsVectorLayer(result_score['OUTPUT'], 'Score', 'ogr')
    QgsProject.instance().addMapLayer(scored_layer)

    # 3. Create the thematic map showing fast food accessibility score
    thematic_map_output_path = os.path.join(output_directory, "FastFoodAccessibilityMap.shp")

    if os.path.exists(thematic_map_output_path):
        base, ext = os.path.splitext(thematic_map_output_path)
        thematic_map_output_path = f"{base}_1{ext}"

    # Create a Graduated Symbol Renderer using 'Score' field
    symbol = QgsSymbol.defaultSymbol(scored_layer.geometryType())

    renderer = QgsGraduatedSymbolRenderer('', [])
    renderer.setClassAttribute('Score')
    renderer.setMode(QgsGraduatedSymbolRenderer.Quantile)
    renderer.updateClasses(scored_layer, 5)

    # Set the color ramp (green gradient)
    color1 = QColor(144, 238, 144)  # light green
    color2 = QColor(0, 128, 0)  # dark green
    color_ramp = QgsGradientColorRamp(color1, color2)

    renderer.updateColorRamp(color_ramp)
    scored_layer.setRenderer(renderer)
    scored_layer.triggerRepaint()

    # Save thematic map
    QgsVectorFileWriter.writeAsVectorFormat(scored_layer, thematic_map_output_path, "utf-8", scored_layer.crs(), "ESRI Shapefile")
    thematic_layer = QgsVectorLayer(thematic_map_output_path, 'ThematicMap', 'ogr')
    QgsProject.instance().addMapLayer(thematic_layer)

# Execute the function
perform_fastfood_analysis()