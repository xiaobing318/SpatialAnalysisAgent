REM 解释：关闭命令回显功能。默认情况下，批处理文件在执行时会在命令行窗口显示每一条命令。使用 @ECHO OFF 后，命令本身不会被显示，只会显示输出结果。@ 符号确保这一行命令本身也不会被回显。
@ECHO OFF 

REM 解释：设置环境变量 OSGEO4W_ROOT 的值为 QGIS 的安装路径。
set OSGEO4W_ROOT=C:\Program Files\QGIS 3.26.2
REM 解释：将 QGIS 的安装路径添加到系统环境变量 PATH 中。
set PATH=%OSGEO4W_ROOT%\bin;%PATH%
REM 解释：将 QGIS 的应用程序路径添加到系统环境变量 PATH 中。
set PATH=%PATH%;%OSGEO4W_ROOT%\apps\qgis\bin

REM 解释：关闭命令回显功能。默认情况下，批处理文件在执行时会在命令行窗口显示每一条命令。使用 @ECHO OFF 后，命令本身不会被显示，只会显示输出结果。@ 符号确保这一行命令本身也不会被回显。
@echo off
REM 解释：使用call命令调用o4w_env.bat、qt5_env.bat和py3_env.bat文件，这三个文件分别设置了QGIS的环境变量。
call "%OSGEO4W_ROOT%\bin\o4w_env.bat"
call "%OSGEO4W_ROOT%\bin\qt5_env.bat"
call "%OSGEO4W_ROOT%\bin\py3_env.bat"
@echo off

REM 解释：进一步设置 PATH 环境变量，将 C:\Program Files\QGIS 3.26.2\apps\qgis\bin 添加到现有的 PATH 变量的前面。这里使用了 path 命令而不是 set PATH=...，这可能是为了确保在之前设置的 PATH 基础上进一步调整路径顺序。
path %OSGEO4W_ROOT%\apps\qgis\bin;%PATH%
REM 更改目录命令，不仅更改目录，还更改驱动器（如果需要），这是一个批处理文件中的特殊变量，表示当前批处理文件所在的驱动器和路径。例如，如果批处理文件位于 D:\Scripts\setup.bat，那么 %~dp0 的值就是 D:\Scripts\。
cd /d %~dp0