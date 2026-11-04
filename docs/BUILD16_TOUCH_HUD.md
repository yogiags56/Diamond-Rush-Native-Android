# Build 16 — Touch HUD foundation

Added:
- `TouchControlState`: platform-neutral held-state model for directional,
  action, and pause controls. Opposite directions cancel; `releaseAll()` clears
  held states after touch cancellation.
- `TouchHudView`: Android custom overlay drawing stone-toned translucent
  controls with gold outlines; supports simultaneous pointers by pointer ID.
- Standalone JVM checks for the state model.

Not yet connected to the original game engine. In particular, the HUD listener
must be mapped to the original key/action semantics after the key map is traced.
Pause currently reports a control event; it does not yet pause the game.
The Android View source has not been compiled against an Android SDK here.
