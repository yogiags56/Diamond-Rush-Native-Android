# Diamond Rush Native Android Port — Roadmap through Build 245

## Invariants
- Native Android port; not a J2ME emulator wrapper.
- Logical canvas 320×240; gameplay viewport 320×178 at y=31; target tile 24×24.
- Preserve original assets and bytecode-derived behavior.
- Keep unproven runtime fields/arguments opaque.

## Completed foundations
- Builds198–212: sprite/resource/composite parsing and raster foundations.
- Build213: MIDP transforms, draw flags, palette audit.
- Builds214–231: animation, viewport, scene/camera, dispatch, room decoding and tracing.
- Builds232–235: static/dynamic resource origin and composite attribution.
- Build236: concrete leaf draw operations.
- Build237: palette-bound pixel attachment and parser correction.
- Build238: bounded sprite raster execution.
- Build239: resolved frame/composite-to-raster pipeline.
- Build240: original room cell manifest.
- Build241: CFG-derived dispatch resource candidates.
- Build242: dynamic resource origin trace.
- Build243: dynamic sprite/composite/palette attribution.
- Build244: room cell to resource/composite candidate join.
- Build245: exact renderer sprite-callsite descriptor inventory.

## Build245 validation
- Python: 229 passed, 4 existing Pillow deprecation warnings.
- Kotlin production/test compilation and regression runner through Build245 passed.
- 25 sprite draw invocation sites: 16 seven-integer and 9 six-integer signatures.
- Receiver `f[]` slot and composite group are not yet resolved at those sites.

## Next: Build246 — Producer-to-Call Stack Slice
1. Select bounded main-pass sprite callsites.
2. Trace operand-stack producers backward from each invoke.
3. Reconstruct branch merges and local-variable definitions.
4. Preserve JVM signed-byte and integer semantics.
5. Resolve receiver slot/group only where all paths converge on proven values.
6. Keep unknown values opaque and do not rasterize candidate-only rows.
7. Continue treating the six-integer/direct-draw route separately until its argument semantics are proven.

## Outstanding
Full-room rasterization, Android Gradle/device runtime, visual parity, and APK packaging remain incomplete.
