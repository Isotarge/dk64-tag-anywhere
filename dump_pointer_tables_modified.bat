@echo off
echo Started: %date% %time%
python build\dump_pointer_tables_modified.py
echo Completed: %date% %time%