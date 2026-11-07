# Diamond Rush Native Android Port — Roadmap through Build 240

## Fixed invariants
- Native Android port, not a J2ME emulator wrapper.
- Logical canvas 320×240; gameplay viewport 320×178 at y=31.
- Tile target 24×24.
- Preserve original assets, bytecode-derived behavior, room content, animation, and audiovisual behavior.
- Keep uncertain fields and draw arguments opaque until proven.

## Completed milestones
- Builds198–212: resource parsing, sprite decoding, composite graph and raster foundations.
- Build213: MIDP transforms, draw flags, palette selection; 1,125 composite Python/Kotlin parity checks.
- Builds214–222: animation records, viewport, scene traversal, render dispatch, room/map-plane and bytecode CFG reconstruction.
- Builds223–231: native room data model, camera and cell tracing, original room archive decoder; all 41 rooms indexed.
- Builds232–235: static resource consumers, global f[] slot mappings, DF03 parsing and room/composite/animation binding.
- Build236: concrete resource-bound sprite leaf operations.
- Build237: palette-aware pixel binding and corrected interleaved sprite payload parser.
- Build238: per-sprite ARGB raster execution, MIDP transforms, clipping and transparency.
- Build239: resolved composite/frame → pixel binding → raster surface integration.
- Build240: actual original room → ordered viewport cell pass manifest with separate main dispatch, overlay route, and supplemental request evidence.

## Build240 validation
- Python: 215 passed, 4 pre-existing Pillow deprecation warnings.
- Kotlin production + test sources compile; Build223–240 regression runner passes.
- Actual sample: w0.bin room0, 26×21, camera(0,0), 160 candidates / 135 in bounds / 25 out of bounds / 10 overlay requests.
- No complete room raster or APK claimed.

## Next: Build241
Trace actual main-pass branch targets in the sample room to exact sprite/resource consumers. Bind only evidence-backed routes and keep unresolved dispatch branches opaque. Produce a bounded first visible layer only when the full resource, animation, and pixel provenance is available.
