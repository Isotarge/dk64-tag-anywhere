@echo off
echo Started: %date% %time%
python build\extract_maps.py
echo Completed: %date% %time%
pause
