# Diamond Rush Native Android Port — Roadmap through Build 241

## Fixed invariants
- Native Android port, not a J2ME emulator wrapper.
- Logical canvas 320×240; gameplay viewport 320×178 at y=31; tile target 24×24.
- Preserve original assets, logic, room data, animation, and audiovisual behavior.
- Unproven fields, selectors, and arguments remain opaque.

## Milestones
- Builds198–212: resource parsing, sprite decoding, composite graph and rasterization foundations.
- Build213: MIDP transform/draw flags and palette selection audit; 1,125 composite parity cases.
- Builds214–222: animation records, viewport, scene traversal, render dispatch, room/map-plane and bytecode CFG reconstruction.
- Builds223–231: room map model, camera/render dispatch, per-cell tracing, original room archive decoding.
- Builds232–235: resource consumers, static `f[]` bundle attribution, DF03 parsing, resource/composite/animation bindings.
- Build236: concrete resource-bound leaf operations.
- Build237: palette-aware pixel binding and corrected interleaved sprite payload parsing.
- Build238: bounded ARGB sprite raster execution.
- Build239: resolved animation-frame/composite-to-raster integration.
- Build240: original room pass manifest assembly, 41 rooms indexed.
- Build241: CFG-reachable main-dispatch art evidence catalog and original selector frequency audit.

## Build241 validation
- Python: 217 passed, 4 pre-existing Pillow deprecation warnings.
- Kotlin: all production and test sources compiled; Build241 evidence checks passed.
- Research: 88 dispatch evidence rows and 100,906 original serialized selector observations.
- No executable art bindings inferred from CFG reachability unions.

## Next: Build242 — Dynamic f[] Resource Origin Trace
1. Reconstruct `i.j()V` loader state and dynamic array index derivation.
2. Trace object creation, byte payload source, parser invocation, and each `aastore` into `f[]`.
3. Determine whether indices 27, 30, and 56 are populated from a named bundle/entry or runtime stream sequence.
4. Correlate proven object identity to parsed DF03 bundle entries and sprite/composite records.
5. Only create executable bindings when object origin and slot identity are both established.
6. Keep direct draw `f[42]` argument semantics isolated until proven.

Full-room rasterization, Android Gradle/device runtime, visual parity, and APK packaging remain future work.
