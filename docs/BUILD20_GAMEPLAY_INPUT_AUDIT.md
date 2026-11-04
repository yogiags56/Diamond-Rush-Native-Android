# Build 20 — Gameplay input mask audit

Inspected the original `i.f()` update routine and identified a number of
single-bit and composite masks tested by the original helper `a(int)`.
The masks are preserved verbatim as named constants in `OriginalGameplayInput`.

Notable composites observed:
- 4097 = 1 | 4096
- 262146 = 2 | 262144
- 16388 = 4 | 16384
- 65544 = 8 | 65536
- 32784 = 16 | 32768
- 32944 = 16 | 128 | 256
- 33008 = 16 | 64 | 32768

The central update routine branches on the game's current state byte and uses
these combinations for different transitions. This audit intentionally does
not label them universally as movement/digging/action without tracing each
state branch. The current touch HUD's five-button layout can produce the
standard five key bits, but some original branches also test keypad-derived
bits, so exact gameplay parity may require additional virtual controls or
context-sensitive action handling.

No Android SDK compilation or APK build is claimed.
