# Diamond Rush Native Android Port — Roadmap through Build 239

## Fixed project invariants
- Native Android implementation; not a J2ME emulator wrapper.
- Logical canvas 320×240.
- Gameplay viewport 320×178 at y=31.
- Target tile 24×24.
- Preserve original assets, bytecode-derived logic, room data, animation, and audiovisual behavior.
- Keep uncertain arguments/fields opaque until supported by bytecode/runtime evidence.

## Completed foundation
- Builds 198–212: resource parsing, sprite decoding, composite graph and rasterization foundations.
- Build213: draw-flag/MIDP transform and palette-selection audit; 1,125 composite Python/Kotlin parity checks.
- Builds214–222: animation records, viewport, scene traversal, dispatch attribution, room/map-plane and bytecode control-flow reconstruction.
- Builds223–231: room map model, camera/render dispatch, per-cell tracing, room archive decoding.
- Builds232–235: resource consumers, static `f[]` bundle attribution, DF03 parsing, resource/composite/animation bindings.
- Build236: concrete resource-bound leaf draw operations.
- Build237: palette-aware decoded pixel binding; corrected Kotlin interleaved sprite-length/payload parsing.
- Build238: bounded ARGB sprite raster execution, clipping, alpha, MIDP transforms.
- Build239: end-to-end resolved animation-frame/composite → pixel binding → raster surface integration.

## Build239 validation
- Python: 213 passed, 4 pre-existing Pillow deprecation warnings.
- Kotlin: all production and test sources compile; Build223–239 regression runner passes.
- No Android Gradle build, device runtime, full-room render, visual parity, or APK is claimed.

## Next: Build240 — Original Room Render Assembly
1. Select a concrete original room record and preserve its serialized planes.
2. Use the proven main-pass cell traversal and dispatch decisions to build ordered draw requests.
3. Resolve supported static and animated sprite routes using exact global resource bindings.
4. Keep direct-draw argument paths isolated until their six-int semantics are established.
5. Apply camera/cell positioning and viewport clipping without changing established coordinate conventions.
6. Rasterize the ordered operations into a 320×240 surface and emit per-cell provenance.
7. Add a golden fixture and compare against an original reference capture if available.

Build240 should target one bounded room/pass, not claim a complete playable game. Full-room multi-pass integration, Android runtime, parity, and APK remain subsequent milestones.
