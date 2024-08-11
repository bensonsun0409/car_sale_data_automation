@echo off
setlocal enabledelayedexpansion

for /f "usebackq tokens=1,*" %%a in ("whitelist.txt") do (
    if "%%b"=="" (
         python get_searchpage_info.py %%a
    ) else (
         python get_searchpage_info.py %%a %%b
    )
)

echo 所有腳本已啟動，正在等待完成...
pause