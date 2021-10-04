// Functions
extern void setFlag(int flagIndex, int value, char flagType);
extern int checkFlag(int flagIndex, char flagType);
extern void* dk_malloc(int size);
extern void dk_free(void* mallocPtr);
extern void playSound(short soundIndex, int unk0, int unk1, int unk2, int unk3, int unk4);
extern void initiateTransition(int map, int exit);
extern int* getFlagBlockAddress(char flagType);
extern int isAddressActor(void* address);
extern int getTimestamp();
extern void dmaFileTransfer(int romStart, int romEnd, int ramStart);
extern void deleteActor(void* actor);
extern int spawnActor(int actorID, int actorBehaviour);
extern void spawnTextOverlay(int style, int x, int y, char* string, int timer1, int timer2, unsigned char effect, unsigned char speed);
extern float dk_sqrt(float __x);
extern void dk_strFormat(char* destination, char* source, ...);
extern void dk_multiply(double val1, double val2, int unk1, int unk2);
extern double convertTimestamp(double unk0, double unk1, unsigned int unk2, unsigned int unk3);
extern void resetMap();
extern void prepKongColoring();
extern void patchHook(unsigned int hook_rdram_location, int offset_in_hook_list, char hook_byte_size);
extern void* dk_memcpy(void* _dest, void* _src, int size);
extern void SaveToGlobal();
extern int DetectGameOver();
extern int DetectAdventure();
extern void displaySprite(void* control_pointer, void* sprite, int x, int y, int scale, int gif_updatefrequency, int movement_style);
extern void alterSize(void* object, int size);
extern void unkSizeFunction(void* object);
extern void spawnRocketbarrel(void* object, int unk);
extern void playSong(int songIndex);
extern void playCutscene(void* actor, int cutscene_index, int cutscene_type);
extern void setHUDItemAsInfinite(int item_index, int player_index, char isInfinite);
extern void osWritebackDCacheAll();
extern void copyFromROM(int rom_start, void* write_Location, void* file_size_location, int unk1, int unk2, int unk3, int unk4);
extern int getActorSpawnerID(void* actor);
extern void textOverlayCode(void);

// Vanilla data
extern float TransitionSpeed;
extern char CutsceneWillPlay;
extern char KRoolRound;
extern KongBase MovesBase[6];
extern int PlayerOneColor;
extern char Mode;
extern char TBVoidByte;
extern int CurrentMap;
extern int DestMap;
extern int DestExit;
extern char StorySkip;
extern char HelmTimerShown;
extern char TempFlagBlock[0x10];
extern submapInfo SubmapData;
extern char HelmTimerPaused;
extern int LagBoost;
extern int FrameLag;
extern int FrameReal;
extern int RNG;
extern char LogosDestMap;
extern char LogosDestMode;
extern char Gamemode;
extern int* ObjectModel2Pointer;
extern int ObjectModel2Timer;
extern int ObjectModel2Count;
extern int ObjectModel2Count_Dupe;
extern short CutsceneIndex;
extern char CutsceneActive;
extern cutsceneType* CutsceneTypePointer;
extern short PreviousCameraState;
extern short CurrentCameraState;
extern short CameraStateChangeTimer;
extern AutowalkData* AutowalkPointer;
extern char IsAutowalking;
extern WarpInfo PositionWarpInfo;
extern short PositionWarpBitfield;
extern float PositionFloatWarps[3];
extern unsigned short PositionFacingAngle;
extern char ChimpyCam;
extern char ScreenRatio;
extern int* CurrentActorPointer;
extern char LoadedActorCount;
extern loadedActorArr LoadedActorArray[64];
extern SpawnerMasterInfo SpawnerMasterData;
extern RGB MenuSkyTopRGB;
extern RGB MenuSkyRGB;
extern int* ActorArray[];
extern short ActorCount;
extern short ButtonsEnabledBitfield;
extern char JoystickEnabledX;
extern char JoystickEnabledY;
extern char MapState;
extern Controller ControllerInput;
extern Controller NewlyPressedControllerInput;
extern playerData* Player;
extern SwapObjectData* SwapObject;
extern char Character;
extern cameraData* Camera;
extern char ISGActive;
extern unsigned int ISGTimestampMajor;
extern unsigned int ISGTimestampMinor;
extern char ISGPreviousFadeout;
extern unsigned int CurrentTimestampMajor;
extern unsigned int CurrentTimestampMinor;
extern ISGFadeoutData ISGFadeoutArray[];
extern InventoryBase CollectableBase;
extern char ModelTwoTouchCount;
extern short ModelTwoTouchArray[4];
extern char TransitionProgress;
extern Controller BackgroundHeldInput;
extern unsigned int PauseTimestampMajor;
extern unsigned int PauseTimestampMinor;
extern unsigned int HelmStartTimestampMajor;
extern unsigned int HelmStartTimestampMinor;
extern int HelmStartTime;
extern short p1PressedButtons;
extern short p1HeldButtons;
extern char player_count;
extern int* sprite_table[0xAF];
extern char sprite_translucency;
extern int* bbbandit_array[4];
extern char StoredDamage;
extern void* ActorSpawnerPointer;
extern float LZFadeoutProgress;
extern HUDDisplay* HUD;

// Hack data