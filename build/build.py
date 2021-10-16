import os
import shutil
import gzip
import zlib
import subprocess
from recompute_pointer_table import dumpPointerTableDetails, replaceROMFile, writeModifiedPointerTablesToROM, parsePointerTables

import time
start = time.process_time()

ROMName = "./rom/dk64.z64"
newROMName = "./rom/dk64-tag-anywhere.z64"

if os.path.exists(newROMName):
	os.remove(newROMName)
shutil.copyfile(ROMName, newROMName)

file_dict = [
	{
		"name": "Static ASM Code",
		"start": 0x113F0,
		"compressed_size": 0xB15E4,
		"source_file": "bin/StaticCode.bin",
		"use_external_gzip": True,
	},
	{
		"name": "Nintendo Logo",
		"start": 0x1156AC4,
		"compressed_size": 0xA0C,
		"source_file": "bin/Nintendo.png",
		#"source_file": "bin/Nintendo_TJ.png",
		#"source_file": "bin/Nintendo_Adam.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "Dolby Logo",
		"start": 0x116818C,
		"compressed_size": 0x880,
		"source_file": "bin/Dolby.png",
		"texture_format": "i4",
	},
	{
		"name": "Title Screen",
		"start": 0x112F54E, # - 0x101C50 = 0x102D8FE
		"compressed_size": 0x32FE,
		"source_file": "bin/Title.png",
		#"source_file": "bin/Title_Bigger.png",
		"texture_format": "rgba5551",
		"use_zlib": True,
	},
	{
		"name": "Menu Text",
		"start": 0x1118420,
		"compressed_size": 0x37A,
		"source_file": "bin/Menu.bin",
	},
]

print("DK64 Extractor")

with open(ROMName, "r+b") as fh:
	print("[1 / 4] - Unzipping files from ROM")
	for x in file_dict:
		if "texture_format" in x:
			x["do_not_extract"] = True
			x["output_file"] = x["source_file"].replace(".png", "." + x["texture_format"])

		if not "output_file" in x:
			x["output_file"] = x["source_file"]

		if "use_external_gzip" in x and x["use_external_gzip"]:
			x["output_file"] = x["output_file"] + ".gz"

		if "do_not_extract" in x and x["do_not_extract"]:
			x["do_not_delete_source"] = True
		
		if not ("do_not_extract" in x and x['do_not_extract']):
			fh.seek(x["start"])
			byte_read = fh.read(x["compressed_size"])

			if os.path.exists(x["source_file"]):
				os.remove(x["source_file"])

			with open(x["source_file"], "wb") as fg:
				dec = gzip.decompress(byte_read)
				fg.write(dec)

print("[2 / 5] - Modifying extracted files")
import modules

with open(newROMName, "r+b") as fh:
	print("[3 / 5] - Parsing Pointer Tables")
	#parsePointerTables(fh)

	print("[4 / 5] - Writing modified files to ROM")
	for x in file_dict:
		if "texture_format" in x:
			if x["texture_format"] == "rgba5551":
				result = subprocess.check_output(["./build/n64tex.exe", x["texture_format"], x["source_file"]])
			elif x["texture_format"] == "i4":
				result = subprocess.check_output(["./build/n64tex.exe", x["texture_format"], x["source_file"]])
			else:
				print(" - ERROR: Unsupported texture format " + x["texture_format"])

		if "use_external_gzip" in x and x["use_external_gzip"]:
			if os.path.exists(x["source_file"]):
				result = subprocess.check_output(["./build/gzip.exe", "-f", "-n", "-q", "-9", x["output_file"].replace(".gz", "")])
				if os.path.exists(x["output_file"]):
					with open(x["output_file"],"r+b") as outputFile:
						# Chop off gzip footer
						outputFile.truncate(len(outputFile.read()) - 8)

		if os.path.exists(x["output_file"]):
			byte_read = bytes()
			with open(x["output_file"], "rb") as fg:
				byte_read = fg.read()

			if "use_external_gzip" in x and x["use_external_gzip"]:
				compress = byte_read
				compress = bytearray(compress)
			elif "use_zlib" in x and x["use_zlib"]:
				compressor = zlib.compressobj(zlib.Z_BEST_COMPRESSION, zlib.DEFLATED, 25)
				compress = compressor.compress(byte_read)
				compress += compressor.flush()
				compress = bytearray(compress)
				# Zero out timestamp in gzip header to make builds deterministic
				compress[4] = 0
				compress[5] = 0
				compress[6] = 0
				compress[7] = 0
			else:
				compress = bytearray(gzip.compress(byte_read, compresslevel=9))
				# Zero out timestamp in gzip header to make builds deterministic
				compress[4] = 0
				compress[5] = 0
				compress[6] = 0
				compress[7] = 0

			if "compressed_size" in x and len(compress) > x["compressed_size"]:
				print(" - ERROR: " + x["output_file"] + " is too big, expected compressed size <= " + hex(x["compressed_size"]) + " but got size " + hex(len(compress)) + ")")
				#replaceROMFile(x["start"], compress)
			else:
				print(" - Writing " + x['output_file'] + " to ROM, compressed size " + hex(len(compress)))
				fh.seek(x["start"])
				fh.write(compress)
		else:
			print(x["output_file"] + " does not exist")

		# Cleanup temporary files
		if not ("do_not_delete" in x and x["do_not_delete"]):
			if not ("do_not_delete_output" in x and x["do_not_delete_output"]):
				if os.path.exists(x["output_file"]):
					os.remove(x["output_file"])
			if not ("do_not_delete_source" in x and x["do_not_delete_source"]):
				if os.path.exists(x["source_file"]):
					os.remove(x["source_file"])

	print("[5 / 5] - Writing modified pointer tables to ROM")
	#writeModifiedPointerTablesToROM(fh)

	#print("[6 / 5] - Dumping details of all pointer tables")
	#dumpPointerTableDetails()

import generate_watch_file

#print("TIME TAKEN: " + str(time.process_time() - start))

exit()