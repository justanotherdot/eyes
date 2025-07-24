@echo off
REM Windows startup script for Eyes
REM This file should be placed in the Windows Startup folder

REM Change this path to where your eyes.exe is located
set EYES_PATH=C:\eyes\eyes.exe

REM Run eyes with default 20-minute intervals
"%EYES_PATH%" --interval 20