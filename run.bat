@echo off
chcp 65001 >nul
echo ====================================
echo   云软通话记录服务启动中...
echo ====================================
cd /d "%~dp0"
echo 激活虚拟环境...
call venv\Scripts\activate.bat
echo 启动Flask服务...
python app.py
pause
