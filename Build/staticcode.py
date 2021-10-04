import os
import shutil
from compressFile import compressGZipFile

StaticCodeFile = "StaticCode_Copy.bin"

if os.path.exists(StaticCodeFile):
  os.remove(StaticCodeFile)

shutil.copyfile("StaticCode.bin", StaticCodeFile)

with open(StaticCodeFile, "r+b") as fh:
	# RDRAM Address - 0x5FB300 = ROM address
	fh.seek(0xE64)
	fh.write(bytearray([0x8,0x0,0x37,0xA2])) #Code Hook
	fh.seek(0x15212)
	fh.write(bytearray([0x80,0x5D])) # Heap Shrink
	# fh.seek(0x119247)
	# fh.write(bytearray([0x22])) # File Start Map
	# fh.seek(0x11925B)
	# fh.write(bytearray([0x0])) # File Start Exit

compressGZipFile("StaticCode_Copy.bin", "StaticCode_Copy.bin.gz", False)