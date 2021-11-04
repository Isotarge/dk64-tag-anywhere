import subprocess
import json
import math

def encodeExits(decoded_filename : str, encoded_filename :str):
    result = subprocess.check_output(["./build/dk64converter.exe", "encode", "exits", decoded_filename])

def decodeExits(decoded_filename : str, encoded_filename :str):
    result = subprocess.check_output(["./build/dk64converter.exe", "decode", "exits", encoded_filename])

def encodeExitsPython(decoded_filename : str, encoded_filename :str):
    # TODO: exits.json -> exits.bin
    return 0

def decodeExitsPython(decoded_filename : str, encoded_filename : str):
    with open(encoded_filename, "r+b") as fh:
        byte_read = fh.read()
        num_exits = math.floor(len(byte_read) / 0xA)
        exits = []
        for i in range(num_exits):
            exit_base = i * 0xA
            this_exit = byte_read[exit_base:exit_base+0xA]
            exits.append({
                "x_pos": int.from_bytes(this_exit[0x0:0x2], byteorder="big"),
                "y_pos": int.from_bytes(this_exit[0x2:0x4], byteorder="big"),
                "z_pos": int.from_bytes(this_exit[0x4:0x6], byteorder="big"),
                "angle": int.from_bytes(this_exit[0x6:0x8], byteorder="big", signed=True),
                "has_autowalk": this_exit[0x8],
                "size": this_exit[0x9],
            })

        with open(decoded_filename, "w") as fjson:
            fjson.write(json.dumps(exits, indent=4, default=str))