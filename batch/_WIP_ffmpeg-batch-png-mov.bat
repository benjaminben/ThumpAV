@echo off
setlocal enabledelayedexpansion

@REM rem Check if FFmpeg is installed
@REM set "ffmpeg=ffmpeg.exe"
@REM if not exist "!ffmpeg!" (
@REM     echo FFmpeg not found. Make sure FFmpeg is installed and added to PATH.
@REM     pause
@REM     exit /b
@REM )

@REM rem Check if any files were dragged onto the batch script
@REM if "%~1" == "" (
@REM     echo No files dragged. Drag PNG files onto this script to convert them to MOV.
@REM     pause
@REM     exit /b
@REM )

rem Create a temporary text file to store a list of PNG files
set "tmpfile=%TEMP%\png_list.txt"
del "!tmpfile!" 2>nul

rem Loop through the dragged files and create the list
for %%A in (%*) do (
    echo file '%%~A'>>"!tmpfile!"
)

rem Convert the PNG files to MOV using FFmpeg
"%ffmpeg%" -f concat -i "!tmpfile!" -c:v libx264 -pix_fmt yuv420p output.mov

rem Clean up the temporary text file
del "!tmpfile!" 2>nul

echo Conversion completed. The MOV file is named 'output.mov'.
pause