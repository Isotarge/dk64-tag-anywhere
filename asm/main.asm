.n64 // Let armips know we're coding for the N64 architecture
.open "rom/dk64-tag-anywhere.z64", "rom/dk64-tag-anywhere-dev.z64", 0 // Open the ROM file
.include "asm/symbols.asm" // Tell armips' linker where to find the game's function(s)

// Patch boot routine to DMA our code from ROM
// DMA our custom code from ROM to RAM, run code we overwrote with hook, then run our custom code on boot
.definelabel bootStart, 0x01FED020

.headersize 0x7FFFF400
.org 0x80000764
LUI a0, hi(bootStart) // Start of ROM copy
LUI a1, hi(bootStart + 0x11FE0)
ADDIU a1, a1, lo(bootStart + 0x11FE0)
ADDIU a0, a0, lo(bootStart)
LUI a2, 0x805D
JAL dmaFileTransfer
ORI a2, a2, 0xAE00 // RAM location to copy to
J displacedBootCode
NOP

.headersize 0x7FFFF400
.org 0x80000A30
.headersize 0x7E5EDDE0
.org 0x805DAE00

START:
	displacedBootCode:
		LUI v0, 0x8001
		ADDIU v0, v0, 0xDCC4
		// Write per frame hook
		LUI t3, hi(mainASMFunctionJump)
		LW t3, lo(mainASMFunctionJump) (t3)
		LUI t4, 0x8060
		SW t3, 0xC164 (t4) // Store per frame hook
		J 0x80000784
		LUI t6, 0x000D
		// End of boot code

	mainASMFunction:
		JAL	0x805FC2B0
		NOP
		JAL cFuncLoop
		NOP
		NOP
		J 0x805FC16C
		NOP

	mainASMFunctionJump:
		J mainASMFunction // Instruction copied and used as a hook
		NOP

.align 0x10
END:

.include "asm/objects.asm"
.close // Close the ROM file