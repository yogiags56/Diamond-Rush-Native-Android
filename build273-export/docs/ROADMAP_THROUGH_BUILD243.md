# Diamond Rush Native Android Port — Roadmap through Build243

## Invariants
- Native Android implementation, not a J2ME emulator wrapper.
- Logical canvas 320×240; gameplay viewport 320×178 at y=31.
- Target tile 24×24.
- Preserve original assets, logic, rooms, animation, and audiovisual behavior.
- Do not infer unknown arguments, fields, group indices, or palette choices.

## Completed milestones
- Builds198–212: resource parsing, sprite decoding, composite graph/raster foundations.
- Build213: MIDP transform and palette-selection audit; 1,125 composite parity checks.
- Builds214–222: animation records, viewport, scene traversal, dispatch, bytecode CFG and map-plane reconstruction.
- Builds223–231: room map model, camera/render dispatch, room archive decoding and per-cell traces.
- Builds232–235: resource consumers, static global `f[]` mappings, DF03 parsing and bindings.
- Build236: concrete resource-bound leaf draw operations.
- Build237: palette-aware pixel binding; corrected interleaved Kotlin sprite payload parser.
- Build238: bounded ARGB sprite raster execution.
- Build239: resolved animation-frame/composite-to-raster integration.
- Build240: original room cell manifest and overlay census.
- Build241: evidence-backed main-dispatch art candidates.
- Build242: exact dynamic resource origins for `f[27]`, `f[30]`, and `f[56]`.
- Build243: group/component/sprite attribution and decoding for all three dynamic resources.

## Build243 validation
- Python: 222 passed, 4 pre-existing Pillow deprecation warnings.
- Kotlin: all production/test sources compile; Build223–243 regression runner passes.
- 21 composite groups, 51 component records, 28 sprites, 40 palette decode instances, 10,256 decoded pixels.
- No complete room raster, Android Gradle build, device runtime, visual parity, or APK is claimed.

## Next: Build244 — Room Cell to Dynamic Composite Group Join
- Join original room cells and exact dispatch branches to bytecode-confirmed resource slots.
- Recover group-index arguments from actual draw-call operand/data flow.
- Preserve per-cell placement and transform flags as audited values.
- Resolve palette selection only with explicit evidence.
- Produce provenance for every resolved room-cell draw.
- Keep `f[42]` direct-draw path isolated until its six arguments are understood.

## Later milestones
- Build245+: rasterize the first room layer with only fully resolved dynamic operations.
- Then integrate remaining static/animated overlays and direct-draw paths.
- Establish golden screenshot comparison against the original game.
- Integrate Android Gradle and device runtime; package APK only after those checks pass.
