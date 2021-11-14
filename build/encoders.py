import json
import math
import struct
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

def ScriptHawkSetPosition(x, y, z):
    return "Game.setPosition(" + str(x) + "," + str(y) + "," + str(z) + ");"

def floatAt(data : bytes, offset : int):
    return struct.unpack('>f', data[offset:offset+4])[0]

def decodeLoadingZones(decoded_filename : str, encoded_filename :str):
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
    with open(encoded_filename, "rb") as fh:
        byte_read = fh.read()
        num_loading_zones = int.from_bytes(byte_read[0x0:0x2], byteorder="big")
        
        loading_zones = []
        loading_zone_base = 2
        for i in range(num_loading_zones):
            this_loading_zone = byte_read[loading_zone_base:loading_zone_base+0x38]
            object_type = int.from_bytes(this_loading_zone[0x10:0x12], byteorder="big")
            destination_map = int.from_bytes(this_loading_zone[0x12:0x14], byteorder="big")
            destination_map_name = maps[destination_map] if destination_map < len(maps) else "Unknown " + hex(destination_map)
            lz_data = {
                "x_pos": int.from_bytes(this_loading_zone[0x0:0x2], byteorder="big", signed=True),
                "y_pos": int.from_bytes(this_loading_zone[0x2:0x4], byteorder="big", signed=True),
                "z_pos": int.from_bytes(this_loading_zone[0x4:0x6], byteorder="big", signed=True),
                "radius": int.from_bytes(this_loading_zone[0x6:0x8], byteorder="big", signed=True),
                "height": int.from_bytes(this_loading_zone[0x8:0xA], byteorder="big", signed=True),
                "unkA": int.from_bytes(this_loading_zone[0xA:0xC], byteorder="big"), # Probably an index, values range from 0-50 except 38 is never seen
                "activation_type": this_loading_zone[0xC],
                "boolD": True if this_loading_zone[0xD] == 1 else False, # If set, enter K. Rool LZ is active without all keys
                "unkE": this_loading_zone[0xE], # Usually 1, but values range from 0-4
                "unkF": this_loading_zone[0xF], # Usually 0, but other known values are 2,4,5,32,48,50,64,75,80,96,128,144,209,228,255
                "object_type": object_type,
                "object_type_name": lz_object_types[object_type],
                "destination_map": destination_map,
                "destination_map_name": destination_map_name,
                "destination_exit": int.from_bytes(this_loading_zone[0x14:0x16], byteorder="big"),
                "transition_type": int.from_bytes(this_loading_zone[0x16:0x18], byteorder="big"),
                "unk18": int.from_bytes(this_loading_zone[0x18:0x1A], byteorder="big"),
                "cutscene_is_tied": int.from_bytes(this_loading_zone[0x1A:0x1C], byteorder="big"),
                "cutscene_index": int.from_bytes(this_loading_zone[0x1C:0x1E], byteorder="big"),
                "shift_camera_to_kong": int.from_bytes(this_loading_zone[0x1E:0x20], byteorder="big"),
                "unk20": this_loading_zone[0x20:0x38].hex(" ").upper(), # TODO: Break this down into smaller fields
            }

            # sampleValue("loading_zone->unkA", lz_data["unkA"])
            # sampleValue("loading_zone->boolD", lz_data["boolD"])
            # sampleValue("loading_zone->unkE", lz_data["unkE"])
            # sampleValue("loading_zone->unkF", lz_data["unkF"])
            # sampleValue("loading_zone->unkF", lz_data["unk20"])
            # lz_data["SETPOS"] = ScriptHawkSetPosition(lz_data["x_pos"], lz_data["y_pos"], lz_data["z_pos"])

            if not "Loading Zone" in lz_data["object_type_name"]:
                del lz_data["destination_map_name"]

            loading_zones.append(lz_data)
            loading_zone_base += 0x38

        with open(decoded_filename, "w") as fjson:
            json.dump(loading_zones, fjson, indent=4, default=str)

def encodeLoadingZones(decoded_filename : str, encoded_filename :str):
    with open(decoded_filename) as fjson:
        loading_zones = json.load(fjson)
        with open(encoded_filename, "w+b") as fh:
            fh.write(len(loading_zones).to_bytes(2, byteorder="big"))
            for loading_zone in loading_zones:
                fh.write(int(loading_zone["x_pos"]).to_bytes(2, byteorder="big", signed=True))
                fh.write(int(loading_zone["y_pos"]).to_bytes(2, byteorder="big", signed=True))
                fh.write(int(loading_zone["z_pos"]).to_bytes(2, byteorder="big", signed=True))
                fh.write(int(loading_zone["radius"]).to_bytes(2, byteorder="big", signed=True))
                fh.write(int(loading_zone["height"]).to_bytes(2, byteorder="big", signed=True))
                fh.write(int(loading_zone["unkA"]).to_bytes(2, byteorder="big"))
                fh.write(int(loading_zone["activation_type"]).to_bytes(1, byteorder="big"))
                fh.write(int(1 if loading_zone["boolD"] else 0).to_bytes(1, byteorder="big"))
                fh.write(int(loading_zone["unkE"]).to_bytes(1, byteorder="big"))
                fh.write(int(loading_zone["unkF"]).to_bytes(1, byteorder="big"))
                fh.write(int(loading_zone["object_type"]).to_bytes(2, byteorder="big"))
                fh.write(int(loading_zone["destination_map"]).to_bytes(2, byteorder="big"))
                fh.write(int(loading_zone["destination_exit"]).to_bytes(2, byteorder="big"))
                fh.write(int(loading_zone["transition_type"]).to_bytes(2, byteorder="big"))
                fh.write(int(loading_zone["unk18"]).to_bytes(2, byteorder="big"))
                fh.write(int(loading_zone["cutscene_is_tied"]).to_bytes(2, byteorder="big"))
                fh.write(int(loading_zone["cutscene_index"]).to_bytes(2, byteorder="big"))
                fh.write(int(loading_zone["shift_camera_to_kong"]).to_bytes(2, byteorder="big"))
                fh.write(bytes.fromhex(loading_zone["unk20"]))

def decodeExits(decoded_filename : str, encoded_filename : str):
    with open(encoded_filename, "rb") as fh:
        byte_read = fh.read()
        num_exits = math.floor(len(byte_read) / 0xA)
        exits = []
        exit_base = 0
        for i in range(num_exits):
            this_exit = byte_read[exit_base:exit_base+0xA]
            exits.append({
                "x_pos": int.from_bytes(this_exit[0x0:0x2], byteorder="big", signed=True),
                "y_pos": int.from_bytes(this_exit[0x2:0x4], byteorder="big", signed=True),
                "z_pos": int.from_bytes(this_exit[0x4:0x6], byteorder="big", signed=True),
                "angle": int.from_bytes(this_exit[0x6:0x8], byteorder="big", signed=True),
                "has_autowalk": this_exit[0x8],
                "size": this_exit[0x9],
            })
            exit_base += 0xA

        with open(decoded_filename, "w") as fjson:
            json.dump(exits, fjson, indent=4, default=str)

def encodeExits(decoded_filename : str, encoded_filename :str):
    with open(decoded_filename) as fjson:
        exits = json.load(fjson)
        with open(encoded_filename, "w+b") as fh:
            for exit in exits:
                fh.write(int(exit["x_pos"]).to_bytes(2, byteorder="big", signed=True))
                fh.write(int(exit["y_pos"]).to_bytes(2, byteorder="big", signed=True))
                fh.write(int(exit["z_pos"]).to_bytes(2, byteorder="big", signed=True))
                fh.write(int(exit["angle"]).to_bytes(2, byteorder="big", signed=True))
                fh.write(int(exit["has_autowalk"]).to_bytes(1, byteorder="big"))
                fh.write(int(exit["size"]).to_bytes(1, byteorder="big"))

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
                path["points"] = []

                for p in range(num_points):
                    this_point = byte_read[path_base:path_base+0xA]
                    
                    path["points"].append({
                        "unk0": int.from_bytes(this_point[0x0:0x2], byteorder="big", signed=True),
                        "x_pos": int.from_bytes(this_point[0x2:0x4], byteorder="big", signed=True),
                        "y_pos": int.from_bytes(this_point[0x4:0x6], byteorder="big", signed=True),
                        "z_pos": int.from_bytes(this_point[0x6:0x8], byteorder="big", signed=True),
                        "speed": this_point[0x8], # 1 - 3 in vanilla
                        "unk9": this_point[0x9],
                    })
                    # sampleValue("path->point->unk0", int.from_bytes(this_point[0x0:0x2], byteorder="big", signed=True))
                    # sampleValue("path->point->speed", this_point[0x8])
                    # sampleValue("path->point->unk9", this_point[0x9])
                    path_base += 0xA

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

                for p in range(num_points):
                    point = path["points"][p]
                    # Path points
                    fh.write(int(point["unk0"]).to_bytes(2, byteorder="big", signed=True))
                    fh.write(int(point["x_pos"]).to_bytes(2, byteorder="big", signed=True))
                    fh.write(int(point["y_pos"]).to_bytes(2, byteorder="big", signed=True))
                    fh.write(int(point["z_pos"]).to_bytes(2, byteorder="big", signed=True))
                    fh.write(int(point["speed"]).to_bytes(1, byteorder="big"))
                    fh.write(int(point["unk9"]).to_bytes(1, byteorder="big"))

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
            this_checkpoint = byte_read[checkpoint_base:checkpoint_base+0x1C]
            mapping = int.from_bytes(byte_read[5+i*2:7+i*2], byteorder="big")
            checkpoint = {
                "x_pos": int.from_bytes(this_checkpoint[0x0:0x2], byteorder="big", signed=True),
                "y_pos": int.from_bytes(this_checkpoint[0x2:0x4], byteorder="big", signed=True),
                "z_pos": int.from_bytes(this_checkpoint[0x4:0x6], byteorder="big", signed=True),
                "angle": int.from_bytes(this_checkpoint[0x6:0x8], byteorder="big", signed=True),
                "unk8": floatAt(this_checkpoint, 0x8),
                "unkC": floatAt(this_checkpoint, 0xC),
                "unk10": int.from_bytes(this_checkpoint[0x10:0x12], byteorder="big"),
                "unk12": int.from_bytes(this_checkpoint[0x12:0x14], byteorder="big"),
                "unk14": floatAt(this_checkpoint, 0x14),
                "unk18": int.from_bytes(this_checkpoint[0x18:0x1A], byteorder="big"),
                "unk1A": int.from_bytes(this_checkpoint[0x1A:0x1C], byteorder="big"),
            }

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
            fh.write(bytes([0x1]))
            fh.write(len(checkpoints).to_bytes(2, byteorder="big")) # Num Checkpoints
            fh.write(len(checkpoints).to_bytes(2, byteorder="big")) # Num Mappings

            # Checkpoint index mapping
            for checkpointIndex, checkpoint in enumerate(checkpoints):
                if "mapping" in checkpoint:
                    fh.write(checkpoint["mapping"].to_bytes(2, byteorder="big"))
                else:
                    fh.write(checkpointIndex.to_bytes(2, byteorder="big"))

            # Checkpoint data
            for checkpointIndex, checkpoint in enumerate(checkpoints):
                fh.write(int(checkpoint["x_pos"]).to_bytes(2, byteorder="big", signed=True))
                fh.write(int(checkpoint["y_pos"]).to_bytes(2, byteorder="big", signed=True))
                fh.write(int(checkpoint["z_pos"]).to_bytes(2, byteorder="big", signed=True))
                fh.write(int(checkpoint["angle"]).to_bytes(2, byteorder="big", signed=True))
                fh.write(struct.pack('>f', checkpoint["unk8"])) # Float
                fh.write(struct.pack('>f', checkpoint["unkC"])) # Float
                fh.write(int(checkpoint["unk10"]).to_bytes(2, byteorder="big"))
                fh.write(int(checkpoint["unk12"]).to_bytes(2, byteorder="big"))
                fh.write(struct.pack('>f', checkpoint["unk14"])) # Float
                fh.write(int(checkpoint["unk18"]).to_bytes(2, byteorder="big"))
                fh.write(int(checkpoint["unk1A"]).to_bytes(2, byteorder="big"))

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
                        # this_point["SETPOS"] = ScriptHawkSetPosition(this_point["x_pos"], this_point["y_pos"], this_point["z_pos"])
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
                            "unk6": byte_read[read_header+0x6:read_header+0xA].hex(" ").upper(),
                        }
                        # this_point["SETPOS"] = ScriptHawkSetPosition(this_point["x_pos"], this_point["y_pos"], this_point["z_pos"])
                        unknown_data["points_0xA"].append(this_point)
                        read_header += 0xA

                # unknown_data["unkFooterAddress"] = hex(read_header)
                unknown_data["unkFooter"] = byte_read[read_header+0x0:read_header+0x4].hex(" ").upper()
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

def decodeSetup(decoded_filename : str, encoded_filename : str):
    with open(encoded_filename, "rb") as fh:
        byte_read = fh.read()
        pointer = 0

        setup = {}

        # Object Model 2
        num_model2 = int.from_bytes(byte_read[pointer:pointer+0x4], byteorder="big")
        pointer += 4

        if num_model2 > 0:
            setup["model2"] = []
            for i in range(num_model2):
                this_model2 = byte_read[pointer:pointer+0x30]
                model2_data = {
                    "x_pos": floatAt(this_model2, 0x0),
                    "y_pos": floatAt(this_model2, 0x4),
                    "z_pos": floatAt(this_model2, 0x8),
                    "scale": floatAt(this_model2, 0xC),
                    "unk10": this_model2[0x10:0x18].hex(" ").upper(),
                    "angle18": floatAt(this_model2, 0x18),
                    "angle1C": floatAt(this_model2, 0x1C),
                    "angle20": floatAt(this_model2, 0x20),
                    "unk24": floatAt(this_model2, 0x24),
                    "behaviour": int.from_bytes(this_model2[0x28:0x2A], byteorder="big"),
                    "unk2A": this_model2[0x2A:0x30].hex(" ").upper(),
                }
                model2_data["name"] = model2_names[model2_data["behaviour"]]

                # sampleValue("model2->name", model2_data["name"])
                # sampleValue("model2->unk10", model2_data["unk10"])
                # sampleValue("model2->angle18", model2_data["angle18"])
                # sampleValue("model2->angle1C", model2_data["angle1C"])
                # sampleValue("model2->angle20", model2_data["angle20"])
                # sampleValue("model2->unk24", model2_data["unk24"])
                # sampleValue("model2->unk2A", model2_data["unk2A"])

                setup["model2"].append(model2_data)
                pointer += 0x30

        # Conveyor Data
        num_conveyor = int.from_bytes(byte_read[pointer:pointer+0x4], byteorder="big")
        pointer += 4

        if num_conveyor > 0:
            for i in range(num_conveyor):
                this_conveyor = byte_read[pointer:pointer+0x24]
                model2_index = int.from_bytes(this_conveyor[0x0:0x4], byteorder="big")
                conveyor_data = {
                    "unk4": floatAt(this_conveyor, 0x4),
                    "unk8": floatAt(this_conveyor, 0x8),
                    "unkC": floatAt(this_conveyor, 0xC),
                    "unk10": floatAt(this_conveyor, 0x10),
                    "unk14": floatAt(this_conveyor, 0x14),
                    "unk18": floatAt(this_conveyor, 0x18),
                    "unk1C": floatAt(this_conveyor, 0x1C),
                    "unk20": floatAt(this_conveyor, 0x20),
                }

                setup["model2"][model2_index]["conveyor_data"] = conveyor_data
                pointer += 0x24

        # Actor Spawners
        num_actor_spawners = int.from_bytes(byte_read[pointer:pointer+0x4], byteorder="big")
        pointer += 4

        if num_actor_spawners > 0:
            setup["actors"] = []
            for i in range(num_actor_spawners):
                this_actor = byte_read[pointer:pointer+0x38]
                actor_data = {
                    "x_pos": floatAt(this_actor, 0x0),
                    "y_pos": floatAt(this_actor, 0x4),
                    "z_pos": floatAt(this_actor, 0x8),
                    "scale": floatAt(this_actor, 0xC),
                    "unk10": floatAt(this_actor, 0x10),
                    "unk14": this_actor[0x14:0x32].hex(" ").upper(),
                    "behaviour": int.from_bytes(this_actor[0x32:0x34], byteorder="big"),
                    "unk34": this_actor[0x34:0x38].hex(" ").upper(),
                }

                actor_data["name"] = actor_names[actor_data["behaviour"] + 0x10]
                # actor_data["SETPOS"] = ScriptHawkSetPosition(actor_data["x_pos"], actor_data["y_pos"], actor_data["z_pos"])

                # sampleValue("actor_spawner->name", actor_data["name"])

                setup["actors"].append(actor_data)
                pointer += 0x38

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
                    fh.write(struct.pack('>f', this_model2["x_pos"])) # Float
                    fh.write(struct.pack('>f', this_model2["y_pos"])) # Float
                    fh.write(struct.pack('>f', this_model2["z_pos"])) # Float
                    fh.write(struct.pack('>f', this_model2["scale"])) # Float
                    fh.write(bytes.fromhex(this_model2["unk10"]))
                    fh.write(struct.pack('>f', this_model2["angle18"])) # Float
                    fh.write(struct.pack('>f', this_model2["angle1C"])) # Float
                    fh.write(struct.pack('>f', this_model2["angle20"])) # Float
                    fh.write(struct.pack('>f', this_model2["unk24"])) # Float
                    fh.write(int(this_model2["behaviour"]).to_bytes(2, byteorder="big"))
                    fh.write(bytes.fromhex(this_model2["unk2A"]))

                    if "conveyor_data" in this_model2:
                        num_conveyors += 1

            # Conveyor Data
            fh.write(num_conveyors.to_bytes(4, byteorder="big"))

            if num_conveyors > 0:
                for i, this_model2 in enumerate(setup["model2"]):
                    if "conveyor_data" in this_model2:
                        conveyor_data = this_model2["conveyor_data"]
                        fh.write(i.to_bytes(4, byteorder="big")) # Model 2 Index
                        fh.write(struct.pack('>f', conveyor_data["unk4"])) # Float
                        fh.write(struct.pack('>f', conveyor_data["unk8"])) # Float
                        fh.write(struct.pack('>f', conveyor_data["unkC"])) # Float
                        fh.write(struct.pack('>f', conveyor_data["unk10"])) # Float
                        fh.write(struct.pack('>f', conveyor_data["unk14"])) # Float
                        fh.write(struct.pack('>f', conveyor_data["unk18"])) # Float
                        fh.write(struct.pack('>f', conveyor_data["unk1C"])) # Float
                        fh.write(struct.pack('>f', conveyor_data["unk20"])) # Float

            # Actor Spawners
            fh.write(num_actor_spawners.to_bytes(4, byteorder="big"))

            if num_actor_spawners > 0:
                for i, this_actor in enumerate(setup["actors"]):
                    fh.write(struct.pack('>f', this_actor["x_pos"])) # Float
                    fh.write(struct.pack('>f', this_actor["y_pos"])) # Float
                    fh.write(struct.pack('>f', this_actor["z_pos"])) # Float
                    fh.write(struct.pack('>f', this_actor["scale"])) # Float
                    fh.write(struct.pack('>f', this_actor["unk10"])) # Float
                    fh.write(bytes.fromhex(this_actor["unk14"]))
                    fh.write(int(this_actor["behaviour"]).to_bytes(2, byteorder="big"))
                    fh.write(bytes.fromhex(this_actor["unk34"]))