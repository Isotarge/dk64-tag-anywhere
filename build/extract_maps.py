import os
import sys
import shutil
import zlib
import json
import hashlib

ROMName = "./rom/dk64.z64"

from map_names import maps
from recompute_pointer_table import num_tables, pointer_tables, getFileInfo, parsePointerTables, make_safe_filename
from encoders import valueSamples

skip_tests = [
    "codec_test/2/paths.bin", # Original bin contains unused paths, so we do not need to make sure this file matches exactly
    "codec_test/8/paths.bin", # Original bin contains unused paths, so we do not need to make sure this file matches exactly
    "codec_test/196/paths.bin", # Original bin contains unused paths, so we do not need to make sure this file matches exactly
]

tests_passed = 0
tests_failed = 0

def extractMaps(runCodecTests : bool):
    global maps
    global tests_failed

    if runCodecTests and os.path.exists("codec_test"):
        shutil.rmtree("codec_test")

    for mapIndex, mapName in enumerate(maps):
        mapPath = "maps/" + str(mapIndex) + " - " + make_safe_filename(mapName) + "/"
        if runCodecTests:
            mapPath = "codec_test/" + str(mapIndex) + "/"
        if not os.path.exists(mapPath):
            os.makedirs(mapPath)

        extractMap(mapIndex, mapPath, runCodecTests)

    if runCodecTests and os.path.exists("codec_test") and tests_failed == 0:
        shutil.rmtree("codec_test")

def extractMap(mapIndex : int, mapPath : str, runCodecTests : bool):
    global pointer_tables
    global num_tables
    global tests_passed
    global tests_failed

    if len(pointer_tables) < num_tables:
        # print("Warning: Pointer tables not initialized when calling extractMap(" + str(mapIndex) + ")")
        return

    for pointer_table in pointer_tables:
        if not "encoded_filename" in pointer_table:
            continue

        if len(pointer_tables[pointer_table["index"]]["entries"]) <= mapIndex:
            # print("Warning: Pointer table " + str(pointer_table["index"]) + " did not contain an entry for index " + str(mapIndex))
            return

        entry = pointer_tables[pointer_table["index"]]["entries"][mapIndex]
        file_info = getFileInfo(pointer_table["index"], entry["index"])
        if file_info:
            if len(file_info["data"]) > 0:
                decoded_filename = mapPath + pointer_table["decoded_filename"]
                encoded_filename = mapPath + pointer_table["encoded_filename"]
                data = file_info["data"]
                if len(data) > 3 and data[0] == 0x1F and data[1] == 0x8B and data[2] == 0x08:
                    data = zlib.decompress(data, 15 + 32)

                with open(encoded_filename, "wb") as fh:
                    fh.write(data)

                if "decoder" in pointer_table and callable(pointer_table["decoder"]):
                    pointer_table["decoder"](decoded_filename, encoded_filename)

                if runCodecTests and not encoded_filename in skip_tests:
                    if "encoder" in pointer_table and callable(pointer_table["encoder"]):
                        pointer_table["encoder"](decoded_filename, encoded_filename + ".test")

                    # Compare the original bin, and the re-encoded bin
                    if os.path.exists(encoded_filename) and os.path.exists(encoded_filename + ".test"):
                        with open(encoded_filename, "rb") as f_original:
                            with open(encoded_filename + ".test", "rb") as f_reencoded:
                                originalSHA1 = hashlib.sha1(f_original.read()).hexdigest().upper()
                                reencodedSHA1 = hashlib.sha1(f_reencoded.read()).hexdigest().upper()
                                if originalSHA1 == reencodedSHA1:
                                    tests_passed += 1
                                else:
                                    tests_failed += 1
                                    print("[FAIL] " + encoded_filename + " Original: " + originalSHA1 + " Re-encoded: " + reencodedSHA1)

if __name__ == '__main__':
    # Measure how long this takes
    import time
    start = time.time()
    shouldRunTests = len(sys.argv) > 1 and sys.argv[1] == '--test-codecs'
    with open(ROMName, "rb") as fh:
        print("[1 / 2] - Parsing pointer tables")
        parsePointerTables(fh)
        print("[2 / 2] - Extracting maps")
        extractMaps(shouldRunTests)
        print(json.dumps(valueSamples, indent=4, default=str, sort_keys=True))
        if shouldRunTests:
            print("PASSED " + str(tests_passed) + " / " + str(tests_passed + tests_failed)  + " TESTS")

    end = time.time()
    print("Completed in " + str(round(end - start, 3)) + " seconds")