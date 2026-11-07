# Diamond Rush Native Android Port — Roadmap through Build 244

## Invariants
- Native Android port, not a J2ME emulator wrapper.
- Logical canvas 320×240; gameplay viewport 320×178 at y=31; target tile 24×24.
- Preserve original assets and bytecode-derived behavior.
- Treat unproven fields/arguments as opaque.

## Completed
- Builds198–212: sprite/resource/composite parsing and raster foundations.
- Build213: MIDP transforms, draw flags, palette audit.
- Builds214–231: animation, viewport, scene/camera, render dispatch, room decoding and tracing.
- Builds232–235: dynamic/static resource origin, resource and composite attribution.
- Build236: concrete leaf draw operations.
- Build237: palette-bound pixel attachment and Kotlin parser correction.
- Build238: bounded sprite raster execution.
- Build239: resolved frame/composite-to-raster pipeline.
- Build240: original room cell manifest and overlay census.
- Build241: CFG-derived main dispatch resource candidates.
- Build242: dynamic resource origin trace, including f[27], f[30], f[56].
- Build243: sprite/composite/palette attribution for those dynamic resources.
- Build244: joins room cells to dynamic resource/composite candidates without falsely asserting runtime selection.

## Build244 validation
- Python: 225 passed, 4 existing Pillow deprecation warnings.
- Kotlin production/test compilation succeeded; regression runner through Build244 passed.
- Candidate join: 1,530 rows, 90 in-bounds cells with dynamic candidates.

## Next: Build245 — Runtime Render-Argument Provenance
1. Trace bytecode stack values reaching render calls for supported `bJ` branches.
2. Resolve actual global `f[]` slot and composite group arguments, not merely CFG-reachable candidates.
3. Preserve signed-byte and JVM integer semantics.
4. Add exact fixtures for argument provenance and branch conditions.
5. Promote only proven cell/resource/group combinations to draw operations.
6. Keep `f[42]` direct six-int path opaque until separately decoded.

## Not yet complete
Full-room rasterization, Android Gradle/device runtime, screenshot visual parity, and APK packaging remain outstanding.
