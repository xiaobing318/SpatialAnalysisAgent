# SpatialAnalysisAgent
The Spatial Analysis Agent is a plugin integration of an autonomous GIS agent for spatial analysis and QGIS. This plugin leverages QGIS processing tools to perfom spatial analysis within QGIS.

# Installation
- [Download](https://github.com/Teakinboyewa/SpatialAnalysisAgent/archive/refs/heads/master.zip) the master repository of the plugin from github
- Launch QGIS software and navigate to ```Plugin >  Manage and install Plugins.. > Install from ZIP```
- Click on ```...``` to select the directory of the downloaded zip file and ```Install plugin```

# User Manual
The User Manual is available [here](https://github.com/Teakinboyewa/SpatialAnalysisAgent/blob/master/User%20Manual.md)

# Plugin Interface

![Plugin Interface.png](Docs%2FPluginGUI.png)

![Settings.png](Docs%2FPluginSetting.png)

Note: API keys input here will only be stored locally on the user's computer ('plugin_dir/SpatialAnalysisAgent/config.ini').  

# Usage
Find some usage example on the Data Request [Examples](https://github.com/Teakinboyewa/AutonomousGIS_GeodataRetrieverAgent/blob/master/Data%20request%20examples.md) page


# Installing required libraries
## Required python libraries
- ```openai```
- ```QSwitchControl```
- ```nest-asyncio```

**Note:** You may need to install some other python libraries that may not be present in your QGIS environment. Follow the steps below to install the libraries mentioned or others

### Libraries installation guide
Using 'openai' as an example, follow these steps to install any python library:
- Open the QGIS Python Console by navigating to ```Plugins``` > ```Python Console``` or press ```Ctrl+Alt+P```
- In the console, run these two lines of code sequentially:
  ```python
  import pip
  pip.main(['install', 'openai'])
