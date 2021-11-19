// Functions
extern void setFlag(s32 flagIndex, s32 value, s8 flagType);
extern s32 checkFlag(s32 flagIndex, s8 flagType);
extern void* dk_malloc(s32 size);
extern void dk_free(void* mallocPtr);
extern void playSound(s16 soundIndex, s32 volume, f32 unk1, f32 pitch, s32 unk3, s32 unk4);
extern void initiateTransition(s32 map, s32 exit);
extern s32* getFlagBlockAddress(s8 flagType);
extern s32 isAddressActor(void* address);
extern s32 getTimestamp();
extern void dmaFileTransfer(s32 romStart, s32 romEnd, s32 ramStart);
extern void deleteActor(void* actor);
extern s32 spawnActor(s32 actorID, s32 actorBehaviour);
extern void spawnTextOverlay(s32 style, s32 x, s32 y, s8* string, s32 timer1, s32 timer2, u8 effect, u8 speed);
extern f32 dk_sqrt(f32 __x);
extern void dk_strFormat(s8* destination, s8* source, ...);
extern void dk_multiply(f64 val1, f64 val2, s32 unk1, s32 unk2);
extern f64 convertTimestamp(f64 unk0, f64 unk1, u32 unk2, u32 unk3);
extern void resetMap();
extern void prepKongColoring();
extern void* dk_memcpy(void* _dest, void* _src, s32 size);
extern void SaveToGlobal();
extern s32 DetectGameOver();
extern s32 DetectAdventure();
extern void displaySprite(void* control_pointer, void* sprite, s32 x, s32 y, s32 scale, s32 gif_updatefrequency, s32 movement_style);
extern void alterSize(void* object, s32 size);
extern void unkSizeFunction(void* object);
extern void spawnRocketbarrel(void* object, s32 unk);
extern void playSong(s32 songIndex);
extern void playCutscene(void* actor, s32 cutscene_index, s32 cutscene_type);
extern void setHUDItemAsInfinite(s32 item_index, s32 player_index, s8 isInfinite);
extern void osWritebackDCacheAll();
extern void copyFromROM(s32 rom_start, void* write_Location, void* file_size_location, s32 unk1, s32 unk2, s32 unk3, s32 unk4);
extern s32 getActorSpawnerID(void* actor);
extern void textOverlayCode(void);

// Vanilla data
extern f32 TransitionSpeed;
extern s8 CutsceneWillPlay;
extern s8 KRoolRound;
extern KongBase MovesBase[6];
extern s32 PlayerOneColor;
extern s8 Mode;
extern s8 TBVoidByte;
extern s32 CurrentMap;
extern s32 DestMap;
extern s32 DestExit;
extern u16 ParentMap;
extern s8 StorySkip;
extern s8 HelmTimerShown;
extern s8 TempFlagBlock[0x10];
extern submapInfo SubmapData;
extern s8 HelmTimerPaused;
extern s32 LagBoost;
extern s32 FrameLag;
extern s32 FrameReal;
extern s32 RNG;
extern s8 LogosDestMap;
extern s8 LogosDestMode;
extern s8 Gamemode;
extern s32* ObjectModel2Pointer; // TODO: Object model 2 struct array
extern s32 ObjectModel2Timer;
extern s32 ObjectModel2Count;
extern s32 ObjectModel2Count_Dupe;
extern s16 CutsceneIndex;
extern s16 CutsceneTimer;
extern s8 CutsceneActive;
extern cutsceneType* CutsceneTypePointer;
extern s16 PreviousCameraState;
extern s16 CurrentCameraState;
extern s16 CameraStateChangeTimer;
extern AutowalkData* AutowalkPointer;
extern s8 IsAutowalking;
extern WarpInfo PositionWarpInfo;
extern s16 PositionWarpBitfield;
extern f32 PositionFloatWarps[3];
extern u16 PositionFacingAngle;
extern s8 ChimpyCam;
extern s8 ScreenRatio;
extern actorData* CurrentActorPointer;
extern s8 LoadedActorCount;
extern loadedActorArr LoadedActorArray[64];
extern SpawnerMasterInfo SpawnerMasterData;
extern void* ActorSpawnerArrayPointer;
extern RGB MenuSkyTopRGB;
extern RGB MenuSkyRGB;
extern actorData* ActorArray[];
extern s16 ActorCount;
extern s16 ButtonsEnabledBitfield;
extern s8 JoystickEnabledX;
extern s8 JoystickEnabledY;
extern s8 MapState;
extern Controller ControllerInput;
extern Controller NewlyPressedControllerInput;
extern playerData* Player;
extern SwapObjectData* SwapObject;
extern s8 Character;
extern cameraData* Camera;
extern s8 ISGActive;
extern u32 ISGTimestampMajor; // TODO: Does our compiler support unsigned long?
extern u32 ISGTimestampMinor;
extern s8 ISGPreviousFadeout;
extern u32 CurrentTimestampMajor; // TODO: Does our compiler support unsigned long?
extern u32 CurrentTimestampMinor;
extern ISGFadeoutData ISGFadeoutArray[];
extern InventoryBase CollectableBase;
extern s8 ModelTwoTouchCount;
extern s16 ModelTwoTouchArray[4];
extern s8 TransitionProgress;
extern Controller BackgroundHeldInput;
extern u32 PauseTimestampMajor; // TODO: libultra type (OSTime)
extern u32 PauseTimestampMinor;
extern u32 HelmStartTimestampMajor; // TODO: libultra type (OSTime)
extern u32 HelmStartTimestampMinor;
extern s32 HelmStartTime;
extern s16 p1PressedButtons; // TODO: libultra type
extern s16 p1HeldButtons; // TODO: libultra type
extern s8 player_count;
extern s32* sprite_table[0xAF];
extern s8 sprite_translucency;
extern s32* bbbandit_array[4];
extern s8 StoredDamage;
extern void* ActorSpawnerPointer;
extern f32 LZFadeoutProgress;
extern HUDDisplay* HUD;

// Hack data