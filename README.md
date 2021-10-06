# Donkey Kong 64 - Tag Anywhere V5

Made with love by Isotarge

With help from:
- Tom Ballaam
- 2dos
- Mittenz
- retroben
- Kaze Emanuar
- SubDrag
- runehero123
- Skill
- TJ Blakely
- GloriousLiar
- Adam Whitmore
- Znernicus
- Zorulda
- ChristianVega64
- Rain
- Shygoo
- tj90241

It takes a village to free a kong.

## Controls
- D-Pad Left to tag backwards
- D-PAD Right or L Button to tag forwards

## Features
The mystery menu options are unlocked without capturing banana fairies for your convenience.

This hack includes two modes, toggled by the story skip in the options menu.

### Story Skip Off
- [x] Only DK unlocked from start, but you can tag anywhere once other kongs are unlocked

### Story Skip On
- [x] All kongs unlocked from beginning
- [x] Golden Banana dances skipped
- [x] All first time text skipped from beginning
- [x] All moves, guns, camera, unlocked from the start
- [x] Training barrels completed
- [x] File starts in in DK Isles rather than Training Grounds
- [x] K. Lumsy cutscenes compressed (all keys behave like 3 and 8)
- [x] Snide's cutscenes compressed (shortest contraption animation, all blueprints turn at once)
- [x] Faster Troff n Scoff feeding

### Stretch goals
- [ ] Fix origin warp when tagging just before grabbing a tree
- [ ] Set Arcade high scores to max to skip high score entry during 101 run
- [ ] K. Lumsy compression is working great, but it would be greater if all keys that you have could be turned in at once
- [ ] It would be nice if it remembers whether you have story skip on between resets (use unused global block?)

### Tom's feedback
- [ ] If speedrun mode on, autocancel some cutscenes (Practice ROM has a cutscene cancel code. If the game were to check the cutscene index + map + cutscene type, and if it's a certain combination, cancel that cutscene). For example, skipping the free Diddy cutscenes
- [x] Set melon count to 2 or 3 with speedrun mode to align itself with the moves being unlocked
- [x] If speedrun mode, inventory isn't stocked with items upon entering file for the first time. Makes getting oranges annoying as you can't take a fairy photo either since you don't have film and the fairy queen can't give it to you either.
- [x] Enable crash stack trace byte

## Building Pre-requisites
```
1. Python 3
2. n64chain + n64crc in your path
```

## Build Setup
```
1. Copy dk64.z64 into /src/rom
2. Run src/build.bat
```