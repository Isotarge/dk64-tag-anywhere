import subprocess
import os
import shutil
import gzip
from compressFile import compressGZipFile

StaticCodeFile = "StaticCode_Copy.bin"

if os.path.exists(StaticCodeFile):
  os.remove(StaticCodeFile)

shutil.copyfile("StaticCode.bin", StaticCodeFile);

jump_data_start = 0x1FFF000
with open("./../src/rom/dk64-tag-anywhere-temp.z64", "rb") as fg:
	fg.seek(jump_data_start + 0x00)
	patch_gktimer_hook = fg.read(8)
	fg.seek(jump_data_start + 0x8)
	patch_lag_hook = fg.read(0x8)
	fg.seek(jump_data_start + 0x10)
	patch_save_hook = fg.read(0x8)
	fg.seek(jump_data_start + 0x18)
	patch_sprite_hook = fg.read(0x8)
	fg.seek(jump_data_start + 0x20)
	patch_speed_hook = fg.read(0x8)

with open(StaticCodeFile, "r+b") as fh:
	# RDRAM Address - 0x5FB300 = ROM address
	fh.seek(0xE64)
	fh.write(bytearray([0x8,0x0,0x37,0xA2])) #Code Hook
	fh.seek(0x15212)
	fh.write(bytearray([0x80,0x5D])) # Heap Shrink
	fh.seek(0x119247)
	fh.write(bytearray([0x22])) # File Start Map
	fh.seek(0x11925B)
	fh.write(bytearray([0x0])) # File Start Exit
	# Graphical overlay
	fh.seek(0x91074)
	fh.write(bytearray([0x3c,0x18,0x80,0x80,0x27,0x18,0xFA,0x00]))
	fh.seek(0x91010)
	fh.write(bytearray([0x3c,0x06,0x80,0x80,0x24,0xC6,0xFA,0x00]))
	fh.seek(0x90F40)
	fh.write(bytearray([0x3c,0x12,0x80,0x80,0x26,0x52,0xFA,0x00]))
	fh.seek(0x91064)
	fh.write(bytearray([0x28,0x41,0x00,0x20]))
	# Kong Colouring
	fh.seek(0x8F32F)
	fh.write(bytearray([0x00]))
	fh.seek(0x8F150)
	fh.write(bytearray([0x00,0x00,0x00,0x00]))
	fh.seek(0x8F158)
	fh.write(bytearray([0x00,0x00,0x00,0x00]))
	# GK Timer Hook
	fh.seek(0x4AD74)
	fh.write(patch_gktimer_hook)
	# Lag Hook
	fh.seek(0x5374)
	fh.write(patch_lag_hook)
	# Save Hook
	fh.seek(0x12BCC)
	fh.write(patch_save_hook)
	# EEPROM Patch
	fh.seek(0x12288)
	fh.write(bytearray([0x0,0x0,0x0,0x0])) # Prevents overwrite of other data
	# Sprite Hook
	fh.seek(0xB04D0)
	fh.write(patch_sprite_hook)
	# Speed hook
	fh.seek(0x6A054)
	fh.write(patch_speed_hook)

compressGZipFile("StaticCode_Copy.bin","StaticCode_Copy.bin.gz",False)