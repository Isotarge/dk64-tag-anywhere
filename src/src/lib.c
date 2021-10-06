#include "../include/common.h"

void playSFX(short sfxIndex) {
	playSound(sfxIndex, 0x7FFF, 0x427C0000, 0x3F800000, 0, 0);
}

void setPermanentFlag(short flagIndex) {
	setFlag(flagIndex, 1, 0);
}

void setGlobalFlag(short flagIndex) {
	setFlag(flagIndex, 1, 1);
}

void setTemporaryFlag(short flagIndex) {
	setFlag(flagIndex, 1, 2);
}

void* findActorWithType(int search_actor_type) {
	for (int i = 0; i < ActorCount; i++) {
		actorData* _actor_ = (actorData*)ActorArray[i];
		if (_actor_->actorType == search_actor_type) {
			return _actor_;
		}
	}
	return 0;
}