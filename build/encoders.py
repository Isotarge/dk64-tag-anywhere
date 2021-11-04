import subprocess
import json
import math

def encodeExitsCSharp(decoded_filename : str, encoded_filename :str):
    result = subprocess.check_output(["./build/dk64converter.exe", "encode", "exits", decoded_filename])

def decodeExitsCSharp(decoded_filename : str, encoded_filename :str):
    result = subprocess.check_output(["./build/dk64converter.exe", "decode", "exits", encoded_filename])

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
    with open(encoded_filename, "r+b") as fh:
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
    with open(encoded_filename, "r+b") as fh:
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