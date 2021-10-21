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
		# fh.seek(0x8D690) # RDRAM 80688990
		# fh.write(bytearray([0x24, 0x14, 0x00, 0x01])) # ADDIU $s4 $zero 0x0001
		# fh.seek(0x369B4) # RDRAM 80631CB4
		# fh.write(bytearray([0x10, 0x00, 0x00, 0x28])) # BEQ $zero $zero 0x0028
		# fh.seek(0x369B8) # RDRAM 80631CB8
		# fh.write(bytearray([0x00, 0x00, 0x00, 0x00])) # NOP
		# fh.seek(0x369BC) # RDRAM 80631CBC
		# fh.write(bytearray([0x00, 0x00, 0x00, 0x00])) # NOP
		# Load race overlay when no overlay specified
		# fh.seek(0x15108) # RDRAM 80631048
		# fh.write(bytearray([0x24, 0x09, 0x00, 0x05])) # ADDIU $t1 $zero 0x0005