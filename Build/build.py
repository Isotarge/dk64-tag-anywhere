import os
import shutil
import gzip

file_dict = {
	"files": [
		{
			"start": 0x113F0,
			"compressed_size": 0xF064C, # GEDECOMPRESS - B15DC, PYTHON - B17A8, FINALISE ROM - B15E0
			"source_file": "StaticCode.bin",
			"output_file": "StaticCode_Copy.bin.gz",
			"name": "Static ASM Code"
		},
	]
}

print("Tag Anywhere Extractor")
print("[0 / 2] - Analyzing ROM")
ROMName = "./rom/dk64.z64"
with open(ROMName, "r+b") as fh:
	print("[1 / 2] - Unzipping files from ROM")
	for x in file_dict["files"]:
		fh.seek(x["start"])
		byte_read = fh.read(x["compressed_size"])
		binName = x["source_file"]

		if os.path.exists(binName):
			os.remove(binName)

		with open(binName, "wb") as fg:
			dec = gzip.decompress(byte_read)
			if x["source_file"] == "StaticCode.bin":
				fg.write(dec[:0x149160])
			else:
				fg.write(dec)

import modules
newROMName = "dk64-tag-anywhere.z64"
if os.path.exists(newROMName):
	os.remove(newROMName)
shutil.copyfile(ROMName, newROMName)

with open(newROMName, "r+b") as fh:
	print("[2 / 2] - Writing modified compressed files to ROM")
	for x in file_dict["files"]:
		binName = x["output_file"]
		if os.path.exists(binName):
			with open(binName, "rb") as fg:
				byte_read = fg.read()
				if x["source_file"] != "StaticCode.bin":
					compress = gzip.compress(byte_read, compresslevel=9)
				else:
					compress = byte_read
					if (len(compress) > 0xB15E2): # Proper limit is 0xB15E0
						print("ERROR: STATIC CODE BIN IS TOO BIG (" + hex(len(compress)) + ")")
				fh.seek(x["start"])
				fh.write(compress)
		else:
			print(x["output_file"] + " does not exist")

for x in file_dict["files"]:
	if os.path.exists(x["output_file"]):
		os.remove(x["output_file"])
	if os.path.exists(x["source_file"]):
		os.remove(x["source_file"])
	if os.path.exists("StaticCode_Copy.bin"):
		os.remove("StaticCode_Copy.bin")

# crc patch
with open(newROMName, "r+b") as fh:
	fh.seek(0x3154)
	fh.write(bytearray([0, 0, 0, 0]))

if os.path.exists("dk64-tag-anywhere.z64"):
	shutil.copyfile("dk64-tag-anywhere.z64", "./rom/dk64-tag-anywhere-python.z64")
	os.remove("dk64-tag-anywhere.z64")

exit()