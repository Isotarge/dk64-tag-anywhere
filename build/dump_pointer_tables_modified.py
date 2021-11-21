from recompute_pointer_table import parsePointerTables, dumpPointerTableDetails

ROMName = "./rom/dk64-tag-anywhere-dev.z64"

with open(ROMName, "rb") as fh:
    parsePointerTables(fh)
    dumpPointerTableDetails("rom/pointer_tables_modified.log", fh)