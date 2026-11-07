# Diamond Rush Native Android Port — Roadmap through Build 247

## Fixed invariants
- Native Android port, not a J2ME emulator wrapper.
- Logical canvas 320×240; gameplay viewport 320×178 at y=31; target tile 24×24.
- Preserve original assets, room content, animation and audiovisual behavior.
- Treat unproven values/fields as opaque.

## Completed milestones
- Builds198–212: resource, sprite, composite parsing and raster foundations.
- Build213: MIDP transform and palette/draw-flag audit.
- Builds214–231: animation, viewport, scene/camera, dispatch, room decoding and tracing.
- Builds232–235: resource origin and static/dynamic sprite attribution.
- Build236: concrete resource-bound leaf operations.
- Build237: palette-aware pixel binding and Kotlin parser correction.
- Build238: deterministic sprite raster execution.
- Build239: resolved frame/composite raster integration.
- Build240: original-room cell manifest and overlay census.
- Build241: CFG-derived dispatch candidates.
- Build242: dynamic resource origin trace (`f[27]`, `f[30]`, `f[56]`).
- Build243: dynamic sprite/composite/palette attribution.
- Build244: room-cell to dynamic composite candidate join.
- Build245: 25 sprite draw callsite inventory.
- Build246: explicit receiver slot identification for 13 callsites; remaining callsites retained unresolved.
- Build247: callee overload semantics proven: seven-int component entry, six-int recursive composite expansion, four-int leaf sprite draw.

## Build247 validation
- Python: 234 passed, 4 existing Pillow deprecation warnings.
- Kotlin production/test compilation succeeded; Build223–247 regression runner passed.
- 11 structural assertions against original callee bytecode passed.

## Next: Build248 — Caller Argument Stack Reconstruction
- Reconstruct full operand stack at all 25 callsites in `i.D()V`.
- Resolve receiver, overload role, group/component index, coordinates and flags where proven.
- Follow CFG merge edges and local-variable stores/loads.
- Preserve unknown values where branches merge incompatibly.
- Promote only fully supported callsites to concrete draw operations.

## Not yet complete
Full original-room rasterization, Android Gradle build, Android device/emulator runtime, screenshot visual parity, and APK packaging remain outstanding.
