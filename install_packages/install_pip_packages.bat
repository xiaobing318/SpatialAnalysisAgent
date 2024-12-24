REM 解释：打开命令回显功能。默认情况下，批处理文件在执行时会在命令行窗口显示每一条命令。
@echo ON
REM 解释：切换到对应的目录下
cd /d %~dp0
REM 解释：调用py3-env.bat文件
call "py3-env.bat"
REM 解释：使用python中的install模块安装requirements.txt中的依赖包
python3 -m pip install -r requirements.txt
REM 解释：暂停脚本的执行，等待用户按任意键继续
pause