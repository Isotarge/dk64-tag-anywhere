import os
import subprocess
import shutil

open('./asm/objects.asm', 'w').close()

with open('./asm/objects.asm', 'a') as obj_asm:
	# traverse whole directory
	for root, dirs, files in os.walk(r'src'):
		# select file name
		for file in files:
			# check the extension of files
			if file.endswith('.c'):
				# print whole path of files
				_o = os.path.join(root, file).replace("/","_").replace("\\","_").replace(".c", ".o")
				print(os.path.join(root, file))
				obj_asm.write(".importobj \"obj/" + _o + "\"\n")
				cmd = ["mips64-elf-gcc", "-Wall", "-O1", "-mtune=vr4300", "-march=vr4300", "-mabi=32", "-fomit-frame-pointer", "-G0", "-c", os.path.join(root, file)]
				p = subprocess.Popen(cmd)
				p.wait()
				shutil.move("./" + file.replace(".c",".o"), "obj/" + _o)