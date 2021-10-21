import os
import shutil
import gzip
import zlib
import subprocess

# Infrastructure for recomputing DK64 global pointer tables
from recompute_pointer_table import dumpPointerTableDetails, replaceROMFile, writeModifiedPointerTablesToROM, parsePointerTables, getFileInfo
from extract_maps import extractMaps

# Patcher functions for the extracted files
from staticcode import patchStaticCode
from mainmenu import patchMainMenu

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
		"patcher": patchStaticCode
	},
	{
		"name": "Nintendo Logo",
		"start": 0x1156AC4,
		"source_file": "bin/Nintendo.png",
		#"source_file": "bin/Nintendo_TJ.png",
		#"source_file": "bin/Nintendo_Adam.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "Dolby Logo",
		"start": 0x116818C,
		"source_file": "bin/Dolby.png",
		"texture_format": "i4",
	},
	{
		"name": "Title Screen",
		"start": 0x112F54E,
		#"source_file": "bin/Title.png",
		"source_file": "bin/Title_Bigger.png",
		"texture_format": "rgba5551",
		"use_zlib": True,
	},
	{
		"name": "Menu Text",
		"start": 0x1118420,
		"source_file": "bin/Menu.bin",
		"patcher": patchMainMenu
	},
	# {
	# 	"name": "Custom Map Setup",
	# 	"start": 0xD0EBE4, # Test Map
	# 	#"start": 0xD1DF04, # Aztec
	# 	"source_file": "bin/CustomSetup.bin",
	# 	"do_not_extract": True,
	# }
]

print("DK64 Extractor")

with open(ROMName, "r+b") as fh:
	print("[1 / 6] - Parsing pointer tables")
	parsePointerTables(fh)

	print("[2 / 6] - Extracting files from ROM")
	#extractMaps()

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
		
		if not ("do_not_extract" in x and x["do_not_extract"]):
			byte_read = bytes()
			file_info = getFileInfo(x["start"])
			if file_info:
				x["compressed_size"] = len(file_info["data"])
				byte_read = file_info["data"]
			else:
				fh.seek(x["start"])
				byte_read = fh.read(x["compressed_size"])

			if not ("do_not_delete_source" in x and x["do_not_delete_source"]):	
				if os.path.exists(x["source_file"]):
					os.remove(x["source_file"])

				with open(x["source_file"], "wb") as fg:
					dec = gzip.decompress(byte_read)
					fg.write(dec)

print("[3 / 6] - Patching Extracted Files")
for x in file_dict:
	if "patcher" in x and callable(x["patcher"]):
		print(" - Running patcher for " + x["source_file"])
		x["patcher"](x["source_file"])

with open(newROMName, "r+b") as fh:
	print("[4 / 6] - Writing patched files to ROM")
	for x in file_dict:
		if "texture_format" in x:
			if x["texture_format"] in ["rgba5551", "i4"]:
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
			uncompressed_size = 0
			with open(x["output_file"], "rb") as fg:
				byte_read = fg.read()
				uncompressed_size = len(byte_read)

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

			print(" - Writing " + x["output_file"] + " (" + hex(len(compress)) + ") to ROM")
			replaceROMFile(fh, x["start"], compress, uncompressed_size)
		else:
			print(x["output_file"] + " does not exist")

		# Cleanup temporary files
		if not ("do_not_delete" in x and x["do_not_delete"]):
			if not ("do_not_delete_output" in x and x["do_not_delete_output"]):
				if os.path.exists(x["output_file"]) and x["output_file"] != x["source_file"]:
					os.remove(x["output_file"])
			if not ("do_not_delete_source" in x and x["do_not_delete_source"]):
				if os.path.exists(x["source_file"]):
					os.remove(x["source_file"])

	print("[5 / 6] - Writing recomputed pointer tables to ROM")
	writeModifiedPointerTablesToROM(fh)

	print("[6 / 6] - Dumping details of all pointer tables to build.log")
	dumpPointerTableDetails()

import generate_watch_file

exit()