// Functions
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
.definelabel osWritebackDCacheAll, 0x800052E0
.definelabel copyFromROM, 0x8060B140
.definelabel getActorSpawnerIDFromTiedActor, 0x80688E68
.definelabel textOverlayCode, 0x8069DA54

// Vanilla data
.definelabel TransitionSpeed, 0x807FD88C
.definelabel CutsceneWillPlay, 0x8075533B
.definelabel KRoolRound, 0x80750AD4
.definelabel MovesBase, 0x807FC950 // End: 0x807FCB28
.definelabel PlayerOneColor, 0x807552F4
.definelabel Mode, 0x80755318
.definelabel TBVoidByte, 0x807FBB63
.definelabel CurrentMap, 0x8076A0A8
.definelabel DestMap, 0x807444E4
.definelabel DestExit, 0x807444E8
.definelabel ParentMap, 0x8076A172 // u16
.definelabel StorySkip, 0x8074452C
.definelabel HelmTimerShown, 0x80755350 // u8
.definelabel TempFlagBlock, 0x807FDD90
.definelabel SubmapData, 0x8076A160
.definelabel HelmTimerPaused, 0x80713C9B // u8
.definelabel LagBoost, 0x80744478 // u32
.definelabel FrameLag, 0x8076AF10
.definelabel FrameReal, 0x80767CC4
.definelabel RNG, 0x80746A40 // u32
.definelabel LogosDestMap, 0x807132BF // u8
.definelabel LogosDestMode, 0x807132CB // u8
.definelabel Gamemode, 0x80755314 // u8
.definelabel ObjectModel2Pointer, 0x807F6000
.definelabel ObjectModel2Timer, 0x8076A064
.definelabel ObjectModel2Count, 0x807F6004
.definelabel ObjectModel2Count_Dupe, 0x80747D70
.definelabel CutsceneIndex, 0x807476F4
.definelabel CutsceneTimer, 0x807476F0 // u16
.definelabel CutsceneActive, 0x807444EC
.definelabel CutsceneTypePointer, 0x807476FC
.definelabel PreviousCameraState, 0x807F5CF0
.definelabel CurrentCameraState, 0x807F5CF2
.definelabel CameraStateChangeTimer, 0x807F5CEC
.definelabel AutowalkPointer, 0x807FD70C
.definelabel IsAutowalking, 0x807463B8
.definelabel PositionWarpInfo, 0x807FC918 // WarpInfo Struct
.definelabel PositionWarpBitfield, 0x8076AEE2
.definelabel PositionFloatWarps, 0x8076AEE4 // f32 x 3
.definelabel PositionFacingAngle, 0x8076AEF0 // u16
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
.definelabel ModelTwoTouchCount, 0x807FD798 // u8
.definelabel ModelTwoTouchArray, 0x807FD790 // u16 array
.definelabel TransitionProgress, 0x807ECC60 // u8
.definelabel BackgroundHeldInput, 0x807ECD40 // u32
.definelabel PauseTimestampMajor, 0x807445C0 // u32
.definelabel PauseTimestampMinor, 0x807445C4 // u32
.definelabel HelmStartTimestampMajor, 0x80755340 // u32
.definelabel HelmStartTimestampMinor, 0x80755344 // u32
.definelabel HelmStartTime, 0x8075534C // u32
.definelabel p1PressedButtons, 0x807ECD48
.definelabel p1HeldButtons, 0x807ECD58
.definelabel player_count, 0x807FC928
.definelabel sprite_table, 0x80755390
.definelabel sprite_translucency, 0x807FC80F
.definelabel bbbandit_array, 0x8002DB80
.definelabel StoredDamage, 0x807FCC4D // s8
.definelabel ActorSpawnerPointer, 0x807FC400 // u32 ptr
.defineLabel LZFadeoutProgress, 0x807FD888 // f32
.defineLabel HUD, 0x80754280 // u32 ptr

// Hack data
