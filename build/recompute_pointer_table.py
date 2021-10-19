from typing import BinaryIO

# The address of the next available byte of free space in ROM
# used when appending files to the end of the ROM
#next_available_free_space = 0x1FED020
next_available_free_space = 0x2000000

#num_tables = 27
num_tables = 32
pointer_tables = []
main_pointer_table_offset = 0x101C50

files = {}

pointer_table_names = [
	"Unknown 0",
	"Map Geometry",
	"Map Walls",
	"Map Floors",
	"Unknown 4",
	"Unknown 5",
	"Unknown 6",
	"Unknown 7",
	"Map Cutscenes",
	"Map Object Setups",
	"Map Data 0xA",
	"Unknown 11",
	"Text",
	"Unknown 13",
	"Textures",
	"Map Balloon Trajectories",
	"Map Character Spawners",
	"Unknown 17",
	"Map Loading Zones",
	"Unknown 19",
	"Unknown 20",
	"Unknown 21",
	"Unknown 22",
	"Map Exits",
	"Unknown 24",
	"Textures",
	"Unknown 26",
	"Unknown 27",
	"Unknown 28",
	"Unknown 29",
	"Unknown 30",
	"Unknown 31",
	"Unknown 32",
]
maps = [
	"Test Map", # 0
	"Funky's Store",
	"DK Arcade",
	"K. Rool Barrel: Lanky's Maze",
	"Jungle Japes: Mountain",
	"Cranky's Lab",
	"Jungle Japes: Minecart",
	"Jungle Japes",
	"Jungle Japes: Army Dillo",
	"Jetpac",
	"Kremling Kosh! (very easy)", # 10
	"Stealthy Snoop! (normal, no logo)",
	"Jungle Japes: Shell",
	"Jungle Japes: Lanky's Cave",
	"Angry Aztec: Beetle Race",
	"Snide's H.Q.",
	"Angry Aztec: Tiny's Temple",
	"Hideout Helm",
	"Teetering Turtle Trouble! (very easy)",
	"Angry Aztec: Five Door Temple (DK)",
	"Angry Aztec: Llama Temple", # 20
	"Angry Aztec: Five Door Temple (Diddy)",
	"Angry Aztec: Five Door Temple (Tiny)",
	"Angry Aztec: Five Door Temple (Lanky)",
	"Angry Aztec: Five Door Temple (Chunky)",
	"Candy's Music Shop",
	"Frantic Factory",
	"Frantic Factory: Car Race",
	"Hideout Helm (Level Intros, Game Over)",
	"Frantic Factory: Power Shed",
	"Gloomy Galleon", # 30
	"Gloomy Galleon: K. Rool's Ship",
	"Batty Barrel Bandit! (easy)",
	"Jungle Japes: Chunky's Cave",
	"DK Isles Overworld",
	"K. Rool Barrel: DK's Target Game",
	"Frantic Factory: Crusher Room",
	"Jungle Japes: Barrel Blast",
	"Angry Aztec",
	"Gloomy Galleon: Seal Race",
	"Nintendo Logo", # 40
	"Angry Aztec: Barrel Blast",
	"Troff 'n' Scoff", # 42
	"Gloomy Galleon: Shipwreck (Diddy, Lanky, Chunky)",
	"Gloomy Galleon: Treasure Chest",
	"Gloomy Galleon: Mermaid",
	"Gloomy Galleon: Shipwreck (DK, Tiny)",
	"Gloomy Galleon: Shipwreck (Lanky, Tiny)",
	"Fungi Forest",
	"Gloomy Galleon: Lighthouse",
	"K. Rool Barrel: Tiny's Mushroom Game", # 50
	"Gloomy Galleon: Mechanical Fish",
	"Fungi Forest: Ant Hill",
	"Battle Arena: Beaver Brawl!",
	"Gloomy Galleon: Barrel Blast",
	"Fungi Forest: Minecart",
	"Fungi Forest: Diddy's Barn",
	"Fungi Forest: Diddy's Attic",
	"Fungi Forest: Lanky's Attic",
	"Fungi Forest: DK's Barn",
	"Fungi Forest: Spider", # 60
	"Fungi Forest: Front Part of Mill",
	"Fungi Forest: Rear Part of Mill",
	"Fungi Forest: Mushroom Puzzle",
	"Fungi Forest: Giant Mushroom",
	"Stealthy Snoop! (normal)",
	"Mad Maze Maul! (hard)",
	"Stash Snatch! (normal)",
	"Mad Maze Maul! (easy)",
	"Mad Maze Maul! (normal)", # 69
	"Fungi Forest: Mushroom Leap", # 70
	"Fungi Forest: Shooting Game",
	"Crystal Caves",
	"Battle Arena: Kritter Karnage!",
	"Stash Snatch! (easy)",
	"Stash Snatch! (hard)",
	"DK Rap",
	"Minecart Mayhem! (easy)", # 77
	"Busy Barrel Barrage! (easy)",
	"Busy Barrel Barrage! (normal)",
	"Main Menu", # 80
	"Title Screen (Not For Resale Version)",
	"Crystal Caves: Beetle Race",
	"Fungi Forest: Dogadon",
	"Crystal Caves: Igloo (Tiny)",
	"Crystal Caves: Igloo (Lanky)",
	"Crystal Caves: Igloo (DK)",
	"Creepy Castle",
	"Creepy Castle: Ballroom",
	"Crystal Caves: Rotating Room",
	"Crystal Caves: Shack (Chunky)", # 90
	"Crystal Caves: Shack (DK)",
	"Crystal Caves: Shack (Diddy, middle part)",
	"Crystal Caves: Shack (Tiny)",
	"Crystal Caves: Lanky's Hut",
	"Crystal Caves: Igloo (Chunky)",
	"Splish-Splash Salvage! (normal)",
	"K. Lumsy",
	"Crystal Caves: Ice Castle",
	"Speedy Swing Sortie! (easy)",
	"Crystal Caves: Igloo (Diddy)", # 100
	"Krazy Kong Klamour! (easy)",
	"Big Bug Bash! (very easy)",
	"Searchlight Seek! (very easy)",
	"Beaver Bother! (easy)",
	"Creepy Castle: Tower",
	"Creepy Castle: Minecart",
	"Kong Battle: Battle Arena",
	"Creepy Castle: Crypt (Lanky, Tiny)",
	"Kong Battle: Arena 1",
	"Frantic Factory: Barrel Blast", # 110
	"Gloomy Galleon: Pufftoss",
	"Creepy Castle: Crypt (DK, Diddy, Chunky)",
	"Creepy Castle: Museum",
	"Creepy Castle: Library",
	"Kremling Kosh! (easy)",
	"Kremling Kosh! (normal)",
	"Kremling Kosh! (hard)",
	"Teetering Turtle Trouble! (easy)",
	"Teetering Turtle Trouble! (normal)",
	"Teetering Turtle Trouble! (hard)", # 120
	"Batty Barrel Bandit! (easy)",
	"Batty Barrel Bandit! (normal)",
	"Batty Barrel Bandit! (hard)",
	"Mad Maze Maul! (insane)",
	"Stash Snatch! (insane)",
	"Stealthy Snoop! (very easy)",
	"Stealthy Snoop! (easy)",
	"Stealthy Snoop! (hard)",
	"Minecart Mayhem! (normal)",
	"Minecart Mayhem! (hard)", # 130
	"Busy Barrel Barrage! (hard)",
	"Splish-Splash Salvage! (hard)",
	"Splish-Splash Salvage! (easy)",
	"Speedy Swing Sortie! (normal)",
	"Speedy Swing Sortie! (hard)",
	"Beaver Bother! (normal)",
	"Beaver Bother! (hard)",
	"Searchlight Seek! (easy)",
	"Searchlight Seek! (normal)",
	"Searchlight Seek! (hard)", # 140
	"Krazy Kong Klamour! (normal)",
	"Krazy Kong Klamour! (hard)",
	"Krazy Kong Klamour! (insane)",
	"Peril Path Panic! (very easy)",
	"Peril Path Panic! (easy)",
	"Peril Path Panic! (normal)",
	"Peril Path Panic! (hard)",
	"Big Bug Bash! (easy)",
	"Big Bug Bash! (normal)",
	"Big Bug Bash! (hard)", # 150
	"Creepy Castle: Dungeon",
	"Hideout Helm (Intro Story)",
	"DK Isles (DK Theatre)",
	"Frantic Factory: Mad Jack",
	"Battle Arena: Arena Ambush!",
	"Battle Arena: More Kritter Karnage!",
	"Battle Arena: Forest Fracas!",
	"Battle Arena: Bish Bash Brawl!",
	"Battle Arena: Kamikaze Kremlings!",
	"Battle Arena: Plinth Panic!", # 160
	"Battle Arena: Pinnacle Palaver!",
	"Battle Arena: Shockwave Showdown!",
	"Creepy Castle: Basement",
	"Creepy Castle: Tree",
	"K. Rool Barrel: Diddy's Kremling Game",
	"Creepy Castle: Chunky's Toolshed",
	"Creepy Castle: Trash Can",
	"Creepy Castle: Greenhouse",
	"Jungle Japes Lobby",
	"Hideout Helm Lobby", # 170
	"DK's House",
	"Rock (Intro Story)",
	"Angry Aztec Lobby",
	"Gloomy Galleon Lobby",
	"Frantic Factory Lobby",
	"Training Grounds",
	"Dive Barrel",
	"Fungi Forest Lobby",
	"Gloomy Galleon: Submarine",
	"Orange Barrel", # 180
	"Barrel Barrel",
	"Vine Barrel",
	"Creepy Castle: Crypt",
	"Enguarde Arena",
	"Creepy Castle: Car Race",
	"Crystal Caves: Barrel Blast",
	"Creepy Castle: Barrel Blast",
	"Fungi Forest: Barrel Blast",
	"Fairy Island",
	"Kong Battle: Arena 2", # 190
	"Rambi Arena",
	"Kong Battle: Arena 3",
	"Creepy Castle Lobby",
	"Crystal Caves Lobby",
	"DK Isles: Snide's Room",
	"Crystal Caves: Army Dillo",
	"Angry Aztec: Dogadon",
	"Training Grounds (End Sequence)",
	"Creepy Castle: King Kut Out",
	"Crystal Caves: Shack (Diddy, upper part)", # 200
	"K. Rool Barrel: Diddy's Rocketbarrel Game",
	"K. Rool Barrel: Lanky's Shooting Game",
	"K. Rool Fight: DK Phase",
	"K. Rool Fight: Diddy Phase",
	"K. Rool Fight: Lanky Phase",
	"K. Rool Fight: Tiny Phase",
	"K. Rool Fight: Chunky Phase",
	"Bloopers Ending",
	"K. Rool Barrel: Chunky's Hidden Kremling Game",
	"K. Rool Barrel: Tiny's Pony Tail Twirl Game", # 210
	"K. Rool Barrel: Chunky's Shooting Game",
	"K. Rool Barrel: DK's Rambi Game",
	"K. Lumsy Ending",
	"K. Rool's Shoe",
	"K. Rool's Arena", # 215
	"UNKNOWN 216",
	"UNKNOWN 217",
	"UNKNOWN 218",
	"UNKNOWN 219",
	"UNKNOWN 220",
	"UNKNOWN 221",
]

def parsePointerTables(fh : BinaryIO):
	global pointer_tables
	global main_pointer_table_offset
	global maps
	global num_tables

	# Read pointer table addresses
	fh.seek(main_pointer_table_offset)
	i = 0
	while i < num_tables:
		absolute_address = int.from_bytes(fh.read(4), "big") + main_pointer_table_offset
		pointer_tables.append({
			"index": i,
			"absolute_address": absolute_address,
			"new_absolute_address": absolute_address,
			"num_entries": 0,
			"entries": [],
		})
		i += 1

	# Read pointer table lengths
	fh.seek(main_pointer_table_offset + num_tables * 4)
	i = 0
	while i < num_tables:
		pointer_tables[i]["num_entries"] = int.from_bytes(fh.read(4), "big")
		i += 1

	# Read pointer table entries and data
	for x in pointer_tables:
		if x["num_entries"] > 0:
			i = 0
			while i < x["num_entries"]:
				# Compute address and size information about the pointer
				fh.seek(x["absolute_address"] + i * 4)
				raw_int = int.from_bytes(fh.read(4), "big")
				absolute_address = (raw_int & 0x7FFFFFFF) + main_pointer_table_offset
				next_absolute_address = (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF) + main_pointer_table_offset
				absolute_size = next_absolute_address - absolute_address
				x["entries"].append({
					"index": i,
					"absolute_address": absolute_address,
					"next_absolute_address": next_absolute_address,
					"bit_set": (raw_int & 0x80000000) > 0,
				})

				# Read data
				if absolute_size > 0:
					fh.seek(absolute_address)
					addFileToDatabase(absolute_address, fh.read(absolute_size))
				i += 1

def addFileToDatabase(absolute_address : int, data: bytes):
	global files
	global pointer_tables

	has_been_written_to_rom = False
	is_pointer_table = False
	for x in pointer_tables:
		if x["absolute_address"] == absolute_address:
			has_been_written_to_rom = True
			is_pointer_table = True
			#print("WARNING: POINTER TABLE " + str(x["index"]) + " BEING USED AS FILE!")
			break

	files[hex(absolute_address)] = {
		"original_absolute_address": absolute_address,
		"new_absolute_address": absolute_address,
		"has_been_modified": False,
		"is_bigger_than_original": False,
		"has_been_written_to_rom": has_been_written_to_rom,
		"is_pointer_table": is_pointer_table,
		"data": data,
	}

def getFileInfo(absolute_address: int):
	if hex(absolute_address) in files:
		return files[hex(absolute_address)]

def replaceROMFile(fh : BinaryIO, absolute_address : int, data: bytes):
	global files

	# Allow replacing files not contained in pointer tables
	# Eg. Static Code
	if not hex(absolute_address) in files:
		fh.seek(absolute_address)
		fh.write(data)
		return

	file_info = getFileInfo(absolute_address)
	if file_info:
		# Align data to 2 byte boundary for DMA
		if (len(data) % 2 == 1):
			data_array = bytearray(data)
			data_array.append(0)
			data = bytes(data_array)

		file_info["has_been_modified"] = True
		file_info["is_bigger_than_original"] = len(data) > len(file_info["data"])
		file_info["data"] = data

force_table_rewrite = [
	# 0, # Unknown 0
	# 1, # Map Geometry
	# 2, # Map Walls
	# 3, # Map Floors
	# 4, # Unknown 4
	# 5, # Unknown 5
	# 6, # Unknown 6
	# 7, # Unknown 7
	# 8, # Map Cutscenes
	# 9, # Map Object Setups
	# 10, # Map Data 0xA
	# 11, # Unknown 11
	# 12, # Text
	# 13, # Unknown 13
	# 14, # Textures
	# 15, # Map Balloon Trajectories
	# 16, # Map Character Spawners
	# 17, # Unknown 17
	# 18, # Map Loading Zones
	# 19, # Unknown 19
	# 20, # Unknown 20
	# 21, # Unknown 21
	# 22, # Unknown 22
	# 23, # Map Exits
	# 24, # Unknown 24
	# 25, # Textures
	# 26, # Unknown 26
	# 27, # Unknown 27
	# 28, # Unknown 28
	# 29, # Unknown 29
	# 30, # Unknown 30
	# 31, # Unknown 31
	# 32, # Unknown 32
]

def shouldWritePointerTable(index : int):
	global pointer_tables

	if index in force_table_rewrite:
		return True

	if pointer_tables[index]:
		for y in pointer_tables[index]["entries"]:
			file_info = getFileInfo(y["absolute_address"])
			if file_info:
				if file_info["has_been_modified"]:
					return True

	return False

def shouldRelocatePointerTable(index : int):
	global pointer_tables

	if index in force_table_rewrite:
		return True

	if pointer_tables[index]:
		for y in pointer_tables[index]["entries"]:
			file_info = getFileInfo(y["absolute_address"])
			if file_info:
				if file_info["has_been_modified"] and file_info["is_bigger_than_original"]:
					return True

	return False

def writeModifiedPointerTablesToROM(fh : BinaryIO):
	global next_available_free_space
	global pointer_tables
	global main_pointer_table_offset

	# Reserve pointer table space and write new data
	for x in pointer_tables:
		# No need to recompute pointer tables with no entries in them
		if x["num_entries"] == 0:
			continue

		if not shouldWritePointerTable(x["index"]):
			continue

		# Reserve free space for the pointer table in ROM
		space_required = x["num_entries"] * 4 + 4
		should_relocate = shouldRelocatePointerTable(x["index"])
		if should_relocate:
			x["new_absolute_address"] = next_available_free_space
			next_available_free_space += space_required

		# Update the file_info entry for the pointer table to point to the new reserved absolute address
		pointer_table_file_info = getFileInfo(x["absolute_address"])
		if pointer_table_file_info:
			pointer_table_file_info["new_absolute_address"] = x["new_absolute_address"]
		
		# Append all files referenced by the pointer table to ROM
		for y in x["entries"]:
			file_info = getFileInfo(y["absolute_address"])
			if file_info:
				if len(file_info["data"]) > 0:
					if not file_info["has_been_written_to_rom"]:
						if should_relocate:
							# Append the file to the ROM at the address of the next available free space
							file_info["new_absolute_address"] = next_available_free_space
							# Move the free space pointer along
							next_available_free_space += len(file_info["data"])
						file_info["has_been_written_to_rom"] = True
						#print("   - File " + hex(file_info["original_absolute_address"]) + " is being written to ROM at new address " + hex(file_info["new_absolute_address"]))
						fh.seek(file_info["new_absolute_address"])
						fh.write(file_info["data"])
					# else:
					# 	print("   - File " + hex(file_info["original_absolute_address"]) + " has already been written to ROM, skipping")

	# Recompute the pointer tables using the new file addresses and write them in the reserved space
	for x in pointer_tables:
		# No need to recompute pointer tables with no entries in them
		if x["num_entries"] == 0:
			continue

		if not shouldWritePointerTable(x["index"]):
			continue

		i = 0
		last_file_info = False
		while i < x["num_entries"]:
			y = x["entries"][i]
			# Pointers to regular files calculated as normal
			fh.seek(x["new_absolute_address"] + y["index"] * 4)
			file_info = getFileInfo(y["absolute_address"])
			if file_info:
				last_file_info = file_info
				adjusted_pointer = file_info["new_absolute_address"] - main_pointer_table_offset
				if y["bit_set"]:
					adjusted_pointer |= 0x80000000
				fh.write(adjusted_pointer.to_bytes(4, "big"))
			else:
				# If no file info is found, it probably means this pointer isn't used for anything other then size calculation
				# So, we'll base it on the last file info we found until I come up with a better solution
				if last_file_info:
					adjusted_pointer = (last_file_info["new_absolute_address"] + len(last_file_info["data"])) - main_pointer_table_offset
					fh.write(adjusted_pointer.to_bytes(4, "big"))
				else:
					print("TODO: last_file_info not found for pointer at " + (x["new_absolute_address"] + y["index"] * 4))

			i += 1

		# The last pointer doesn't need to point to anything, except exactly after the file before it
		# This allows the game to figure out the compressed size of the entry before it to DMA into RDRAM
		# The pointer serves no other purpose
		last_entry = x["entries"][x["num_entries"] - 1]
		last_file_info = getFileInfo(last_entry["absolute_address"])
		if last_file_info:
			adjusted_pointer = file_info["new_absolute_address"] + len(file_info["data"]) - main_pointer_table_offset
			fh.seek(x["new_absolute_address"] + x["num_entries"] * 4)
			fh.write(adjusted_pointer.to_bytes(4, "big"))
		else:
			print("WARNING: NO FILE INFO FOUND FOR " + hex(x["entries"][i - 1]["absolute_address"]))

		# Redirect the global pointer to the new table
		fh.seek(main_pointer_table_offset + x["index"] * 4)
		fh.write((x["new_absolute_address"] - main_pointer_table_offset).to_bytes(4, "big"))

def dumpPointerTableDetails():
	global pointer_tables
	global pointer_table_names

	with open("build.log", "w") as fh:
		for x in pointer_tables:
			fh.writelines
			fh.write(str(x["index"]) + ": " + pointer_table_names[x["index"]] + ": " + hex(x["new_absolute_address"]) + " (" + str(x["num_entries"]) + " entries)")
			fh.write("\n")
			for y in x["entries"]:
				file_info = getFileInfo(y["absolute_address"])
				if file_info:
					# Yes I know this is slow, working on it
					if x["num_entries"] == 221:
						fh.write(" - " + str(y["index"]) + ": " + hex(x["new_absolute_address"] + y["index"] * 4) + " -> " + hex(file_info["new_absolute_address"]) + " (" + hex(len(file_info["data"])) + ") (" + str(y["bit_set"]) + ") (" + maps[y["index"]] + ")")
						fh.write("\n")
					else:
						fh.write(" - " + str(y["index"]) + ": " + hex(x["new_absolute_address"] + y["index"] * 4) + " -> " + hex(file_info["new_absolute_address"]) + " (" + hex(len(file_info["data"])) + ") (" + str(y["bit_set"]) + ")")
						fh.write("\n")
					# fh.write("    - " + file_info["data"].hex())
					# fh.write("\n")
				else:
					# TODO: This probably means a pointer in a table was pointing to a pointer table
					# yo dawg
					fh.write(" - " + str(y["index"]) + ": " + hex(x["new_absolute_address"] + y["index"] * 4) + " - WARNING: File info not found for " + hex(y["absolute_address"]))
					fh.write("\n")