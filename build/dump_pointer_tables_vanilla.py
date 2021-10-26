from recompute_pointer_table import parsePointerTables, dumpPointerTableDetails

newROMName = "./rom/dk64.z64"

with open(newROMName, "r+b") as fh:
    parsePointerTables(fh)
    dumpPointerTableDetails("pointer_tables_vanilla.log", fh)