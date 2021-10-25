from recompute_pointer_table import parsePointerTables, dumpPointerTableDetails

ROMName = "./rom/dk64-tag-anywhere-dev.z64"

with open(ROMName, "r+b") as fh:
    print("[1 / 2] - Parsing pointer tables")
    parsePointerTables(fh)
    print("[2 / 2] - Dumping to file")
    dumpPointerTableDetails("pointer_tables_modified.log", fh)