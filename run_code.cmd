@echo off
setlocal enabledelayedexpansion

for /f "usebackq tokens=1,*" %%a in ("whitelist3.txt") do (
    if "%%b"=="" (
        call python get_searchpage_info.py %%a
    ) else (
        call python get_searchpage_info.py %%a %%b
    )
    timeout /t 5 /nobreak
)

echo All script start, waiting for finish...
