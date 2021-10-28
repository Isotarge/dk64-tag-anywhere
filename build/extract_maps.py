from typing import BinaryIO
import os
import zlib

ROMName = "./rom/dk64.z64"

from recompute_pointer_table import num_tables, pointer_tables, maps, getFileInfo, parsePointerTables

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

    if len(pointer_tables) < num_tables:
        # print("Warning: Pointer tables not initialized when calling extractMap(" + str(mapIndex) + ")")
        return

    for pointer_table in pointer_tables:
        if not "output_filename" in pointer_table:
            continue

        if len(pointer_tables[pointer_table["index"]]["entries"]) <= mapIndex:
            # print("Warning: Pointer table " + str(pointer_table["index"]) + " did not contain an entry for index " + str(mapIndex))
            return

        entry = pointer_tables[pointer_table["index"]]["entries"][mapIndex]
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

                if "decoder" in pointer_table and callable(pointer_table["decoder"]):
                    pointer_table["decoder"](built_filename)

if __name__ == '__main__':
    with open(ROMName, "r+b") as fh:
        print("[1 / 2] - Parsing pointer tables")
        parsePointerTables(fh)
        print("[2 / 2] - Extracting maps")
        extractMaps()