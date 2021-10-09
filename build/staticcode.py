with open("bin/StaticCode.bin", "r+b") as fh:
	# RDRAM Address - 0x5FB300 = ROM address
	fh.seek(0x15212)
	fh.write(bytearray([0x80,0x5D])) # Heap Shrink: lui t5, 0x805d
	# fh.seek(0x119247)
	# fh.write(bytearray([0x22])) # File Start Map
	# fh.seek(0x11925B)
	# fh.write(bytearray([0x0])) # File Start Exit