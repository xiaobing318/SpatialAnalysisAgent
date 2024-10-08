#  Spatial Analysis Agent User Manual
# Installation Guide
[//]: # (- In QGIS, ```select Plugins``` > ```Manage and Install Plugins...```)
[//]: # (- Find ```AutonomousGIS_GeoDataRetrieverAgent``` and click ```Install Plugin```)
[//]: # ()
[//]: # (Alternatively,)

- [Download](https://github.com/Teakinboyewa/SpatialAnalysisAgent/archive/refs/heads/master.zip) the master repository of the plugin from github
- Launch QGIS software and navigate to ```Plugin >  Manage and install Plugins.. > Install from ZIP```
- Click on ```...``` to select the directory of the downloaded zip file and ```Install plugin```

![Installation_page.png](Doc%2FInstallation_page.png)

- Click ```Yes``` to install all missing dependencies.
  
![Install dependencies.png](Docs%2FInstall%20dependencies.png)

- If successful, a success message will be displayed, then you can close the ```Plugins``` dialog. If you face any difficulty in installing any dependencies click here ([learn more about installing dependencies]())

![Plugin installation success.png](Docs%2FPlugin%20installation%20success.png)

# MacOS users
## After the installation of the plugin, you need to install the "nest_asyncio" manually. Follow the steps below:
- Open the QGIS Python Console by navigating to ```Plugins``` > ```Python Console``` or press ```Ctrl+Alt+P```
- In the console, run these two lines of code:
  ```python
  import pip
  pip.main(['install', 'nest-asyncio'])
- If you encounter any issue you can also try installing "nest_asyncio" via the terminal by pointing to QGIS python interpreter:
  
  ```python
  /Applications/QGIS3.38.1.app/Contents/MacOS/bin/python3 -m pip install nest_asyncio

- Restart the QGIS Software.
- Navigate to ```Plugins > Manage and install plugins```.  Ensure the plugin is checked.

![CheckBox.png](Docs%2FCheckBox.png)

# Opening the Plugin

- Load the ```Autonomous GIS - GeoData Retrieve Agent``` on ```Plugins```on menubar, or via its icon on the plugins toolbar.

![Plugin icon on toolbar.png](Docs%2FPlugin%20icon%20on%20toolbar.png)

# How to Use the Plugin
- The plugin interface consists of three tabs - ```Data Request Page```, ```Settings```, and ```Help```
- Data requests are made in the ```Data Request Page```. This consists of the ```Code pad``` which displays the AI-generated codes, ```Information Panel``` which displays the agent running information, ```Data request message panel``` which enables the user to enter the resuest message in natural language command, and the ```Output dirctory``` which enables user to set the desired path to save the downloaded data.

![Plugin Interface.png](Docs%2FPlugin%20Interface.png)

- The ```Settings``` tab, enable the user to select models and to set the Openai API keys and other data sources API keys. Find more details about [OpenAI API key](https://platform.openai.com/account/api-keys) and [data sources](https://github.com/Teakinboyewa/AutonomousGIS_GeodataRetrieverAgent/blob/master/User_manual.md#data-sources)

![PluginSetting.png](Docs%2FPluginSetting.png)

Note: API keys input here will only be stored locally on the user's computer ('plugin_dir/LLM-Find/config.ini').  

# Adding a new tool documentation



# Case studies

