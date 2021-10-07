@echo off
echo Started: %date% %time%

mkdir obj
python build\compile.py
move *.o obj\

python build\build.py
build\armips.exe asm\main.asm
del rom\dk64-tag-anywhere-python.z64
rmdir /s /q .\obj
build\n64crc.exe rom\dk64-tag-anywhere-dev.z64
echo Completed: %date% %time%
pause