@echo off

echo %cd%

echo start build

if exist "build" rd/s/q "build"
if exist "dist" rd/s/q "dist"

pyinstaller src/main.py

xcopy "src/conf" "dist/main/conf" /s/e/d/y/i
xcopy "src/resources" "dist/main/resources" /s/e/d/y/i

md "dist/main/temp"
md "dist/main/log"

pause