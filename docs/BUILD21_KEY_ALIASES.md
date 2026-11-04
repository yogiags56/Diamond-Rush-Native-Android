# Build 21 — Original key alias audit

The original `i.g(int)` Java ME bytecode contains a `tableswitch` mapping
some ASCII character codes to the same internal bit flags as numeric keys.
This build transcribes and tests those aliases, without asserting that they
are new gameplay actions.

Aliases (ASCII code -> bit):
- 98 (b) -> 262144
- 102 (f) -> 16384
- 103 (g) -> 32768
- 104 (h) -> 65536
- 106 (j) -> 512
- 109 (m) -> 1024
- 110 (n) -> 524288
- 114 (r) -> 2048
- 115 (s) -> 4096
- 116 (t) -> 256
- 118 (v) -> 131072
- 121 (y) -> 8192

The original `i.f()` branches on the game state and tests composite masks,
so no universal gameplay-action labels have been assigned to these aliases.

Tests cover aliases, non-mapped letters, and the ignored -10 code.
The game still does not render playable levels in the Android prototype.
No Android SDK build or APK is claimed.
