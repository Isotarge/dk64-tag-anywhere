#include "vars.h"

extern void setPermanentFlag(s16 flagIndex);
extern void setGlobalFlag(s16 flagIndex);
extern void setTemporaryFlag(s16 flagIndex);
extern void* findActorWithType(s32 search_actor_type);

extern s32 inBadMap(void);
extern s32 inBadMovementState(void);
extern void tagAnywhere(void);