import os
import shutil
import gzip

ROMName = "./rom/dk64.z64"
newROMName = "dk64-tag-anywhere.z64"

file_dict = {
	"files": [
		{
			"start": 0x113F0,
			"compressed_size": 0xB15E4, # GEDECOMPRESS - B15DC, PYTHON - B17A8, FINALISE ROM - B15E0
			"source_file": "StaticCode.bin",
			"output_file": "StaticCode.bin.gz",
			"output_file_is_compressed": True,
			"name": "Static ASM Code"
		},
	]
}

print("Tag Anywhere Extractor")
print("[0 / 2] - Analyzing ROM")

with open(ROMName, "r+b") as fh:
	print("[1 / 2] - Unzipping files from ROM")
	for x in file_dict["files"]:
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
				if "output_file_is_compressed" in x:
					compress = byte_read
				else:
					compress = gzip.compress(byte_read, compresslevel=9)
				if "compressed_size" in x and len(compress) > x["compressed_size"]:
					print("ERROR: " + x["output_file"] + " is too big, expected compressed size <= " + hex(x["compressed_size"]) + " but got size " + hex(len(compress)) + ")")
				fh.seek(x["start"])
				fh.write(compress)
		else:
			print(x["output_file"] + " does not exist")

for x in file_dict["files"]:
	if os.path.exists(x["output_file"]):
		os.remove(x["output_file"])
	if os.path.exists(x["source_file"]):
		os.remove(x["source_file"])

# crc patch
with open(newROMName, "r+b") as fh:
	fh.seek(0x3154)
	fh.write(bytearray([0, 0, 0, 0]))

if os.path.exists(newROMName):
	shutil.copyfile(newROMName, "./rom/dk64-tag-anywhere-python.z64")
	os.remove(newROMName)

import generate_watch_file

exit()