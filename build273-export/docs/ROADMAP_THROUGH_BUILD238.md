# Diamond Rush Native Android Port — Roadmap Through Build 238

## Project invariants
- Native Android port, not a J2ME emulator wrapper.
- Logical canvas 320×240; gameplay viewport 320×178 at y=31.
- Tile target 24×24.
- Preserve original resources, room data, signed-byte behavior, packed metadata, animation timing, MIDP transforms, transparency, and draw ordering.
- Keep resource IDs and unknown field semantics numeric/opaque until bytecode or runtime evidence proves their meaning.
- Keep Python reference tests, Kotlin compilation, Android Gradle, device runtime, visual parity, and APK status distinct.

## Milestone status
| Stage | Builds | Status |
|---|---:|---|
| 1. Resource & Asset Reconstruction | 198–212 | Baseline completed |
| 2. Graphics Engine Reconstruction | 213–214 | Static baseline completed |
| 3. Gameplay Engine Reverse Engineering | 215–222 | Static baseline completed; unresolved sites retained |
| 4. Native renderer/resource integration | 223–238 | In progress |
| 5. Gameplay mechanics | 246–260 | Planned |
| 6. Android integration and release | 261–275 | Planned |

## Build history
- **198–209:** resource discovery, DF03 parser, payload decoding, composite graph and bytecode boundary audit.
- **210:** original field consumer audit across 94 resources.
- **211:** sprite pixel decoding, 1,372/1,372.
- **212:** composite rasterization baseline, 300 no-transform groups.
- **213:** MIDP transforms, draw flags, palette selection; 1,125 composite parity checks.
- **214:** five-byte animation frame records, 188 sequences, 1,238 records, viewport geometry.
- **215–216:** gameplay render helpers, camera/map traversal, two cell passes, distinct `bJ` and `bI` dispatch domains.
- **217–222:** room planes, mutation evidence, CFG/dataflow, exception handling and render-read provenance.
- **223–226:** native room/map model, logical canvas, camera/redraw scaffold, dispatch and overlay attribution.
- **227–230:** typed dispatch, per-cell trace, room scene trace, main-pass draw-command planner.
- **231:** original room archive integration; 41 room records indexed.
- **232:** numeric sprite-resource consumer attribution.
- **233:** ten static bundle-entry to global `f[]` slot mappings.
- **234:** DF03 parser reconstruction; 94/94 payloads and 1,372 sprite records. Build237 later corrected Kotlin interleaved payload parsing.
- **235:** ten static slots bind to 87 sprite records, 843 composite component references, 85 animation frame references (82 valid groups and three `0xFF` no-group sentinels), and 719 expanded animation leaf references. Only `f[9]` and `f[10]` among those ten static slots are direct `i.D()V` render-method consumers.
- **236:** concrete resource-bound sprite draw-operation model; leaf sprite dimensions, position, flags, opaque arguments and composite provenance are preserved.
- **237:** explicit palette-aware pixel binding; corrected Kotlin interleaved sprite payload parsing; full Kotlin original-JAR audit decoded 2,604 sprite/palette combinations across 94 DF03 resources.
- **238:** deterministic execution of palette-bound sprite draws onto a bounded ARGB surface, with MIDP transform bits, alpha blending, clipping, painter's order and safety checks.

## Build238 validation
- Python tests: **209 passed, 4 existing Pillow deprecation warnings**.
- Kotlin: all production and test Kotlin source files compiled together.
- Kotlin regression runner: available Build223–Build238 checks passed; older Build224–Build227 test-source/fixture defects were corrected and re-run.
- Android Gradle, device runtime, full original-room rasterization, screenshot parity and APK remain unverified.

## Next milestones
- **239 — Composite/frame render integration:** connect animation placement, composite expansion, palette-bound leaves and raster execution.
- **240 — First complete original room:** render a deterministic full scene using original room records and proven resource references.
- **241–245 — Layer/occlusion, actors/effects, HUD/menu and visual parity.**
- **246–260 — Player control, movement, collision, interaction, enemies, hazards, puzzles, progression and save/load.**
- **261–275 — Android shell, lifecycle, input, audio, resource packaging, performance, compatibility, device validation and APK release.

## Explicit non-claims
Build238 proves deterministic sprite raster execution in pure Kotlin fixtures. It does not prove end-to-end original-room rendering, Android runtime rendering, visual parity, or APK packaging.
