@echo off
setlocal enabledelayedexpansion

for /f "usebackq tokens=1,*" %%a in ("whitelist.txt") do (
    if "%%b"=="" (
        start /b python script1.py %%a
        start /b python script2.py %%a
    ) else (
        start /b python script1.py %%a %%b
        start /b python script2.py %%a %%b
    )
)

echo 所有腳本已啟動，正在等待完成...
pause