import json
import math
import struct

# Useful for detecting booleans, enums, etc
valueSamples = {}
def sampleValue(tag : str, value):
    if not tag in valueSamples:
        valueSamples[tag] = {
            "min": math.inf,
            "max": -math.inf,
            "all": []
        }
    valueSamples[tag]["min"] = min(value, valueSamples[tag]["min"])
    valueSamples[tag]["max"] = max(value, valueSamples[tag]["max"])
    valueSamples[tag]["all"].append(value)

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

def decodeExits(decoded_filename : str, encoded_filename : str):
    with open(encoded_filename, "rb") as fh:
        byte_read = fh.read()
        num_exits = math.floor(len(byte_read) / 0xA)
        exits = []
        for i in range(num_exits):
            exit_base = i * 0xA
            this_exit = byte_read[exit_base:exit_base+0xA]
            exits.append({
                "x_pos": int.from_bytes(this_exit[0x0:0x2], byteorder="big", signed=True),
                "y_pos": int.from_bytes(this_exit[0x2:0x4], byteorder="big", signed=True),
                "z_pos": int.from_bytes(this_exit[0x4:0x6], byteorder="big", signed=True),
                "angle": int.from_bytes(this_exit[0x6:0x8], byteorder="big", signed=True),
                "has_autowalk": this_exit[0x8],
                "size": this_exit[0x9],
            })

        with open(decoded_filename, "w") as fjson:
            json.dump(exits, fjson, indent=4, default=str)

def decodePaths(decoded_filename : str, encoded_filename : str):
    with open(encoded_filename, "rb") as fh:
        byte_read = fh.read()

        paths = []
        num_paths = int.from_bytes(byte_read[0x0:0x2], byteorder="big", signed=False)
        path_base = 2
        for i in range(num_paths):
            this_path = byte_read[path_base:path_base+0x6]
            num_points = int.from_bytes(this_path[0x2:0x4], byteorder="big")
            path = {
                "id": int.from_bytes(this_path[0x0:0x2], byteorder="big"),
                "unk4": int.from_bytes(this_path[0x4:0x6], byteorder="big"),
            }
            #sampleValue("path->unk4", path["unk4"])
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
                    #sampleValue("path->point->unk0", int.from_bytes(this_point[0x0:0x2], byteorder="big", signed=True))
                    #sampleValue("path->point->speed", this_point[0x8])
                    #sampleValue("path->point->unk9", this_point[0x9])
                    path_base += 0xA

            paths.append(path)

        with open(decoded_filename, "w") as fjson:
            json.dump(paths, fjson, indent=4, default=str)

def encodePaths(decoded_filename : str, encoded_filename : str):
    with open(decoded_filename) as fjson:
        paths = json.load(fjson)
        with open(encoded_filename, "w+b") as fh:
            # File header
            fh.write(len(paths).to_bytes(2, byteorder="big", signed=False))

            for path in paths:
                num_points = len(path["points"]) if "points" in path else 0

                # Path header
                fh.write(int(path["id"]).to_bytes(2, byteorder="big", signed=False))
                fh.write(num_points.to_bytes(2, byteorder="big", signed=False))
                fh.write(int(path["unk4"]).to_bytes(2, byteorder="big", signed=False))

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
        num_checkpoints = int.from_bytes(byte_read[0x1:0x3], byteorder="big", signed=False)
        num_checkpoint_mappings = int.from_bytes(byte_read[0x3:0x5], byteorder="big", signed=False)

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
                "unk8": struct.unpack('>f', this_checkpoint[0x8:0xC])[0], # Float
                "unkC": struct.unpack('>f', this_checkpoint[0xC:0x10])[0], # Float
                "unk10": int.from_bytes(this_checkpoint[0x10:0x12], byteorder="big"),
                "unk12": int.from_bytes(this_checkpoint[0x12:0x14], byteorder="big"),
                "unk14": struct.unpack('>f', this_checkpoint[0x14:0x18])[0], # Float
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
            fh.write(len(checkpoints).to_bytes(2, byteorder="big", signed=False)) # Num Checkpoints
            fh.write(len(checkpoints).to_bytes(2, byteorder="big", signed=False)) # Num Mappings

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
        
        # fences?
        fence_count = int.from_bytes(byte_read[0x0:0x2], byteorder="big", signed=False)
        read_header += 2

        if fence_count > 0:
            extract["fences"] = []
            for i in range(fence_count):
                unknown_data = {}

                # Points
                num_points = int.from_bytes(byte_read[read_header:read_header + 2], byteorder="big")
                read_header += 2

                if num_points > 0:
                    unknown_data["points"] = []
                    for i in range(num_points):
                        unknown_data["points"].append({
                            "x_pos": int.from_bytes(byte_read[read_header+0x0:read_header+0x2], byteorder="big", signed=True),
                            "y_pos": int.from_bytes(byte_read[read_header+0x2:read_header+0x4], byteorder="big", signed=True),
                            "z_pos": int.from_bytes(byte_read[read_header+0x4:read_header+0x6], byteorder="big", signed=True),
                        })
                        read_header += 0x6

                # Unknown path data
                num_0xA_structs = int.from_bytes(byte_read[read_header:read_header + 2], byteorder="big")
                read_header += 2

                if num_0xA_structs > 0:
                    unknown_data["0xA_structs"] = []
                    for i in range(num_0xA_structs):
                        unknown_data["0xA_structs"].append({
                            "x_pos": int.from_bytes(byte_read[read_header+0x0:read_header+0x2], byteorder="big", signed=True),
                            "y_pos": int.from_bytes(byte_read[read_header+0x2:read_header+0x4], byteorder="big", signed=True),
                            "z_pos": int.from_bytes(byte_read[read_header+0x4:read_header+0x6], byteorder="big", signed=True),
                            "unk6Raw": byte_read[read_header+0x6:read_header+0xA].hex(" ").upper(),
                        })
                        read_header += 0xA

                read_header += 4

                extract["fences"].append(unknown_data)

        # Spawners
        spawn_count = int.from_bytes(byte_read[read_header:read_header + 2], byteorder="big")
        read_header += 2

        if spawn_count > 0:
            extract["character_spawners"] = []
            for i in range (spawn_count):
                spawner_data = {
                    "enemy_val": byte_read[read_header+0x0],
                    "unk1": byte_read[read_header+0x1],
                    "y_rot": int.from_bytes(byte_read[read_header+0x2:read_header+0x4], byteorder="big"),
                    "x_pos": int.from_bytes(byte_read[read_header+0x4:read_header+0x6], byteorder="big", signed=True),
                    "y_pos": int.from_bytes(byte_read[read_header+0x6:read_header+0x8], byteorder="big", signed=True),
                    "z_pos": int.from_bytes(byte_read[read_header+0x8:read_header+0xA], byteorder="big", signed=True),
                    # 0xA is cutscene model, which is read further down
                    "unkB": byte_read[read_header+0xB],
                    "max_idle_speed": byte_read[read_header+0xC],
                    "max_aggro_sped": byte_read[read_header+0xD],
                    "unkE": byte_read[read_header+0xE],
                    "scale": byte_read[read_header+0xF],
                    "aggro": byte_read[read_header+0x10],
                    "unk11": byte_read[read_header+0x11],
                    "initial_spawn_state": byte_read[read_header+0x12],
                    "spawn_trigger": byte_read[read_header+0x13],
                    "initial_respawn_timer": byte_read[read_header+0x14],
                    "unk15": byte_read[read_header+0x15],
                }

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