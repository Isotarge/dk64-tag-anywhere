def patchStaticCode(filename):
	with open(filename, "r+b") as fh:
		# RDRAM Address - 0x5FB300 = ROM address

		# Heap Shrink
		fh.seek(0x15212)
		fh.write(bytearray([0x80,0x5D])) # Heap Shrink: lui t5, 0x805d

		# Starting Map & Exit
		# fh.seek(0x119247)
		# fh.write(bytearray([0x22])) # File Start Map
		# fh.seek(0x11925B)
		# fh.write(bytearray([0x0])) # File Start Exit

		# Load race overlay when no overlay specified
		# fh.seek(0x15108) # RDRAM 80631048
		# fh.write(bytearray([0x24, 0x09, 0x00, 0x05])) # ADDIU $t1 $zero 0x0005

		# Increase Object Model 2 Per Map Count
		fh.seek(0x36D24)
		fh.write(bytearray([0x24, 0x0a, 0x02, 0x12])) # li $t2, 465 (original, Jungle Japes)
		fh.seek(0x36D34)
		fh.write(bytearray([0x24, 0x0b, 0x02, 0x12])) # li $t3, 450 (original, All Other Maps)
		fh.seek(0x36CF4)
		fh.write(bytearray([0x24, 0x19, 0x02, 0x12])) # li $t9, 500 (original, Frantic Factory)
		fh.seek(0x36D14)
		fh.write(bytearray([0x24, 0x09, 0x02, 0x12])) # li $t1, 485 (original, Gloomy Galleon)
		fh.seek(0x36D04)
		fh.write(bytearray([0x24, 0x08, 0x02, 0x12])) # li $t0, 500 (original, Angry Aztec)
		fh.seek(0x36CE4)
		fh.write(bytearray([0x24, 0x18, 0x02, 0x12])) # li $t8, 530 (original, Fungi Forest)