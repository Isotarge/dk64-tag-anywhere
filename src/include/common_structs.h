typedef struct floatPos {
	/* 0x000 */ float xPos;
	/* 0x004 */ float yPos;
	/* 0x008 */ float zPos;
} floatPos;

typedef struct actorData {
	/* 0x000 */ char unk_00[0x58];
	/* 0x058 */ int actorType;
	/* 0x05C */ char unk_5C[0x7C-0x5C];
	/* 0x07C */ float xPos;
	/* 0x080 */ float yPos;
	/* 0x084 */ float zPos;
	/* 0x088 */ char unk_80[0xB8-0x88];
	/* 0x0B8 */ float hSpeed;
	/* 0x0BC */ char unk_BC[0x154-0xBC];
	/* 0x154 */ char control_state;
	/* 0x155 */ char control_state_progress;
	/* 0x156 */ char unk_156[0x180-0x156];
	/* 0x180 */ void* tied_character_spawner;
} actorData;

typedef struct cameraData {
	/* 0x000 */ char unk_00[0x7C];
	/* 0x07C */ float xPos;
	/* 0x080 */ float yPos;
	/* 0x084 */ float zPos;
	/* 0x088 */ char unk_88[0x15F-0x88];
	/* 0x15F */ char facing_angle;
	/* 0x160 */ char unk_160[0x1FC-0x160];
	/* 0x1FC */ float viewportX;
	/* 0x200 */ float viewportY;
	/* 0x204 */ float viewportZ;
	/* 0x208 */ char unk_208[0x22A-0x208];
	/* 0x22A */ short viewportRotation;
	/* 0x22C */ char unk_22C[0x26B-0x22C];
	/* 0x26B */ char camera_state;
} cameraData;

typedef struct bone_array {
	/* 0x000 */ char unk_00[0x58];
	/* 0x058 */ short xPos;
	/* 0x05A */ short yPos;
	/* 0x05C */ short zPos;
} bone_array;

typedef struct rendering_params {
	/* 0x000 */ char unk_00[0x14];
	/* 0x014 */ bone_array* bone_array1;
	/* 0x018 */ bone_array* bone_array2;
} rendering_params;

typedef struct playerData {
	/* 0x000 */ char unk_00[0x4];
	/* 0x004 */ rendering_params* rendering_param_pointer;
	/* 0x008 */ char unk_08[0x58 - 0x8];
	/* 0x058 */ int characterID; //02 is dk, 03 is diddy, 04 is lanky, etc
	/* 0x05C */ char unk_5C[0x60-0x5C];
	/* 0x060 */ int obj_props_bitfield;
	/* 0x064 */ char unk_64[0x6A-0x64];
	/* 0x06A */ short grounded_bitfield;
	/* 0x06C */ short unk_bitfield;
	/* 0x06E */ char unk_6E[0x7C-0x6E];
	/* 0x07C */ float xPos;
	/* 0x080 */ float yPos;
	/* 0x084 */ float zPos;
	/* 0x088 */ char unk_88[0xA4-0x88];
	/* 0x0A4 */ float floor;
	/* 0x0A8 */ char unk_A8[0xB8-0xA8];
	/* 0x0B8 */ float hSpeed;
	/* 0x0BC */ char unk_BC[0x4];
	/* 0x0C0 */ float yVelocity;
	/* 0x0C4 */ float yAccel;
	/* 0x0C8 */ char unk_C4[0xE6 - 0xC8];
	/* 0x0E6 */ short facing_angle;
	/* 0x0E8 */ short skew_angle;
	/* 0x0EA */ char unk_EA[0xEE - 0xEA];
	/* 0x0EE */ short next_facing_angle;
	/* 0x0F0 */ char unk_F0[0x110 - 0xF0];
	/* 0x110 */ char touching_object;
	/* 0x111 */ char unk_111[0x128 - 0x111];
	/* 0x128 */ short strong_kong_value;
	/* 0x12A */ char unk_12A[2];
	/* 0x12C */ short chunk;
	/* 0x12E */ char unk_12E[0x13C - 0x12E];
	/* 0x13C */ int* collision_queue_pointer;
	/* 0x140 */ char unk_140[0x147 - 0x140];
	/* 0x147 */ char hand_state;
	/* 0x148 */ char unk_148[0x154 - 0x148];
	/* 0x154 */ char control_state;
	/* 0x155 */ char control_state_progress;
	/* 0x156 */ char unk_156[0x18A-0x156];
	/* 0x18A */ short moving_angle;
	/* 0x18C */ char unk_18C[0x1B8-0x18C];
	/* 0x1B8 */ float velocity_cap;
	/* 0x1BC */ char unk_1BC[0x1D0-0x1BC];
	/* 0x1D0 */ short ostand_value;
	/* 0x1D2 */ char unk_1D2[0x208-0x1D2];
	/* 0x208 */ void* vehicle_actor_pointer;
	/* 0x20C */ char was_gun_out;
	/* 0x20D */ char unk_20D[0x23C - 0x20D];
	/* 0x23C */ short unk_rocketbarrel_value1;
	/* 0x23E */ short unk_rocketbarrel_value2;
	/* 0x240 */ char unk_240[0x284 - 0x240];
	/* 0x284 */ cameraData* camera_pointer;
	/* 0x288 */ char unk_288[0x323 - 0x288];
	/* 0x323 */ char unk_rocketbarrel_value3;
	/* 0x324 */ char unk_324[0x328 - 0x324];
	/* 0x328 */ actorData* krool_timer_pointer;
	/* 0x32C */ actorData* held_actor;
	/* 0x330 */ char unk_330[0x36F - 0x330];
	/* 0x36F */ char new_kong;
	/* 0x370 */ int strong_kong_ostand_bitfield;
} playerData; //size 0x630

typedef struct TextOverlay {
	/* 0x000 */ char unk_00[0x84];
	/* 0x004 */ //u16
	/* 0x006 */ //u16
	/* 0x008 */ //u8
	/* 0x009 */ //u8
	/* 0x054 */ //layer ID?
	/* 0x084 */ float style;
	/* 0x088 */ char unk_88[0x15F-0x88];
	/* 0x15F */ char opacity;
	/* 0x160 */ char unk_160[0x0A];
	/* 0x16A */ unsigned char red;
	/* 0x16B */ unsigned char green;
	/* 0x16C */ unsigned char blue;
	/* 0x16D */ char unk_16D[0x0B];
	/* 0x178 */ char* string;
} TextOverlay;

typedef struct Screen {
	/* 0x000 */ int* TextArray;
	/* 0x004 */ const int* FunctionArray;
	/* 0x005 */ char ArrayItems;
	/* 0x006 */ char ParentScreen;
	/* 0x007 */ char ParentPosition;
} Screen;

typedef const struct MapWarp {
	/* 0x000 */ const unsigned char* maps;
	/* 0x004 */ const unsigned char* exits;
	/* 0x008 */ char screen;
} MapWarp;

typedef struct Controller {
	/* 0x000 */ short Buttons;
	/* 0x002 */ char stickX;
	/* 0x003 */ char stickY;
} Controller;

typedef struct InventoryBase {
	/* 0x000 */ short StandardAmmo;
	/* 0x002 */ short HomingAmmo;
	/* 0x004 */ short Oranges;
	/* 0x006 */ short Crystals;
	/* 0x008 */ short Film;
	/* 0x00A */ char unk0A;
	/* 0x00B */ char Health;
	/* 0x00C */ char Melons;
} InventoryBase;

typedef struct PosState {
	/* 0x000 */ float xCamera;
	/* 0x004 */ float yCamera;
	/* 0x008 */ float zCamera;
	/* 0x00C */ float yVelocity;
	/* 0x010 */ float yAccel;
	/* 0x014 */ float hVelocity;
	/* 0x018 */ float yFloor;
	/* 0x01C */ short xStored1;
	/* 0x01E */ short yStored1;
	/* 0x020 */ short zStored1;
	/* 0x022 */ short xStored2;
	/* 0x024 */ short yStored2;
	/* 0x026 */ short zStored2;
	/* 0x028 */ short facing_angle;
	/* 0x02A */ short skew_angle;
	/* 0x02C */ float xPos;
	/* 0x030 */ float yPos;
	/* 0x034 */ float zPos;
	/* 0x038 */ char control_state;
	/* 0x039 */ char control_state_progress;
	/* 0x03A */ char map;
	/* 0x03B */ char bone_array_counter;
	/* 0x03C */ short cameraRotation;
	/* 0x03E */ char cameraState;
} PosState;

typedef struct TimerInfo {
	/* 0x000 */ unsigned int Start;
	/* 0x004 */ unsigned int Timer;
	/* 0x008 */ char Mode;
	/* 0x009 */ char StartMode;
	/* 0x00A */ char PauseMode;
	/* 0x00B */ char FinishMode;
	/* 0x00C */ unsigned int Reduction;
	/* 0x010 */ unsigned int TimerPostReduction;
} TimerInfo;

typedef struct AutowalkData {
	/* 0x000 */ char unk_00[0x12];
	/* 0x012 */ short xPos;
	/* 0x014 */ char unk_14[0x2];
	/* 0x016 */ short zPos;
} AutowalkData;

typedef struct RGB {
	/* 0x000 */ unsigned char red;
	/* 0x001 */ unsigned char green;
	/* 0x002 */ unsigned char blue;
} RGB;

typedef struct KongBase {
	/* 0x000 */ char special_moves;
	/* 0x001 */ char simian_slam;
	/* 0x002 */ char weapon_bitfield;
	/* 0x003 */ char ammo_belt;
	/* 0x004 */ char instrument_bitfield;
	/* 0x005 */ char unk_05[0x2];
	/* 0x007 */ char coins;
	/* 0x008 */ short instrument_energy;
	/* 0x00A */ short cb_count[0xE];
	/* 0x026 */ short tns_cb_count[0xE];
	/* 0x042 */ short gb_count[0xE];
} KongBase;

typedef struct ISGFadeoutData {
	/* 0x000 */ int FadeoutTime;
	/* 0x004 */ char FadeoutMap;
	/* 0x005 */ char unk_05[0x3];
} ISGFadeoutData;

typedef struct GiantKoshaData {
	/* 0x000 */ short timer;
} GiantKoshaData;

typedef struct SwapObjectData {
	/* 0x000 */ char unk_00[0x210];
	/* 0x210 */ floatPos cameraPositions[4];
	/* 0x240 */ char unk_21C[0x29C-0x240];
	/* 0x29C */ short action_type;
} SwapObjectData;

typedef struct sandstormData {
	/* 0x000 */ char unk_00[0x54];
	/* 0x054 */ char sandstorm_active;
} sandstormData;

typedef struct snagData {
	/* 0x000 */ char unk_00[0x48];
	/* 0x048 */ char reset;
	/* 0x049 */ char unk_49[0x54-0x49];
	/* 0x054 */ char check;
	/* 0x055 */ char unk_55[0x60-0x55];
	/* 0x060 */ char state;
	/* 0x061 */ char unk_61[0x9B-0x61];
	/* 0x09B */ char resettrigger;
} snagData;

typedef struct ModelTwoData {
	/* 0x000 */ char unk_00[0x7C];
	/* 0x07C */ void* behaviour_pointer;
	/* 0x080 */ char unk_80[0x84-0x80];
	/* 0x084 */ short object_type;
	/* 0x086 */ char unk_86[0x4];
	/* 0x08A */ short object_id;
	/* 0x08C */ char unk_8C[0x4];
} ModelTwoData;

typedef struct WarpInfo {
	/* 0x000 */ short xPos;
	/* 0x002 */ short yPos;
	/* 0x004 */ short zPos;
	/* 0x006 */ unsigned char facing_angle; // (val / 255) * 4096
	/* 0x007 */ unsigned char camera_angle; // (player + 0x284)->0x15F
	/* 0x008 */ char will_autowalk;
	/* 0x009 */ char spawn_at_origin;
} WarpInfo;

typedef struct flagMenuData {
	/* 0x000 */ const short* flagArray;
	/* 0x004 */ const char* flagTypeArray;
	/* 0x008 */ const int* flagText;
	/* 0x00C */ char screenIndex;
	/* 0x00D */ char flagCount;
} flagMenuData;

typedef struct cutsceneInfo {
	/* 0x000 */ char csdata[0xC];
} cutsceneInfo;

typedef struct cutsceneType {
	/* 0x000 */ char unk_00[0xD0];
	/* 0x0D0 */ cutsceneInfo* cutscene_databank;
} cutsceneType;

typedef struct spriteDisplay {
	/* 0x000 */ int disappear;
	/* 0x004 */ char unk_04[0x11];
	/* 0x015 */ char unk_15;
} spriteDisplay;

typedef struct spriteControl {
	/* 0x000 */ float movement_style;
	/* 0x004 */ float pointer_offset_0x15;
	/* 0x008 */ float xPos;
	/* 0x00C */ float yPos;
	/* 0x010 */ float scale;
	/* 0x014 */ float unk_14;
	/* 0x018 */ int unk_18;
	/* 0x01C */ int unk_1C;
} spriteControl;

typedef struct otherSpriteControl {
	/* 0x000 */ char unk_000[0x28];
	/* 0x028 */ unsigned char left_stretch;
	/* 0x029 */ unsigned char right_stretch;
	/* 0x02A */ unsigned char up_stretch;
	/* 0x02B */ unsigned char down_stretch;
	/* 0x02C */ char unk_02C[0x340-0x2C];
	/* 0x340 */ float xPos;
	/* 0x344 */ float yPos;
	/* 0x348 */ char unk_348[8];
	/* 0x350 */ char gif_update_frequency;
	/* 0x351 */ char unk_351[0xB];
	/* 0x35C */ spriteControl* gif_control_pointer;
	/* 0x360 */ float xScale;
	/* 0x364 */ float yScale;
	/* 0x368 */ char unk_368[0x2];
	/* 0x36A */ char transparency1;
	/* 0x36B */ char transparency2;
	/* 0x36C */ char transparency3;
	/* 0x36D */ char transparency4;
	/* 0x36E */ char unk_36E[0x384-0x36E];
	/* 0x384 */ int* some_pointer;
} otherSpriteControl;

typedef struct submapInfo {
	/* 0x000 */ char in_submap;
	/* 0x001 */ char unk_01;
	/* 0x003 */ short transition_properties_bitfield;
	/* 0x004 */ char unk_04[0x12-4];
	/* 0x012 */ short parent_map;
	/* 0x014 */ char parent_exit;
} submapInfo;

typedef struct MinigameController {
	/* 0x000 */ char unk_00[0x1C5];
	/* 0X000 */ char hit_count;
} MinigameController;

typedef struct SpawnerInfo {
	/* 0x000 */ unsigned char enemy_value;
	/* 0x001 */ char unk_01[0x14-0x1];
	/* 0x014 */ char respawnTimerInit;
	/* 0x015 */ char unk_15[0x18-0x15];
	/* 0x018 */ void* tied_actor;
	/* 0x01C */ char unk_1C[0x42-0x1C];
	/* 0x042 */ char spawn_state;
	/* 0x043 */ char unk_43[0x48 - 0x43];
} SpawnerInfo;

typedef struct pppanicController {
	/* 0x000 */ char unk_00[0x1B1];
	/* 0x1B1 */ char hit_count1;
	/* 0x1B2 */ char unk_1B2;
	/* 0x1B3 */ char hit_count2;
} pppanicController;

typedef struct krazykkcontroller {
	/* 0x000 */ char unk_00[0x1BD];
	/* 0x1BD */ char hit_count1;
	/* 0x1BE */ char unk_1BE;
	/* 0x1BF */ char hit_count2;
} krazykkcontroller;

typedef struct slotArray {
	/* 0x000 */ char unk_10[0x16];
	/* 0x016 */ short hit_count;
} slotArray;

typedef struct bbbanditcontroller {
	/* 0x000 */ char unk_00[0x11C];
	/* 0x11C */ actorData* slot_pointer;
	/* 0x120 */ char unk_120[0x154-0x120];
	/* 0x154 */ char control_state;
	/* 0x155 */ char unk_155[0x174-0x155];
	/* 0x174 */ slotArray* handle_pointer;
} bbbanditcontroller;

typedef struct bbbashcontroller {
	/* 0x000 */ char unk_00[0x1A1];
	/* 0x1A1 */ char hit_count;
} bbbashcontroller;

typedef struct kkoshcontroller {
	/* 0x000 */ char unk_00[0x1CB];
	/* 0x1CB */ char hit_count;
} kkoshcontroller;

typedef struct sseekcontroller {
	/* 0x000 */ char unk_00[0x19F];
	/* 0x19F */ char hit_count;
} sseekcontroller;

typedef struct SpawnerArray {
	/* 0x000 */ SpawnerInfo SpawnerData[120];
} SpawnerArray;

typedef struct SpawnerMasterInfo {
	/* 0x000 */ short count;
	/* 0x002 */ char unk_02[2];
	/* 0x004 */ SpawnerArray* array;
} SpawnerMasterInfo;

typedef struct filestateInfo {
	/* 0x000 */ char perm_flags[0x140];
	/* 0x140 */ char moves_base[0x1E0];
	/* 0x320 */ char inventory[0x10];
	/* 0x330 */ char temp_flags[0x10];
} filestateInfo;

typedef struct loadedActorArr {
	/* 0x000 */ actorData* actor;
	/* 0x004 */ int unk_04;
} loadedActorArr;

typedef struct actorSpawnerData {
	/* 0x000 */ char unk_00[4];
	/* 0x004 */ floatPos positions;
	/* 0x010 */ char unk_10[0x44-0x10];
	/* 0x044 */ void* tied_actor;
	/* 0x048 */ char unk_48[0x5A-0x58];
	/* 0x05A */ short id;
	/* 0x05C */ char unk_5C[0x64-0x5C];
	/* 0x064 */ void* previous_spawner;
	/* 0x068 */ void* next_spawner;
} actorSpawnerData;