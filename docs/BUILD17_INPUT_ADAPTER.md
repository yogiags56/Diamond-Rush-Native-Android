# Build 17 — Touch-to-MIDP input adapter

Added `MidpInputAdapter`, an isolated bridge from touch HUD held states to
Java ME Canvas-style key press/release events. It emits transitions only,
prevents repeated press events while a finger remains held, and releases held
keys on cancellation. Pause is surfaced as a separate Android command.

Important compatibility caveat: the adapter currently uses standard MIDP
game-action key constants (-1 through -5). The original Diamond Rush class's
`keyPressed` / `keyReleased` implementation still must be traced to confirm
whether it uses `getGameAction`, Nokia-specific key codes, or custom mappings.
Do not wire this adapter to live gameplay until that verification is complete.

Standalone JVM tests validate event transitions. No Android SDK build or APK
is claimed.
