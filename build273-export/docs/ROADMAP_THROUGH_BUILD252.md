# Diamond Rush Native Android Port — Roadmap through Build252

## Invariants
- Native Android implementation, not a J2ME emulator wrapper.
- Logical canvas 320×240; gameplay viewport 320×178 at y=31; target tile 24×24.
- Preserve original assets and bytecode-derived behavior; uncertain values remain opaque.

## Completed foundations
- Builds198–212: original resource parsing, sprite decoding, composite reconstruction.
- Build213: MIDP transforms, draw flags, palette selection audit.
- Builds214–231: animation, viewport, scene/camera, dispatch, room archive and map-plane reconstruction.
- Builds232–235: resource origin and static/dynamic binding.
- Build236: concrete leaf draw operations.
- Build237: palette-aware pixel binding and Kotlin parser correction.
- Build238: sprite raster execution.
- Build239: resolved frame/composite raster integration.
- Builds240–244: original room manifest, dynamic resource origins, composite attribution, cell/resource candidate join.
- Builds245–251: renderer callsite inventory, receiver provenance, callee semantics, caller producer evidence, worklist snapshots, descriptor contracts.
- Build252: conservative symbolic replay of linear producer slices for all 25 renderer callsites.

## Build252 validation
- Python: 245 passed, 4 existing Pillow deprecation warnings.
- 25 callsite slices parsed; 447 instructions recognized; 427 supported operations processed; 32 stack underflows preserved as unknown.
- No new Kotlin source or Android build was performed.

## Next: Build253 — CFG-Aware Symbolic State Merge
- Use complete `i.D()V` instruction stream and CFG, not only excerpts.
- Propagate abstract operand stack and locals across basic blocks.
- Merge states conservatively at branch joins.
- Model JVM signed-byte and integer semantics.
- Validate invocation shape against descriptor contracts.
- Keep unsupported instructions and ambiguous values unknown.

## Later milestones
- Build254–260: receiver, composite group, component, coordinate and transform argument resolution; first evidence-backed room layer.
- Build261–275: full-room rasterization and golden-image comparisons.
- Build276–295: gameplay rendering, interactions, HUD and audio.
- Build296–315: Android native integration, controls, lifecycle, save/load and optimization.
- Build316+: device testing, APK packaging, parity and release.

## Outstanding
Full-room rendering, Android Gradle/device runtime, visual parity, and playable APK remain incomplete.
