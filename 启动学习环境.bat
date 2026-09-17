@echo off
chcp 936 >nul
cd /d "%~dp0"
title AI Learning Environment

rem 补齐本地站点需要的两个生成文件（gitignore 的，换电脑克隆后缺失）
where node >nul 2>&1 && node scripts\gen_site_meta.js

echo.
echo   ============================================
echo     本地学习环境启动中...
echo.
echo     学习看板:  http://localhost:8931/学习看板.html
echo     课程网站:  http://localhost:8931/site/index.html
echo.
echo     * 浏览器即将自动打开学习看板
echo     * 保持本窗口开着；关闭窗口 = 停止服务
echo   ============================================
echo.

start /b python -m http.server 8931 >nul 2>&1
timeout /t 2 /nobreak >nul
start "" "http://localhost:8931/%E5%AD%A6%E4%B9%A0%E7%9C%8B%E6%9D%BF.html"

echo   服务已启动。按任意键停止服务并退出...
pause >nul
