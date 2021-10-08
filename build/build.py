import os
import shutil
import gzip

ROMName = "./rom/dk64.z64"
newROMName = "./rom/dk64-tag-anywhere.z64"

file_dict = {
	"files": [
		{
			"name": "Static ASM Code",
			"start": 0x113F0,
			"compressed_size": 0xB15E4,
			"source_file": "StaticCode.bin",
			"output_file": "StaticCode.bin.gz",
			"output_file_is_compressed": True
		},
		{
			"name": "Nintendo Logo",
			"start": 0x1156AC4,
			"compressed_size": 0xA0C,
			"source_file": "bin/Thumb.bin",
			"do_not_extract": True
		},
		{
			"start": 0x1118420,
			"compressed_size": 0x37A,
			"source_file": "bin/Menu.bin",
			"name": "Menu Text",
		},
	]
}

print("DK64 Extractor")

with open(ROMName, "r+b") as fh:
	print("[1 / 2] - Unzipping files from ROM")
	for x in file_dict["files"]:
		if not "output_file" in x:
			x["output_file"] = x["source_file"]
		if not ("do_not_extract" in x and x['do_not_extract']):
			fh.seek(x["start"])
			byte_read = fh.read(x["compressed_size"])

			if os.path.exists(x["source_file"]):
				os.remove(x["source_file"])

			with open(x["source_file"], "wb") as fg:
				dec = gzip.decompress(byte_read)
				fg.write(dec)

import modules

if os.path.exists(newROMName):
	os.remove(newROMName)
shutil.copyfile(ROMName, newROMName)

with open(newROMName, "r+b") as fh:
	print("[2 / 2] - Writing modified compressed files to ROM")
	for x in file_dict["files"]:
		if os.path.exists(x["output_file"]):
			with open(x["output_file"], "rb") as fg:
				byte_read = fg.read()
				if "output_file_is_compressed" in x and x["output_file_is_compressed"]:
					compress = byte_read
				else:
					compress = gzip.compress(byte_read, compresslevel=9)
				if "compressed_size" in x and len(compress) > x["compressed_size"]:
					print(" - ERROR: " + x["output_file"] + " is too big, expected compressed size <= " + hex(x["compressed_size"]) + " but got size " + hex(len(compress)) + ")")
				else:
					print(" - Writing " + x['output_file'] + " to ROM, compressed size " + hex(len(compress)))
					fh.seek(x["start"])
					fh.write(compress)
					# Zero out timestamp in gzip header to make builds more deterministic
					fh.seek(x["start"] + 4)
					fh.write(bytearray([0, 0, 0, 0]))
		else:
			print(x["output_file"] + " does not exist")

for x in file_dict["files"]:
	if not ("do_not_delete" in x and x["do_not_delete"]):
		if not ("do_not_extract" in x and x["do_not_extract"]):
			if os.path.exists(x["output_file"]):
				os.remove(x["output_file"])
			if os.path.exists(x["source_file"]):
				os.remove(x["source_file"])

import generate_watch_file

exit()