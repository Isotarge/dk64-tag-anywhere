import hashlib
from map_names import maps
from typing import BinaryIO

from encoders import encodeExits, decodeExits, encodePaths, decodePaths, encodeCheckpoints, decodeCheckpoints

pointer_tables = [
	{
		"index": 0,
		"name": "Music MIDI",
	},
	{
		"index": 1,
		"name": "Map Geometry",
		"encoded_filename": "geometry.bin",
		"decoded_filename": "geometry.todo",
	},
	{
		"index": 2,
		"name": "Map Walls",
		"encoded_filename": "walls.bin",
		"decoded_filename": "walls.obj",
		"dont_overwrite_uncompressed_sizes": True,
	},
	{
		"index": 3,
		"name": "Map Floors",
		"encoded_filename": "floors.bin",
		"decoded_filename": "floors.obj",
		"dont_overwrite_uncompressed_sizes": True,
	},
	{
		"index": 4,
		"name": "Object Model 2 Geometry",
	},
	{
		"index": 5,
		"name": "Actor Geometry",
	},
	{
		"index": 6,
		"name": "Unknown 6",
		"dont_overwrite_uncompressed_sizes": True,
	},
	{
		"index": 7,
		"name": "Textures (Uncompressed)",
		"dont_overwrite_uncompressed_sizes": True,
	},
	{
		"index": 8,
		"name": "Map Cutscenes",
		"encoded_filename": "cutscenes.bin",
		"decoded_filename": "cutscenes.todo",
	},
	{
		"index": 9,
		"name": "Map Object Setups",
		"encoded_filename": "setup.bin",
		"decoded_filename": "setup.yaml",
	},
	{
		"index": 10,
		"name": "Map Object Model 2 Behaviour Scripts",
		"encoded_filename": "object_behaviour_scripts.bin",
		"decoded_filename": "object_behaviour_scripts.todo",
	},
	{
		"index": 11,
		"name": "Animations",
		"dont_overwrite_uncompressed_sizes": True,
	},
	{
		"index": 12,
		"name": "Text",
	},
	{
		"index": 13,
		"name": "Unknown 13",
	},
	{
		"index": 14,
		"name": "Textures",
	},
	{
		"index": 15,
		"name": "Map Paths",
		"encoded_filename": "paths.bin",
		"decoded_filename": "paths.json",
		"encoder": encodePaths,
		"decoder": decodePaths,
		"do_not_compress": True,
		"dont_overwrite_uncompressed_sizes": True,
	},
	{
		"index": 16,
		"name": "Map Character Spawners",
		"encoded_filename": "character_spawners.bin",
		"decoded_filename": "character_spawners.yaml",
	},
	{
		"index": 17,
		"name": "Unknown 17",
	},
	{
		"index": 18,
		"name": "Map Loading Zones",
		"encoded_filename": "loading_zones.bin",
		"decoded_filename": "loading_zones.yaml",
	},
	{
		"index": 19,
		"name": "Unknown 19",
	},
	{
		"index": 20,
		"name": "Unknown 20",
		"dont_overwrite_uncompressed_sizes": True,
	},
	{
		"index": 21,
		"name": "Map Autowalk Data",
		"encoded_filename": "autowalk.bin",
		"decoded_filename": "autowalk.yaml",
		"do_not_compress": True,
		"dont_overwrite_uncompressed_sizes": True,
	},
	{
		"index": 22,
		"name": "Unknown 22",
	},
	{
		"index": 23,
		"name": "Map Exits",
		"encoded_filename": "exits.bin",
		"decoded_filename": "exits.json",
		"do_not_compress": True,
		"dont_overwrite_uncompressed_sizes": True,
		"encoder": encodeExits,
		"decoder": decodeExits,
	},
	{
		"index": 24,
		"name": "Map Race Checkpoints",
		"encoded_filename": "race_checkpoints.bin",
		"decoded_filename": "race_checkpoints.json",
		"encoder": encodeCheckpoints,
		"decoder": decodeCheckpoints,
	},
	{
		"index": 25,
		"name": "Textures",
	},
	{
		"index": 26,
		"name": "Uncompressed File Sizes",
		"dont_overwrite_uncompressed_sizes": True,
	},
	{
		"index": 27,
		"name": "Unknown 27",
	},
	{
		"index": 28,
		"name": "Unknown 28",
	},
	{
		"index": 29,
		"name": "Unknown 29",
	},
	{
		"index": 30,
		"name": "Unknown 30",
	},
	{
		"index": 31,
		"name": "Unknown 31",
	},
]

num_tables = len(pointer_tables)
main_pointer_table_offset = 0x101C50

# The address of the next available byte of free space in ROM
# used when appending files to the end of the ROM
#next_available_free_space = 0x1FED020
next_available_free_space = 0x2000000

# These will be indexed by pointer table index then by SHA1 hash of the data
pointer_table_files = []
for x in pointer_tables:
	pointer_table_files.append({})

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
	# 14, # Textures
	# 15, # Map Paths
	# 16, # Map Character Spawners
	# 18, # Map Loading Zones
	# 21, # Map Autowalk Data
	# 23, # Map Exits
	# 24, # Map Race Checkpoints
	# 25, # Textures
]

def make_safe_filename(s : str):
    def safe_char(c : str):
        if c.isalnum():
            return c
        else:
            return "_"
    return "".join(safe_char(c) for c in s).rstrip("_")

def getOriginalUncompressedSize(fh : BinaryIO, pointer_table_index : int, file_index : int):
	global pointer_tables

	if "dont_overwrite_uncompressed_sizes" in pointer_tables[pointer_table_index]:
		return 0

	ROMAddress = pointer_tables[26]["entries"][pointer_table_index]["absolute_address"] + file_index * 4

	# print("Reading size for file " + str(pointer_table_index) + "->" + str(file_index) + " from ROM address " + hex(ROMAddress))

	fh.seek(ROMAddress)
	return int.from_bytes(fh.read(4), "big")

# Write the new uncompressed size back to ROM to prevent malloc buffer overruns when decompressing
def writeUncompressedSize(fh: BinaryIO, pointer_table_index : int, file_index : int, uncompressed_size : int):
	global pointer_tables

	if "dont_overwrite_uncompressed_sizes" in pointer_tables[pointer_table_index]:
		return 0

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
	for x in pointer_tables:
		absolute_address = int.from_bytes(fh.read(4), "big") + main_pointer_table_offset
		x["absolute_address"] = absolute_address
		x["new_absolute_address"] = absolute_address

	# Read pointer table lengths
	fh.seek(main_pointer_table_offset + num_tables * 4)
	for x in pointer_tables:
		x["num_entries"] = int.from_bytes(fh.read(4), "big")
		x["entries"] = []

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
					"new_absolute_address": absolute_address,
					"next_absolute_address": next_absolute_address,
					"bit_set": (raw_int & 0x80000000) > 0,
					"original_sha1": "",
					"new_sha1": "",
				})

	# Read data and original uncompressed size
	# Note: Needs to happen after all entries are read for annoying reasons
	for x in pointer_tables:
		if x["num_entries"] > 0:
			for y in x["entries"]:
				if not y["bit_set"]:
					absolute_size = y["next_absolute_address"] - y["absolute_address"]
					if absolute_size > 0:
						file_info = addFileToDatabase(fh, y["absolute_address"], absolute_size, x["index"], y["index"])

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
						#y["bit_set"] = False # We'll turn this back on later when recomputing pointer tables

def addFileToDatabase(fh : BinaryIO, absolute_address : int, absolute_size: int, pointer_table_index : int, file_index : int):
	global pointer_tables
	global pointer_table_files

	# TODO: Get rid of this check
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

	# TODO: Get this working
	if pointer_table_index == 8 and file_index == 0:
		print(" - WARNING: Tried to replace Test Map cutscenes. This will replace global cutscenes, so it has been disabled for now to prevent crashes.")
		return

	# Align data to 2 byte boundary for DMA
	if (len(data) % 2 == 1):
		data_array = bytearray(data)
		data_array.append(0)
		data = bytes(data_array)

	# Insert the new data into the database
	dataSHA1Hash = hashlib.sha1(data).hexdigest()
	pointer_table_files[pointer_table_index][dataSHA1Hash] = {
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
		earliest_file_address = 0
		if should_relocate:
			x["new_absolute_address"] = next_available_free_space
			next_available_free_space += space_required
			earliest_file_address = next_available_free_space

		# Append all files referenced by the pointer table to ROM
		for y in x["entries"]:
			file_info = getFileInfo(x["index"], y["index"])
			if file_info:
				if len(file_info["data"]) > 0:
					if should_relocate:
						# Append the file to the ROM at the address of the next available free space
						y["new_absolute_address"] = next_available_free_space
						# Move the free space pointer along
						next_available_free_space += len(file_info["data"])
					fh.seek(y["new_absolute_address"])
					fh.write(file_info["data"])

	# Recompute the pointer tables using the new file addresses and write them in the reserved space
	for x in pointer_tables:
		if not shouldWritePointerTable(x["index"]):
			continue

		adjusted_pointer = 0
		next_pointer = 0
		for y in x["entries"]:
			file_info = getFileInfo(x["index"], y["index"])
			if file_info:
				# Pointers to regular files calculated as normal
				adjusted_pointer = y["new_absolute_address"] - main_pointer_table_offset
				next_pointer = y["new_absolute_address"] + len(file_info["data"]) - main_pointer_table_offset

				# Update the uncompressed filesize
				if y["original_sha1"] != y["new_sha1"]:
					writeUncompressedSize(fh, x["index"], y["index"], file_info["uncompressed_size"])
			else:
				adjusted_pointer = next_pointer

			# Fix for tables with no entry at slot 0
			if adjusted_pointer == 0:
				adjusted_pointer = earliest_file_address - main_pointer_table_offset
				next_pointer = earliest_file_address - main_pointer_table_offset

			# Update the pointer
			fh.seek(x["new_absolute_address"] + y["index"] * 4)
			fh.write(adjusted_pointer.to_bytes(4, "big"))
			fh.write(next_pointer.to_bytes(4, "big"))

		# Redirect the global pointer to the new table
		fh.seek(main_pointer_table_offset + x["index"] * 4)
		fh.write((x["new_absolute_address"] - main_pointer_table_offset).to_bytes(4, "big"))

def dumpPointerTableDetails(filename : str, fr : BinaryIO):
	global pointer_tables
	global main_pointer_table_offset

	with open(filename, "w") as fh:
		for x in pointer_tables:
			fh.write(str(x["index"]) + ": " + x["name"] + ": " + hex(x["new_absolute_address"]) + " (" + str(x["num_entries"]) + " entries)")
			fh.write("\n")
			for y in x["entries"]:
				fh.write(" - " + str(y["index"]) + ": ")
				fh.write(hex(x["new_absolute_address"] + y["index"] * 4) + " -> ")
				fr.seek(x["new_absolute_address"] + y["index"] * 4)
				pointing_to = (int.from_bytes(fr.read(4), "big") & 0x7FFFFFFF) + main_pointer_table_offset
				fh.write(hex(pointing_to))

				file_info = getFileInfo(x["index"], y["index"])
				if file_info and "new_absolute_address" in file_info:
					fh.write(" (" + hex(len(file_info["data"])) + ")")
				else:
					fh.write(" WARNING: File info not found")

				uncompressed_size = getOriginalUncompressedSize(fr, x["index"], y["index"])
				if uncompressed_size > 0:
					fh.write(" (" + hex(uncompressed_size) + ")")
				fh.write(" (" + str(y["bit_set"]) + ")")

				if x["num_entries"] == 221:
					fh.write(" (" + maps[y["index"]] + ")")

				fh.write(" (" + str(y["new_sha1"]) + ")")
				fh.write("\n")