import os
import shutil
import gzip
import zlib
import subprocess

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
		"start": 0x112F54E,
		"compressed_size": 0x32FE,
		"source_file": "bin/Title.png",
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
	print("[1 / 2] - Unzipping files from ROM")
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

import modules

with open(newROMName, "r+b") as fh:
	print("[2 / 2] - Writing modified compressed files to ROM")
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
						# Chop off footer
						outputFile.truncate(len(outputFile.read()) - 8)

		if os.path.exists(x["output_file"]):
			with open(x["output_file"], "rb") as fg:
				byte_read = fg.read()
				if "use_external_gzip" in x and x["use_external_gzip"]:
					compress = byte_read
				elif "use_zlib" in x and x["use_zlib"]:
					compressor = zlib.compressobj(zlib.Z_BEST_COMPRESSION, zlib.DEFLATED, 25)
					compress = compressor.compress(byte_read)
					compress += compressor.flush()
				else:
					compress = gzip.compress(byte_read, compresslevel=9)

				if "compressed_size" in x and len(compress) > x["compressed_size"]:
					print(" - ERROR: " + x["output_file"] + " is too big, expected compressed size <= " + hex(x["compressed_size"]) + " but got size " + hex(len(compress)) + ")")
				else:
					print(" - Writing " + x['output_file'] + " to ROM, compressed size " + hex(len(compress)))
					fh.seek(x["start"])
					fh.write(compress)
					# Zero out timestamp in gzip header to make builds deterministic
					fh.seek(x["start"] + 4)
					fh.write(bytearray([0, 0, 0, 0]))
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

import generate_watch_file

exit()