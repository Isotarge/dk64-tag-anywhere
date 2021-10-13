from typing import BinaryIO

def dothething(fh : BinaryIO):
  main_pointer_table_offset = 0x101C50
  pointer_tables = []
  #num_tables = 27
  num_tables = 32

  fh.seek(main_pointer_table_offset)
  i = 0
  while i < num_tables:
    relative_address = int.from_bytes(fh.read(4), "big")
    pointer_tables.append({
      "relative_address": relative_address,
      "absolute_address": relative_address + main_pointer_table_offset,
      "num_entries": 0
    })
    i += 1

  fh.seek(main_pointer_table_offset + num_tables * 4)
  i = 0
  while i < num_tables:
    pointer_tables[i]["num_entries"] = int.from_bytes(fh.read(4), "big")
    i += 1

  for x in pointer_tables:
    if x["num_entries"] > 0:
      print(hex(x["absolute_address"]) + ": " + str(x["num_entries"]))
