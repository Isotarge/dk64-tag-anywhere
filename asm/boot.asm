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

.align 0x10
END: