import os

def updateOtherVars(lag_hook,gktimer_hook,kong_hook,flag_hook,pause_hook,speed_hook,graphicalhooks,comment_out):
	lines = [];
	lines.append("// Lag Hook - NOTE: UPDATE ON EVERY REVISION")
	lines.append("LI 	a1, " + hex(lag_hook))
	lines.append("SW 	a1, 0x80600674")
	lines.append("SW 	r0, 0x80600678")

	lines.append("// GK Timer Hook - NOTE: UPDATE ON EVERY REVISION")
	lines.append("LI 	a1, " + hex(gktimer_hook))
	lines.append("SW 	a1, 0x80646074")
	lines.append("SW 	r0, 0x80646078")

	lines.append("// Kong Hook - NOTE: UPDATE ON EVERY REVISION")
	lines.append("LI 	a1, " + hex(kong_hook))
	lines.append("SW 	a1, 0x806F3750")
	lines.append("SW 	r0, 0x806F3754")

	lines.append("// Flag Hook - NOTE: UPDATE ON EVERY REVISION")
	lines.append("LI 	a1, " + hex(flag_hook))
	lines.append("SW 	a1, 0x8073129C")
	lines.append("SW 	r0, 0x807312A0")

	lines.append("// Pause Menu Hook - NOTE: UPDATE ON EVERY REVISION")
	lines.append("LI 	a1, " + hex(pause_hook))
	lines.append("SW 	a1, 0x805FC890")
	lines.append("SW 	r0, 0x805FC894")

	lines.append("// Speed Hook - NOTE: UPDATE ON EVERY REVISION")
	lines.append("LI 	a1, " + hex(speed_hook))
	lines.append("SW 	a1, 0x80665354")
	lines.append("SW 	r0, 0x80665358")

	lines.append("// Graphical Overlay Space Expansion - NOTE: UPDATE ON EVERY REVISION")
	lines.append("LI 	a1, " + hex(graphicalhooks[0]))
	lines.append("SW 	a1, 0x8068C374")
	lines.append("LI 	a1, " + hex(graphicalhooks[1]))
	lines.append("SW 	a1, 0x8068C378")
	lines.append("LI 	a1, " + hex(graphicalhooks[2]))
	lines.append("SW 	a1, 0x8068C310")
	lines.append("LI 	a1, " + hex(graphicalhooks[3]))
	lines.append("SW 	a1, 0x8068C314")
	lines.append("LI 	a1, " + hex(graphicalhooks[4]))
	lines.append("SW 	a1, 0x8068C240")
	lines.append("LI 	a1, " + hex(graphicalhooks[5]))
	lines.append("SW 	a1, 0x8068C244")
	lines.append("LI 	a1, " + hex(graphicalhooks[6]))
	lines.append("SW 	a1, 0x8068C364")

	if os.path.exists("./../Source/Features/OtherVars.asm"):
		os.remove("./../Source/Features/OtherVars.asm")
	with open("./../Source/Features/OtherVars.asm","a") as fh:
		for e in lines:
			complete_line = ""
			if comment_out:
				complete_line = "// "
			fh.write(complete_line + e + "\n")