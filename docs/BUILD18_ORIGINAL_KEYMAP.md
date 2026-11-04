# Build 18 — Original Diamond Rush key mapping

Inspected the original JAR's `i.keyPressed(int)`, `i.keyReleased(int)` and
private static `i.g(int)` bytecode.

Confirmed behavior:
- keyPressed ignores -10, normalizes other negative key codes using abs(),
  converts recognized keys into a bit flag, ORs it into the input mask.
- keyReleased clears the corresponding bit flag.
- Standard MIDP game-action key constants map as:
  - UP (-1) -> bit 1
  - DOWN (-2) -> bit 2
  - LEFT (-3) -> bit 4
  - RIGHT (-4) -> bit 8
  - FIRE (-5) -> bit 16
- The helper also recognizes additional numeric/keypad key codes, including
  23, 42, 35, and 48..57, with their own bit flags.
- The original class has a special state-dependent fallback to key 53 when
  key normalization returns zero and its mode/state byte equals 30.

Added `DiamondRushKeyMap` as a standalone, testable transcription of the
recognized mappings and centralized the adapter constants through it.

Scope caveat: this verifies the key normalization and bitmask mapping, not yet
the gameplay meaning of every bit in every game state. The touch HUD remains
a source-level component; no Android SDK build or APK is claimed.
