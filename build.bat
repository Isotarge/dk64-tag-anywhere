@echo off
title Cranky's Lab Build System
python build\build.py
python build\dump_pointer_tables_vanilla.py
pause