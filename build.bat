@echo off
echo Started: %date% %time%

mkdir obj
python build\compile.py
move *.o obj\
echo.

python build\build.py
echo.
build\armips.exe asm\main.asm -sym rom\dk64-tag-anywhere-dev.sym
del rom\dk64-tag-anywhere-python.z64
rmdir /s /q .\obj
echo.
build\n64crc.exe rom\dk64-tag-anywhere-dev.z64
echo.
echo Completed: %date% %time%
echo.
echo If you would like to create a BPS batch,
pause
build\flips.exe --create "rom\dk64.z64" "rom\dk64-tag-anywhere-dev.z64" "rom\dk64-tag-anywhere-dev.bps"
pause