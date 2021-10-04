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

callFunc:
	// a0 = function addr
	ADDI 	sp, sp, -8
	SW 		ra, 0x4 (sp)
	JALR 	a0
	NOP
	LW 		ra, 0x4 (sp)
	JR 		ra
	ADDIU 	sp, sp, 8

getTimestampDiff:
	// a0 = major timestamp
	// a1 = minor timestamp
	ADDIU 	sp, sp, -0xA8
	SW 		ra, 0x4C (sp)
	SW 		a0, 0x40 (sp)
	JAL 	getTimestamp
	SW 		a1, 0x44 (sp)
	LW 		t6, 0x40 (sp)
	LW 		t7, 0x44 (sp)
	ADDIU 	a2, r0, 0
	SLTU 	at, v1, t7
	SUBU 	a0, v0, t6
	SUBU 	a0, a0, at
	ADDIU 	a3, r0, 0x40
	JAL 	dk_multiply
	SUBU 	a1, v1, t7
	OR 		a0, v0, r0
	OR 		a1, v1, r0
	ADDIU 	a2, r0, 0
	JAL 	convertTimestamp
	ADDIU 	a3, r0, 3000
	OR 		a0, v0, r0
	OR 		a1, v1, r0
	ADDIU 	a2, r0, 0
	JAL 	convertTimestamp
	ADDIU 	a3, r0, 10000
	LW 		ra, 0x4C (sp)
	ADDIU 	sp, sp, 0xA8
	JR 		ra
	ADDIU 	v0, v1, 0

getTimestampDiffInTicks:
	// a0 = major timestamp
	// a1 = minor timestamp
	ADDIU 	sp, sp, -0xA8
	SW 		ra, 0x4C (sp)
	SW 		a0, 0x40 (sp)
	JAL 	getTimestamp
	SW 		a1, 0x44 (sp)
	LW 		t6, 0x40 (sp)
	LW 		t7, 0x44 (sp)
	SLTU 	at, v1, t7
	SUBU 	a0, v0, t6
	SUBU 	a0, a0, at
	SUBU 	a1, v1, t7
	SW 		a0, TempTimestampStorageMajor
	SW 		a1, TempTimestampStorageMinor
	LW 		ra, 0x4C (SP)
	JR 		ra
	ADDIU 	sp, sp, 0xA8

timestampDiffToMilliseconds:
	// a0 = major timestamp
	// a1 = minor timestamp
	ADDIU 	sp, sp, -0xA8
	SW 		ra, 0x4C (sp)
	ADDIU 	a3, r0, 0x40
	JAL 	dk_multiply
	ADDIU 	a2, r0, 0
	OR 		a0, v0, r0
	OR 		a1, v1, r0
	ADDIU 	a2, r0, 0
	JAL 	convertTimestamp
	ADDIU 	a3, r0, 3000
	OR 		a0, v0, r0
	OR 		a1, v1, r0
	ADDIU 	a2, r0, 0
	JAL 	convertTimestamp
	ADDIU 	a3, r0, 10000
	LW 		ra, 0x4C (sp)
	ADDIU 	sp, sp, 0xA8
	JR 		ra
	ADDIU 	v0, v1, 0

getGiantKoshaAddress:
	LW 		v1, 0x0 (a0)
	ADDIU 	s0, v1, 6
	SW 		r0, GiantKoshaTimerAddress
	SRA  	t8, s0, 16
	SLTIU 	t8, t8, 0x8000
	BNEZ 	t8, getGiantKoshaAddress_Finish
	SRA 	t8, s0, 16
	SLTIU 	t8, t8, 0x8080
	BEQZ 	t8, getGiantKoshaAddress_Finish
	NOP
	SW 		s0, GiantKoshaTimerAddress

	getGiantKoshaAddress_Finish:
		J 		0x8064607c
		OR 		s0, a0, r0

getOtherSpritePointer:
	JR 		ra
	OR 		v0, a1, r0

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

timestampAdd:
	// a0 = Timestamp 1 double
	// a1 = Timestamp 2 double
	LD		t0, 0x0 (a0)
	LD 		t3, 0x0 (a1)
	DADDU 	t0, t0, t3
	LUI	 	t6, hi(TempTimestampStorageMajor)
	JR 		ra
	SD 		t0, lo(TempTimestampStorageMajor) (t6)

pauseHook:
	//J 	setPauseVolume
	NOP
kongHook:
	//J 	kongCode
	NOP
flagHook:
	//J 	writeLastUpdatedFlags
	NOP
TextResizeHook:
	//J 	resizeActiveMenuFont
	NOP
DefineAMFontHook:
	//J 	defineActiveMenuOtherParams
	NOP
ActorRunDuringFrameAdvanceHook:
	//J 	handleFrameAdvanceActorRun
	NOP
TextOverlayIsolationHook:
	//J 	isolateTextOverlays
	NOP

loadExtraHooks:
	// Color other font styles
	ADDIU t3, r0, 1
	LUI t4, 0x806A
	SH 	t3, 0xD43A (t4)

	ADDIU t3, r0, 0x1000
	LUI t4, 0x806A
	SH 	t3, 0xD738 (t4)

	LUI t3, hi(pauseHook)
	LW t3, lo(pauseHook) (t3)
	LUI t4, 0x8060
	SW t3, 0xC890 (t4) // Store Hook

	LUI t3, hi(flagHook)
	LW t3, lo(flagHook) (t3)
	LUI t4, 0x8073
	SW t3, 0x129C (t4) // Store Hook

	LUI t3, hi(TextResizeHook)
	LW t3, lo(TextResizeHook) (t3)
	LUI t4, 0x806A
	SW 	t3, 0xD88C (t4) // Store Hook

	LUI t3, hi(DefineAMFontHook)
	LW t3, lo(DefineAMFontHook) (t3)
	LUI t4, 0x806A
	SW 	t3, 0xD8B0 (t4) // Store Hook

	LUI t3, hi(ActorRunDuringFrameAdvanceHook)
	LW t3, lo(ActorRunDuringFrameAdvanceHook) (t3)
	LUI t4, 0x8060
	SW 	t3, 0xC3FC (t4) // Store Hook

	LUI t3, hi(TextOverlayIsolationHook)
	LW t3, lo(TextOverlayIsolationHook) (t3)
	LUI t4, 0x8068
	SW 	t3, 0x8928 (t4) // Store Hook
	SW 	r0, 0x892C (t4) // Store NOP

	LUI t3, hi(kongHook)
	LW t3, lo(kongHook) (t3)
	LUI t4, 0x806F
	JR 	ra
	SW t3, 0x3750 (t4) // Store Hook

getObjectArrayAddr:
	// a0 = initial address
	// a1 = common object size
	// a2 = index
	MULTU 	a1, a2
	MFLO	a1
	JR 		ra
	ADD 	v0, a0, a1

.align 0x10
END: