# 1 Spatial Analysis Agent User Manual
```c
/*
notes:杨小兵-2024-12-17

1、这个文件将会讲述如何使用Spatial Analysis Agent
*/
```

# 2 Installation Guide
[//]: # (- In QGIS, ```select Plugins``` > ```Manage and Install Plugins...```)
[//]: # (- Find ```AutonomousGIS_GeoDataRetrieverAgent``` and click ```Install Plugin```)
[//]: # ()
[//]: # (Alternatively,)

- [Download](https://github.com/Teakinboyewa/SpatialAnalysisAgent/archive/refs/heads/master.zip) the master repository of the plugin from github
- Launch QGIS software and navigate to ```Plugin >  Manage and install Plugins.. > Install from ZIP```
- Click on ```...``` to select the directory of the downloaded zip file and ```Install plugin```

![Installation_page.png](Doc%2FInstallation_page.png)
```c
/*
notes:杨小兵-2024-12-17

1、上述内容讲述的是如何在QGIS中安装Spatial Analysis Agent插件
*/
```

- If successful, a success message will be displayed, then you can close the ```Plugins``` dialog.

![Plugin install successful.png](Doc%2FPlugin%20install%20successful.png)

[//]: # (# MacOS users)

[//]: # (## After the installation of the plugin, you need to install the "nest_asyncio" manually. Follow the steps below:)

[//]: # (- Open the QGIS Python Console by navigating to ```Plugins``` > ```Python Console``` or press ```Ctrl+Alt+P```)

[//]: # (- In the console, run these two lines of code:)

[//]: # (  ```python)

[//]: # (  import pip)

[//]: # (  pip.main&#40;['install', 'nest-asyncio']&#41;)

[//]: # (- If you encounter any issue you can also try installing "nest_asyncio" via the terminal by pointing to QGIS python interpreter:)

[//]: # (  )
[//]: # (  ```python)

[//]: # (  /Applications/QGIS3.38.1.app/Contents/MacOS/bin/python3 -m pip install nest_asyncio)

- Navigate to ```Plugins > Manage and install plugins```.  Ensure the plugin is checked.

![CheckBox.png](Doc%2FCheckBox.png)

# 3 Opening the Plugin

- Load the ```Spatial Analysis Agent``` on ```Plugins```on menubar, or via its icon on the plugins toolbar.

![Plugin Icon oon toolbar.png](Doc%2FPlugin%20Icon%20oon%20toolbar.png)

- Once the plugin is loaded, a dialog indicating any missing dependencies will appear. Ensure you install all the dependencies by clicking the Yes button.

![Missing dependencies.png](Doc%2FMissing%20dependencies.png)

- After the installation of the missing dependencies, restart the QGIS software.

# 4 How to Use the Plugin

## 4.1 Plugin interface


![Plugin Interface.png](Doc%2FPlugin%20Interface.png)

- The plugin interface consists of five tabs - ```Request Page```, ```Reports```, ```Solution Graph```, ```Settings```, and ```Help```
- ```Data Request Page```:  is the main tab where user can make a request. This consists of the ```Code panel``` which displays the AI-generated codes, ```Information Panel``` which displays the agent running information, ```Message panel``` which enables the users to enter the task they want to perform, and the ```Data directories``` which contain the data path of all the data loaded into QGIS.
-  ```Report```: allows users to access and visualize various forms of generated reports such as charts, plots, statistical reports, etc., in different format like html and image.
-  ```Solution Graph```: This tab displays the steps/breakdown of performing the task requested by user is displayed in as a graph.
-  ```Settings```: This tab enable users to set the OpenAI API keys (Find more details about [OpenAI API key](https://platform.openai.com/account/api-keys)), select the model (e.g, gpt-4). Users can check the "Chat Mode" box to switch to chat with AI. Also, the ```Settings``` tab allow users to set the workspace directory, i.e where results will be saved on their computer. A default directory is set by default after the installation of the plugin. Additionally, users can add tool documentation file to either their local machine or to the Plugin's GitHub repository ([find out more](https://github.com/Teakinboyewa/SpatialAnalysisAgent/blob/master/SpatialAnalysisAgent/Tools_Documentation/Tools_documentationREADME.MD)).

Note: API keys input here will only be stored locally on the user's computer ('plugin_dir/SpatialAnalysisAgent/config.ini'). 

![Settings.png](Doc%2FSettings.png)

- ```Help```: This contains guide on how to use the CoPilot


# 5 Adding a new tool documentation

This plugin includes comprehensive documentation for QGIS native tools. To enhance the functionality and performance of the plugin, users have the option to create and integrate customized tools. For more information on how to add custom tool documentation, [click here](https://github.com/Teakinboyewa/SpatialAnalysisAgent/blob/master/SpatialAnalysisAgent/Tools_Documentation/Tools_documentationREADME.MD).
```c
/*
notes:杨小兵-2024-12-17

1、这部分信息是比较重要的
*/
```

# 6 Case studies

The case studies demonstrate the capabilities of the Spatial Analysis Agent across three categories:

1. Tool Selection Capability: Showcases the agent's ability to identify and recommend the appropriate tool(s) for specific operations.
2. Code Generation Accuracy: Demonstrates the agent's proficiency in generating executable code to perform various spatial analysis tasks.
3. End-to-End Problem Solving: Evaluates the agent's ability to select the appropriate tool, generate the correct code, and successfully execute the complete operation.

Explore the detailed case studies on the [Case Study page](https://github.com/Teakinboyewa/SpatialAnalysisAgent/blob/master/Case_Studies.md).

