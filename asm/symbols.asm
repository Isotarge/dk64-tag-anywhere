; libultra
.definelabel osTvType, 0x80000300
.definelabel osRomBase, 0x80000308
.definelabel osResetType, 0x8000030C
.definelabel osMemSize, 0x80000318
.definelabel osAppNMIBuffer, 0x8000031C

.definelabel memcpy, 0x80003000
.definelabel osInvalDCache, 0x80004520
.definelabel osPiRawStartDma, 0x800045D0
.definelabel osPiGetStatus, 0x800046B0
.definelabel osRecvMesg, 0x800046C0
.definelabel osViBlack, 0x80004800
.definelabel osSetThreadPri, 0x80004870
.definelabel osCreateMesgQueue, 0x80004950
.definelabel osSetEventMesg, 0x80004980
.definelabel osCreateThread, 0x800049F0
.definelabel osStartThread, 0x80004B40
.definelabel osCreateViManager, 0x80004C90
.definelabel viMgrMain, 0x80004E10
.definelabel osViSetMode, 0x80004FA0
.definelabel bzero, 0x800051C0
.definelabel osInvalICache, 0x80005260
.definelabel osWriteBackDCacheAll, 0x800052E0
.definelabel osInitialize, 0x80005310
.definelabel osWritebackDCache, 0x80005670
.definelabel osViSwapBuffer, 0x80005760
.definelabel __osGetFpcCsr, 0x80005A80
.definelabel guSprite2DInit, 0x80005A90
.definelabel osStopThread, 0x80005AE0
.definelabel osDpSetStatus, 0x80005BA0
.definelabel __osSpSetStatus, 0x80005BB0
.definelabel osViSetSpecialFeatures, 0x80005BC0
.definelabel guTranslateF, 0x80005D80
.definelabel guTranslate, 0x80005DC8
.definelabel guPerspectiveF, 0x80005E20
.definelabel guPerspective, 0x80006050
.definelabel osGetTime, 0x800060B0
.definelabel osSetTime, 0x80006140
.definelabel guLookAtHiliteF, 0x80006170
.definelabel guLookAtHilite, 0x800068A8
.definelabel guLookAtF, 0x80006960
.definelabel guLookAt, 0x80006C18
.definelabel guOrthoF, 0x80006C90
.definelabel guOrtho, 0x80006DE4
.definelabel osAiSetNextBuffer, 0x80006E50
.definelabel osAiGetLength, 0x80006F00
.definelabel osPiStartDma, 0x80006F10
.definelabel osContInit, 0x80007020
.definelabel __osContGetInitData, 0x80007190
.definelabel __osPackRequestData, 0x80007260
.definelabel __ull_to_f, 0x800075B0
.definelabel osSetTimer, 0x800077C0
.definelabel osGetThreadId, 0x800078A0
.definelabel osEepromLongRead, 0x800078C0
.definelabel osEepromWrite, 0x80007950
.definelabel __osPackEepWriteData, 0x80007AC8
.definelabel __osEepStatus, 0x80007B74
.definelabel osEepromProbe, 0x80007D20
.definelabel osMotorStartStop, 0x80007D90
.definelabel _MakeMotorData, 0x80007EF8
.definelabel osMotorInit, 0x80008004
.definelabel osDpGetStatus, 0x80008160
.definelabel osViGetCurrentFramebuffer, 0x80008170
.definelabel osViGetNextFramebuffer, 0x800081B0
.definelabel osSpTaskYielded, 0x800081F0
.definelabel osSpTaskLoad, 0x8000838C
.definelabel osSpTaskStartGo, 0x8000851C
.definelabel osSpTaskYield, 0x80008560
.definelabel guScaleF, 0x80008580
.definelabel guScale, 0x800085D4
.definelabel guRotateF, 0x80008620
.definelabel guRotate, 0x800087B4
.definelabel guMtxXFMF, 0x80008810
.definelabel guMtxCatF, 0x800088B0
.definelabel guMtxXFML, 0x80008A20
.definelabel guMtxCatL, 0x80008A80
.definelabel guAlignF, 0x80008AE0
.definelabel guAlign, 0x80008CA0
.definelabel osPiReadIo, 0x80008CF0
.definelabel osViGetCurrentMode, 0x80008D30
.definelabel guPositionF, 0x80008D80
.definelabel guPosition, 0x80008F30
.definelabel osVirtualToPhysical, 0x80008FA0
.definelabel __osDisableInt, 0x80009020
.definelabel __osRestoreInt, 0x80009040
.definelabel __osDequeueThread, 0x80009060
.definelabel __osExceptionPreamble, 0x800090A0
.definelabel __osException, 0x800090B0
.definelabel send_mesg, 0x800095D4
.definelabel __osEnqueueAndYield, 0x800096BC
.definelabel __osEnqueueThread, 0x800097BC
.definelabel __osPopThread, 0x80009804
.definelabel __osDispatchThread, 0x80009814
.definelabel __osViInit, 0x800099A0
.definelabel __osTimerServicesInit, 0x80009AE0
.definelabel __osTimerInterrupt, 0x80009B6C
.definelabel __osSetTimerIntr, 0x80009CE4
.definelabel __osInsertTimer, 0x80009D58
.definelabel osGetThreadPri, 0x80009EE0
.definelabel __osViGetCurrentContext, 0x80009F00
.definelabel __osViSwapContext, 0x80009F10
.definelabel osSendMesg, 0x8000A210
.definelabel osGetCount, 0x8000A360
.definelabel __osSetSR, 0x8000A370
.definelabel __osGetSR, 0x8000A380
.definelabel __osSetFpcCsr, 0x8000A390
.definelabel __osSiRawReadIo, 0x8000A3A0
.definelabel __osSiRawWriteIo, 0x8000A3F0
.definelabel osUnmapTLBAll, 0x8000A440
.definelabel osMapTLBRdb, 0x8000A490
.definelabel osPiRawReadIo, 0x8000A4F0
.definelabel osCreatePiManager, 0x8000A550
.definelabel guMtxF2L, 0x8000A6C0
.definelabel guMtxIdentF, 0x8000A7C0
.definelabel guMtxIdent, 0x8000A848
.definelabel guMtxL2F, 0x8000A878
.definelabel cosf, 0x8000A930
.definelabel sinf, 0x8000AAA0
.definelabel sqrtf, 0x8000AC60
.definelabel __osAiDeviceBusy, 0x8000AC70
.definelabel osJamMesg, 0x8000ACA0
.definelabel osPiGetCmdQueue, 0x8000ADF0
.definelabel __osSiRawStartDma, 0x8000AE20
.definelabel __osSiCreateAccessQueue, 0x8000AED0
.definelabel __osSiGetAccess, 0x8000AF20
.definelabel __osSiRelAccess, 0x8000AF64
.definelabel osEepromRead, 0x8000AF90
.definelabel __osPackEepReadData, 0x8000B154
.definelabel __osContAddressCrc, 0x8000B1E0
.definelabel __osContDataCrc, 0x8000B2B0
.definelabel __osPackRamWriteDataSafe, 0x8000B350
.definelabel __osContRamReadData, 0x8000B3D0
.definelabel __osSpGetStatus, 0x8000B600
.definelabel bcopy, 0x8000B610
.definelabel __osSpSetPc, 0x8000B920
.definelabel __osSpRawStartDma, 0x8000B960
.definelabel __osSpDeviceBusy, 0x8000B9F0
.definelabel guNormalize, 0x8000BA20
.definelabel __osPiCreateAccessQueue, 0x8000BAB0
.definelabel __osPiGetAccess, 0x8000BB00
.definelabel __osPiRelAccess, 0x8000BB44
.definelabel __osProbeTLB, 0x8000BB70
.definelabel osSetIntMask, 0x8000BC30
.definelabel osDestroyThread, 0x8000BCD0
.definelabel __osSetCompare, 0x8000BDE0
.definelabel __osSiDeviceBusy, 0x8000BDF0
.definelabel __osDevMgrMain, 0x8000C000
.definelabel __osContRamWrite, 0x8000C490
.definelabel osPfsIsPlug, 0x8000C6E0
.definelabel __osPfsRequestData, 0x8000C880
.definelabel __osPfsGetInitData, 0x8000C950
.definelabel __osPfsGetStatus, 0x8000CA20
.definelabel __osPfsRequestOneChannel, 0x8000CAF0
.definelabel __osPfsGetOneChannelData, 0x8000CBB4
.definelabel __osResetGlobalIntMask, 0x8000CC50
.definelabel osEPiRawWriteIo, 0x8000CCB0
.definelabel osEPiRawReadIo, 0x8000CE10
.definelabel __osSetGlobalIntMask, 0x8000CF70
.definelabel osYieldThread, 0x8000CFC0
.definelabel __osSumcalc, 0x8000D010
.definelabel __osIdCheckSum, 0x8000D084
.definelabel __osRepairPackId, 0x8000D180
.definelabel __osCheckPackId, 0x8000D4D0
.definelabel __osGetId, 0x8000D634
.definelabel __osViDevMgr, 0x8000EF00
.definelabel __osRunQueue, 0x800100E8
.definelabel __osActiveQueue, 0x800100EC
.definelabel __osViCurr, 0x80010190
.definelabel __osViNext, 0x80010194
.definelabel __OSGlobalIntMask, 0x800100B0
.definelabel hdwrBugFlag, 0x800100C0
.definelabel __osThreadTail, 0x800100E0
.definelabel __osRunningThread, 0x800100F0
.definelabel __osTimerList, 0x800101A0
.definelabel __osPiDevMgr, 0x800101B0
.definelabel __osCurrentHandle, 0x800101D0
.definelabel __osEventStateTab, 0x80013B10
.definelabel retrace, 0x80014DA0
.definelabel __osContLastCmd, 0x80014E00
.definelabel tmp_task, 0x80014F50
.definelabel __osCurrentTime, 0x80014FE0
.definelabel __osBaseCounter, 0x80014FE8
.definelabel __osViIntrCount, 0x80014FEC
.definelabel __osEepPifRam, 0x800162E0

.definelabel n_alInit, 0x80739320
.definelabel n_alClose, 0x8073938C
.definelabel alLink, 0x807393E0
.definelabel alUnlink, 0x80739414
.definelabel n_alSynNew, 0x80739460
.definelabel n_alAudioFrame, 0x80739A64
.definelabel __n_allocParam, 0x80739C88
.definelabel __n_freeParam, 0x80739CE8
.definelabel _n_collectPVoices, 0x80739D14
.definelabel _n_freePVoice, 0x80739D80
.definelabel _n_timeToSamplesNoRound, 0x80739DC0
.definelabel __n_nextSampleTime,  0x80739E5C
.definelabel alSeqpStop, 0x80739F00
.definelabel alSeqpSetSeq, 0x80739F40
.definelabel alSepqSetVol, 0x80739F90
.definelabel alEvtqNew, 0x8073B1D0
.definelabel alEvtqNextEvent, 0x8073B26C
.definelabel alEvtqPostEvent, 0x8073B310
.definelabel alEvtqFlushType, 0x8073B490
.definelabel n_alSynDelete, 0x8073D140

; Functions
.definelabel setFlag, 0x8073129C
.definelabel checkFlag, 0x8073110C
.definelabel dk_malloc, 0x80610FE8
.definelabel dk_free, 0x80611408
.definelabel playSound, 0x80609140
.definelabel initiateTransition, 0x805FF378
.definelabel getFlagBlockAddress, 0x8060E25C
.definelabel isAddressActor, 0x8067AF44
.definelabel getTimestamp, 0x800060B0
.definelabel dmaFileTransfer, 0x80000450
.definelabel deleteActor, 0x806785D4
.definelabel spawnActor, 0x80677FA8
.definelabel spawnTextOverlay, 0x8069D0F8
.definelabel dk_sqrt, 0x8000AC60
.definelabel dk_strFormat, 0x800031E0
.definelabel dk_multiply, 0x80005918
.definelabel convertTimestamp, 0x80005818
.definelabel resetMap, 0x805FFFC8
.definelabel prepKongColoring, 0x8068A508
.definelabel dk_memcpy, 0x80003000
.definelabel SaveToGlobal, 0x8060DEA8
.definelabel DetectGameOver, 0x80714394
.definelabel DetectAdventure, 0x8071432C
.definelabel displaySprite, 0x806AB4EC
.definelabel alterSize, 0x806D0468
.definelabel unkSizeFunction, 0x806CFF9C
.definelabel spawnRocketbarrel, 0x806C7BAC
.definelabel playSong, 0x80602A94
.definelabel playCutscene, 0x8061CC40
.definelabel setHUDItemAsInfinite, 0x806FB370
.definelabel copyFromROM, 0x8060B140
.definelabel getActorSpawnerIDFromTiedActor, 0x80688E68
.definelabel textOverlayCode, 0x8069DA54

; Vanilla data
.definelabel TransitionSpeed, 0x807FD88C
.definelabel CutsceneWillPlay, 0x8075533B
.definelabel KRoolRound, 0x80750AD4
.definelabel MovesBase, 0x807FC950 ; End: 0x807FCB28
.definelabel PlayerOneColor, 0x807552F4
.definelabel Mode, 0x80755318
.definelabel TBVoidByte, 0x807FBB63
.definelabel CurrentMap, 0x8076A0A8
.definelabel DestMap, 0x807444E4
.definelabel DestExit, 0x807444E8
.definelabel ParentMap, 0x8076A172 ; u16
.definelabel StorySkip, 0x8074452C
.definelabel HelmTimerShown, 0x80755350 ; u8
.definelabel TempFlagBlock, 0x807FDD90
.definelabel SubmapData, 0x8076A160
.definelabel HelmTimerPaused, 0x80713C9B ; u8
.definelabel LagBoost, 0x80744478 ; u32
.definelabel FrameLag, 0x8076AF10
.definelabel FrameReal, 0x80767CC4
.definelabel RNG, 0x80746A40 ; u32
.definelabel LogosDestMap, 0x807132BF ; u8
.definelabel LogosDestMode, 0x807132CB ; u8
.definelabel Gamemode, 0x80755314 ; u8
.definelabel ObjectModel2Pointer, 0x807F6000
.definelabel ObjectModel2Timer, 0x8076A064
.definelabel ObjectModel2Count, 0x807F6004
.definelabel ObjectModel2Count_Dupe, 0x80747D70
.definelabel CutsceneIndex, 0x807476F4
.definelabel CutsceneTimer, 0x807476F0 ; u16
.definelabel CutsceneActive, 0x807444EC
.definelabel CutsceneTypePointer, 0x807476FC
.definelabel PreviousCameraState, 0x807F5CF0
.definelabel CurrentCameraState, 0x807F5CF2
.definelabel CameraStateChangeTimer, 0x807F5CEC
.definelabel AutowalkPointer, 0x807FD70C
.definelabel IsAutowalking, 0x807463B8
.definelabel PositionWarpInfo, 0x807FC918 ; WarpInfo Struct
.definelabel PositionWarpBitfield, 0x8076AEE2
.definelabel PositionFloatWarps, 0x8076AEE4 ; f32 x 3
.definelabel PositionFacingAngle, 0x8076AEF0 ; u16
.definelabel ChimpyCam, 0x80744530
.definelabel ScreenRatio, 0x807444C0
.definelabel CurrentActorPointer, 0x807FBB44
.definelabel LoadedActorCount, 0x807FBB35
.definelabel LoadedActorArray, 0x807FB930
.definelabel SpawnerMasterData, 0x807FDC88
.definelabel ActorSpawnerArrayPointer, 0x807FDC8C
.definelabel MenuSkyTopRGB, 0x80754F4C
.definelabel MenuSkyRGB, 0x80754F4F
.definelabel ActorArray, 0x807FBFF0
.definelabel ActorCount, 0x807FC3F0
.definelabel ButtonsEnabledBitfield, 0x80755308
.definelabel JoystickEnabledX, 0x8075530C
.definelabel JoystickEnabledY, 0x80755310
.definelabel MapState, 0x8076A0B1
.definelabel ControllerInput, 0x80014DC4
.definelabel NewlyPressedControllerInput, 0x807ECD66
.definelabel Player, 0x807FBB4C
.definelabel SwapObject, 0x807FC924
.definelabel Character, 0x8074E77C
.definelabel Camera, 0x807FB968
.definelabel ISGActive, 0x80755070
.definelabel ISGTimestampMajor, 0x807F5CE0
.definelabel ISGTimestampMinor, 0x807F5CE4
.definelabel ISGPreviousFadeout, 0x807F5D14
.definelabel CurrentTimestampMajor, 0x80014FE0
.definelabel CurrentTimestampMinor, 0x80014FE4
.definelabel ISGFadeoutArray, 0x80747708
.definelabel CollectableBase, 0x807FCC40
.definelabel ModelTwoTouchCount, 0x807FD798 ; u8
.definelabel ModelTwoTouchArray, 0x807FD790 ; u16 array
.definelabel TransitionProgress, 0x807ECC60 ; u8
.definelabel BackgroundHeldInput, 0x807ECD40 ; u32
.definelabel PauseTimestampMajor, 0x807445C0 ; u32
.definelabel PauseTimestampMinor, 0x807445C4 ; u32
.definelabel HelmStartTimestampMajor, 0x80755340 ; u32
.definelabel HelmStartTimestampMinor, 0x80755344 ; u32
.definelabel HelmStartTime, 0x8075534C ; u32
.definelabel p1PressedButtons, 0x807ECD48
.definelabel p1HeldButtons, 0x807ECD58
.definelabel player_count, 0x807FC928
.definelabel sprite_table, 0x80755390
.definelabel sprite_translucency, 0x807FC80F
.definelabel bbbandit_array, 0x8002DB80
.definelabel StoredDamage, 0x807FCC4D ; s8
.definelabel ActorSpawnerPointer, 0x807FC400 ; u32 ptr
.defineLabel LZFadeoutProgress, 0x807FD888 ; f32
.defineLabel HUD, 0x80754280 ; u32 ptr

; Hack data
