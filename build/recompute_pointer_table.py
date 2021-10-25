import hashlib
from map_names import maps
from typing import BinaryIO

import json

# The address of the next available byte of free space in ROM
# used when appending files to the end of the ROM
#next_available_free_space = 0x1FED020
next_available_free_space = 0x2000000

#num_tables = 27
num_tables = 32
pointer_tables = []
main_pointer_table_offset = 0x101C50

# These will be indexed by pointer table index then by SHA1 hash of the data
pointer_table_files = []
for i in range(num_tables):
	pointer_table_files.append({})

pointer_table_names = [
	"Music MIDI",
	"Map Geometry",
	"Map Walls",
	"Map Floors",
	"Object Model 2 Geometry",
	"Actor Geometry",
	"Unknown 6",
	"Textures (Uncompressed)",
	"Map Cutscenes",
	"Map Object Setups",
	"Map Object Model 2 Behaviour Scripts",
	"Animations",
	"Text",
	"Unknown 13",
	"Textures",
	"Map Paths",
	"Map Character Spawners",
	"Unknown 17",
	"Map Loading Zones",
	"Unknown 19",
	"Unknown 20",
	"Map Data 0x15",
	"Unknown 22",
	"Map Exits",
	"Map Race Checkpoints",
	"Textures",
	"Uncompressed File Sizes",
	"Unknown 27",
	"Unknown 28",
	"Unknown 29",
	"Unknown 30",
	"Unknown 31",
	"Unknown 32",
]
force_table_rewrite = [
	# 0, # Music MIDI
	# 1, # Map Geometry
	# 2, # Map Walls
	# 3, # Map Floors
	# 4, # Object Model 2 Geometry
	# 5, # Actor Geometry
	# 7, # Textures (Uncompressed)
	# 8, # Map Cutscenes
	# 9, # Map Object Setups
	# 10, # Map Object Model 2 Behaviour Scripts
	# 11, # Animations
	# 12, # Text
	# 13, # Unknown 13
	# 14, # Textures
	# 15, # Map Paths
	# 16, # Map Character Spawners
	# 17, # Unknown 17
	# 18, # Map Loading Zones
	# 19, # Unknown 19
	# 20, # Unknown 20
	# 21, # Map Data 0x15
	# 22, # Unknown 22
	# 23, # Map Exits
	# 24, # Map Race Checkpoints
	# 25, # Textures
]

def getOriginalUncompressedSize(fh : BinaryIO, pointer_table_index : int, file_index : int):
	global pointer_tables

	ROMAddress = pointer_tables[26]["entries"][pointer_table_index]["absolute_address"] + file_index * 4

	# print("Reading size for file " + str(pointer_table_index) + "->" + str(file_index) + " from ROM address " + hex(ROMAddress))

	fh.seek(ROMAddress)
	return int.from_bytes(fh.read(4), "big")

# Write the new uncompressed size back to ROM to prevent malloc buffer overruns when decompressing
def writeUncompressedSize(fh: BinaryIO, pointer_table_index : int, file_index : int, uncompressed_size : int):
	global pointer_tables

	ROMAddress = pointer_tables[26]["entries"][pointer_table_index]["absolute_address"] + file_index * 4

	print(" - Writing new uncompressed size " + hex(uncompressed_size) + " for file " + str(pointer_table_index) + "->" + str(file_index) + " to ROM address " + hex(ROMAddress))

	fh.seek(ROMAddress)
	fh.write(int.to_bytes(uncompressed_size, 4, "big"))

def parsePointerTables(fh : BinaryIO):
	global pointer_tables
	global main_pointer_table_offset
	global maps
	global num_tables

	# Read pointer table addresses
	fh.seek(main_pointer_table_offset)
	for i in range(num_tables):
		absolute_address = int.from_bytes(fh.read(4), "big") + main_pointer_table_offset
		pointer_tables.append({
			"index": i,
			"absolute_address": absolute_address,
			"new_absolute_address": absolute_address,
			"num_entries": 0,
			"entries": [],
		})

	# Read pointer table lengths
	fh.seek(main_pointer_table_offset + num_tables * 4)
	for x in pointer_tables:
		x["num_entries"] = int.from_bytes(fh.read(4), "big")

	# Read pointer table entries
	for x in pointer_tables:
		if x["num_entries"] > 0:
			for i in range(x["num_entries"]):
				# Compute address and size information about the pointer
				fh.seek(x["absolute_address"] + i * 4)
				raw_int = int.from_bytes(fh.read(4), "big")
				absolute_address = (raw_int & 0x7FFFFFFF) + main_pointer_table_offset
				next_absolute_address = (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF) + main_pointer_table_offset
				x["entries"].append({
					"index": i,
					"pointer_address": hex(x["absolute_address"] + i * 4),
					"absolute_address": absolute_address,
					"next_absolute_address": next_absolute_address,
					"bit_set": (raw_int & 0x80000000) > 0,
					"original_sha1": "",
					"new_sha1": "",
				})

	# Read data and original uncompressed size
	# Note: Needs to happen after all entries are read for annoying reasons
	quickSHA1Lookup = []
	for x in pointer_tables:
		quickSHA1Lookup.append({})
		if x["num_entries"] > 0:
			for y in x["entries"]:
				if not y["bit_set"]:
					absolute_size = y["next_absolute_address"] - y["absolute_address"]
					if absolute_size > 0:
						file_info = addFileToDatabase(fh, y["absolute_address"], absolute_size, x["index"], y["index"])
						quickSHA1Lookup[x["index"]][y["absolute_address"]] = file_info["sha1"]

	# Go back over and look up SHA1s for the bit_set entries
	# Note: Needs to be last because it's possible earlier entries point to later entries that might not have data yet
	for x in pointer_tables:
		if x["num_entries"] > 0:
			for y in x["entries"]:
				if y["bit_set"]:
					fh.seek(y["absolute_address"])
					lookup_index = int.from_bytes(fh.read(2), "big")
					file_info = getFileInfo(x["index"], lookup_index)
					if file_info:
						y["original_sha1"] = file_info["sha1"]
						y["new_sha1"] = file_info["sha1"]
						y["bit_set"] = False # We'll turn this back on later when recomputing pointer tables

				# Find an entry with the same absolute address and copy the cached SHA1
				if y["new_sha1"] == "":
					if y["absolute_address"] in quickSHA1Lookup[x["index"]]:
						quickSHA1 = quickSHA1Lookup[x["index"]][y["absolute_address"]]
						y["original_sha1"] = quickSHA1
						y["new_sha1"] = quickSHA1

def addFileToDatabase(fh : BinaryIO, absolute_address : int, absolute_size: int, pointer_table_index : int, file_index : int):
	global pointer_tables
	global pointer_table_files

	for x in pointer_tables:
		if x["absolute_address"] == absolute_address:
			print("WARNING: POINTER TABLE " + str(x["index"]) + " BEING USED AS FILE!")
			return

	fh.seek(absolute_address)
	data = fh.read(absolute_size)

	dataSHA1Hash = hashlib.sha1(data).hexdigest()

	pointer_tables[pointer_table_index]["entries"][file_index]["original_sha1"] = dataSHA1Hash
	pointer_tables[pointer_table_index]["entries"][file_index]["new_sha1"] = dataSHA1Hash

	pointer_table_files[pointer_table_index][dataSHA1Hash] = {
		"has_been_written_to_rom": False,
		"new_file_index": file_index, # We'll use this to compute the 2 byte lookup for bit_set style pointers in the recomputed tables
		"new_absolute_address": absolute_address,
		"data": data,
		"sha1": dataSHA1Hash,
		"uncompressed_size": getOriginalUncompressedSize(fh, pointer_table_index, file_index),
	}
	return pointer_table_files[pointer_table_index][dataSHA1Hash]

def getFileInfo(pointer_table_index : int, file_index : int):
	global pointer_tables
	global pointer_table_files
	if not pointer_table_index in range(len(pointer_tables)):
		return
	
	if not file_index in range(len(pointer_tables[pointer_table_index]["entries"])):
		return

	if not pointer_tables[pointer_table_index]["entries"][file_index]["new_sha1"] in pointer_table_files[pointer_table_index]:
		return

	return pointer_table_files[pointer_table_index][pointer_tables[pointer_table_index]["entries"][file_index]["new_sha1"]]

def replaceROMFile(pointer_table_index : int, file_index : int, data: bytes, uncompressed_size : int):
	global pointer_tables
	global pointer_table_files

	# Align data to 2 byte boundary for DMA
	if (len(data) % 2 == 1):
		data_array = bytearray(data)
		data_array.append(0)
		data = bytes(data_array)

	# Insert the new data into the database
	dataSHA1Hash = hashlib.sha1(data).hexdigest()
	pointer_table_files[pointer_table_index][dataSHA1Hash] = {
		"has_been_written_to_rom": False,
		"new_file_index": file_index, # We'll use this to compute the 2 byte lookup for bit_set style pointers in the recomputed tables
		"data": data,
		"sha1": dataSHA1Hash,
		"uncompressed_size": uncompressed_size,
	}

	# Update the entry in the pointer table to point to the new data
	pointer_tables[pointer_table_index]["entries"][file_index]["new_sha1"] = dataSHA1Hash

def shouldWritePointerTable(index : int):
	global pointer_tables

	# Table 6 is nonsense.
	# Table 26 is a special case, it should never be manually overwritten
	# Instead, it should be recomputed based on the new uncompressed file sizes of the replaced files
	# This fixes heap corruption caused by a buffer overrun when decompressing a replaced file into a malloc'd buffer
	if index in [6, 26]:
		return False

	# No need to recompute pointer tables with no entries in them
	if pointer_tables[index]["num_entries"] == 0:
		return False

	if index in force_table_rewrite:
		return True

	# TODO: Better logic for this
	if pointer_tables[index]:
		for y in pointer_tables[index]["entries"]:
			if y["original_sha1"] != y["new_sha1"]:
				return True

	return False

def writeModifiedPointerTablesToROM(fh : BinaryIO):
	global next_available_free_space
	global pointer_tables
	global main_pointer_table_offset

	# Reserve pointer table space and write new data
	for x in pointer_tables:
		if not shouldWritePointerTable(x["index"]):
			continue

		# Reserve free space for the pointer table in ROM
		space_required = x["num_entries"] * 4 + 4
		should_relocate = shouldWritePointerTable(x["index"])
		if should_relocate:
			x["new_absolute_address"] = next_available_free_space
			next_available_free_space += space_required

		# Append all files referenced by the pointer table to ROM
		for y in x["entries"]:
			file_info = getFileInfo(x["index"], y["index"])
			if file_info:
				if len(file_info["data"]) > 0:
					if not file_info["has_been_written_to_rom"]:
						if should_relocate:
							# Append the file to the ROM at the address of the next available free space
							file_info["new_absolute_address"] = next_available_free_space
							y["test_new_absolute_address"] = next_available_free_space
							# Move the free space pointer along
							next_available_free_space += len(file_info["data"])
						file_info["new_file_index"] = y["index"]
						# TODO: Re-enable deduplication once crashes are figured out
						#file_info["has_been_written_to_rom"] = True
						fh.seek(file_info["new_absolute_address"])
						fh.write(file_info["data"])
					else:
						# Create a bit set pointer instead for this index
						print("Warning: File " + hex(file_info["new_absolute_address"]) + " has already been written to ROM")
						y["bit_set"] = True
						y["bit_set_absolute_address"] = next_available_free_space
						fh.seek(next_available_free_space)
						fh.write(file_info["new_file_index"].to_bytes(2, "big"))
						# next_available_free_space += 2
						# TODO: What do these bytes mean
						fh.write(bytearray([0x08, 0x00]))
						fh.write(bytearray([0x00, 0x00, 0x00, 0x00]))
						next_available_free_space += 8

	# Recompute the pointer tables using the new file addresses and write them in the reserved space
	for x in pointer_tables:
		if not shouldWritePointerTable(x["index"]):
			continue

		last_file_info = False
		adjusted_pointer = 0
		for y in x["entries"]:
			file_info = getFileInfo(x["index"], y["index"])
			if file_info:
				# Pointers to regular files calculated as normal
				last_file_info = file_info
				# TODO: Figure this out
				#adjusted_pointer = file_info["new_absolute_address"] - main_pointer_table_offset
				adjusted_pointer = y["test_new_absolute_address"] - main_pointer_table_offset
				if y["bit_set"]:
					adjusted_pointer = y["bit_set_absolute_address"] - main_pointer_table_offset
					adjusted_pointer |= 0x80000000
			else:
				# If no file info is found, it probably means this pointer isn't used for anything other then size calculation
				# So, we'll base it on the last file info we found until I come up with a better solution
				if last_file_info:
					adjusted_pointer = last_file_info["new_absolute_address"] + len(last_file_info["data"]) - main_pointer_table_offset
				else:
					print("TODO: last_file_info not found for pointer at " + hex(x["new_absolute_address"] + y["index"] * 4))

			# Update the pointer
			fh.seek(x["new_absolute_address"] + y["index"] * 4)
			fh.write(adjusted_pointer.to_bytes(4, "big"))

			# Update the uncompressed filesize
			if file_info and y["original_sha1"] != y["new_sha1"]:
				writeUncompressedSize(fh, x["index"], y["index"], file_info["uncompressed_size"])

		# The last pointer doesn't need to point to anything, except exactly after the file before it
		# This allows the game to figure out the compressed size of the entry before it to DMA into RDRAM
		# The pointer serves no other purpose
		if last_file_info:
			adjusted_pointer = last_file_info["new_absolute_address"] + len(last_file_info["data"]) - main_pointer_table_offset
			fh.seek(x["new_absolute_address"] + x["num_entries"] * 4)
			fh.write(adjusted_pointer.to_bytes(4, "big"))

		# Redirect the global pointer to the new table
		fh.seek(main_pointer_table_offset + x["index"] * 4)
		fh.write((x["new_absolute_address"] - main_pointer_table_offset).to_bytes(4, "big"))

def dumpPointerTableDetails(fr : BinaryIO):
	global pointer_tables
	global pointer_table_names

	with open("build.log", "w") as fh:
		# fh.write(json.dumps(pointer_tables, indent=4, default=str))
		# fh.write("\n")
		for x in pointer_tables:
			fh.write(str(x["index"]) + ": " + pointer_table_names[x["index"]] + ": " + hex(x["new_absolute_address"]) + " (" + str(x["num_entries"]) + " entries)")
			fh.write("\n")
			for y in x["entries"]:
				file_info = getFileInfo(x["index"], y["index"])
				
				fh.write(" - " + str(y["index"]) + ": ")
				fh.write(hex(x["new_absolute_address"] + y["index"] * 4) + " -> ")

				if file_info and "new_absolute_address" in file_info:
					fh.write(hex(file_info["new_absolute_address"]))
					fh.write(" (" + hex(len(file_info["data"])) + ")")
				else:
					fh.write("WARNING: File info not found for " + hex(y["absolute_address"]))

				fh.write(" (" + str(y["bit_set"]) + ")")

				# Yes I know this is slow, working on it
				if x["num_entries"] == 221:
					fh.write(" (" + maps[y["index"]] + ")")

				fh.write(" (" + str(y["new_sha1"]) + ")")
				fh.write("\n")

				if y["bit_set"]:
					fr.seek(y["absolute_address"])
					temp_bytes = fr.read(8)
					fh.write(temp_bytes.hex())
					fh.write("\n")

				# Output full data
				# fh.write("    - " + file_info["data"].hex())
				# fh.write("\n")