#include "vars.h"

extern void setPermanentFlag(short flagIndex);
extern void setGlobalFlag(short flagIndex);
extern void setTemporaryFlag(short flagIndex);
extern void* findActorWithType(int search_actor_type);

extern int inBadMap(void);
extern int inBadMovementState(void);
extern void tagAnywhere(void);