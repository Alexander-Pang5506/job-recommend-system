@echo off
chcp 65001 > nul
echo ================================
echo  招聘推荐系统 - 启动脚本
echo ================================
echo.

REM 设置 Python 编码为 UTF-8
set PYTHONIOENCODING=utf-8

REM 检查 MySQL 是否运行
echo [1/3] 检查 MySQL 服务...
"D:\Anaconda\python.exe" -c "import pymysql; conn = pymysql.connect(host='localhost', user='root', password='12345678', connect_timeout=3); print('MySQL 连接成功'); conn.close()" 2>nul
if errorlevel 1 (
    echo [警告] MySQL 可能未启动，请手动启动 MySQL 服务
    echo       MySQL 路径：C:\Users\P.sir\Desktop\mysql-8.0.30-winx64\bin\mysqld.exe
    pause
)

echo.
echo [2/3] 启动 Django 开发服务器...
echo       访问地址：http://localhost:8000
echo       管理后台：http://localhost:8000/admin
echo       按 Ctrl+C 停止服务器
echo.

"D:\Anaconda\python.exe" manage.py runserver 0.0.0.0:8000

echo.
echo 服务器已停止。
pause
