#include "../include/common.h"

void cFuncLoop(void) {
	// Increase Object Model 2 Per Map Count
	*(unsigned int *)(0x80632024) = 0x240a0212; // li $t2, 465 (original, Jungle Japes)
	*(unsigned int *)(0x80632034) = 0x240b0212; // li $t3, 450 (original, All Other Maps)
	*(unsigned int *)(0x80631FF4) = 0x24190212; // li $t9, 500 (original, Frantic Factory)
	*(unsigned int *)(0x80632014) = 0x24090212; // li $t1, 485 (original, Gloomy Galleon)
	*(unsigned int *)(0x80632004) = 0x24080212; // li $t0, 500 (original, Angry Aztec)
	*(unsigned int *)(0x80631FE4) = 0x24180212; // li $t8, 530 (original, Fungi Forest)

	// Fix Bone Displacement
	// Note: This will crash on console
	// Note: Only enable this if you're playing on old versions of BizHawk, mupen64(plus) or PJ64
	// *(unsigned int *)(0x8061963C) = 0x00000000;

	tagAnywhere();
}
