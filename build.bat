@echo off
echo Started: %date% %time%
echo.
echo Compiling C code
mkdir obj
python build\compile.py
move *.o obj\ > NUL
echo.

python build\build.py
echo.
build\armips.exe asm\main.asm -sym rom\dk64-tag-anywhere-dev.sym
del rom\dk64-tag-anywhere.z64
rmdir /s /q .\obj > NUL
build\n64crc.exe rom\dk64-tag-anywhere-dev.z64
echo.
echo Completed: %date% %time%
echo.
echo If you would like to create a BPS batch,
pause
build\flips.exe --create "rom\dk64.z64" "rom\dk64-tag-anywhere-dev.z64" "rom\dk64-tag-anywhere-dev.bps"
pause