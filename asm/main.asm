.n64
.open "rom/dk64-tag-anywhere-dev.z64", 0

.include "asm/symbols.asm" ; Tell armips' linker where to find the game's function(s)

; Patch boot routine to DMA our code from ROM to RAM and run it
.definelabel bootStart, 0x01FED020

.orga 0x3154 ; ROM
.org 0x80002554 ; RDRAM
NOP ; CRC Patch

.orga 0x1364 ; ROM
.org 0x80000764 ; RDRAM

modifiedBootCode:
	LI a0, bootStart ; Start of ROM copy
	LI a1, (bootStart + 0x11FE0) ; End of ROM copy
	LUI a2, 0x805D
	JAL dmaFileTransfer
	ORI a2, a2, 0xAE00 ; RAM location to copy to
	J displacedVanillaBootCode
	NOP
resumeVanillaBootCode:

.orga bootStart ; ROM
.org 0x805DAE00 ; RDRAM

displacedVanillaBootCode:
	LUI v0, 0x8001
	ADDIU v0, v0, 0xDCC4
	; Write per frame hook
	LUI t3, hi(mainASMFunctionJump)
	LW t3, lo(mainASMFunctionJump) (t3)
	LUI t4, 0x8060
	SW t3, 0xC164 (t4) ; Store per frame hook
	LUI t3, 0 ; These make multiplayer not hard crash
	LUI t4, 1 ; These make multiplayer not hard crash
	LUI t5, 1 ; These make multiplayer not hard crash
	LUI t9, 0xD ; These make multiplayer not hard crash
	LUI t8, 0xD ; These make multiplayer not hard crash
	J resumeVanillaBootCode
	LUI t6, 0x000D

mainASMFunction:
	JAL	0x805FC2B0
	NOP
	JAL cFuncLoop
	NOP
	J 0x805FC16C
	NOP

mainASMFunctionJump:
	J mainASMFunction ; Instruction copied and used as a hook
	NOP

.align 0x10

.include "asm/objects.asm"
.close