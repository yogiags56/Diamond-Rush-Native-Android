# Diamond Rush Native Android Port — Roadmap through Build 249

## Invariants
- Native Android port, not a J2ME emulator wrapper.
- Logical canvas 320×240; gameplay viewport 320×178 at y=31; target tile 24×24.
- Preserve original assets and bytecode-derived behavior.
- Unknown fields/arguments remain opaque until proven.

## Completed foundation
- Builds198–212: resource parsing, sprite decoding, composite/raster foundations.
- Build213: MIDP transforms, draw flags and palette audit.
- Builds214–231: animation, viewport, scene/camera, dispatch, room decoding and bytecode analysis.
- Builds232–235: resource origin and composite attribution.
- Build236: concrete leaf draw operation model.
- Build237: palette-bound pixel binding and Kotlin parser correction.
- Build238: sprite raster execution.
- Build239: resolved frame/composite raster pipeline.
- Build240: original room cell manifest.
- Build241–243: dynamic resource origin, sprite and composite attribution.
- Build244: room-cell to dynamic-resource candidate join.
- Build245–246: render callsite and receiver provenance.
- Build247: original renderer callee semantics.
- Build248: caller argument producer evidence.
- Build249: joins 25 draw callsites to Build221 instruction-entry worklist snapshots.

## Build249 result
- 25 callsites examined.
- 4 matching instruction-entry stack snapshots; 21 unmatched in the exported worklist.
- 0 composite groups resolved.
- Python regression: 237 passed, 4 existing Pillow deprecation warnings.
- No Kotlin source changed; Build248 Kotlin compilation remains the latest validated compile.

## Next: Build250 — Focused JVM Operand-Stack Interpreter
1. Extract the exact instruction ranges from argument producers to each invoke.
2. Model all opcodes on those paths, including dup/swap and integer/category-2 stack behavior where present.
3. Track local-variable provenance and CFG merge sets.
4. Validate invocation stack depth and descriptor arity.
5. Emit receiver and argument provenance only when each value has a unique supported origin.
6. Keep unresolved values UNKNOWN and direct-draw f[42] separate until proven.

## Outstanding
Full-room rasterization, Android Gradle build, device runtime, screenshot parity, and APK packaging remain incomplete.
