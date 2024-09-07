chcp 65001
@echo off
setlocal enabledelayedexpansion

rem 日志文件路径
set "logFile=script_log.txt"

rem 记录开始时间
set "startTime=%time%"

for /f "usebackq tokens=1,*" %%a in ("whitelist.txt") do (
    set "retryCount=0"
    :retry
    if "%%b"=="" (
        python get_searchpage_info.py %%a >> "%logFile%" 2>&1
    ) else (
        python get_searchpage_info.py %%a %%b >> "%logFile%" 2>&1
    )
    rem 检查上一个命令的退出码
    if !errorlevel! neq 0 (
        echo "Error encountered while processing %%a %%b" >> "%logFile%"
        set /a retryCount+=1
        if !retryCount! leq 3 (
            echo "Retrying %%a %%b (Attempt !retryCount!)" >> "%logFile%"
            timeout /t 10 >nul
            goto retry
        )
    )
    rem 等待上一个进程完成
    timeout /t 5 >nul
)

rem 记录结束时间
set "endTime=%time%"

rem 计算时间差
echo 開始時間: %startTime% >> "%logFile%"
echo 結束時間: %endTime% >> "%logFile%"

rem 计算时间差的脚本
call :CalculateTimeDifference "%startTime%" "%endTime%" >> "%logFile%"

echo 所有腳本已啟動，正在等待完成...
pause
goto :EOF

:CalculateTimeDifference
setlocal
set "start=%~1"
set "end=%~2"

rem 计算开始时间的小时、分钟、秒
for /f "tokens=1-4 delims=:.," %%a in ("%start%") do (
    set /a "startH=1%%a-100"
    set /a "startM=1%%b-100"
    set /a "startS=1%%c-100"
)

rem 计算结束时间的小时、分钟、秒
for /f "tokens=1-4 delims=:.," %%a in ("%end%") do (
    set /a "endH=1%%a-100"
    set /a "endM=1%%b-100"
    set /a "endS=1%%c-100"
)

rem 计算时间差
set /a "startTotalSeconds=(startH*3600)+(startM*60)+startS"
set /a "endTotalSeconds=(endH*3600)+(endM*60)+endS"
set /a "diffSeconds=endTotalSeconds-startTotalSeconds"

rem 输出时间差
set /a "diffH=diffSeconds/3600"
set /a "diffM=(diffSeconds%%3600)/60"
set /a "diffS=diffSeconds%%60"

echo 執行時間: %diffH% 小時 %diffM% 分鐘 %diffS% 秒

endlocal
goto :EOF
