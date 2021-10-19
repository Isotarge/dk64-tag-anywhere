def patchStaticCode(filename):
	with open(filename, "r+b") as fh:
		# RDRAM Address - 0x5FB300 = ROM address
		fh.seek(0x15212)
		fh.write(bytearray([0x80,0x5D])) # Heap Shrink: lui t5, 0x805d
		# fh.seek(0x119247)
		# fh.write(bytearray([0x22])) # File Start Map
		# fh.seek(0x11925B)
		# fh.write(bytearray([0x0])) # File Start Exit
		# Enable setup files larger than originals
		# fh.seek(0x8D690)
		# fh.write(bytearray([0x24, 0x14, 0x00, 0x01]))
		# fh.seek(0x369B4)
		# fh.write(bytearray([0x10, 0x00, 0x00, 0x28]))
		# fh.seek(0x369B8)
		# fh.write(bytearray([0x00, 0x00, 0x00, 0x00]))
		# fh.seek(0x369BC)
		# fh.write(bytearray([0x00, 0x00, 0x00, 0x00]))