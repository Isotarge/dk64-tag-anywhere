START:
	displacedBootCode:
		LUI v0, 0x8001
		ADDIU v0, v0, 0xDCC4
		//write per frame hook
		//
		LUI t3, hi(mainASMFunctionJump)
		LW t3, lo(mainASMFunctionJump) (t3)
		LUI t4, 0x8060
		SW t3, 0xC164 (t4) //store per frame hook
		J 0x80000784
		LUI t6, 0x000D
		//end of boot code
		/////////////////////////////////////////////////////

mainASMFunction:
	JAL	0x805FC2B0
	NOP
	JAL cFuncLoop
	NOP
	NOP
	J 0x805FC16C
	NOP

mainASMFunctionJump:
	J mainASMFunction //instruction copied and used as a hook
	NOP

mainASMFunctionVanilla:
	JAL	0x805FC2B0
	NOP

patchHook:
	// a0 = Hook Location
	// a1 = Offset in hook list
	// a2 = hook_size_in_bytes
	ADDIU sp, sp, -0x38
	SW 	ra, 0x1C (sp)
	SW 	a2, 0x20 (sp)
	ADDIU a2, a0, 0 // RDRAM location
	LUI a0, 0x01FF //start of ROM copy
	ORI a0, a0, 0xF000
	LW 	a1, 0x20 (sp)
	JAL dmaFileTransfer
	ADDU a1, a0, a1
	LW 	ra, 0x1C (sp)
	JR 	ra
	ADDIU sp, sp, 0x38

.align 0x10
END: