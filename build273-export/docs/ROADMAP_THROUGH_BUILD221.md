# Diamond Rush Native Android Port — Roadmap Through Build 221

## Project invariants
- Native Android port, not a J2ME emulator wrapper.
- Logical canvas 320×240; gameplay viewport 320×178 at y=31.
- Tile target 24×24.
- Preserve original assets, logic, room content, animations, and audiovisual behavior.
- Unknown field/value semantics remain opaque until proven.

## Milestone status

| Stage | Builds | Status |
|---|---:|---|
| 1. Resource & Asset Reconstruction | 198–212 | Completed |
| 2. Graphics Engine Reconstruction | 213–214 | Main static audit completed |
| 3. Gameplay Engine Reconstruction | 215–222 | In progress — Build 221 completed |
| 4. Native Gameplay Runtime | 223–226 | Not started |
| 5. Android Integration & Release | 227–230 | Not started |

## Build history
- **198–212:** resource discovery, DF03 parsing, payload decoding, composite graph, sprite decode, rasterization.
- **213–214:** draw flags, palette selection, animation records, viewport geometry.
- **215–216:** gameplay scene layers, camera/map traversal, separate `bJ` and `bI` render dispatch domains.
- **217:** room data-plane loading and proven setter for `a:[[B` / `b:[[I`.
- **218:** map mutation candidate sites and instruction-level branch edges.
- **219:** conservative direct-pattern map-plane attribution.
- **220:** basic-block index, CFG edges, approximate reachability, linear stack trace.
- **221:** worklist-based stack/local propagation and bounded state merges for five priority methods.

## Next: Build 222
- Model exception handlers and all encountered JVM stack opcodes.
- Trace map-plane read paths into rendering consumers.
- Separate room initialization from runtime gameplay mutation.
- Build an evidence-backed mutation taxonomy and finalize Stage 3 static reconstruction.

## Validation status
Python/static analysis tests do not establish Android runtime correctness. Kotlin compile, Android Gradle, device execution, visual parity, and APK packaging remain outstanding.
