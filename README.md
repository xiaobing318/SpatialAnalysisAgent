# 1 SpatialAnalysisAgent
The Spatial Analysis Agent is a user-friendly plugin that serves as a "Copilot" in QGIS software. This GIS Copilot allows users to perform geospatial analysis directly within QGIS using natural language queries, making it accessible for both experts and beginners.
```c
/*
notes:杨小兵-2024-12-17

1、当前项目的名称是SpatialAnalysisAgent（空间分析agent）
2、The Spatial Analysis Agent是一个用户友好的插件，这个插件在QGIS软件中作为一个Copilot
3、这个GIS Copilot允许用户在QGIS中直接使用自然语言执行地理空间分析
4、这个GIS Copilot插件对于专家和初学者更加容易上手
*/
```

The Copilot leverages QGIS processing tools, and other external tools such as Python libraries (e.g., Geopandas, Rasterio, seaborn, etc.). Whether working with vector data, raster analysis, the Spatial Analysis Agent offers a flexible, AI-driven approach to enhance and automate GIS workflows.
```c
/*
notes:杨小兵-2024-12-17

1、Copilot 利用 QGIS 处理工具和其他外部工具，例如 Python 库（例如 Geopandas、Rasterio、seaborn 等）。无论是处理矢量数据还是栅格分析，the Spatial Analysis Agent都提供了一种灵活的 AI 驱动方法来增强和自动化 GIS 工作流程。
*/
```

For more details on the framework used by this plugin, refer to our preprint manuscript: Temitope Akinboyewa, Zhenlong Li, Huan Ning, and M. Naser Lessani. 2024. *"GIS Copilot: Towards an Autonomous GIS Agent for Spatial Analysis."* arXiv. 
https://doi.org/10.48550/arXiv.2411.03205
```c
/*
notes:杨小兵-2024-12-17

1、对于这个插件使用框架的更多信息，参考预印版：GIS Copilot: Towards an Autonomous GIS Agent for Spatial Analysis
*/
```

QGIS Plugin page: https://plugins.qgis.org/plugins/SpatialAnalysisAgent-master/
```c
/*
notes:杨小兵-2024-12-17

1、给出了the Spatial Analysis Agent这个插件在QGIS仓库的位置
*/
```

# 2 Installation
- In QGIS software, select  ```Plugins``` > ```Manage and Install Plugins...```
- Find ```AutonomousGIS-SpatialAnalysisAgent``` and click ```Install Plugin```
```c
/*
notes:杨小兵-2024-12-17

1、上述讲述的是在QGIS中如何下载安装AutonomousGIS-SpatialAnalysisAgent
*/
```

Alternatively,

- [Download](https://github.com/Teakinboyewa/SpatialAnalysisAgent/archive/refs/heads/master.zip) the master repository of the plugin from GitHub
- Launch QGIS software and navigate to ```Plugin >  Manage and install Plugins.. > Install from ZIP```
- Click on ```...``` to select the directory of the downloaded zip file and ```Install plugin```

# 3 User Manual
The User Manual is available [here](https://github.com/Teakinboyewa/SpatialAnalysisAgent/blob/master/User_Manual.md)
```c
/*
notes:杨小兵-2024-12-17

1、上述给出的是一个如何使用该插件的用户手册
*/
```

# 4 Plugin Interface

![User Interface.png](Doc%2FUser%20Interface.png)

![Settings_tab.png](Doc%2FSettings_tab.png)

Note: API keys input here will only be stored locally on the user's computer ('plugin_dir/SpatialAnalysisAgent/config.ini').  
```c
/*
notes:杨小兵-2024-12-17

1、注意API keys的输出将仅会存储到用户机器的本地（具体的位置是：plugin_dir/SpatialAnalysisAgent/config.ini）
2、采用配置文件的形式是比较常见的
*/
```

# 5 Demonstration

https://github.com/user-attachments/assets/4c69d024-22c4-4458-ad6f-9b660715aef9


https://github.com/user-attachments/assets/4b23eba4-3e99-47ec-85d6-6efb7ebb6b20


[//]: # (### Normalized Difference Vegetation Index &#40;NDVI&#41; generation with remote sensing images)
[//]: # (<h2 style="margin-bottom: 0;">Normalized Difference Vegetation Index &#40;NDVI&#41; generation with remote sensing images</h2>)
<a href="https://www.youtube.com/watch?v=1QbvKbWEgX0&t=8s" target="_blank">
  <img src="https://img.youtube.com/vi/1QbvKbWEgX0/0.jpg" alt="YouTube Video" width="800">
</a>


[//]: # (### Fast food accessibility analysis)
<a href="https://youtu.be/wSEQILjgNWI&t=8s" target="_blank">
  <img src="https://img.youtube.com/vi/wSEQILjgNWI/0.jpg" alt="YouTube Video" width="800">
</a>

<a href="https://youtu.be/rmKfJBOOm6E&t=8s" target="_blank">
  <img src="https://img.youtube.com/vi/rmKfJBOOm6E/0.jpg" alt="YouTube Video" width="800">
</a>

<a href="https://youtu.be/rhm_wAhPbRU&t=8s" target="_blank">
  <img src="https://img.youtube.com/vi/rhm_wAhPbRU/0.jpg" alt="YouTube Video" width="800">
</a>

<a href="https://youtu.be/MV2R5cEfpxg&t=8s" target="_blank">
  <img src="https://img.youtube.com/vi/MV2R5cEfpxg/0.jpg" alt="YouTube Video" width="800">
</a>


Find more examples on the [Case Studies](https://github.com/Teakinboyewa/SpatialAnalysisAgent/blob/master/Case_Studies.md) page


# 6 Installing required libraries

This plugin requires Python >= 3.11 
```c
/*
notes:杨小兵-2024-12-17

1、这个要求不是特别容易满足
*/
```

## 6.1 Required python libraries
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
- ```rasterio```

**Note:** All the required python libraries are expected to be installed automatically. However, if any of these python libraries failed to install automatically, you may install them manually by following the steps below to install the libraries.
```c
/*
notes:杨小兵-2024-12-17

1、注意：所有这些要求的python库将会自动下载。但是如果这些python库中的任何一个自动安装失败的话，你可能需要安装下列的步骤手动下载安装这些库
*/
```

### Libraries installation guide
Using 'openai' as an example, follow these steps to install any python library:
- Open the QGIS Python Console by navigating to ```Plugins``` > ```Python Console``` or press ```Ctrl+Alt+P```
- In the console, run these two lines of code sequentially:
  ```python
  import pip
  pip.main(['install', 'openai'])
```c
/*
notes:杨小兵-2024-12-17

1、以openai这个python库作为一个例子，按照这些步骤安装任意的python库
2、安装步骤
  2.1 Plugins--->Python Console打开python console
  2.2 在python console中顺序运行上述提到的两行代码
*/
```