@echo off
setlocal enabledelayedexpansion

for /f "usebackq tokens=1,*" %%a in ("whitelist.txt") do (
    if "%%b"=="" (
        start /b python main0717.py %%a
        start /b python main0717.py %%a
    ) else (
        start /b python main0717.py %%a %%b
        start /b python main0717.py %%a %%b
    )
)

echo 所有腳本已啟動，正在等待完成...
pause