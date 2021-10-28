import subprocess

def encodeExits(filename : str):
    result = subprocess.check_output(["./build/dk64converter.exe", "encode", "exits", filename])

def decodeExits(filename : str):
    result = subprocess.check_output(["./build/dk64converter.exe", "decode", "exits", filename])