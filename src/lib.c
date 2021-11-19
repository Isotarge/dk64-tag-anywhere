#include "../include/common.h"

void setPermanentFlag(s16 flagIndex) {
	setFlag(flagIndex, 1, 0);
}

void setGlobalFlag(s16 flagIndex) {
	setFlag(flagIndex, 1, 1);
}

void setTemporaryFlag(s16 flagIndex) {
	setFlag(flagIndex, 1, 2);
}

void* findActorWithType(s32 search_actor_type) {
	for (s32 i = 0; i < ActorCount; i++) {
		actorData* _actor_ = (actorData*)ActorArray[i];
		if (_actor_->actorType == search_actor_type) {
			return _actor_;
		}
	}
	return 0;
}