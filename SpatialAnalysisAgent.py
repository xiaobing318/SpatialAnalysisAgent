# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Spatial_Analysis_Agent
                                 A QGIS plugin
 A plugin integration between QGIS and Large Language Model (LLM) for Spatial Analysis
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2024-08-12
        git sha              : $Format:%H$
        copyright            : (C) 2024 by GIBD
        email                : teakinboyewa@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""


# 从QtCore中导入设置、翻译器、核心应用、QT库
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
# 从QtGui中导入QIcon
from qgis.PyQt.QtGui import QIcon
# 从QtWidgets中导入QAction
from qgis.PyQt.QtWidgets import QAction
# 从生成的资源中导入（Initialize Qt resources from file resources.py）
from .resources import *
# 从自定义文件中导入dockwidget（Import the code for the DockWidget）
from .SpatialAnalysisAgent_dockwidget import SpatialAnalysisAgentDockWidget
# 从python的标准库中导入路径相关库
import os.path

"""
    此代码是一个 QGIS 插件（SpatialAnalysisAgent）的主体类实现代码。该插件在 QGIS 环境中运行，用于在 QGIS 中添加菜单项、工具栏图标和
停靠窗口（DockWidget），从而为用户提供空间分析相关功能的交互界面。在 QGIS 中使用该插件，可以让用户通过菜单、工具栏与空间分析代理界面进行
交互，对地图数据进行分析和处理。插件可在 QGIS 主程序中添加自己的图标与菜单条目，并可启动一个停靠窗口进行参数设置和结果显示。
"""
class SpatialAnalysisAgent:
    """QGIS Plugin Implementation."""

    """
        初始化插件主类，保存 QGIS 接口引用，设置插件目录与国际化翻译文件加载，并初始化菜单、动作列表和其他插件资源。通过这些初始化，使得
    插件有能力将自己的界面元素（菜单、图标）整合进 QGIS 主程序。
    """
    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.(QGIS接口实例，用于在运行时操作QGIS应用)
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface(保存QGIS接口引用，以便在插件中使用QGIS的功能)
        self.iface = iface
        # initialize plugin directory(初始化插件目录，__file__是当前文件路径，通过os.path.dirname获取其所在目录)
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale(初始化本地化语言环境，从QSettings中获取用户语言设置，默认为en_US)
        locale = QSettings().value('locale/userLocale', 'en_US')[0:2]
        # 根据当前语言构建翻译文件路径
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'SpatialAnalysisAgent_{}.qm'.format(locale))
        # 如果存在相应的语言翻译文件，则加载翻译器
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes(初始化动作列表和菜单名称)
        self.actions = []
        # 定义插件在 QGIS 菜单中的显示名称，self.tr 是一个用于翻译的函数（通常在插件中定义，用于支持多语言）
        self.menu = self.tr(u'&AutonomousGIS-SpatialAnalysisAgent')
        # TODO: We are going to let the user set this up in a future iteration(将来可让用户自行设置工具栏)
        # self.toolbar = self.iface.addToolBar(u'Spatial_Analysis_Agent')
        # self.toolbar.setObjectName(u'Spatial_Analysis_Agent')
        
        # #print "** INITIALIZING Spatial_Analysis_Agent"

        # 设置一个布尔值标志 self.pluginIsActive，用于跟踪插件是否处于激活状态。初始值为 False，表示插件尚未激活
        self.pluginIsActive = False
        # 初始化 self.dockwidget 属性为 None，该属性将用于存储插件的停靠窗口（dock widget）实例。在插件运行过程中，可能会创建并分配一个具体的停靠窗口实例。
        self.dockwidget = None

    """
        noinspection PyMethodMayBeStatic
        封装了字符串翻译功能，返回给定字符串的翻译结果，以支持多语言界面。
    """
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.
        杨小兵-2024-12-18：说明了之所以需要自己实现这个方法，是因为当前类没有继承自 QObject。在 Qt 框架中，QObject 提供了内置的翻译支持（如 self.tr() 方法），
        但由于类未继承 QObject，因此需要手动实现翻译功能
        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        # QCoreApplication.translate用于获取翻译文本
        return QCoreApplication.translate('SpatialAnalysisAgent', message)

    """
        向 QGIS 工具栏和菜单中添加一个动作（action），包括设置图标、回调函数和文本等属性。这使得插件能够在 QGIS 界面中插入按钮和菜单项，
    供用户点击使用。
    """
    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        
        """添加一个动作（action）到工具栏或菜单中。
        :param icon_path: 动作图标路径
        :param text: 动作显示文本
        :param callback: 动作触发时调用的回调函数
        :param enabled_flag: 是否启用该动作
        :param add_to_menu: 是否添加到菜单中
        :param add_to_toolbar: 是否添加到工具栏中
        :param status_tip: 鼠标悬停提示
        :param whats_this: 帮助提示
        :param parent: 父组件
        :return: 创建的QAction对象
        """

        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # self.toolbar.addAction(action)
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)

        return action

    """
        在 QGIS 图形界面中初始化插件的界面元素（如工具栏图标、菜单项）。
    """
    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        # 定义图标路径
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        # 调用add_action添加一个菜单项和图标到QGIS界面
        self.add_action(
            icon_path,
            text=self.tr(u'AutonomousGIS Spatial Analysis Agent'),
            callback=self.run,
            parent=self.iface.mainWindow())

    """
        当插件的停靠窗口关闭时执行的清理函数，主要用于解除信号连接、释放资源，确保插件在关闭后不影响 QGIS 的正常运行。
    """
    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        #print "** CLOSING Spatial_Analysis_Agent"

        # disconnects(与dockwidget关闭信号断开连接，防止引用循环)
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain for reuse if plugin is reopened Commented next statement since it 
        # causes QGIS crashe when closing the docked window(不需要时可将dockwidget设为None（在此注释掉，因为可能导致QGIS崩溃）)
        # self.dockwidget = None

        # 设置插件激活状态为False，表示插件已关闭
        self.pluginIsActive = False

    """
        从 QGIS 界面中移除该插件的菜单项和图标，与 `initGui` 对应，在卸载插件时进行清理。
    """
    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        #print "** UNLOAD Spatial_Analysis_Agent"
        # 迭代所有创建的actions，将其从菜单和工具栏中移除
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&AutonomousGIS-SpatialAnalysisAgent'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        # del self.toolbar
    
    """
        当用户点击插件图标或菜单项启动插件时调用此函数。它会检查插件是否已经激活，如果没有则创建和显示停靠窗口（dockwidget），
    并进行相关信号连接，使用户可以通过该窗口进行交互。
    """
    def run(self):
        """Run method that loads and starts the plugin"""
        # 如果插件当前不处于激活状态
        if not self.pluginIsActive:
            self.pluginIsActive = True

            #print "** STARTING Spatial_Analysis_Agent"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference(如果dockwidget尚未创建，则创建一个新的dockwidget实例)
                self.dockwidget = SpatialAnalysisAgentDockWidget()

            # connect to provide cleanup on closing of dockwidget(将dockwidget的关闭信号与onClosePlugin连接，这样当dock关闭时可以执行清理)
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget(将dockwidget添加到QGIS界面右侧的停靠区域，并显示出来)
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
            self.dockwidget.show()
