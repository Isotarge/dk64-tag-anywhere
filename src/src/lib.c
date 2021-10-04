#include "../include/common.h"

static const unsigned char bad_maps[] = {
	0x01, // Funky's
	0x03, // Lanky's Maze
	0x05, // Cranky's Lab
	0x0A, // KKosh (V Easy)
	0x0F, // Snide's
	0x12, // TTTrouble (V Easy)
	0x19, // Candy's
	0x20, // BBBandit (Easy)
	0x23, // DK Target Minigame
	0x2A, // Troff n Scoff
	0x32, // Tiny Mush Bounce Minigame
	0x35, // Crown - Beaver Bother
	0x41, // SSnoop (Normal)
	0x42, // MMMaul (Hard)
	0x43, // SSnatch (Hard)
	0x44, // MMMaul (Easy)
	0x45, // MMMaul (Normal)
	0x49, // Crown - Kritter Karnage
	0x4A, // SSnatch (Easy)
	0x4B, // SSnatch (Hard)
	0x4D, // MMayhem (Easy)
	0x4E, // BBBarrage (Easy)
	0x4F, // BBBarrage (Normal)
	0x60, // SSSalvage (Normal)
	0x63, // SSSortie (Easy)
	0x65, // Krazy KK (Easy)
	0x66, // BBBash (V Easy)
	0x67, // SSeek (V Easy)
	0x68, // BBother (Easy)
	// All values between 0x73 and 0x96 (Inclusive). Various bonus minigames
	0x9B, // Crown - Arena Ambush
	0x9C, // Crown - More Kritter Karnage
	0x9D, // Crown - Forest Fracas
	0x9E, // Crown - Bish Bash Brawl
	0x9F, // Crown - Kamikaze Kremlings
	0xA0, // Crown - Plinth Panic
	0xA1, // Crown - Pinnacle Palaver
	0xA2, // Crown - Shockwave Showdown
	0xA5, // Diddy Kremling Game
	0xC9, // Diddy Rocketbarrel Game
	0xCA, // Lanky Shooting Game
	0xD1, // Chunky ? Box Game
	0xD2, // Tiny "Floor is Lava" Game
	0xD3, // Chunky Shooting Game
	0xD4, // DK Rambi Game
};

void playSFX(short sfxIndex) {
	playSound(sfxIndex,0x7FFF,0x427C0000,0x3F800000,0,0);
}

void setPermFlag(short flagIndex) {
	setFlag(flagIndex,1,0);
}

void isPaused(void) {
	IsPauseMenuOpen = 0;
	for (int i = 0; i < ActorCount; i++) {
		actorData* _actor = (actorData*)ActorArray[i];
		if ((_actor->actorType == 95) || (_actor->actorType == 343) || (_actor->actorType == 342)) {
			IsPauseMenuOpen = 1;
		}
	}
}

void checkMapType(void) {
	InBadMap = 0;
	if ((CurrentMap >= 0x73) && (CurrentMap <= 0x96)) {
		InBadMap = 1;
	} else {
		for (int i = 0; i < 44; i++) {
			if (CurrentMap == bad_maps[i]) {
				InBadMap = 1;
			}
		}
	}
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