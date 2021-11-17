def patchMainMenu(filename):
	with open(filename, "r+b") as fh:
		fh.seek(0x70E)
		fh.write("SPEED MODE".encode("ascii")) # Originally: STORY SKIP

def patchDolbyText(filename):
	with open(filename, "r+b") as fh:
		fh.seek(0x30)
		fh.write("            ".encode("ascii")) # Originally: PRESENTED IN
		fh.seek(0x3C)
		fh.write("  WITH HELP FROM THE DK64 KREW   ".encode("ascii")) # Originally: DOLBY AND THE DOUBLE-D SYMBOL ARE
		fh.seek(0x5D)
		fh.write("IT TAKES A VILLAGE TO FREE A KONG".encode("ascii")) # Originally: TRADEMARKS OF DOLBY LABORATORIES.