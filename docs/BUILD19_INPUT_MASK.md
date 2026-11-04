# Build 19 — Original input bitmask behavior

The original class exposes a private static `a(int)` helper that returns
whether `(ah & argument) != 0`. Its `keyPressed` handler ORs the normalized
key bit into `ah`; `keyReleased` clears that bit using `ah &= ~bit`.

Added `OriginalInputMask`, a platform-neutral model of those storage
semantics. It also reproduces two handler details:
- key code -10 is ignored.
- when the game's state byte is 30 and a key normalizes to zero, the handler
  substitutes the normalized code for key 53 (bit 32768).

Tests cover simultaneous held keys, independent releases, ignored key -10,
state-30 fallback, additional keypad codes, and clearing the mask.

This is not yet a complete gameplay port: the meaning of each input bit
depends on the game's current state and is still being traced. No Android
SDK compilation or APK build is claimed.
