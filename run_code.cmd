@echo off
setlocal enabledelayedexpansion

:: 設定日期格式，例如 "2024-11-15"
set "current_date=%date:~0,4%-%date:~5,2%-%date:~8,2%"

for /f "usebackq tokens=1,*" %%a in ("whitelist3.txt") do (
    if "%%b"=="" (
        call python get_searchpage_info.py %%a %current_date%
    ) else (
        call python get_searchpage_info.py %%a %%b %current_date%
    )   
    timeout /t 5 /nobreak
)

echo All script start, waiting for finish...
