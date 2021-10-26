from recompute_pointer_table import parsePointerTables, dumpPointerTableDetails

ROMName = "./rom/dk64-tag-anywhere-dev.z64"

with open(ROMName, "r+b") as fh:
    parsePointerTables(fh)
    dumpPointerTableDetails("pointer_tables_modified.log", fh)