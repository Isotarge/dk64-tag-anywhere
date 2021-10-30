#include "../include/common.h"

void cFuncLoop(void) {
	// Enable stack trace upon crash
	*(char *)(0x807563B4) = 1;
	*(int *)(0x80731F78) = 0;

	// Set Arcade High Scores
	*(unsigned int *)(0x807467EC) = 999950;
	*(unsigned int *)(0x807467F0) = 999950;
	*(unsigned int *)(0x807467F4) = 999950;
	*(unsigned int *)(0x807467F8) = 999950;
	*(unsigned int *)(0x807467FC) = 999950;

	// Unlock Mystery Menu
	if (!checkFlag(0, 1)) {
		for (int i = 0; i < 35; i++) {
			setFlag(i, 1, 1);
		}
	}

	// Fix Bone Displacement
	// Note: This will crash on console
	// Note: Only enable this if you're playing on old versions of BizHawk, mupen64(plus) or PJ64
	// *(unsigned int *)(0x8061963C) = 0x00000000;

	tagAnywhere();
}
