# Diamond Rush Native Android Port — Roadmap Through Build 237

## Project invariants
- Native Android port, not a J2ME emulator wrapper.
- Logical canvas 320×240; gameplay viewport 320×178 at y=31.
- Tile target 24×24.
- Preserve original resources, room data, signed-byte behavior, packed metadata, animation timing, transforms, transparency, and draw ordering.
- Keep resource IDs and unknown field semantics numeric/opaque until bytecode or runtime evidence proves their meaning.
- Keep Python reference tests, Kotlin compilation, Android Gradle, device runtime, visual parity, and APK status distinct.

## Milestone status
| Stage | Builds | Status |
|---|---:|---|
| 1. Resource & Asset Reconstruction | 198–212 | Baseline completed |
| 2. Graphics Engine Reconstruction | 213–214 | Static baseline completed |
| 3. Gameplay Engine Reverse Engineering | 215–222 | Static baseline completed; unresolved sites retained |
| 4. Native renderer/resource integration | 223–237 | In progress |
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
- **234:** DF03 parser reconstruction; Python reference audit parsed 94/94 DF03 payloads and indexed 1,372 sprite records. Build237 later corrected the separate Kotlin parser's multi-sprite interleaved payload cursor.
- **235:** ten static slots bind to 87 sprite records, 843 composite component references, 85 animation frame references (82 valid groups and three `0xFF` no-group sentinels), and 719 expanded animation leaf references. Only `f[9]` and `f[10]` among those ten static slots are direct `i.D()V` render-method consumers.
- **236:** concrete resource-bound sprite draw-operation model; leaf sprite dimensions, position, flags, opaque arguments and composite provenance are preserved.
- **237:** explicit palette-aware pixel binding; corrected Kotlin interleaved sprite payload parsing; full Kotlin original-JAR audit decoded 2,604 sprite/palette combinations across 94 DF03 resources.

## Build237 validation
- Python tests: **203 passed, 4 existing Pillow deprecation warnings**.
- Kotlin: all pure legacy package sources plus Build234/236/237 checks compiled; all selected checks executed successfully.
- Original JAR: 24 bundles, 94 DF03 payloads, 1,372 sprite records, 112 palette rows, 2,604 sprite/palette combinations and 415,896 decoded ARGB pixels.
- Build235 static mappings: 10 slots, 12 palette variants, 114 sprite/palette instances and 28,932 decoded pixels. Both palette rows were preserved for `f[10]` and `f[59]`.
- Android Gradle, device runtime, full-room rasterization, visual parity and APK remain unverified.

## Next milestones
- **238 — Sprite raster execution:** deterministic MIDP transforms, alpha handling, clipping and target pixel surface with golden fixtures.
- **239 — Composite/frame render integration:** combine animation placement, composite expansion and leaf rasterization while preserving order and flags.
- **240 — First complete original room:** generate a full deterministic room scene from original room records and proven resource references.
- **241–245 — Layer/occlusion, actors/effects, HUD/menu and visual parity.**
- **246–260 — Player control, movement, collision, interaction, enemies, hazards, puzzles, progression and save/load.**
- **261–275 — Android shell, lifecycle, input, audio, resource packaging, performance, compatibility, device validation and APK release.

## Explicit non-claims
Build237 does not prove runtime palette selection at every callsite and does not perform MIDP transforms, clipping, target-surface writes, complete room rendering, Android runtime rendering, or APK packaging.
