.n64 // Let armips know we're coding for the N64 architecture
.open "rom/dk64-tag-anywhere-python.z64", "rom/dk64-tag-anywhere-dev.z64", 0 // Open the ROM file
.include "asm/symbols.asm" // Include dk64.asm to tell armips' linker where to find the game's function(s)
.include "asm/bootPatch.asm" //patch boot routine to DMA our code from ROM
.headersize 0x7FFFF400
.org 0x80000A30
.headersize 0x7E5EDDE0
.org 0x805DAE00
.include "asm/boot.asm" //include modified boot code
.include "asm/objects.asm"
.close // Close the ROM file