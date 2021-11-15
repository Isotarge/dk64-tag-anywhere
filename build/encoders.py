import json
import math
import struct
from typing import BinaryIO
from map_names import maps
from model2_names import model2_names
from actor_names import actor_names

# Useful for detecting booleans, enums, indexes etc
valueSamples = {}
def sampleValue(tag : str, value):
    if not tag in valueSamples:
        valueSamples[tag] = {
            "min": math.inf,
            "max": -math.inf,
            "all": {}
        }
    if type(value) == int or type(value) == float:
        valueSamples[tag]["min"] = min(value, valueSamples[tag]["min"])
        valueSamples[tag]["max"] = max(value, valueSamples[tag]["max"])
    if not value in valueSamples[tag]["all"]:
        valueSamples[tag]["all"][value] = 0
    valueSamples[tag]["all"][value] += 1
    return value

dump_scripthawk_positions = False
def ScriptHawkSetPosition(x, y, z):
    return "Game.setPosition(" + str(x) + "," + str(y) + "," + str(z) + ");"

def getStructSize(struct_fields : list):
    totalSize = 0
    for field in struct_fields:
        # Short-cuts
        if field["type"] == "byte":
            field["size"] = 1
        elif field["type"] == "short":
            field["size"] = 2
        elif field["type"] == "ushort":
            field["size"] = 2
        elif field["type"] == float:
            field["size"] = 4

        totalSize += field["size"]

    return totalSize

def readStructArray(byte_read : bytes, offset : int, length : int, struct_fields : list):
    decoded_struct_array = []
    read_head = offset
    struct_size = getStructSize(struct_fields)
    for i in range(length):
        decoded_struct_array.append(readStruct(byte_read, read_head, struct_fields))
        read_head += struct_size
    return decoded_struct_array

def readStruct(byte_read : bytes, offset : int, struct_fields : list):
    read_head = offset
    decoded_struct = {}
    for field in struct_fields:
        # Short-cuts
        if field["type"] == "byte":
            field["type"] = "uint"
            field["size"] = 1
        if field["type"] == "short":
            field["type"] = int
            field["size"] = 2
        elif field["type"] == "ushort":
            field["type"] = "uint"
            field["size"] = 2

        # Actual reads
        if field["type"] == int:
            decoded_struct[field["name"]] = int.from_bytes(byte_read[read_head:read_head + field["size"]], byteorder="big", signed=True)
        elif field["type"] == "uint":
            decoded_struct[field["name"]] = int.from_bytes(byte_read[read_head:read_head + field["size"]], byteorder="big")
        elif field["type"] == float:
            field["size"] = 4
            decoded_struct[field["name"]] = struct.unpack('>f', byte_read[read_head:read_head+4])[0]
        elif field["type"] == bool:
            decoded_struct[field["name"]] = True if int.from_bytes(byte_read[read_head:read_head + field["size"]], byteorder="big") else False
        elif field["type"] == bytes:
            decoded_struct[field["name"]] = byte_read[read_head:read_head + field["size"]].hex(" ").upper()
        else:
            print("Unknown field type in readStruct(): " + field["type"])

        if "index_of" in field:
            index_offset = 0
            if "index_offset" in field:
                index_offset = field["index_offset"]

            if decoded_struct[field["name"]] + index_offset < len(field["index_of"]):
                decoded_struct[field["name"] + "_name"] = field["index_of"][decoded_struct[field["name"]] + index_offset]
            else:
                decoded_struct[field["name"] + "_name"] = "Unknown " + hex(decoded_struct[field["name"]] + index_offset)

        if "sample" in field:
            sampleName = field["sample"] if type(field["sample"]) == str else field["name"]
            sampleValue(sampleName, decoded_struct[field["name"]])

        read_head += field["size"]
    
    if dump_scripthawk_positions and "x_pos" in decoded_struct and "y_pos" in decoded_struct and "z_pos" in decoded_struct:
        decoded_struct["SetPosition"] = ScriptHawkSetPosition(decoded_struct["x_pos"], decoded_struct["y_pos"], decoded_struct["z_pos"])

    return decoded_struct

def writeStructArray(fh : BinaryIO, struct_array : list, struct_fields: list, include_count : bool = False, count_bytes : int = 0):
    if include_count:
        fh.write(len(struct_array).to_bytes(count_bytes, byteorder="big"))
    
    for struct_data in struct_array:
        writeStruct(fh, struct_data, struct_fields)

def writeStruct(fh : BinaryIO, struct_data : dict, struct_fields : list):
    for field in struct_fields:
        # Short-cuts
        if field["type"] == "byte":
            field["type"] = "uint"
            field["size"] = 1
        elif field["type"] == "short":
            field["type"] = int
            field["size"] = 2
        elif field["type"] == "ushort":
            field["type"] = "uint"
            field["size"] = 2

        # Actual reads
        if field["type"] == int:
            fh.write(int(struct_data[field["name"]]).to_bytes(field["size"], byteorder="big", signed=True))
        elif field["type"] == "uint":
            fh.write(int(struct_data[field["name"]]).to_bytes(field["size"], byteorder="big"))
        elif field["type"] == float:
            fh.write(struct.pack('>f', struct_data[field["name"]]))
        elif field["type"] == bool:
            fh.write(bytes([1 if struct_data[field["name"]] else 0]))
        elif field["type"] == bytes:
            fh.write(bytes.fromhex(struct_data[field["name"]]))
        else:
            print("Unknown field type in readStruct(): " + field["type"])

lz_object_types = [
    "Unknown 0x0", # In maps 6,14,30,43,55,106 (Minecarts, Aztec Beetle Race, Galleon, Shipwreck)
    "Unused 0x1",
    "Unknown 0x2", # In Castle Minecart / MJ / Fungi (Rabbit Race)
    "Boss Door Trigger 0x3", # Also sets boss fadeout type as fade instead of spin. In toolshed too??
    "Unknown 0x4", # In Fungi Minecart
    "Cutscene Trigger 0x5",
    "Unknown 0x6", # In Treehouse / MJ / Fungi. Not phase reset plane
    "Unknown 0x7", # In Fungi / Fungi Minecart
    "Unknown 0x8", # In Fungi / Fungi Minecart
    "Loading Zone 0x9",
    "Cutscene Trigger 0xA",
    "Unknown 0xB", # In Minecart Mayhem
    "Loading Zone + Objects 0xC", # Alows objects through
    "Loading Zone 0xD",
    "Unused 0xE",
    "Warp Trigger 0xF", # Factory Poles
    "Loading Zone 0x10",
    "Loading Zone 0x11", # Snide's, Return to Parent Map?
    "Unused 0x12",
    "Unknown 0x13", # In maps 7,17,30,34,38,47,48,194 (Japes, Helm, Galleon, Isles, Aztec, Shipwreck, Fungi, Caves)
    "Boss Loading Zone 0x14", # Takes you to the boss of that level
    "Cutscene Trigger 0x15",
    "Unknown 0x16", # In Aztec Beetle Race
    "Cutscene Trigger 0x17",
    "Unknown 0x18", # In Fungi Minecart
    "Trigger 0x19", # Seal Race
    "Unknown 0x1A", # In Caves Beetle Race
    "Slide Trigger 0x1B", # Beetle Races
    "Unknown 0x1C", # Beetle Races
    "Unused 0x1D",
    "Unused 0x1E",
    "Unused 0x1F",
    "Cutscene Trigger 0x20",
    "Unused 0x21",
    "Unused 0x22",
    "Unused 0x23",
    "Unknown 0x24", # Cannon Trigger? Also used Aztec Snake Road and maps 7,17,26,34,38,48,72,173
    "Unknown 0x25", # In Factory
    "Unknown 0x26", # In BFI & K. Lumsy. Seems to be centred around torches?
]

lz_struct = [
    {"name": "x_pos",                "type": "short"},
    {"name": "y_pos",                "type": "short"},
    {"name": "z_pos",                "type": "short"},
    {"name": "radius",               "type": "short"},
    {"name": "height",               "type": "short"},
    {"name": "unkA",                 "type": "ushort"}, # Probably an index, values range from 0-50 except 38 is never seen
    {"name": "activation_type",      "type": "byte"},
    {"name": "boolD",                "type": bool, "size": 1},     # If set, enter K. Rool LZ is active without all keys
    {"name": "unkE",                 "type": "byte"},   # Usually 1, but values range from 0-4
    {"name": "unkF",                 "type": "byte"},   # Usually 0, but other known values are 2,4,5,32,48,50,64,75,80,96,128,144,209,228,255
    {"name": "object_type",          "type": "short", "index_of": lz_object_types},
    {"name": "destination_map",      "type": "ushort", "index_of": maps},
    {"name": "destination_exit",     "type": "ushort"},
    {"name": "transition_type",      "type": "ushort"},
    {"name": "unk18",                "type": "ushort"},
    {"name": "cutscene_is_tied",     "type": "ushort"},
    {"name": "cutscene_index",       "type": "ushort"},
    {"name": "shift_camera_to_kong", "type": "ushort"},
    {"name": "unk20",                "type": bytes, "size": 0x38 - 0x20}, # TODO: Break this down into smaller fields
]

def decodeLoadingZones(decoded_filename : str, encoded_filename :str):
    with open(encoded_filename, "rb") as fh:
        byte_read = fh.read()
        num_loading_zones = int.from_bytes(byte_read[0x0:0x2], byteorder="big")

        loading_zones = readStructArray(byte_read, 2, num_loading_zones, lz_struct)
        for lz_data in loading_zones:
            if not "Loading Zone" in lz_data["object_type_name"]:
                del lz_data["destination_map_name"]

        with open(decoded_filename, "w") as fjson:
            json.dump(loading_zones, fjson, indent=4, default=str)

def encodeLoadingZones(decoded_filename : str, encoded_filename :str):
    with open(decoded_filename) as fjson:
        loading_zones = json.load(fjson)
        
        with open(encoded_filename, "w+b") as fh:
            writeStructArray(fh, loading_zones, lz_struct, include_count=True, count_bytes=2)

exit_struct = [
    {"name": "x_pos",        "type": "short"},
    {"name": "y_pos",        "type": "short"},
    {"name": "z_pos",        "type": "short"},
    {"name": "angle",        "type": "short"},
    {"name": "has_autowalk", "type": "byte"},
    {"name": "size",         "type": "byte"},
]

def decodeExits(decoded_filename : str, encoded_filename : str):
    with open(encoded_filename, "rb") as fh:
        byte_read = fh.read()
        num_exits = math.floor(len(byte_read) / 0xA)
        exits = readStructArray(byte_read, 0, num_exits, exit_struct)
        with open(decoded_filename, "w") as fjson:
            json.dump(exits, fjson, indent=4, default=str)

def encodeExits(decoded_filename : str, encoded_filename :str):
    with open(decoded_filename) as fjson:
        exits = json.load(fjson)
        with open(encoded_filename, "w+b") as fh:
            writeStructArray(fh, exits, exit_struct)

autowalk_point_struct = [
    {"name": "x_pos", "type": "short"},
    {"name": "y_pos", "type": "short"},
    {"name": "z_pos", "type": "short"},
    {"name": "unk6",  "type": bytes, "size": 0x12 - 0x6}
]

def decodeAutowalk(decoded_filename : str, encoded_filename :str):
    with open(encoded_filename, "rb") as fh:
        byte_read = fh.read()
        path_base = 0
        autowalk_paths = []

        num_paths = int.from_bytes(byte_read[0x0:0x2], byteorder="big")
        path_base += 2
        for i in range(num_paths):
            num_points = int.from_bytes(byte_read[path_base+0:path_base+2], byteorder="big")
            path_base += 2
            path = readStructArray(byte_read, path_base, num_points, autowalk_point_struct)
            path_base += num_points * 0x12
            autowalk_paths.append(path)

        with open(decoded_filename, "w") as fjson:
            json.dump(autowalk_paths, fjson, indent=4, default=str)

def encodeAutowalk(decoded_filename : str, encoded_filename :str):
    with open(decoded_filename) as fjson:
        autowalk_paths = json.load(fjson)
        with open(encoded_filename, "w+b") as fh:
            fh.write(len(autowalk_paths).to_bytes(2, byteorder="big"))
            for path in autowalk_paths:
                writeStructArray(fh, path, autowalk_point_struct, include_count=True, count_bytes=2)

path_point_struct = [
    {"name": "unk0",  "type": "short"},
    {"name": "x_pos", "type": "short"},
    {"name": "y_pos", "type": "short"},
    {"name": "z_pos", "type": "short"},
    {"name": "speed", "type": "byte"}, # 1 - 3 in vanilla
    {"name": "unk9",  "type": "byte"},
]

def decodePaths(decoded_filename : str, encoded_filename : str):
    with open(encoded_filename, "rb") as fh:
        byte_read = fh.read()

        paths = []
        num_paths = int.from_bytes(byte_read[0x0:0x2], byteorder="big")
        path_base = 2
        for i in range(num_paths):
            this_path = byte_read[path_base:path_base+0x6]
            num_points = int.from_bytes(this_path[0x2:0x4], byteorder="big")
            path = {
                "id": int.from_bytes(this_path[0x0:0x2], byteorder="big"),
                "unk4": int.from_bytes(this_path[0x4:0x6], byteorder="big"),
            }
            # sampleValue("path->unk4", path["unk4"])
            path_base += 0x6

            if num_points > 0:
                path["points"] = readStructArray(byte_read, path_base, num_points, path_point_struct)
                path_base += num_points * 0xA

            paths.append(path)

        with open(decoded_filename, "w") as fjson:
            json.dump(paths, fjson, indent=4, default=str)

def encodePaths(decoded_filename : str, encoded_filename : str):
    with open(decoded_filename) as fjson:
        paths = json.load(fjson)
        with open(encoded_filename, "w+b") as fh:
            # File header
            fh.write(len(paths).to_bytes(2, byteorder="big"))

            for path in paths:
                num_points = len(path["points"]) if "points" in path else 0

                # Path header
                fh.write(int(path["id"]).to_bytes(2, byteorder="big"))
                fh.write(num_points.to_bytes(2, byteorder="big"))
                fh.write(int(path["unk4"]).to_bytes(2, byteorder="big"))

                # Path points
                if num_points > 0:
                    writeStructArray(fh, path["points"], path_point_struct)

checkpoint_struct = [
    {"name": "x_pos", "type": "short"},
    {"name": "y_pos", "type": "short"},
    {"name": "z_pos", "type": "short"},
    {"name": "angle", "type": "short"},
    {"name": "unk8", "type": float},
    {"name": "unkC", "type": float},
    {"name": "unk10", "type": "ushort"},
    {"name": "unk12", "type": "ushort"},
    {"name": "unk14", "type": float},
    {"name": "unk18", "type": "ushort"},
    {"name": "unk1A", "type": "ushort"},
]

def decodeCheckpoints(decoded_filename : str, encoded_filename : str):
    with open(encoded_filename, "rb") as fh:
        byte_read = fh.read()

        checkpoints = []
        num_checkpoints = int.from_bytes(byte_read[0x1:0x3], byteorder="big")
        num_checkpoint_mappings = int.from_bytes(byte_read[0x3:0x5], byteorder="big")

        if num_checkpoints != num_checkpoint_mappings:
            print(" - Error: Number of checkpoints does not match number of checkpoint mappings.")
            return 0

        checkpoint_base = 5 + num_checkpoint_mappings * 2
        for i in range(num_checkpoints):
            mapping = int.from_bytes(byte_read[5+i*2:7+i*2], byteorder="big")
            checkpoint = readStruct(byte_read, checkpoint_base, checkpoint_struct)

            # Only include the mapping in the JSON if it does not match the physical index
            if mapping != i:
                checkpoint["mapping"] = mapping

            checkpoints.append(checkpoint)
            checkpoint_base += 0x1C

        with open(decoded_filename, "w") as fjson:
            json.dump(checkpoints, fjson, indent=4, default=str)

def encodeCheckpoints(decoded_filename : str, encoded_filename : str):
    with open(decoded_filename) as fjson:
        checkpoints = json.load(fjson)
        with open(encoded_filename, "w+b") as fh:
            # File header
            fh.write(bytes([0x1])) # Seems to always be 1
            fh.write(len(checkpoints).to_bytes(2, byteorder="big")) # Num Checkpoints
            fh.write(len(checkpoints).to_bytes(2, byteorder="big")) # Num Mappings

            # Checkpoint index mapping
            for checkpointIndex, checkpoint in enumerate(checkpoints):
                if "mapping" in checkpoint:
                    fh.write(int(checkpoint["mapping"]).to_bytes(2, byteorder="big"))
                else:
                    fh.write(checkpointIndex.to_bytes(2, byteorder="big"))

            # Checkpoint data
            writeStructArray(fh, checkpoints, checkpoint_struct)

def decodeCharacterSpawners(decoded_filename : str, encoded_filename : str):
    with open(encoded_filename, "rb") as fh:
        byte_read = fh.read()
        read_header = 0
        extract = {}
        
        # Fences?
        fence_count = int.from_bytes(byte_read[0x0:0x2], byteorder="big")
        read_header += 2

        if fence_count > 0:
            extract["fences"] = []
            for i in range(fence_count):
                unknown_data = {}

                # Points_0x6
                num_points = int.from_bytes(byte_read[read_header:read_header + 2], byteorder="big")
                read_header += 2

                if num_points > 0:
                    unknown_data["points_0x6"] = []
                    for i in range(num_points):
                        this_point = {
                            "x_pos": int.from_bytes(byte_read[read_header+0x0:read_header+0x2], byteorder="big", signed=True),
                            "y_pos": int.from_bytes(byte_read[read_header+0x2:read_header+0x4], byteorder="big", signed=True),
                            "z_pos": int.from_bytes(byte_read[read_header+0x4:read_header+0x6], byteorder="big", signed=True),
                        }
                        unknown_data["points_0x6"].append(this_point)
                        read_header += 0x6

                # Points_0xA
                num_points_0xA = int.from_bytes(byte_read[read_header:read_header + 2], byteorder="big")
                read_header += 2

                if num_points_0xA > 0:
                    unknown_data["points_0xA"] = []
                    for i in range(num_points_0xA):
                        this_point = {
                            "x_pos": int.from_bytes(byte_read[read_header+0x0:read_header+0x2], byteorder="big", signed=True),
                            "y_pos": int.from_bytes(byte_read[read_header+0x2:read_header+0x4], byteorder="big", signed=True),
                            "z_pos": int.from_bytes(byte_read[read_header+0x4:read_header+0x6], byteorder="big", signed=True),
                            "unk6": byte_read[read_header+0x6:read_header+0xA].hex(" ").upper(), # TODO: Break this down into smaller fields
                        }
                        unknown_data["points_0xA"].append(this_point)
                        read_header += 0xA

                # unknown_data["unkFooterAddress"] = hex(read_header)
                unknown_data["unkFooter"] = byte_read[read_header+0x0:read_header+0x4].hex(" ").upper() # TODO: Break this down into smaller fields
                read_header += 4

                extract["fences"].append(unknown_data)

        # Spawners
        spawn_count = int.from_bytes(byte_read[read_header:read_header + 2], byteorder="big")
        read_header += 2

        if spawn_count > 0:
            extract["character_spawners"] = []
            for i in range (spawn_count):
                spawner_data = {
                    # "spawner_address": hex(read_header),
                    "enemy_val": byte_read[read_header+0x0],
                    "unk1": byte_read[read_header+0x1],
                    "y_rot": int.from_bytes(byte_read[read_header+0x2:read_header+0x4], byteorder="big"),
                    "x_pos": int.from_bytes(byte_read[read_header+0x4:read_header+0x6], byteorder="big", signed=True),
                    "y_pos": int.from_bytes(byte_read[read_header+0x6:read_header+0x8], byteorder="big", signed=True),
                    "z_pos": int.from_bytes(byte_read[read_header+0x8:read_header+0xA], byteorder="big", signed=True),
                    # 0xA is cutscene model, which is read further down
                    "unkB": byte_read[read_header+0xB],
                    "max_idle_speed": byte_read[read_header+0xC],
                    "max_aggro_speed": byte_read[read_header+0xD],
                    "unkE": byte_read[read_header+0xE],
                    "scale": byte_read[read_header+0xF],
                    "aggro": byte_read[read_header+0x10],
                    "unk11": byte_read[read_header+0x11],
                    "initial_spawn_state": byte_read[read_header+0x12],
                    "spawn_trigger": byte_read[read_header+0x13],
                    "initial_respawn_timer": byte_read[read_header+0x14],
                    "unk15": byte_read[read_header+0x15],
                }
                # spawner_data["SETPOS"] = ScriptHawkSetPosition(spawner_data["x_pos"], spawner_data["y_pos"], spawner_data["z_pos"])
                # sampleValue("character_spawner->unk1", spawner_data["unk1"])
                # sampleValue("character_spawner->unkB", spawner_data["unkB"])
                # sampleValue("character_spawner->unkE", spawner_data["unkE"])
                # sampleValue("character_spawner->unk11", spawner_data["unk11"])
                # sampleValue("character_spawner->initial_spawn_state", spawner_data["initial_spawn_state"])
                # sampleValue("character_spawner->initial_respawn_timer", spawner_data["initial_respawn_timer"])
                # sampleValue("character_spawner->unk15", spawner_data["unk15"])

                # TODO: This is true for several spawners, figure out why
                # if spawner_data["enemy_val"] != 0x50 and byte_read[read_header+0xA] != 0:
                    # print("NON CUTSCENE OBJECT HAS CUTSCENE MODEL BYTE SET " + hex(spawner_data["enemy_val"]) + " " + hex(byte_read[read_header+0xA]) + " " + decoded_filename)

                if spawner_data["enemy_val"] == 0x50 or byte_read[read_header+0xA] != 0:
                    spawner_data["cutscene_model"] = byte_read[read_header+0xA]

                extra_count = int(byte_read[read_header+0x11])
                read_header += 0x16

                # TODO: Figure what it does
                if (extra_count > 0):
                    spawner_data["extra_data"] = []
                    for j in range(extra_count):
                        spawner_data["extra_data"].append(int.from_bytes(byte_read[read_header+0:read_header+2], byteorder="big"))
                        read_header += 2

                extract["character_spawners"].append(spawner_data)

        # Note: This is the case for several maps
        # TODO: Figure out why, and if/how they map fences onto spawners
        # if spawn_count != fence_count:
            # print("FENCE COUNT (" + str(fence_count) + ") != SPAWN COUNT (" + str(spawn_count) + ") IN " + decoded_filename)

        with open(decoded_filename, "w") as fjson:
            json.dump(extract, fjson, indent=4, default=str)

def encodeCharacterSpawners(decoded_filename : str, encoded_filename : str):
    # TODO
    return 0

setup_model2_struct = [
    {"name": "x_pos",     "type": float},
    {"name": "y_pos",     "type": float},
    {"name": "z_pos",     "type": float},
    {"name": "scale",     "type": float},
    {"name": "unk10",     "type": bytes, "size": 0x18 - 0x10}, # TODO: Break this down into smaller fields
    {"name": "angle18",   "type": float},
    {"name": "angle1C",   "type": float},
    {"name": "angle20",   "type": float},
    {"name": "unk24",     "type": float},
    {"name": "behaviour", "type": "short", "index_of": model2_names},
    {"name": "unk2A",     "type": bytes, "size": 0x30 - 0x2A}, # TODO: Break this down into smaller fields
]
setup_conveyor_data_struct = [
    {"name": "model2Index", "type": int, "size": 4}, # Note: Not included in JSON, instead this struct lives in setup["model2"][index]["conveyorData"]
    {"name": "unk4",        "type": float},
    {"name": "unk8",        "type": float},
    {"name": "unkC",        "type": float},
    {"name": "unk10",       "type": float},
    {"name": "unk14",       "type": float},
    {"name": "unk18",       "type": float},
    {"name": "unk1C",       "type": float},
    {"name": "unk20",       "type": float},
]
setup_actor_spawner_struct = [
    {"name": "x_pos",     "type": float},
    {"name": "y_pos",     "type": float},
    {"name": "z_pos",     "type": float},
    {"name": "scale",     "type": float},
    {"name": "unk10",     "type": float},
    {"name": "unk14",     "type": bytes,    "size": 0x32 - 0x14}, # TODO: Break this down into smaller fields
    {"name": "behaviour", "type": "ushort", "index_of": actor_names, "index_offset": 0x10},
    {"name": "unk34",     "type": bytes,    "size": 0x38 - 0x34}, # TODO: Break this down into smaller fields
]

def decodeSetup(decoded_filename : str, encoded_filename : str):
    with open(encoded_filename, "rb") as fh:
        byte_read = fh.read()
        pointer = 0

        setup = {}

        # Object Model 2
        num_model2 = int.from_bytes(byte_read[pointer:pointer+0x4], byteorder="big")
        pointer += 4

        if num_model2 > 0:
            setup["model2"] = readStructArray(byte_read, pointer, num_model2, setup_model2_struct)
            pointer += num_model2 * 0x30

        # Conveyor Data
        num_conveyor = int.from_bytes(byte_read[pointer:pointer+0x4], byteorder="big")
        pointer += 4

        if num_conveyor > 0:
            for i in range(num_conveyor):
                conveyor_data = readStruct(byte_read, pointer, setup_conveyor_data_struct)

                # Put this struct in to the right spot and get rid of unneeded data
                model2_index = conveyor_data["model2Index"]
                del conveyor_data["model2Index"]
                setup["model2"][model2_index]["conveyor_data"] = conveyor_data

                pointer += 0x24

        # Actor Spawners
        num_actor_spawners = int.from_bytes(byte_read[pointer:pointer+0x4], byteorder="big")
        pointer += 4

        if num_actor_spawners > 0:
            setup["actors"] = readStructArray(byte_read, pointer, num_actor_spawners, setup_actor_spawner_struct)
            pointer += num_actor_spawners * 0x38

        with open(decoded_filename, "w") as fjson:
            json.dump(setup, fjson, indent=4, default=str)

def encodeSetup(decoded_filename : str, encoded_filename : str):
    with open(decoded_filename) as fjson:
        setup = json.load(fjson)

        with open(encoded_filename, "w+b") as fh:
            num_conveyors = 0
            num_model2 = len(setup["model2"]) if "model2" in setup else 0
            num_actor_spawners = len(setup["actors"]) if "actors" in setup else 0

            # Model 2            
            fh.write(num_model2.to_bytes(4, byteorder="big"))

            if num_model2 > 0:
                for i, this_model2 in enumerate(setup["model2"]):
                    writeStruct(fh, this_model2, setup_model2_struct)
                    if "conveyor_data" in this_model2:
                        num_conveyors += 1

            # Conveyor Data
            fh.write(num_conveyors.to_bytes(4, byteorder="big"))

            if num_conveyors > 0:
                for i, this_model2 in enumerate(setup["model2"]):
                    if "conveyor_data" in this_model2:
                        conveyor_data = this_model2["conveyor_data"]
                        conveyor_data["model2Index"] = i
                        writeStruct(fh, conveyor_data, setup_conveyor_data_struct)

            # Actor Spawners
            fh.write(num_actor_spawners.to_bytes(4, byteorder="big"))

            if num_actor_spawners > 0:
                writeStructArray(fh, setup["actors"], setup_actor_spawner_struct)