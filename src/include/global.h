#include "vars.h"

extern void playSFX(short sfxIndex);
extern void setPermFlag(short flagIndex);
extern void openStateMenu(void);
extern void openTimerSettingsMenu(void);
extern void openFileStateMainMenu(void);
extern void openFlagSubmenu(int screenIndex);
extern void toggleFlag(void);
extern void handleMapWarping(int map, int levelIndex);
extern int convertIDToIndex(short obj_index);
extern void* findActorWithType(int search_actor_type);

extern void tagAnywhere(void);
extern void handleTimer(void);
extern void ramViewUpdate(void);
extern void displaySavePrompt(void);
extern void handleAutomoonkick(void);
extern void handleSpawnPrevention(void);
extern void controlWatchView(void);
extern void updateLoadedActorNoTextOverlayList(int callType);
extern void shouldRefreshTOMenu(void);