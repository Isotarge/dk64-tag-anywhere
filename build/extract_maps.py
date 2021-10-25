from typing import BinaryIO
import os
import zlib

ROMName = "./rom/dk64.z64"

from recompute_pointer_table import num_tables, pointer_tables, maps, getFileInfo, parsePointerTables

relevant_pointer_tables = [
    {
        "index": 1,
        "name": "Map Geometry",
        "output_filename": "geometry.bin",
    },
    {
        "index": 2,
        "name": "Map Walls",
        "output_filename": "walls.bin",
    },
    {
        "index": 3,
        "name": "Map Floors",
        "output_filename": "floors.bin",
    },
    {
        "index": 8,
        "name": "Map Cutscenes",
        "output_filename": "cutscenes.bin",
    },
    {
        "index": 9,
        "name": "Map Setups",
        "output_filename": "setup.bin",
    },
    {
        "index": 10,
        "name": "Map Object Model 2 Behaviour Scripts",
        "output_filename": "object_behaviour_scripts.bin",
        "do_not_reimport": True,
    },
    {
        "index": 15,
        "name": "Map Paths",
        "output_filename": "paths.bin",
        "do_not_compress": True,
    },
    {
        "index": 16,
        "name": "Map Character Spawners",
        "output_filename": "character_spawners.bin",
    },
    {
        "index": 18,
        "name": "Map Loading Zones",
        "output_filename": "loading_zones.bin",
    },
    {
        "index": 21,
        "name": "Map Data 0x15",
        "output_filename": "map_0x15.bin",
        "do_not_compress": True,
    },
    {
        "index": 23,
        "name": "Map Exits",
        "output_filename": "exits.bin",
        "do_not_compress": True,
    },
    {
        "index": 24,
        "name": "Map Race Checkpoints",
        "output_filename": "race_checkpoints.bin",
    },
]

def make_safe_filename(s):
    def safe_char(c):
        if c.isalnum():
            return c
        else:
            return "_"
    return "".join(safe_char(c) for c in s).rstrip("_")

def extractMaps():
    global maps

    for mapIndex, mapName in enumerate(maps):
        mapPath = "maps/" + str(mapIndex) + " - " + make_safe_filename(mapName) + "/"
        if not os.path.exists(mapPath):
            os.makedirs(mapPath)

        extractMap(mapIndex, mapPath)

def extractMap(mapIndex : int, mapPath : str):
    global pointer_tables
    global num_tables
    global relevant_pointer_tables

    if len(pointer_tables) < num_tables:
        # print("Warning: Pointer tables not initialized when calling extractMap(" + str(mapIndex) + ")")
        return

    for pointer_table in relevant_pointer_tables:
        if len(pointer_tables[pointer_table["index"]]["entries"]) <= mapIndex:
            # print("Warning: Pointer table " + str(pointer_table["index"]) + " did not contain an entry for index " + str(mapIndex))
            return

        entry = pointer_tables[pointer_table["index"]]["entries"][mapIndex]

        if entry["bit_set"]:
            file_info = getFileInfo(pointer_table["index"], entry["index"])
            if file_info:
                index = int.from_bytes(bytes([file_info["data"][0], file_info["data"][1]]), "big")
                entry = pointer_tables[pointer_table["index"]]["entries"][index]

        file_info = getFileInfo(pointer_table["index"], entry["index"])
        if file_info:
            if len(file_info["data"]) > 0:
                built_filename = mapPath + pointer_table["output_filename"]
                data = file_info["data"]
                if len(data) > 3 and data[0] == 0x1F and data[1] == 0x8B and data[2] == 0x08:
                    with open(built_filename, "wb") as fh:
                        fh.write(zlib.decompress(data, 15 + 32))
                else:
                    with open(built_filename, "wb") as fh:
                        fh.write(data)

if __name__ == '__main__':
    with open(ROMName, "r+b") as fh:
        print("[1 / 2] - Parsing pointer tables")
        parsePointerTables(fh)
        print("[2 / 2] - Extracting maps")
        extractMaps()