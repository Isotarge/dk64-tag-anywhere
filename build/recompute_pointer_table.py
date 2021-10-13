from typing import BinaryIO

def dothething(fh : BinaryIO):
  main_pointer_table_offset = 0x101C50
  pointer_tables = []
  pointer_table_names = [
    "Unknown 0",
    "Map Geometry",
    "Map Walls",
    "Map Floors",
    "Unknown 4",
    "Unknown 5",
    "Unknown 6",
    "Unknown 7",
    "Map Cutscenes",
    "Map Object Setups",
    "Map Data 0xA",
    "Unknown 11",
    "Unknown 12",
    "Unknown 13",
    "Unknown 14",
    "Map Balloon Trajectories",
    "Map Character Spawners",
    "Unknown 17",
    "Map Loading Zones",
    "Unknown 19",
    "Unknown 20",
    "Unknown 20",
    "Unknown 21",
    "Map Exits",
    "Unknown 23",
    "Unknown 24",
    "Unknown 25",
    "Unknown 26",
    "Unknown 27",
    "Unknown 28",
    "Unknown 29",
    "Unknown 30",
    "Unknown 31",
    "Unknown 32",
  ]
  #num_tables = 27
  num_tables = 32

  fh.seek(main_pointer_table_offset)
  i = 0
  while i < num_tables:
    relative_address = int.from_bytes(fh.read(4), "big")
    pointer_tables.append({
      "index": i,
      "name": pointer_table_names[i],
      "relative_address": relative_address,
      "absolute_address": relative_address + main_pointer_table_offset,
      "num_entries": 0,
      "entries": []
    })
    i += 1

  fh.seek(main_pointer_table_offset + num_tables * 4)
  i = 0
  while i < num_tables:
    pointer_tables[i]["num_entries"] = int.from_bytes(fh.read(4), "big")
    i += 1

  for x in pointer_tables:
    if x["num_entries"] > 0:
      fh.seek(x["absolute_address"])
      i = 0
      while i < x["num_entries"]:
        relative_address = int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF
        x["entries"].append({
          "index": i,
          "pointer_address": x["absolute_address"] + i * 4,
          "relative_address": relative_address,
          "absolute_address": relative_address + main_pointer_table_offset,
          "absolute_size": 0,
        })
        i += 1
      print(str(x["index"]) + ": " + x["name"] + ": " + hex(x["absolute_address"]) + " (" + str(x["num_entries"]) + " entries)")
      for y in x["entries"]:
        if y["index"] < 10:
          print(" - " + str(y["index"]) + ": " + hex(y["pointer_address"]) + " -> " + hex(y["absolute_address"]) + " (" + hex(y["absolute_size"]) + ")")
        else:
          break
