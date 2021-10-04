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
python cleanup.py
n64crc "rom/dk64-tag-anywhere-dev.z64"
echo Completed: %date% %time%
pause