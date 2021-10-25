from recompute_pointer_table import parsePointerTables, dumpPointerTableDetails

newROMName = "./rom/dk64.z64"

with open(newROMName, "r+b") as fh:
    print("[1 / 2] - Parsing pointer tables")
    parsePointerTables(fh)
    print("[2 / 2] - Dumping to file")
    dumpPointerTableDetails("pointer_tables_vanilla.log", fh)