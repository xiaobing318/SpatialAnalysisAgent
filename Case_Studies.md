# Case Studies
The case studies demonstrate the capabilities of the Spatial Analysis Agent across three categories:

1. Tool Selection Capability: Showcases the agent's ability to identify and recommend the appropriate tool(s) for specific operations.
2. Code Generation Accuracy: Demonstrates the agent's proficiency in generating executable code to perform various spatial analysis tasks.
3. End-to-End Problem Solving: Evaluates the agent's ability to select the appropriate tool, generate the correct code, and successfully execute the complete operation.

## Level 1: Tool Selection Capability
### Case: Add new fields for x and y to the fast food restaurants layer, then extract the elevation values from the DEM layer and save the results in a new layer.

![FastFoodElevation.png](Doc%2FCase%20Studies%2FLevel%201%2FPA%20DEM%20and%20Fast%20foods%2FFastFoodElevation.png)

### Case: Perform the following task: 1) Reproject this road vector layer to NAD27/ UTM Zone 10 . 2) Create a new field that contains the length of the road features. Let the name of the field be "Length". 3) Extract roads that have length shorter than 100-meters.

![RoadNetwork.png](Doc%2FCase%20Studies%2FLevel%201%2FRoadNetwork%2FRoadNetwork.png)

### Case: Can you please delete all the empty columns?

![Delete empty fields.png](Doc%2FCase%20Studies%2FLevel%201%2FData%20processing%2FDelete%20empty%20fields.png)

## Level 2: Code Generation Accuracy
### Case: "Calculate the ruggedness index for Penssylvania, then summarize the ruggedness index value for each counties"

![Ruggedness.png](Doc%2FCase%20Studies%2FLevel%202%2FRuggedness%2FRuggedness.png)

![Codes2.png](Doc%2FCase%20Studies%2FLevel%202%2FRuggedness%2FCodes2.png)


### Case: "Create barchart showing obesity prevalence in the United States. Ensure all labels are clear"

![Obesity Barchart Map.png](Doc%2FCase%20Studies%2FLevel%202%2FObesity%20Barchart%2FObesity%20Barchart%20Map.png)

![Obesity Barchart.png](Doc%2FCase%20Studies%2FLevel%202%2FObesity%20Barchart%2FObesity%20Barchart.png)

![Code.png](Doc%2FCase%20Studies%2FLevel%202%2FObesity%20Barchart%2FCode.png)


### Case: Perform the following tasks: 1) Count the fast food restaurants in each county and store the result in a new field named "Count". 2) Calculate the fast food accessibility score for each county as (Count / Population) * 1,000 and store the result in a new field named "Score". 3) Create a thematic map showing the fast food accessibility score for each county. 

![Thematic map.png](Doc%2FCase%20Studies%2FLevel%202%2FObesity%20Score%20and%20fast%20food%2FThematic%20map.png)

![3sD9wcDDey.png](Doc%2FCase%20Studies%2FLevel%202%2FObesity%20Score%20and%20fast%20food%2F3sD9wcDDey.png)

### Case: Perform the following task: 1) Clip the DEM to PA Boundaries and load the clipped DEM. 2) Generate the zonal statistics for every county in PA, focusing on average elevation. 3) Create a choropleth map showing the average elevation of each county in PA, using a red color gradient to represent elevation differences. Load the Choropleth map
![Elevation Choropleth.png](Doc%2FCase%20Studies%2FLevel%202%2FElevation%20Choropleth%2FElevation%20Choropleth.png)

![Elevation_ChoroplethCodes.png](Doc%2FCase%20Studies%2FLevel%202%2FElevation%20Choropleth%2FElevation_ChoroplethCodes.png)


## Level 3: End-to-End Problem Solving

### Case: "Can you please generate a HTML report to show the building area for each building? You can look at the columns information, if no building area exists, please calculate yourself. Also make sure to use map projection when calculating area."

![Case1.png](Doc%2FCase%20Studies%2FLevel%203%2FCase1.png)

### Case: "What kind of analysis can I do for the DEM data?"
![DEM Analysis Outputs2.png](Doc%2FCase%20Studies%2FLevel%203%2FDEM%20Analysis%2FDEM%20Analysis%20Outputs2.png)

### Calculate the correlation coefficients between obesity rates and supermarket visit rates for each states in the USA. Let the result be in html format

![Correlation coefficient case report.png](Doc%2FCase%20Studies%2FLevel%203%2FCorrelation%20Coefficient%2FCorrelation%20coefficient%20case%20report.png)

### Case: Apply an affine transformation to the vector layer to scale by a factor of 2 and rotate 30 degrees.

![Affine transformation.png](Doc%2FCase%20Studies%2FLevel%202%2FAffine%20Transformation%2FAffine%20transformation.png)

### Case: Can you please select the residential area and calculate the total area covered by the residential area in square kilometers

![Selection of Land use.png](Doc%2FCase%20Studies%2FLevel%203%2FSelection%20of%20Land%20use.png)

### Case: Can you please create 20 random points in the DEM extend, and extract the elevation value for each point?

![Random Points.png](Doc%2FCase%20Studies%2FLevel%203%2FRandom%20Points.png)

### Case: Could you please show me the change in population from year 2000 to year 2008 for each counties in South Carolina?

![Pop change.png](Doc%2FCase%20Studies%2FLevel%201%2FData%20processing%2FPop%20change.png)
![Pop change_barplot.png](Doc%2FCase%20Studies%2FLevel%201%2FData%20processing%2FPop%20change_barplot.png)


### Case: Generate contour lines based on the DEM using interval of 2. Add the evelation as an attribute to the contour line layer.

