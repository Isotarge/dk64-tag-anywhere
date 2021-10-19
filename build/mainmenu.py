def patchMainMenu(filename):
	with open(filename, "r+b") as fh:
		fh.seek(0x70E)
		fh.write("SPEED MODE".encode("ascii")) # Originally: STORY SKIP