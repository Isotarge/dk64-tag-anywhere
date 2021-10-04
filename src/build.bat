@echo off
mkdir obj
echo Started: %date% %time%

python compile.py
move *.o obj/

armips asm/jump_list.asm
cd "..\Build\"
python build.py
cd "..\src\"
armips asm/main.asm
del ".\rom\dk64-tag-anywhere-python.z64"
del ".\rom\dk64-tag-anywhere-temp.z64"
rmdir /s /q ".\obj"
n64crc "rom/dk64-tag-anywhere-dev.z64"
echo Completed: %date% %time%
pause