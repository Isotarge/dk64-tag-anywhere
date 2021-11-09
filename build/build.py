import os
import shutil
import gzip
import zlib
import subprocess

print("Compiling C Code")
with open('./asm/objects.asm', 'w') as obj_asm:
	for root, dirs, files in os.walk(r'src'):
		for file in files:
			if file.endswith('.c'):
				_o = os.path.join(root, file).replace("/","_").replace("\\","_").replace(".c", ".o")
				print(os.path.join(root, file))
				obj_asm.write(".importobj \"obj/" + _o + "\"\n")
				cmd = ["mips64-elf-gcc", "-Wall", "-O1", "-mtune=vr4300", "-march=vr4300", "-mabi=32", "-fomit-frame-pointer", "-G0", "-c", os.path.join(root, file)]
				subprocess.Popen(cmd).wait()
				shutil.move("./" + file.replace(".c",".o"), "obj/" + _o)
print()

# Infrastructure for recomputing DK64 global pointer tables
from map_names import maps
from recompute_pointer_table import pointer_tables, dumpPointerTableDetails, replaceROMFile, writeModifiedPointerTablesToROM, parsePointerTables, getFileInfo, make_safe_filename
from recompute_overlays import isROMAddressOverlay, readOverlayOriginalData, replaceOverlayData, writeModifiedOverlaysToROM

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
		"pointer_table_index": 14,
		"file_index": 94,
		"source_file": "bin/Nintendo.png",
		#"source_file": "bin/Nintendo_TJ.png",
		#"source_file": "bin/Nintendo_Adam.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "Dolby Logo",
		"pointer_table_index": 14,
		"file_index": 176,
		"source_file": "bin/Dolby.png",
		"texture_format": "i4",
	},
	{
		"name": "Title Screen",
		"pointer_table_index": 14,
		"file_index": 44,
		"source_file": "bin/Title.png",
		"texture_format": "rgba5551",
		"use_zlib": True,
	},
	{
		"name": "Menu Text",
		"pointer_table_index": 12,
		"file_index": 37,
		"source_file": "bin/Menu.bin",
		"patcher": patchMainMenu
	},
	# {
	# 	"name": "Chunky's Vest Back (Green & Yellow)",
	# 	"pointer_table_index": 25,
	# 	"file_index": 3769,
	# 	"do_not_delete": True,
	# 	"do_not_extract": True,
	# 	"source_file": "bin/ChunkyVest.bin",
	# 	# "texture_format": "rgba5551",
	# },
]

map_replacements = [
	# {
	# 	"name": "Test Map",
	# 	"map_index": 0,
	# 	# "map_folder": "maps/208 - Bloopers_Ending/"
	# 	# "map_folder": "maps/38 - Angry_Aztec/"
	# 	"map_folder": "maps/path_test/"
	# },
	# {
	# 	"name": "Fairy Island Exit Test",
	# 	"map_index": 189,
	# 	"map_folder": "maps/exit_test/"
	# },
	# {
	# 	"name": "Japes Exit Test",
	# 	"map_index": 7,
	# 	"map_folder": "maps/exit_test/"
	# },
]

# Test all map replacements at once
# TODO: Why does this crash with any combination of floors||walls||geometry
# for mapIndex, mapName in enumerate(maps):
# 	mapPath = "maps/" + str(mapIndex) + " - " + make_safe_filename(mapName) + "/"
# 	map_replacements.append({
# 		"name": mapName,
# 		"map_index": mapIndex,
# 		"map_folder": mapPath,
# 	})

print("DK64 Extractor")

with open(ROMName, "rb") as fh:
	print("[1 / 7] - Parsing pointer tables")
	parsePointerTables(fh)
	readOverlayOriginalData(fh)

	for x in map_replacements:
		print(" - Processing map replacement " + x["name"])
		if os.path.exists(x["map_folder"]):
			for y in pointer_tables:
				if "do_not_reimport" in y and y["do_not_reimport"]:
					continue
				if not "encoded_filename" in y:
					continue

				# Convert decoded_filename to encoded_filename using the encoder function
				# Eg. exits.json to exits.bin
				if "encoder" in y and callable(y["encoder"]):
					if "decoded_filename" in y and os.path.exists(x["map_folder"] + y["decoded_filename"]):
						y["encoder"](x["map_folder"] + y["decoded_filename"], x["map_folder"] + y["encoded_filename"])

				if os.path.exists(x["map_folder"] + y["encoded_filename"]):
					print("  - Found " + x["map_folder"] + y["encoded_filename"])
					file_dict.append({
						"name": x["name"] + y["name"],
						"pointer_table_index": y["index"],
						"file_index": x["map_index"],
						"source_file": x["map_folder"] + y["encoded_filename"],
						"do_not_extract": True,
						"do_not_compress": "do_not_compress" in y and y["do_not_compress"],
					})

	print("[2 / 7] - Extracting files from ROM")
	for x in file_dict:
		# N64Tex conversions do not need to be extracted to disk from ROM
		if "texture_format" in x:
			x["do_not_extract"] = True
			x["output_file"] = x["source_file"].replace(".png", "." + x["texture_format"])

		if not "output_file" in x:
			x["output_file"] = x["source_file"]

		# gzip.exe appends .gz to the filename, we'll do the same
		if "use_external_gzip" in x and x["use_external_gzip"]:
			x["output_file"] = x["output_file"] + ".gz"

		# If we're not extracting the file to disk, we're using a custom .bin that shoudn't be deleted
		if "do_not_extract" in x and x["do_not_extract"]:
			x["do_not_delete_source"] = True

		# Extract the compressed file from ROM
		if not ("do_not_extract" in x and x["do_not_extract"]):
			byte_read = bytes()
			if "pointer_table_index" in x and "file_index" in x:
				file_info = getFileInfo(x["pointer_table_index"], x["file_index"])
				if file_info:
					x["start"] = file_info["new_absolute_address"]
					x["compressed_size"] = len(file_info["data"])

			fh.seek(x["start"])
			byte_read = fh.read(x["compressed_size"])

			if not ("do_not_delete_source" in x and x["do_not_delete_source"]):
				if os.path.exists(x["source_file"]):
					os.remove(x["source_file"])

				with open(x["source_file"], "wb") as fg:
					dec = gzip.decompress(byte_read)
					fg.write(dec)

print("[3 / 7] - Patching Extracted Files")
for x in file_dict:
	if "patcher" in x and callable(x["patcher"]):
		print(" - Running patcher for " + x["source_file"])
		x["patcher"](x["source_file"])

with open(newROMName, "r+b") as fh:
	print("[4 / 7] - Writing patched files to ROM")
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

			if "do_not_compress" in x and x["do_not_compress"]:
				compress = bytearray(byte_read)
			elif "use_external_gzip" in x and x["use_external_gzip"]:
				compress = bytearray(byte_read)
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
			if "pointer_table_index" in x and "file_index" in x:
				# More complicated write, update the pointer tables to point to the new data
				replaceROMFile(x["pointer_table_index"], x["file_index"], compress, uncompressed_size)
			elif "start" in x:
				if isROMAddressOverlay(x["start"]):
					replaceOverlayData(x["start"], compress)
				else:
					# Simply write the bytes at the absolute address in ROM specified by x["start"]
					fh.seek(x["start"])
					fh.write(compress)
			else:
				print("  - WARNING: Can't find address information in file_dict entry to write " + x["output_file"] + " (" + hex(len(compress)) + ") to ROM")
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

	print("[5 / 7] - Writing recomputed pointer tables to ROM")
	writeModifiedPointerTablesToROM(fh)
	writeModifiedOverlaysToROM(fh)

	print("[6 / 7] - Dumping details of all pointer tables to build.log")
	dumpPointerTableDetails("build.log", fh)

print("[7 / 7] - Generating BizHawk RAM watch")
import generate_watch_file

exit()