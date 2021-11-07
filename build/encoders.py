import json
import math
import struct

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
                        "speed": this_point[0x8],
                        "unk9": this_point[0x9],
                    })
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