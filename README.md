# SpatialAnalysisAgent  
The Spatial Analysis Agent is a user-friendly plugin that serves as a "Copilot" in QGIS software. This Copilot allows users to perform geospatial analysis directly within QGIS using natural language queries, making it accessible for both experts and beginners.

The plugin leverages QGIS processing tools, and other external tools such as Python libraries (e.g., Geopandas, seaborn, etc.). Whether working with vector data, raster analysis, the Spatial Analysis Agent offers a flexible, AI-driven approach to enhance and automate GIS workflows.
 

# Installation
- [Download](https://github.com/Teakinboyewa/SpatialAnalysisAgent/archive/refs/heads/master.zip) the master repository of the plugin from GitHub
- Launch QGIS software and navigate to ```Plugin >  Manage and install Plugins.. > Install from ZIP```
- Click on ```...``` to select the directory of the downloaded zip file and ```Install plugin```

# User Manual
The User Manual is available [here](https://github.com/Teakinboyewa/SpatialAnalysisAgent/blob/master/User_Manual.md)

# Plugin Interface

![User Interface.png](Doc%2FUser%20Interface.png)

![Settings_tab.png](Doc%2FSettings_tab.png)

Note: API keys input here will only be stored locally on the user's computer ('plugin_dir/SpatialAnalysisAgent/config.ini').  

# Demonstration

https://github.com/user-attachments/assets/4c69d024-22c4-4458-ad6f-9b660715aef9


https://github.com/user-attachments/assets/4b23eba4-3e99-47ec-85d6-6efb7ebb6b20

[![YouTube Video](https://img.youtube.com/vi/1QbvKbWEgX0/0.jpg)](https://youtu.be/1QbvKbWEgX0)

### Normalized Difference Vegetation Index (NDVI) generation with remote sensing images
<a href="https://youtu.be/1QbvKbWEgX0">
  <img src="https://img.youtube.com/vi/1QbvKbWEgX0/0.jpg" alt="YouTube Video" width="800">
</a>

### Fast food accessibility analysis
<a href="https://youtu.be/wSEQILjgNWI">
  <img src="https://img.youtube.com/vi/wSEQILjgNWI/0.jpg" alt="YouTube Video" width="800">
</a>


Find more examples on the [Case Studies](https://github.com/Teakinboyewa/SpatialAnalysisAgent/blob/master/Case_Studies.md) page


# Installing required libraries
## Required python libraries
- ```openai```
- ```langchain_openai```
- ```nest-asyncio```
- ```networkx```
- ```pyvis```
- ```geopandas```
- ```IPython```
- ```iface ```
- ```jsonpickle ```
- ```regex```
- ```toml```
- ```seaborn```
- ```pydantic```

**Note:** All the required python libraries are expected to be installed automatically. However, if any of these python libraries failed to install automatically, you may install them manually by following the steps below to install the libraries.

### Libraries installation guide
Using 'openai' as an example, follow these steps to install any python library:
- Open the QGIS Python Console by navigating to ```Plugins``` > ```Python Console``` or press ```Ctrl+Alt+P```
- In the console, run these two lines of code sequentially:
  ```python
  import pip
  pip.main(['install', 'openai'])
