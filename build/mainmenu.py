with open("bin/Menu.bin", "r+b") as fh:
	fh.seek(0x70E)
	fh.write("SPEED MODE".encode("ascii")) # Originally: STORY SKIP